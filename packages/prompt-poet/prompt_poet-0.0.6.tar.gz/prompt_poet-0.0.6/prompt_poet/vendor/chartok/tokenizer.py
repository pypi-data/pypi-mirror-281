# coding=utf-8
# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from enum import Enum
import logging
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from .gpt2_tokenization import GPT2Tokenizer, TiktokenTokenizer
from typing import List, NamedTuple, Optional, Set
import argparse
import re
import pkg_resources

try:
    import tiktoken

    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False


class TokenizerBackend(Enum):
    GPT2 = "gpt2"
    TIKTOKEN = "tiktoken"


class TokenizerConfig(NamedTuple):
    vocab: Path
    merge: Path

    @staticmethod
    def from_vocab_file(
        vocab_file: str, merge_file: Optional[str] = None
    ) -> TokenizerConfig:
        vocab = Path(vocab_file)
        if merge_file is None:
            assert vocab.name.endswith("vocab.json"), "Vocab file not in right format"
            merge = vocab.parent / re.sub(
                "^(.*)vocab.json$", r"\1merges.txt", vocab.name
            )
        else:
            merge = Path(merge_file)
        return TokenizerConfig(vocab, merge)


PRETRAINED_TOKENIZER_CONFIGS = {
    "heather": TokenizerConfig.from_vocab_file(
        pkg_resources.resource_filename("chartok", "data/bpe-160000-vocab.json")
    ),
    "invincible": TokenizerConfig.from_vocab_file(
        pkg_resources.resource_filename(
            "chartok", "data/invincible-bpe-160000-vocab.json"
        )
    ),
    "gpt2": TokenizerConfig.from_vocab_file(
        pkg_resources.resource_filename("chartok", "data/gpt2-vocab.json")
    ),
}

logger = logging.getLogger(__name__)


def build_tokenizer_offline(
    tokenizer: str,
    tokenization_split_numbers: bool = False,
    tokenization_split_numbers_and_underscores: bool = False,
    tensor_model_parallel_size: int = 1,
    backend=None,
):
    # Megatron default for building tokenizer
    args = argparse.Namespace(
        tokenizer=tokenizer,
        tokenization_split_numbers=tokenization_split_numbers,
        tokenization_split_numbers_and_underscores=tokenization_split_numbers_and_underscores,
        rank=0,
        vocab_extra_ids=0,
        tensor_model_parallel_size=tensor_model_parallel_size,
        make_vocab_size_divisible_by=128,
        backend=backend,
    )
    tokenizer = build_tokenizer(args)
    return tokenizer


def build_tokenizer(args):
    """Initialize tokenizer."""
    logger.debug("building tokenizer")

    if args.tokenizer in PRETRAINED_TOKENIZER_CONFIGS:
        tokenizer_config = PRETRAINED_TOKENIZER_CONFIGS[args.tokenizer]
    else:
        tokenizer_config = TokenizerConfig.from_vocab_file(args.tokenizer)

    tokenizer = _GPT2BPETokenizer(
        tokenizer_config.vocab.as_posix(),
        tokenizer_config.merge.as_posix(),
        split_numbers=args.tokenization_split_numbers,
        split_numbers_and_underscores=args.tokenization_split_numbers_and_underscores,
        backend=getattr(args, "backend", None),
    )

    # Add vocab size.
    args.padded_vocab_size = _vocab_size_with_padding(tokenizer.vocab_size, args)

    return tokenizer


def _vocab_size_with_padding(orig_vocab_size, args):
    """Pad vocab size so it is divisible by model parallel size and
    still having GPU friendly size.

    Always increase it by at least one.
    """
    new_vocab_size = orig_vocab_size + 1
    new_vocab_size += -new_vocab_size % args.make_vocab_size_divisible_by

    if args.rank == 0:
        logger.debug(
            "padded vocab (size: {}) with {} dummy tokens "
            "(new size: {})".format(
                orig_vocab_size, new_vocab_size - orig_vocab_size, new_vocab_size
            )
        )
    return new_vocab_size


class AbstractTokenizer(ABC):
    """Abstract class for tokenizer."""

    def __init__(self, name):
        self.name = name
        super().__init__()

    @property
    @abstractmethod
    def vocab_size(self):
        pass

    @property
    @abstractmethod
    def vocab(self):
        """Dictionary from vocab text token to id token."""
        pass

    @property
    @abstractmethod
    def inv_vocab(self):
        """Dictionary from vocab id token to text token."""
        pass

    @abstractmethod
    def tokenize(self, text):
        pass

    def detokenize(self, token_ids):
        raise NotImplementedError(
            "detokenizer is not implemented for {} " "tokenizer".format(self.name)
        )

    @property
    def cls(self):
        raise NotImplementedError(
            "CLS is not provided for {} " "tokenizer".format(self.name)
        )

    @property
    def sep(self):
        raise NotImplementedError(
            "SEP is not provided for {} " "tokenizer".format(self.name)
        )

    @property
    def pad(self):
        raise NotImplementedError(
            "PAD is not provided for {} " "tokenizer".format(self.name)
        )

    @property
    def eod(self):
        raise NotImplementedError(
            "EOD is not provided for {} " "tokenizer".format(self.name)
        )

    @property
    def mask(self):
        raise NotImplementedError(
            "MASK is not provided for {} " "tokenizer".format(self.name)
        )


