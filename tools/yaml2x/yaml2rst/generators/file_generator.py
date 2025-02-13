"""Main file generation orchestrator."""
import os
from typing import Dict, Any, Protocol, Type
from dataclasses import dataclass

from template_manager import TemplateManager
from .base_generator import BaseGenerator

@dataclass
class GeneratorConfig:
    """Configuration for a generator instance."""
    generator_class: Type[BaseGenerator]
    template_name: str
    output_path: str
    is_single_file: bool = False

class FileGenerator:
    """Orchestrates file generation using content generators and templates."""

    def __init__(self, templates: Dict[str, TemplateManager], lang: str):
        """Initialize the file generator.
        
        Args:
            templates: Dictionary of template managers
            lang: Language code for content generation
        """
        self.templates = templates
        self.lang = lang

    def generate(self, config: GeneratorConfig, build_all: bool, targets: list[str]) -> None:
        """Generate files using the specified generator configuration.
        
        Args:
            config: Generator configuration
            build_all: Flag to build all files
            targets: Specific files to build if not building all
        """
        generator = config.generator_class(self.lang)
        template = self.templates[config.template_name]

        # Create output directory if it doesn't exist
        if not config.is_single_file:
            os.makedirs(config.output_path, exist_ok=True)

        for data in generator.generate():
            data['lang'] = self.lang
            
            # Determine if we should generate this file
            if config.is_single_file:
                dest_path = config.output_path
                should_generate = build_all or dest_path in targets
            else:
                filename = f"{data['filename']}.rst"
                dest_path = os.path.join(config.output_path, filename)
                should_generate = build_all or dest_path in targets or config.output_path in targets

            if should_generate:
                template.write_rst(data, dest_path)

    def generate_makefile(
        self,
        template: TemplateManager,
        output_path: str,
        build_all: bool,
        targets: list[str],
        extra_vars: Dict[str, Any]
    ) -> None:
        """Generate makefile with special handling for build dependencies.
        
        Args:
            template: Template manager for makefile
            output_path: Output file path
            build_all: Flag to build all files
            targets: Specific files to build if not building all
            extra_vars: Additional variables for makefile template
        """
        makefile_vars = {
            'gl_yaml': '',
            'check_yaml': '',
            'faq_yaml': '',
            'depends': []
        }
        makefile_vars.update(extra_vars)

        if build_all or output_path in targets:
            template.write_rst(makefile_vars, output_path)
