"""Makefile generator for managing build dependencies."""
from typing import Dict, Any, List
import os
from dataclasses import dataclass

from freee_a11y_gl import (
    Category, CheckTool, Faq, FaqTag, InfoRef, 
    Guideline, Check, RelationshipManager
)
from ..common_generators import SingleFileGenerator

@dataclass
class MakefileConfig:
    """Configuration for Makefile generation."""
    dest_dirs: Dict[str, str]
    makefile_vars: Dict[str, str]
    base_vars: Dict[str, str]
    vars_list: Dict[str, List[str]]

class MakefileGenerator(SingleFileGenerator):
    """Generates makefile with build dependencies."""

    def __init__(self, lang: str, config: MakefileConfig):
        """Initialize the generator.
        
        Args:
            lang: Language code
            config: Makefile configuration
        """
        super().__init__(lang)
        self.config = config
        self.relationship_manager = RelationshipManager()

    def get_template_data(self) -> Dict[str, Any]:
        """Generate makefile data with all dependencies."""
        build_depends = []
        vars_data = self.config.base_vars.copy()
        
        # Set source YAML files
        vars_data.update({
            'check_yaml': ' '.join(Check.list_all_src_paths()),
            'gl_yaml': ' '.join(Guideline.list_all_src_paths()),
            'faq_yaml': ' '.join(Faq.list_all_src_paths())
        })

        cat_deps, cat_targets = self._process_category_targets()
        check_deps, check_targets = self._process_checktool_targets()
        faq_deps, faq_article_targets, faq_tagpage_targets = self._process_faq_targets()
        info_deps, info_to_gl_targets, info_to_faq_targets = self._process_info_targets()

        # Process all build targets and their dependencies
        build_depends.extend(cat_deps)
        build_depends.extend(check_deps)
        build_depends.extend(faq_deps)
        build_depends.extend(info_deps)

        template_vars = {
            'guideline_category_target': ' '.join(cat_targets),
            'check_example_target': ' '.join(check_targets),
            'faq_article_target': ' '.join(faq_article_targets),
            'faq_tagpage_target': ' '.join(faq_tagpage_targets),
            'info_to_gl_target': ' '.join(info_to_gl_targets) ,
            'info_to_faq_target': ' '.join(info_to_faq_targets)
        }

        result = {**vars_data, **self.config.makefile_vars, **template_vars}
        result['depends'] = build_depends
        
        return result

    def _process_category_targets(self) -> tuple[List[Dict[str, str]], List[str]]:
        """Process category targets and their dependencies."""
        build_depends = []
        category_targets = []
        for cat in Category.list_all():
            filename = f'{cat.id}.rst'
            target = os.path.join(self.config.dest_dirs['guidelines'], filename)
            if target not in category_targets:
                category_targets.append(target)
                build_depends.append({
                    'target': target,
                    'depends': ' '.join(cat.get_dependency())
                })

        return build_depends, category_targets

    def _process_checktool_targets(self) -> tuple[List[Dict[str, str]], List[str]]:
        """Process check tool targets and their dependencies."""
        build_depends = []
        checktool_targets = []

        for tool in CheckTool.list_all():
            filename = f'examples-{tool.id}.rst'
            target = os.path.join(self.config.dest_dirs['checks'], filename)
            if target not in checktool_targets:
                checktool_targets.append(target)
                build_depends.append({
                    'target': target,
                    'depends': ' '.join(tool.get_dependency())
                })

        return build_depends, checktool_targets

    def _process_faq_targets(self) -> tuple[List[Dict[str, str]], List[str], List[str]]:
        """Process FAQ targets and their dependencies."""
        build_depends = []
        article_targets = []
        tagpage_targets = []

        # FAQ articles
        for faq in Faq.list_all():
            filename = f'{faq.id}.rst'
            target = os.path.join(self.config.dest_dirs['faq_articles'], filename)
            if target not in article_targets:
                article_targets.append(target)
                build_depends.append({
                    'target': target,
                    'depends': ' '.join(faq.get_dependency())
                })

        # FAQ tag pages
        for tag in FaqTag.list_all():
            if tag.article_count() == 0:
                continue
            filename = f'{tag.id}.rst'
            target = os.path.join(self.config.dest_dirs['faq_tags'], filename)
            if target not in tagpage_targets:
                dependency = []
                tagpage_targets.append(target)
                for faq in self.relationship_manager.get_tag_to_faqs(tag):
                    dependency.extend(faq.get_dependency())
                build_depends.append({
                    'target': target,
                    'depends': ' '.join(dependency)
                })
            
        return build_depends, article_targets, tagpage_targets

    def _process_info_targets(self) -> tuple[List[Dict[str, str]], List[str], List[str]]:
        """Process info reference targets and their dependencies."""
        build_depends = []
        info_to_gl_targets = []
        info_to_faq_targets = []

        # Info to guidelines
        for info in InfoRef.list_has_guidelines():
            if not info.internal:
                continue
            filename = f'{info.ref}.rst'
            target = os.path.join(self.config.dest_dirs['info2gl'], filename)
            if target not in info_to_gl_targets:
                info_to_gl_targets.append(target)
                build_depends.append({
                    'target': target,
                    'depends': ' '.join([
                        guideline.src_path 
                        for guideline in self.relationship_manager.get_info_to_guidelines(info)
                    ])
                })

        # Info to FAQs
        for info in InfoRef.list_has_faqs():
            if not info.internal:
                continue
            filename = f'{info.ref}.rst'
            target = os.path.join(self.config.dest_dirs['info2faq'], filename)
            if target not in info_to_faq_targets:
                info_to_faq_targets.append(target)
                build_depends.append({
                    'target': target,
                    'depends': ' '.join([
                        faq.src_path 
                        for faq in self.relationship_manager.get_info_to_faqs(info)
                    ])
                })

        return build_depends, info_to_gl_targets, info_to_faq_targets

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate makefile data."""
        required_fields = ['depends', 'gl_yaml', 'check_yaml', 'faq_yaml']
        if not all(field in data for field in required_fields):
            return False

        if not isinstance(data['depends'], list):
            return False

        for dep in data['depends']:
            if not isinstance(dep, dict) or 'target' not in dep or 'depends' not in dep:
                return False

        return True