class _GPT2BPETokenizer(AbstractTokenizer):
    """
    Wrapper around GPT2 BPE tokenizer.

    Args:
        vocab_file: an rclone path to a vocab.json file
        merge_file: an rclone path to a merges.txt file
        split_numbers: whether to represent numbers as unique digits
        backend (optional): specifies whether to use python or tiktoken
          backend. Default is fastest available. Either "gpt2" or "tiktoken".
    """

    def __init__(
        self,
        vocab_file: str,
        merge_file: str,
        split_numbers: bool = False,
        split_numbers_and_underscores: bool = False,
        backend: Optional[str] = None,
    ):
        name = "GPT2 BPE"
        super().__init__(name)

        # the following extra tokens are not included in the vocab file
        extra_token_names = ["bom_ood"]
        extra_tokens = [f"<|{name.upper()}|>" for name in extra_token_names]

        if backend == "tiktoken" or (HAS_TIKTOKEN and backend is None):
            # use the tiktoken backend if the user forces it or we're allowed free
            # reign
            self.tokenizer = TiktokenTokenizer(
                vocab_file,
                merge_file,
                split_numbers=split_numbers,
                split_numbers_and_underscores=split_numbers_and_underscores,
                extra_tokens=extra_tokens,
            )
        elif backend == "gpt2" or (not HAS_TIKTOKEN and backend is None):
            # use the gpt2 backend if the user forces it or we don't have tiktoken
            # installed
            logger.warning("Tokenization can be sped up by pip install tiktoken==0.2.0")
            self.tokenizer = GPT2Tokenizer(
                vocab_file,
                merge_file,
                split_numbers=split_numbers,
                split_numbers_and_underscores=split_numbers_and_underscores,
                extra_tokens=extra_tokens,
            )
        else:
            raise ValueError(
                f"Don't know what to do with tokenizer_backend = {backend}"
            )

        e = self.tokenizer.encoder
        self.eod_id = e["<|endoftext|>"]
        self.bom_id = e["<|beginningofmessage|>"]
        self.bom_emoji_drop_id = e["<|beginningofmessageemojidrop|>"]
        self.eom_id = e["<|endofmessage|>"]
        self.bod_id = e["<|beginningofdialog|>"]
        self.trunc_id = e["<|truncated|>"]
        self.pad_id = e["<|pad|>"]
        self.mask_id = e["<|mask|>"]
        self.bo_innerdialog_id = e["<|beginningofinnerdialog|>"]
        self.eo_innerdialog_id = e["<|endofinnerdialog|>"]
        self.missing_id = e["<|missing|>"]
        self.dynamic_input_id = e["<|dynamicinput|>"]
        self.from_ts = e.get("<|TS|>", None)
        self.end_from_ts = e.get("<|END_TS|>", None)
        self.to_ts = e.get("<|TO_TS|>", None)
        self.end_to_ts = e.get("<|END_TO_TS|>", None)
        self.grounded = e.get("<|GROUNDED|>", None)
        self.end_of_sample_dialog_id = e.get("<|endofsampledialog|>", None)
        for name in extra_token_names:
            setattr(self, name + "_id", e[f"<|{name.upper()}|>"])

        self.special_ids: Set[int] = set(
            [v for v in self.tokenizer.special_tokens.values()]
            + list(range(self.vocab_size - len(extra_tokens), self.vocab_size))
        )

    @property
    def vocab_size(self):
        return len(self.tokenizer.encoder)

    @property
    def vocab(self):
        return self.tokenizer.encoder

    @property
    def inv_vocab(self):
        return self.tokenizer.decoder

    def encode(self, text: str) -> List[int]:
        return self.tokenize(text)

    def decode(self, token_ids: List[int], errors="replace") -> str:
        return self.detokenize(token_ids, errors=errors)

    def tokenize(self, text: str) -> List[int]:
        return self.tokenizer.encode(text)

    def detokenize(self, token_ids: List[int], errors="replace") -> str:
        return self.tokenizer.decode(token_ids, errors=errors)

    @property
    def eod(self):
        return self.eod_id

    @property
    def eom(self):
        return self.eom_id

    @property
    def bom(self):
        return self.bom_id

    @property
    def bom_emoji_drop(self):
        return self.bom_emoji_drop_id

    @property
    def bod(self):
        return self.bod_id

    @property
    def trunc(self):
        return self.trunc_id

    @property
    def pad(self):
        return self.pad_id

    @property
    def mask(self):
        return self.mask_id

    @property
    def begin_innerdialog(self):
        return self.bo_innerdialog_id

    @property
    def end_innerdialog(self):
        return self.eo_innerdialog_id

    @property
    def missing(self):
        return self.missing_id

    @property
    def dynamic_input(self):
        return self.dynamic_input_id

    @property
    def end_of_sample_dialog(self):
        if self.end_of_sample_dialog_id is None:
            raise ValueError("<|endofsampledialog|> is not provided in the vocabulary")
        return self.end_of_sample_dialog_id

    def is_special_token(self, token):
        return token in self.special_ids


