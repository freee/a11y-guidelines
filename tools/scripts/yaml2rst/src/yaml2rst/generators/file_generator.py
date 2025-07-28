"""Main file generation orchestrator."""
from typing import Dict, Any, Type
from dataclasses import dataclass
from pathlib import Path
import logging

from ..template_manager import TemplateManager
from .base_generator import BaseGenerator, GeneratorError
from .mixins import ValidationMixin


@dataclass(frozen=True)
class GeneratorConfig(ValidationMixin):
    """Configuration for a generator instance."""
    generator_class: Type[BaseGenerator]
    template_name: str
    output_path: str
    is_single_file: bool = False
    extra_args: Dict[str, Any] = None

    def validate(self) -> None:
        """Validate configuration parameters using ValidationMixin."""
        config_data = {
            'template_name': self.template_name,
            'output_path': self.output_path
        }

        # Use ValidationMixin methods for consistent validation
        if not self.validate_string_field(config_data, 'template_name'):
            raise ValueError("Template name must not be empty")
        if not self.validate_string_field(config_data, 'output_path'):
            raise ValueError("Output path must not be empty")

        # Validate required fields are present
        if not self.validate_required_fields(
                config_data, ['template_name', 'output_path']):
            raise ValueError("Required configuration fields are missing")


class FileGenerator:
    """Orchestrates file generation using content generators and templates."""

    def __init__(self, templates: Dict[str, TemplateManager], lang: str):
        """Initialize the file generator."""
        self.templates = templates
        self.lang = lang
        self.logger = logging.getLogger(self.__class__.__name__)

    def generate(self, config: GeneratorConfig, build_all: bool,
                 targets: list[str]) -> None:
        """Generate files using the specified generator configuration."""
        try:
            self.logger.info(
                f"Starting generation with config: {config}, "
                f"build_all: {build_all}")
            config.validate()

            if config.template_name not in self.templates:
                raise GeneratorError(
                    f"Template not found: {config.template_name}")

            if config.extra_args:
                generator = config.generator_class(
                    **{'lang': self.lang, **config.extra_args})
            else:
                generator = config.generator_class(self.lang)

            template = self.templates[config.template_name]
            output_path = Path(config.output_path)

            if not config.is_single_file:
                self._ensure_directory(output_path)

            for data in generator.generate():
                try:
                    data['lang'] = self.lang
                    dest_path = self._determine_destination(
                        config, output_path, data)
                    self.logger.info(f"Processing destination: {dest_path}")

                    if self._should_generate(config, build_all, targets,
                                             dest_path):
                        self.logger.info(f"Generating file: {dest_path}")
                        template.write_rst(data, dest_path)
                    else:
                        self.logger.info(f"Skipping file: {dest_path}")

                except Exception as e:
                    self.logger.error(f"Failed to generate file: {e}")
                    raise GeneratorError(
                        f"File generation failed: {e}") from e

        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            raise GeneratorError(f"Failed to generate files: {e}") from e

    def _ensure_directory(self, path: Path) -> None:
        """Ensure the directory exists."""
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            self.logger.error(f"Failed to create directory {path}: {e}")
            raise GeneratorError(
                f"Failed to create directory: {e}") from e

    def _determine_destination(
        self,
        config: GeneratorConfig,
        output_path: Path,
        data: Dict[str, Any]
    ) -> Path:
        """Determine the destination path for the generated file."""
        if config.is_single_file:
            return output_path
        return output_path / f"{data['filename']}.rst"

    def _should_generate(
        self,
        config: GeneratorConfig,
        build_all: bool,
        targets: list[str],
        dest_path: Path
    ) -> bool:
        """Determine if the file should be generated."""
        if build_all:
            return True
        dest_str = str(dest_path)
        if dest_str in targets:
            return True
        if not config.is_single_file and str(dest_path.parent) in targets:
            return True
        return False
