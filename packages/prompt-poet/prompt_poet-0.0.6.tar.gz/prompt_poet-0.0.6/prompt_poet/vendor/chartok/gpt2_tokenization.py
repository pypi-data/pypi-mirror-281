#!/usr/bin/env python3

import json
import logging
import os
import regex as re
from typing import Dict, List, Tuple
from functools import lru_cache

logger = logging.getLogger(__name__)


# Should haved added re.IGNORECASE so BPE merges can happen for
# capitalized versions of contractions
# The only difference is " ?\p{N}+" becomes " ?\p{N}".
VANILLA_REGEX = (
    r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
)
NUMBER_SPLIT_REGEX = (
    r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
)
NUMBER_UNDERSCORE_SPLIT_REGEX = (
    r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}| ?[^\s\p{L}\p{N}_]+|\s+(?!\S)|_+|\s+"""
)


@lru_cache()
def bytes_to_unicode():
    """
    Returns list of utf-8 byte and a corresponding list of unicode strings.
    The reversible bpe codes work on unicode strings.
    This means you need a large # of unicode characters in your vocab if you want to avoid UNKs.
    When you're at something like a 10B token dataset you end up needing around 5K for decent coverage.
    This is a signficant percentage of your normal, say, 32K bpe vocab.
    To avoid that, we want lookup tables between utf-8 bytes and unicode strings.
    And avoids mapping to whitespace/control characters the bpe code barfs on.
    """
    bs = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    cs = bs[:]
    n = 0
    for b in range(2**8):
        if b not in bs:
            bs.append(b)
            cs.append(2**8 + n)
            n += 1
    cs = [chr(n) for n in cs]
    return dict(zip(bs, cs))


def get_pairs(word):
    """Return set of symbol pairs in a word.

    Word is represented as tuple of symbols (symbols being variable-length strings).
    """
    pairs = set()
    prev_char = word[0]
    for char in word[1:]:
        pairs.add((prev_char, char))
        prev_char = char
    return pairs


class _AbstractTokenizer(object):
    def __init__(
        self,
        vocab_file,
        merge_file,
        split_numbers=False,
        split_numbers_and_underscores=False,
        extra_tokens=None,
    ):
        self.encoder = json.load(self._maybe_open_rclone(vocab_file, "r"))
        for tok in extra_tokens:
            if tok in self.encoder:
                continue
            self.encoder[tok] = len(self.encoder)

        self.pat_str = self._build_pat_str(split_numbers, split_numbers_and_underscores)
        self.pat = re.compile(self.pat_str)
        self.decoder: Dict[int, str] = {v: k for k, v in self.encoder.items()}
        self.byte_encoder = bytes_to_unicode()
        self.byte_decoder = {v: k for k, v in self.byte_encoder.items()}
        self.special_tokens = self._find_special_tokens(self.encoder)

    def _build_pat_str(
        self, split_numbers: bool, split_numbers_and_underscores: bool
    ) -> str:
        """
        Return regex pattern according to specified options.
        """
        if split_numbers_and_underscores:
            return NUMBER_UNDERSCORE_SPLIT_REGEX
        elif split_numbers:
            return NUMBER_SPLIT_REGEX
        else:
            return VANILLA_REGEX

    def _find_special_tokens(self, vocab: Dict[str, int]) -> Dict[str, int]:
        """Extracts all the special tokens in the vocab."""
        return {
            k: v for k, v in vocab.items() if k.startswith("<|") and k.endswith("|>")
        }

    @classmethod
    def _load_vocab_file(cls, vocab_file: str) -> Dict[str, int]:
        """
        Load the vocab file.
        """
        with self._maybe_open_rclone(vocab_file) as f:
            return json.load(f)

    def __len__(self):
        return len(self.encoder)

    def convert_tokens_to_ids(self, tokens: List[str]) -> List[int]:
        """Converts a sequence of tokens into ids using the vocab."""
        ids = []
        if isinstance(tokens, str):
            # Can probably delete this
            return self.encoder.get(tokens, 0)
        for token in tokens:
            ids.append(self.encoder.get(token, 0))
        return ids

    @classmethod
    def _maybe_open_rclone(cls, *args, **kwargs):
        """
        Try to open with rclone, falling back to normal IO if not possible.
        """
        try:
            import rclonepy as rclone

            return rclone.open(*args, **kwargs)
        except Exception as e:
            logger.warning(
                f"Could not load vocab file with rclone, falling back to normal open: {e}"
            )
            return open(*args, **kwargs)


class GPT2Tokenizer(_AbstractTokenizer):
    """GPT-2 Byte-level BPE tokenizer."""

    def __init__(
        self,
        vocab_file,
        merge_file,
        split_numbers=False,
        split_numbers_and_underscores=False,
        extra_tokens=None,
    ):
        super().__init__(
            vocab_file=vocab_file,
            merge_file=merge_file,
            split_numbers=split_numbers,
            split_numbers_and_underscores=split_numbers_and_underscores,
            extra_tokens=extra_tokens,
        )
        bpe_data = (
            self._maybe_open_rclone(merge_file, "r", encoding="utf-8")
            .read()
            .split("\n")[1:-1]
        )
        bpe_merges = [tuple(merge.split()) for merge in bpe_data]
        self.bpe_ranks: Dict[Tuple, int] = dict(zip(bpe_merges, range(len(bpe_merges))))
        self.cache: Dict[str, str] = {}

    def bpe(self, token: str) -> str:
        if token in self.cache:
            return self.cache[token]
        word = tuple(token)
        pairs = get_pairs(word)

        if not pairs:
            return token

        while True:
            bigram = min(pairs, key=lambda pair: self.bpe_ranks.get(pair, float("inf")))
            if bigram not in self.bpe_ranks:
                break
            first, second = bigram
            new_word = []
            i = 0
            while i < len(word):
                try:
                    j = word.index(first, i)
                    new_word.extend(word[i:j])
                    i = j
                except Exception:
                    new_word.extend(word[i:])
                    break

                if word[i] == first and i < len(word) - 1 and word[i + 1] == second:
                    new_word.append(first + second)
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
            new_word = tuple(new_word)
            word = new_word
            if len(word) == 1:
                break
            else:
                pairs = get_pairs(word)
        word = " ".join(word)
        self.cache[token] = word
        return word

    def _special_token_regex(self):
        if hasattr(self, "__special_token_regex_cache"):
            return self.__special_token_regex_cache
        joined = "|".join(st.replace("|", "\\|") for st in self.special_tokens)
        pattern = "(" + joined + ")"
        self.__special_token_regex_cache = pattern
        return pattern

    def tokenize(self, text: str) -> List[str]:
        """Tokenize a string."""
        special_token_positions = [
            (x.span(), x.captures()[0])
            for x in re.finditer(self._special_token_regex(), text)
            if x.captures()[0] in self.encoder
        ]
        idx = 0
        full_tokens = []
        # Loop over the special token indices, and encode everything around them
        for (start, end), c in special_token_positions:
            if start == 0:
                full_tokens.append(c)
            else:
                full_tokens.extend(self._byte_encode_raw_text(text[idx:start]))
                full_tokens.append(c)
            idx = end
        if idx < len(text):
            full_tokens.extend(self._byte_encode_raw_text(text[idx:]))
        return full_tokens

    def _byte_encode_raw_text(self, text) -> List[int]:
        bpe_tokens = []
        for token in re.findall(self.pat, text):
            token = "".join(self.byte_encoder[b] for b in token.encode("utf-8"))
            bpe_tokens.extend(bpe_token for bpe_token in self.bpe(token).split(" "))
        return bpe_tokens

    def encode(self, text):
        return self.convert_tokens_to_ids(self.tokenize(text))

    def decode(self, tokens, errors="replace"):
        text = "".join([self.decoder[token] for token in tokens])
        text = bytearray([self.byte_decoder[c] for c in text]).decode(
            "utf-8", errors=errors
        )
        return text


class TiktokenTokenizer(_AbstractTokenizer):
    """GPT-2 Byte-level BPE tokenizer, powered by tiktoken."""

    def __init__(
        self,
        vocab_file,
        merge_file,
        split_numbers=False,
        split_numbers_and_underscores=False,
        extra_tokens=None,
    ):
        super().__init__(
            vocab_file=vocab_file,
            merge_file=merge_file,
            split_numbers=split_numbers,
            split_numbers_and_underscores=split_numbers_and_underscores,
            extra_tokens=extra_tokens,
        )
        self.name = os.path.basename(merge_file)
        self._allowed_special_tokens = set(self.special_tokens.keys())
        # tiktoken expects us to offset our merges if there are any special
        # tokens BEFORE merge tokens
        offset = self._find_special_token_offset(self.special_tokens)
        merges = self._load_merge_file(merge_file)
        self.merges = {m: i + offset for m, i in merges.items()}

        # finally build the actual tokenizer
        self._tiktoken = self._get_tiktoken()

    def _get_tiktoken(self):
        import tiktoken

        return tiktoken.Encoding(
            name=self.name,
            pat_str=self.pat_str,
            mergeable_ranks=self.merges,
            special_tokens=self.special_tokens,
        )

    def _find_special_token_offset(self, special_tokens):
        # Identifies neoffsets stemming from special tokens in the front of
        # the dictionary
        # suppose the hypothetical dictionary
        # <pad>: 0
        # <bos>: 1
        # the: 2
        # ...
        # <finalspecial>: 1000
        # <otherspecial>: 1001
        # we want to identify the offset "2" to raise all our merges by
        reverse = {id_: v for v, id_ in special_tokens.items()}
        for i in range(len(special_tokens) + 1):
            if i not in reverse:
                return i

    def tokenize(self, text: str) -> List[str]:
        """Encode text into a list of string tokens."""
        tokenids = self.encode(text)
        return [self.decode[i] for i in tokenids]

    def encode(self, text: str) -> List[int]:
        """Encode text into a list of tokens."""
        return self._tiktoken.encode(text, allowed_special=self._allowed_special_tokens)

    def decode(self, tokens: List[int], errors="replace") -> str:
        """Decode tokens into a string."""
        return self._tiktoken.decode(tokens, errors=errors)

    def __getstate__(self):
        # tiktoken objects aren't pickleable. That's fine, rebuild it.
        shallow = self.__dict__.copy()
        del shallow["_tiktoken"]
        return shallow

    def __setstate__(self, state):
        for slot, value in state.items():
            setattr(self, slot, value)
        self._tiktoken = self._get_tiktoken()

    @classmethod
    def _load_merge_file(cls, vocab_bpe_file: str) -> Dict[bytes, int]:
        """
        Reads a merges file and creates the bytes->id lookup table.
        """
        rank_to_intbyte = [
            b for b in range(2**8) if chr(b).isprintable() and chr(b) != " "
        ]
        data_gym_byte_to_byte = {chr(b): b for b in rank_to_intbyte}
        n = 0
        for b in range(2**8):
            if b not in rank_to_intbyte:
                rank_to_intbyte.append(b)
                data_gym_byte_to_byte[chr(2**8 + n)] = b
                n += 1
        assert len(rank_to_intbyte) == 2**8

        # vocab_bpe contains the merges along with associated ranks
        with cls._maybe_open_rclone(vocab_bpe_file, "r", encoding="utf-8") as f:
            vocab_bpe_contents = f.read()

        bpe_merges = [
            tuple(merge_str.split())
            for merge_str in vocab_bpe_contents.split("\n")[1:-1]
        ]

        def decode_data_gym(value: str) -> bytes:
            return bytes(data_gym_byte_to_byte[b] for b in value)

        # add the single byte tokens
        bpe_ranks = {bytes([b]): i for i, b in enumerate(rank_to_intbyte)}
        # add the merged tokens
        n = len(bpe_ranks)
        for first, second in bpe_merges:
            bpe_ranks[decode_data_gym(first) + decode_data_gym(second)] = n
            n += 1
        return bpe_ranks
