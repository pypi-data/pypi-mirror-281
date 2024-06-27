from abc import ABC, abstractmethod
from threading import Lock
from importlib.metadata import version, PackageNotFoundError

_tokenizer_lock = Lock()
_TOKENIZER = None


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

def _check_chartok_version():
    install_cmd = "python -m pip install chartok@https://characterai.io/py_wheels/chartok/chartok-0.4.3-py3-none-any.whl"
    try:
        installed_version = version("chartok")
    except PackageNotFoundError:
        raise ImportError(f"The 'chartok' package not found. Consider installing it with `{install_cmd}`.")
    if installed_version != "0.4.3":
        raise ImportError(
            f"Prompt Poet requires chartok==0.4.3, but found {installed_version}. Consider installing it with `{install_cmd}`."
        )

def get_default_tokenizer():
    """Get the default Prompt Poet (PP) tokenizer."""
    # Only build tokenizer if necessary.
    _check_chartok_version()

    # pylint: disable=import-outside-toplevel
    from chartok import heather

    global _TOKENIZER
    with _tokenizer_lock:
        if _TOKENIZER is None:
            _TOKENIZER = heather()
    return _TOKENIZER

