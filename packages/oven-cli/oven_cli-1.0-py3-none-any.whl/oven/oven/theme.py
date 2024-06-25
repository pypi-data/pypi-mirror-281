import logging
from pathlib import Path
from typing import Dict, Optional, List

from importlib import resources

from markdown import Markdown
from jinja2 import Environment, FileSystemLoader

from .utils import load_module
from .config import Config

INTERNAL_FILTERS_PACKAGE = 'oven.oven.internal_filters'
INTERNAL_EXTENSIONS_PACKAGE = 'oven.oven.internal_extensions'


class Theme:
    _instance = None

    def __new__(cls, config: Optional[Config] = None):
        if cls._instance is None:
            cls._instance = super(Theme, cls).__new__(cls)
            cls._instance.__initialize(config)
        return cls._instance

    def __initialize(self, config: Config) -> None:
        self.config = config
        self.env = Environment(loader=FileSystemLoader(self.config.theme_path), autoescape=True)
        self.extensions = []

        self.__load_filters(INTERNAL_FILTERS_PACKAGE, True)
        self.__load_filters(self.config.filters_path)

        if self.config.is_build_config():
            self.__load_extensions(INTERNAL_EXTENSIONS_PACKAGE, True)
            self.__load_extensions(self.config.extensions_path)
            self.markdown = Markdown(extensions=self.extensions)

        if self.config.is_gather_config():
            self.__render_dummy_templates()

    # TODO:
    #   Refactor this so it doesn't 
    #   duplicate with scripts loading
    def __load_modules(self, path: Path, name: str, internal: bool):
        modules = []
        for script_name in map(str, path.iterdir()) if not internal else resources.contents(path):
            if script_name.endswith('.py'):
                if internal:
                    with resources.path(path, script_name) as script_path:
                        modules.append(load_module(name, script_path))
                else:
                    modules.append(load_module(name, script_name))
        return modules

    def __load_filters(self, path: Path, internal: bool = False) -> None:
        if not (internal or path.exists()):
            return
        logging.info(f'[Theme] Loading filters from {path if not internal else 'INTERNAL'}')

        filter_count = 0
        for module in self.__load_modules(path, 'oven_filter', internal):
            if hasattr(module, 'FILTER_NAME') and hasattr(module, 'custom_filter'):
                if not self.config.enabled_filters or module.FILTER_NAME in self.config.enabled_filters:
                    logging.info(f'[Theme] loaded filter: {module.FILTER_NAME}')
                    filter_count += 1
                    self.env.filters[module.FILTER_NAME] = module.custom_filter
        logging.info(f'[Theme] loaded {filter_count} filters')

    def __load_extensions(self, path: Path, internal: bool = False) -> None:
        if not (internal or path.exists()):
            return
        logging.info(f'[Theme] Loading extensions from {path}')

        extensions_count = 0
        left_over_extensions = self.config.enabled_extensions
        for module in self.__load_modules(path, 'oven_extension', internal):
            if hasattr(module, 'EXTENSION_NAME') and hasattr(module, 'EXTENSION_CLASS'):
                if not self.config.enabled_extensions or module.EXTENSION_NAME in self.config.enabled_extensions:
                    logging.info(f'[Theme] loaded extension: {module.EXTENSION_NAME}')
                    extensions_count += 1
                    self.extensions += [module.EXTENSION_CLASS()]
                    left_over_extensions.remove(module.EXTENSION_NAME)

        for extension in left_over_extensions:
            logging.info(f'[Theme] loaded extension: {extension}')
            self.extensions += [extension]
            extensions_count += 1

        logging.info(f'[Theme] loaded {extensions_count} extensions')

    def __render_dummy_templates(self) -> None:
        for template_name in self.env.list_templates():
            template = self.env.get_template(template_name)
            template.render({**self.config.site_context, 'config': self.config, 'lang': self.config.locales_main,
                             'this': ''})

    def render(self, template_name: str, contents: Optional[dict] = None, context: Optional[Dict] = None,
               exclude_pre_render: Optional[List[str]] = None) -> str:
        if not exclude_pre_render:
            exclude_pre_render = []
        template = self.env.get_template(template_name)

        if contents is None:
            contents = {}
        for key, text in contents.items():
            if key not in exclude_pre_render:
                content_template = self.env.from_string(self.markdown.convert(text))
                contents[key] = content_template.render({'lang': context['lang']})
            else:
                contents[key] = self.markdown.convert(text)

        return template.render({**contents, **{**self.config.site_context, **context, 'config': self.config}})
