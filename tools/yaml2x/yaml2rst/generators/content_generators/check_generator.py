"""Generators for check-related content."""
from typing import Dict, Any, Iterator, List

from a11y_guidelines import Check, CheckTool
from ..common_generators import SingleFileGenerator, ListBasedGenerator
from ..base_generator import BaseGenerator

class CheckGeneratorBase(BaseGenerator):
    """Base class for check-related generators."""
    
    def get_dependencies(self) -> list[str]:
        """Get check file dependencies."""
        return Check.list_all_src_paths()

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate check data."""
        return True

class AllChecksGenerator(SingleFileGenerator, CheckGeneratorBase):
    """Generates the all checks page."""

    def get_template_data(self) -> Dict[str, Any]:
        """Generate all checks data."""
        self.logger.info("Generating all checks data")
        allchecks = list(Check.template_data_all(self.lang))  # ジェネレーターをリストに変換
        self.logger.info(f"Generated {len(allchecks)} checks")
        return {'allchecks': allchecks}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate all checks data."""
        return 'allchecks' in data and isinstance(data['allchecks'], list)

class CheckExampleGenerator(ListBasedGenerator[CheckTool], CheckGeneratorBase):
    """Generates check example pages."""

    def get_items(self) -> List[CheckTool]:
        """Get all check tools."""
        return CheckTool.list_all()

    def process_item(self, tool: CheckTool) -> Dict[str, Any]:
        """Process a single check tool."""
        return {
            'filename': f'examples-{tool.id}',
            'examples': tool.example_template_data(self.lang)
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate check example data."""
        required_fields = ['filename', 'examples']
        return all(field in data for field in required_fields)

    def get_dependencies(self) -> list[str]:
        """Get check tool file dependencies."""
        return [tool.src_path for tool in CheckTool.list_all()]
