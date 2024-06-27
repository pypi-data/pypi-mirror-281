"""Templating engine for rendering Jinja templates."""

import logging

import jinja2 as j2

from template_registry import TemplateRegistry


class Template:
    """A Prompt Poet (PP) template orignally represented as a valid *.yaml.j2 file.
    
    :param template_name: The name of the file containing the raw template.
    :param template_dir: The path to the directory housing the file
        `template_name`. If not provided the current working directory will
        be used. 
    :param package_name: The name of a python package used to find `template_name`
        within `template_dir` within the package.
    :param raw_template: A Prompt Poet template file represented as a string.
    :param logger: An optional logger to be used by `Template` and passed to 
        downstream components
    :param from_cache: Whether or not to retrieve the template from a cache.
    :param from_examples: Whether or not to use the Prompt Poet (PP) provided
        examples.
    """

    def __init__(
        self, 
        template_name: str = None, 
        template_dir: str = None, 
        package_name: str = None, 
        raw_template: str = None,
        logger: logging.LoggerAdapter = None,
        from_cache: bool = False,
        from_examples: bool = False,
    ):
        if raw_template and template_name:
            raise ValueError(f"Cannot provide both {raw_template=} and {template_name=}.")

        self._template_name, self._template_dir, self._package_name = (
            self._parse_template_metadata(
                template_name=template_name,
                template_dir=template_dir,
                package_name=package_name,
            )
        )
        self._raw_template = raw_template
        self._provided_logger = logger
        self._from_cache = from_cache
        self._from_examples = from_examples
        self._template = None
        self._rendered_template = None

        self._load_template()

    def _parse_template_metadata(self, template_name: str, template_dir: str, package_name: str) -> tuple[str, str, str]:
        """Parse the template metadata to determine the template source."""
        if template_dir and "/" in template_name:
            raise ValueError("Template name must not contain a path if `template_dir` is provided.")

        if template_dir and package_name:
            raise ValueError("Only one of `template_dir` or `package_name` may be provided.")

        if "/" in template_name:
            template_dir, template_name = template_name.rsplit("/", 1)

        if not template_dir:
            template_dir = "./"

        return (template_name, template_dir, package_name)

    def render_template(self, template_data: dict) -> str:
        """Render the jinja template with the provided template_data data.
        
        Fills the loaded template with the provided data. This is an
        idempotent operation.
        """
        if not self._template:
            raise ValueError(f"Template not loaded: {self._template=}")

        self._rendered_template = self._template.render(template_data)
        return self._rendered_template

    @property
    def rendered_template(self) -> j2.Template:
        return self._rendered_template

    @property
    def template(self) -> j2.Template:
        return self._template

    @property
    def logger(self) -> str:
        if self._provided_logger:
            return self._provided_logger 

        return logging.getLogger(__name__)

    @property
    def template_name(self) -> str:
        return self._template_name

    @property
    def template_dir(self) -> str:
        return self._template_dir

    @property
    def template_package_name(self) -> str:
        return self._template_package_name

    def _load_template(self):
        """Load a jinja2 template."""
        if self._raw_template:
            self._template = j2.Template(self._raw_template) 
        else:
            registry = TemplateRegistry(logger=self._provided_logger)
            self._template = registry.get_template(
                template_name=self._template_name, 
                template_dir=self._template_dir, 
                package_name=self._package_name, 
                use_examples=self._from_examples,
                use_cache=self._from_cache,
            )
