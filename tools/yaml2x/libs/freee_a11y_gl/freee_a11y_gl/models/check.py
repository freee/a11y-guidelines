"""Check-related models for a11y-guidelines."""
from typing import Dict, List, Any, Optional, ClassVar
from dataclasses import dataclass
from .base import BaseModel
from ..relationship_manager import RelationshipManager
from ..config import Config, LanguageCode
from ..utils import uniq

class Check(BaseModel):
    """Check model for accessibility validation criteria."""

    object_type = "check"
    _instances: Dict[str, 'Check'] = {}

    def __init__(self, check: Dict[str, Any]):
        """Initialize check.
        
        Args:
            check: Dictionary containing check data
        """
        super().__init__(check['id'])

        if self.id in self._instances:
            raise ValueError(f'Duplicate check ID: {self.id}')
        
        self.sort_key = check['sortKey']
        if self.sort_key in [c.sort_key for c in self._instances.values()]:
            raise ValueError(f'Duplicate check sortKey: {self.sort_key}')

        self.check_text = check['check']
        self.severity = check['severity']
        self.target = check['target']
        self.platform = check['platform']
        self.src_path = check['src_path']

        # Initialize conditions
        self.conditions = []
        if 'conditions' in check:
            for condition in check['conditions']:
                self.conditions.append(Condition(condition, self))

        # Initialize implementations
        self.implementations = []
        if 'implementations' in check:
            self.implementations = [Implementation(**impl) for impl in check['implementations']]

        Check._instances[self.id] = self

    def condition_platforms(self) -> List[str]:
        """Get list of unique platforms from conditions."""
        return sorted({cond.platform for cond in self.conditions})

    def template_data(self, lang: str, **kwargs) -> Dict[str, Any]:
        """Get template data for check.
        
        Args:
            lang: Language code
            **kwargs: Additional template parameters
            
        Returns:
            Dictionary with check data formatted for templates
        """
        rel = RelationshipManager()
        gl_platform = kwargs.get('platform')

        data = {
            'id': self.id,
            'check': self.check_text[lang],
            'severity': Config.get_severity_tag(self.severity, lang),
            'target': Config.get_check_target_name(self.target, lang),
            'platform': self.join_items(self.platform, lang),
            'guidelines': []
        }

        # Add conditions if present
        if self.conditions:
            if not gl_platform:
                data['conditions'] = [cond.template_data(lang) for cond in self.conditions]
            else:
                data['conditions'] = [
                    cond.template_data(lang) 
                    for cond in self.conditions 
                    if cond.platform == 'general' or cond.platform in gl_platform
                ]

        # Add implementations if present
        if self.implementations:
            data['implementations'] = [impl.template_data(lang) for impl in self.implementations]

        # Add info references if present
        info = rel.get_related_objects(self, 'info_ref')
        if info:
            data['info_refs'] = [inforef.refstring() for inforef in info]

        # Add FAQs if present
        faqs = rel.get_sorted_related_objects(self, 'faq')
        if faqs:
            data['faqs'] = [faq.id for faq in faqs]

        # Add guidelines
        for gl in rel.get_sorted_related_objects(self, 'guideline'):
            data['guidelines'].append(gl.get_category_and_id(lang))

        return data

    @staticmethod
    def join_items(items: List[str], lang: str) -> str:
        """Join platform items with localized separator."""
        return Config.get_list_separator(lang).join(
            [Config.get_platform_name(item, lang) for item in items]
        )

    @classmethod
    def list_all_src_paths(cls) -> List[str]:
        """Get all check source paths."""
        return [check.src_path for check in cls._instances.values()]

    @classmethod
    def template_data_all(cls, lang: str) -> List[Dict[str, Any]]:
        """Get template data for all checks."""
        sorted_checks = sorted(cls._instances, key=lambda x: cls._instances[x].id)
        for check_id in sorted_checks:
            yield cls._instances[check_id].template_data(lang)

