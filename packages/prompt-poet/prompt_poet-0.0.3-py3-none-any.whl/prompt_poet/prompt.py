"""Construct a Prompt Poet (PP) prompt given data and a template."""

import inspect
import logging
import math
from dataclasses import dataclass
from functools import reduce

import yaml
from examples import cai_helpers
from template import Template
from tokenizer import AbstractTokenizer, get_default_tokenizer

SPACE_MARKER = "<|space|>"
DEFAULT_TRUNCATION_STEP = 1000

@dataclass
class PromptPart:
    """Container representing repeated prompt parts from the template."""

    name: str
    raw_string: str
    tokens: list[int] = None


class Prompt:
    """Construct a Prompt Poet (PP) prompt given data and a template.

    :param template_data: The data that will be used to render the Jinja2
        syntax in the template.
    :param template_name: An optional filepath to the file containing the
        raw template.
    :param token_limit: An optional maximum number of tokens used by this
        prompt _after_ truncation via `truncate`. A value of -1 means no
        truncation will take place.
    :param template: An optional `Template` object representing a PP template.
        If provided, this will override `template_name`.
    """

    def __init__(
        self, 
        template_data: dict,
        template_name: str = None,
        template_dir: str = None,
        package_name: str = None,
        raw_template: str = None,
        logger: logging.LoggerAdapter = None,
        tokenizer: AbstractTokenizer = None,
        token_limit: int = -1,
        truncation_step: int = DEFAULT_TRUNCATION_STEP,
        from_cache: bool = False,
        from_examples: bool = False,
        space_marker: str = SPACE_MARKER,
        newline: str = "\n",
        escaped_newline: str = "\\n",
        carriage_return: str = "\r",
        escaped_carriage_return: str = "\\r",
        single_quote: str = "'",
        escaped_single_quote: str = "\'",
    ):
        self._template = Template(
            template_name=template_name,
            template_dir=template_dir,
            package_name=package_name,
            raw_template=raw_template,
            logger=logger,
            from_cache=from_cache,
            from_examples=from_examples,
        )
        self._template_data = template_data
        self._provided_logger = logger
        self._token_limit = token_limit
        self._truncation_step = truncation_step
        self._from_cache = from_cache
        self._from_examples = from_examples
        self._space_marker = space_marker
        self._newline = newline
        self._escaped_newline = escaped_newline
        self._carriage_return = carriage_return
        self._escaped_carriage_return = escaped_carriage_return
        self._single_quote = single_quote
        self._escaped_single_quote = escaped_single_quote
        self._tokenizer = tokenizer

        self._rendered_template = None
        self._parts = None
        self._parts_bak = None

        self._load_special_template_data()
        self._render_parts()

    def tokenize(self):
        """Tokenize the prompt parts."""
        if not self._parts:
            raise ValueError(f"Nothing to tokenize: {self._parts=}.")

        # Lazy load the tokenizer.
        if self._tokenizer is None:
            self._tokenizer = get_default_tokenizer()

        for part in self._parts:
            self._tokenize_part(part)

    def truncate(self, token_limit: int = None):
        """An idempotent operation which truncates the rendered template according to the token limit."""
        if token_limit is not None:
            self.logger.info(f"Overriding {self._token_limit=} with {token_limit=}")
        else:
            token_limit = self._token_limit    

        if token_limit == -1:
            self.logger.info(f"No truncation necessary: {token_limit=}")
            return

        if token_limit <= 0:
            raise ValueError(f"Invalid token limit: {token_limit=}")

        # Reset the parts to the pretruncation state, if necessary. Ensures idempotency.
        self._parts = self.pretruncation_parts

        # TODO: Truncate the parts.

    @property
    def template_name(self) -> str:
        """The metadata associated with the template."""
        return self._template.template_name

    @property
    def template_dir(self) -> str:
        """The metadata associated with the template."""
        return self._template.template_dir

    @property
    def template_package_name(self) -> str:
        """The metadata associated with the template."""
        return self._template.template_package_name

    @property
    def pretruncation_parts(self) -> list[PromptPart]:
        """The parts of the prompt."""
        return self._parts_bak if self._parts_bak else self._parts

    @property
    def parts(self) -> list[PromptPart]:
        """The parts of the prompt."""
        return self._parts

    @property
    def pretruncation_string(self) -> str: 
        """The direct string representation of the final (truncated) prompt."""
        return reduce(
            lambda acc, part: acc + part.raw_string, self.pretruncation_parts, ""
        )

    @property
    def string(self) -> str: 
        """The direct string representation of the final (truncated) prompt."""
        return reduce(
            lambda acc, part: acc + part.raw_string, self._parts, ""
        )

    @property
    def pretruncation_string(self) -> str: 
        """The direct string representation of the final (truncated) prompt."""
        return reduce(lambda acc, part: acc + part.tokens, self.pretruncation_parts, [])

    @property
    def tokens(self) -> str:
        """The direct token representation of the prompt."""
        return reduce(lambda acc, part: acc + part.tokens, self._parts, [])

    @property
    def tokenizer(self) -> AbstractTokenizer:
        """The tokenizer used to tokenize the prompt."""
        if not self._tokenizer:
            self._tokenizer = get_default_tokenizer()

        return self._tokenizer

    @property
    def openai(self) -> str:
        """The OpenAI API specification representation of the prompt."""
        pass

    @property
    def logger(self) -> str:
        if self._provided_logger:
            return self._provided_logger 

        return logging.getLogger(__name__)

    def _calculate_num_tokens_to_truncate(self):
        """Calculates the number of messages to truncate."""
        num_surplus_tokens = max(0, self.num_total_tokens - self.token_limit)
        return (
            math.ceil(num_surplus_tokens / self._truncation_step) * self._truncation_step
        )

    def _tokenize_part(self, part: PromptPart):
        # Avoid retokenizing the part if it has already been tokenized.
        if not part.tokens:
            part.tokens = self._tokenizer.tokenize(part.raw_string)

    def _load_special_template_data(self):
        """Load special data into the template context."""
        if "token_limit" in self._template_data:
            raise ValueError("`token_limit` is a reserved key in the template data.")

        if "escape_special_characters" in self._template_data:
            raise ValueError("`escape_special_characters` is a reserved key in the template data.")

        self._template_data["token_limit"] = self._token_limit
        self._template_data["escape_special_characters"] = self._escape_special_characters

        if self._from_examples:
            cai_functions = {}
            for name, obj in inspect.getmembers(cai_helpers):
                if inspect.isfunction(obj):
                    cai_functions[name] = obj
            self._template_data.update(cai_functions)

    def _render_parts(self):
        self._rendered_template = self._template.render_template(self._template_data)

        try:
            loaded_yaml = yaml.load(self._rendered_template, Loader=yaml.CSafeLoader)
        except Exception as ex:
            self.logger.error(
                f"Error loading yaml from rendered template {ex=}",
                exc_info=True,
            )
            raise ex

        # Note: make sure the fill is performant as this can be large.
        self._parts = [None] * len(loaded_yaml)
        for idx, yaml_part in enumerate(loaded_yaml):
            part = PromptPart(**yaml_part)
            self._cleanup_raw_string(part)
            self._parts[idx] = part

    def _cleanup_raw_string(self, part: PromptPart):
        """Remove whitespace and unescape special characters, if present."""
        raw_string = part.raw_string.strip().replace(self._space_marker, " ")
        part.raw_string = self._unescape_special_characters(raw_string)

    def _escape_special_characters(self, string: str) -> str:
        """Escape sequences that will break yaml parsing."""
        return (
            string.replace(self._newline, self._escaped_newline)
            .replace(self._carriage_return, self._escaped_carriage_return)
            .replace(self._single_quote, self._escaped_single_quote)
        )

    def _unescape_special_characters(self, string: str) -> str:
        """Unescape special characters."""
        return (
            string.replace(self._escaped_newline, self._newline)
            .replace(self._escaped_carriage_return, self._carriage_return)
            .replace(self._escaped_single_quote, self._single_quote)
        )
