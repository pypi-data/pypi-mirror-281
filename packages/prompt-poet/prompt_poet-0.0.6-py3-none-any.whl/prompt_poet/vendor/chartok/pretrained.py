#!/usr/bin/env python
import logging
import os.path

import pkg_resources
from chartok.tokenizer import build_tokenizer_offline, GPT4Tokenizer, HFTokenizer

logger = logging.getLogger(__name__)


def get_tokenizer(name: str):
    if name == "heather":
        return heather()
    elif name == "gpt2" or name == "gpt2_split_digits":
        return gpt2()
    elif name == "gpt2_original":
        return gpt2_original()
    elif name == "invincible":
        return invincible()
    elif name == "gpt4":
        return gpt4()
    elif name == "mistral":
        return mistral()
    else:
        from transformers import AutoTokenizer

        return AutoTokenizer.from_pretrained(name)


DATA_DIR = pkg_resources.resource_filename("chartok", "data")


def invincible():
    """
    Provides an Invincible tokenizer.
    """
    return build_tokenizer_offline(
        tokenizer="invincible", tokenization_split_numbers_and_underscores=True
    )


def heather():
    """
    Provides a Heather tokenizer.
    """
    return build_tokenizer_offline(tokenizer="heather", tokenization_split_numbers=True)


def gpt2_split_digits():
    """
    Provides a GPT-2 tokenizer that splits digits.
    """
    return build_tokenizer_offline(tokenizer="gpt2", tokenization_split_numbers=True)


def gpt2_original():
    """
    Provides a GPT-2 tokenizer.
    """
    return build_tokenizer_offline(tokenizer="gpt2", tokenization_split_numbers=False)


def gpt2():
    """
    Provides a GPT-2 tokenizer that splits digits.
    """
    logger.warning("WARNING: Using this dictionary defaults to splitting digits")
    logger.warning(
        "WARNING: To use the correct GPT2 tokenizer, use `chartok.gpt2_original()`"
    )
    return gpt2_split_digits()


def gpt4():
    tokenizer = GPT4Tokenizer(add_special=True)
    return tokenizer


def mistral():
    tokenizer = HFTokenizer(model_name_or_path="mistralai/Mistral-7B-v0.1")

    return tokenizer


if __name__ == "__main__":
    tok = heather()
    print(tok.tokenize("This is a test"))
    tok2 = gpt4()
    print(tok2.tokenize("This is a test <|pad|><|beginningofmessage|>"))
    print(tok2.detokenize([2028, 374, 264, 1296, 220, 100277, 100278]))
    print(tok2.vocab_size)
    tok3 = mistral()
    print(tok3.tokenize("This is a test<|pad|><|beginningofmessage|><|endoftext|>"))
    print(tok3.detokenize([1, 851, 349, 264, 1369, 32017, 32007, 32000]))
    print(tok3.vocab_size)