class Example:
    """Example use of a check procedure."""

    def __init__(self, procedure: 'Procedure', check: 'Check'):
        """Initialize example.
        
        Args:
            procedure: The procedure this example demonstrates
            check: The check this example belongs to
        """
        self.check_id = check.id
        self.check_text = check.check_text
        self.check_src_path = check.src_path
        self.procedure = procedure

    def template_data(self, lang: str) -> Dict[str, Any]:
        """Get template data for example."""
        template_data = self.procedure.template_data(lang)
        template_data.update({
            'tool': self.procedure.tool.id,
            'check_id': self.check_id,
            'check_text': self.check_text[lang]
        })
        return template_data

class CheckTool:
    """Tool used for accessibility checks."""

    _instances: ClassVar[Dict[str, 'CheckTool']] = {}

    def __init__(self, tool_id: str, names: Dict[str, str]):
        """Initialize check tool.
        
        Args:
            tool_id: Tool identifier
            names: Dictionary of localized names
        """
        self.id = tool_id
        self.names = names
        self.examples: List[Example] = []
        CheckTool._instances[tool_id] = self

    def add_example(self, example: Example) -> None:
        """Add an example for this tool.
        
        Args:
            example: Example instance to add
        """
        self.examples.append(example)

    def get_name(self, lang: str) -> str:
        """Get localized name for tool.
        
        Args:
            lang: Language code
            
        Returns:
            Localized name, falls back to Japanese
        """
        return self.names.get(lang, self.names['ja'])

    def get_dependency(self) -> List[str]:
        """Get list of file dependencies for this tool."""
        return uniq([ex.check_src_path for ex in self.examples])

    def example_template_data(self, lang: str) -> List[Dict[str, Any]]:
        """Get template data for all examples.
        
        Args:
            lang: Language code
            
        Returns:
            List of example template data
        """
        examples: Dict[str, Dict[str, Any]] = {}
        for example in self.examples:
            check_id = example.check_id
            if check_id not in examples:
                examples[check_id] = {
                    'check_id': check_id,
                    'check_text': example.check_text[lang],
                    'tool': self.id,
                    'procedures': []
                }
            examples[check_id]['procedures'].append(example.procedure.template_data(lang))
        return sorted(examples.values(), key=lambda x: x['check_id'])

    @classmethod
    def list_all(cls) -> List['CheckTool']:
        """Get all tool instances."""
        return list(cls._instances.values())

    @classmethod
    def list_all_ids(cls) -> List[str]:
        """Get all tool IDs."""
        return list(cls._instances.keys())

    @classmethod
    def get_by_id(cls, tool_id: str) -> Optional['CheckTool']:
        """Get tool by ID.
        
        Args:
            tool_id: Tool identifier
            
        Returns:
            Tool instance if found, None otherwise
        """
        return cls._instances.get(tool_id)

@dataclass
class YouTube:
    """YouTube video reference."""
    id: str
    title: str

    def template_data(self) -> Dict[str, str]:
        """Get template data for YouTube reference."""
        return {
            'id': self.id,
            'title': self.title
        }

@dataclass
class Method:
    """Implementation method for a check."""
    platform: str
    method: Dict[str, str]

    def template_data(self, lang: str) -> Dict[str, str]:
        """Get template data for method.
        
        Args:
            lang: Language code
        """
        return {
            'platform': Config.get_implementation_target_name(self.platform, lang),
            'method': self.method[lang]
        }

@dataclass
class Implementation:
    """Implementation details for a check."""
    title: Dict[str, str]
    methods: List[Dict[str, Any]]

    def __post_init__(self):
        """Convert method dictionaries to Method objects."""
        self.methods = [Method(**method) for method in self.methods]

    def template_data(self, lang: str) -> Dict[str, Any]:
        """Get template data for implementation."""
        return {
            'title': self.title[lang],
            'methods': [method.template_data(lang) for method in self.methods]
        }