class GPT4Tokenizer:
    def __init__(self, add_special=True):
        self.name = "GPT4"
        if not add_special:
            self.tokenizer = tiktoken.encoding_for_model("gpt-4")
        else:
            enc = tiktoken.encoding_for_model("gpt-4")

            additional_tokens = [
                "<|pad|>",
                "<|beginningofmessage|>",
                "<|beginningofmessageemojidrop|>",
                "<|endofmessage|>",
                "<|beginningofdialog|>",
                "<|truncated|>",
                "<|mask|>",
                "<|beginningofinnerdialog|>",
                "<|endofinnerdialog|>",
                "<|missing|>",
                "<|dynamicinput|>",
                "<|endofsampledialog|>",
                "<|TS|>",
                "<|END_TS|>",
                "<|TO_TS|>",
                "<|END_TO_TS|>",
                "<|GROUNDED|>",
            ]

            idx = enc.n_vocab
            bpe_ranks = enc._mergeable_ranks

            special_tokens = dict()
            for sp in additional_tokens:
                special_tokens[sp] = idx
                idx += 1

            self.tokenizer = tiktoken.Encoding(
                name="gpt4_modified",
                pat_str=enc._pat_str,
                mergeable_ranks=bpe_ranks,
                special_tokens={**enc._special_tokens, **special_tokens},
            )

    @property
    def eom_id(self):
        return self.tokenizer._special_tokens["<|endofmessage|>"]

    @property
    def eom(self):
        return self.eom_id

    @property
    def bom_id(self):
        return self.tokenizer._special_tokens["<|beginningofmessage|>"]

    @property
    def bom(self):
        return self.bom_id

    @property
    def pad(self):
        return self.pad_id

    @property
    def pad_id(self):
        return self.tokenizer._special_tokens["<|pad|>"]

    @property
    def bod_id(self):
        return self.tokenizer._special_tokens["<|beginningofdialog|>"]

    @property
    def bod(self):
        return self.bod_id

    @property
    def eod_id(self):
        return self.tokenizer._special_tokens["<|endoftext|>"]

    @property
    def bod(self):
        return self.eod_id

    def encode(self, text: str) -> List[int]:
        return self.tokenize(text)

    def decode(self, token_ids: List[int], errors="replace") -> str:
        return self.detokenize(token_ids, errors=errors)

    def tokenize(self, text: str) -> List[int]:
        return self.tokenizer.encode(text, allowed_special="all")

    def detokenize(self, token_ids: List[int], errors="replace") -> str:
        return self.tokenizer.decode(token_ids, errors=errors)

    @property
    def vocab_size(self):
        return self.tokenizer.n_vocab


class HFTokenizer:
    def __init__(
        self,
        model_name_or_path="mistralai/Mistral-7B-v0.1",
        add_special_tokens=False,
    ):
        from transformers import AutoTokenizer

        self.add_special_tokens = add_special_tokens
        self.bom = 1
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name_or_path,
        )
        self.bod = 1
        self.eom = 2
        self.eod = 2

        if add_special_tokens:
            special_tokens_dict = {
                "additional_special_tokens": [
                    "<|pad|>",
                    "<|beginningofmessage|>",
                    "<|beginningofmessageemojidrop|>",
                    "<|endofmessage|>",
                    "<|beginningofdialog|>",
                    "<|truncated|>",
                    "<|mask|>",
                    "<|beginningofinnerdialog|>",
                    "<|endofinnerdialog|>",
                    "<|missing|>",
                    "<|dynamicinput|>",
                    "<|endofsampledialog|>",
                    "<|TS|>",
                    "<|END_TS|>",
                    "<|TO_TS|>",
                    "<|END_TO_TS|>",
                    "<|GROUNDED|>",
                ]
            }
            self.tokenizer.add_special_tokens(special_tokens_dict)

    @property
    def eom_id(self):
        return self.tokenizer._convert_token_to_id_with_added_voc("<|endofmessage|>")

    @property
    def bom_id(self):
        return self.tokenizer._convert_token_to_id_with_added_voc(
            "<|beginningofmessage|>"
        )

    def is_special_token(self, token):
        return token < 3

    @property
    def pad_id(self):
        return self.tokenizer._convert_token_to_id_with_added_voc("<|pad|>")

    @property
    def bod_id(self):
        return self.tokenizer._convert_token_to_id_with_added_voc(
            "<|beginningofdialog|>"
        )

    @property
    def eod_id(self):
        return self.tokenizer._convert_token_to_id_with_added_voc("<|endoftext|>")

    def encode(self, text: str) -> List[int]:
        return self.tokenize(text)

    def decode(self, token_ids: List[int]) -> str:
        return self.detokenize(token_ids)

    def tokenize(self, text: str) -> List[int]:
        return self.tokenizer.encode(
            text,
            add_special_tokens=self.add_special_tokens,
        )

    def detokenize(self, token_ids: List[int], **ignored) -> str:
        return self.tokenizer.decode(token_ids)

    @property
    def vocab_size(self):
        return self.tokenizer.vocab_size
