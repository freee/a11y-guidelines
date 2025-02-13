"""Generator for check-related content."""
from typing import Dict, Any, Iterator

from a11y_guidelines import Check, CheckTool
from ..base_generator import BaseGenerator

class AllChecksGenerator(BaseGenerator):
    """Generates the all checks page."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate all checks data.
        
        Yields:
            Dictionary containing all check data
        """
        allchecks = Check.template_data_all(self.lang)
        yield {'allchecks': allchecks}

    def get_dependencies(self) -> list[str]:
        return Check.list_all_src_paths()

class CheckExampleGenerator(BaseGenerator):
    """Generates check example pages."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate check example data.
        
        Yields:
            Dictionary containing check example data for each tool
        """
        for tool in CheckTool.list_all():
            yield {
                'filename': f'examples-{tool.id}',
                'examples': tool.example_template_data(self.lang)
            }

    def get_dependencies(self) -> list[str]:
        return [tool.src_path for tool in CheckTool.list_all()]