class Procedure:
    """Check procedure for validation."""

    def __init__(self, condition: Dict[str, Any], check: 'Check'):
        """Initialize procedure.
        
        Args:
            condition: Dictionary containing procedure data
            check: Parent check instance
        """
        self.id = condition['id']
        tool_name = condition['tool']
        
        # Get or create tool
        if tool_name in CheckTool.list_all_ids():
            tool = CheckTool.get_by_id(tool_name)
            self.tool_display_name = None
        else:
            tool = CheckTool.get_by_id('misc')
            self.tool_display_name = tool_name
        self.tool = tool

        self.procedure = condition['procedure']
        self.note = condition.get('note')
        self.youtube = YouTube(**condition['YouTube']) if 'YouTube' in condition else None

        # Add example to tool
        self.tool.add_example(Example(self, check))

    def template_data(self, lang: str) -> Dict[str, Any]:
        """Get template data for procedure."""
        tool_display_name = self.tool_display_name or self.tool.get_name(lang)
        data = {
            'id': self.id,
            'tool_display_name': tool_display_name,
            'procedure': self.procedure[lang]
        }
        if self.note:
            data['note'] = self.note[lang]
        if self.youtube:
            data['YouTube'] = self.youtube.template_data()
        return data

    def object_data(self, platform: str) -> Dict[str, Any]:
        """Get object data for procedure."""
        tool_link = {
            'text': {},
            'url': {}
        }
        for lang in self.procedure.keys():
            baseurl = Config.get_examples_url(lang)
            tool_link['text'][lang] = self.tool_display_name or self.tool.get_name(lang)
            tool_link['url'][lang] = f'{baseurl}{self.tool.id}.html#{self.id}'
        return {
            'id': self.id,
            'platform': platform,
            'tool': self.tool.id,
            'toolLink': tool_link,
            'procedure': self.procedure
        }

class Condition:
    """Check condition for validation."""

    def __init__(self, condition: Dict[str, Any], check: 'Check'):
        """Initialize condition.
        
        Args:
            condition: Dictionary containing condition data
            check: Parent check instance
        """
        self.type = condition['type']
        self.platform = condition.get('platform')

        if self.type == 'simple':
            self.procedure = Procedure(condition, check)
        else:
            self.conditions = [Condition(cond, check) for cond in condition['conditions']]

    def procedures(self) -> List[Procedure]:
        """Get all procedures in this condition."""
        if self.type == 'simple':
            return [self.procedure]
        procedures = []
        for cond in self.conditions:
            procedures.extend(cond.procedures())
        return procedures

    def summary(self, lang: str) -> str:
        """Get localized summary of condition."""
        if self.type == 'simple':
            return f'{self.procedure.id}{Config.get_pass_text(lang)}'

        simple_conditions = [c.summary(lang) for c in self.conditions if c.type == 'simple']
        complex_conditions = [f'({c.summary(lang)})' for c in self.conditions if c.type != 'simple']

        conjunction_type = 'and' if self.type == 'and' else 'or'
        summary_separator = Config.get_separator(lang, conjunction_type)
        summary_connector = Config.get_conjunction(lang, conjunction_type)
        pass_singular_text = Config.get_pass_singular_text(lang)
        pass_plural_text = Config.get_pass_plural_text(lang)

        if len(simple_conditions) > 1:
            simple_conditions = [c.replace(pass_singular_text, '') for c in simple_conditions]
            simple_summary = f'{summary_separator.join(simple_conditions)}{pass_plural_text}'
            return f'{simple_summary}{summary_connector}{summary_connector.join(complex_conditions)}' if complex_conditions else simple_summary
        else:
            return summary_connector.join(simple_conditions + complex_conditions)

    def template_data(self, lang: str) -> Dict[str, Any]:
        """Get template data for condition."""
        if not self.platform:
            return {}

        data = {
            'platform': Config.get_platform_name(self.platform, lang),
            'condition': self.summary(lang)
        }
        procedures = self.procedures()
        if procedures:
            data['procedures'] = [proc.template_data(lang) for proc in procedures]
        return data

    def object_data(self, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get object data for condition."""
        data = {'type': self.type}
        if hasattr(self, 'platform'):
            data['platform'] = self.platform
            platform = self.platform

        if self.type == 'simple':
            data['procedure'] = self.procedure.object_data(platform)
        else:
            data['conditions'] = [cond.object_data(platform) for cond in self.conditions]
        return data
