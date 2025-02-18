"""Makefile generator for managing build dependencies."""
import os
from typing import Dict, List, Any
from a11y_guidelines import Category, Guideline, Check, CheckTool, Faq, FaqTag, InfoRef, RelationshipManager

class MakefileGenerator:
    """Generates makefile with build dependencies."""

    def __init__(
        self,
        dest_dirs: Dict[str, str],
        makefile_vars: Dict[str, str],
        vars: Dict[str, str],
        vars_list: Dict[str, List[str]]
    ):
        self.dest_dirs = dest_dirs
        self.makefile_vars = makefile_vars
        self.vars = vars
        self.vars_list = vars_list
        self.rel = RelationshipManager()

    def generate_data(self) -> Dict[str, Any]:
        """Generate makefile data with all dependencies."""
        build_depends = []
        
        # Set source YAML files
        self.vars['check_yaml'] = ' '.join(Check.list_all_src_paths())
        self.vars['gl_yaml'] = ' '.join(Guideline.list_all_src_paths())
        self.vars['faq_yaml'] = ' '.join(Faq.list_all_src_paths())

        # Generate category targets
        for cat in Category.list_all():
            filename = f'{cat.id}.rst'
            target = os.path.join(self.dest_dirs['guidelines'], filename)
            self.vars_list['guideline_category_target'].append(target)
            build_depends.append({
                'target': target,
                'depends': ' '.join(cat.get_dependency())
            })

        # Generate check example targets
        for tool in CheckTool.list_all():
            filename = f'examples-{tool.id}.rst'
            target = os.path.join(self.dest_dirs['checks'], filename)
            self.vars_list['check_example_target'].append(target)
            build_depends.append({
                'target': target,
                'depends': ' '.join(tool.get_dependency())
            })

        # Generate FAQ article targets
        for faq in Faq.list_all():
            filename = f'{faq.id}.rst'
            target = os.path.join(self.dest_dirs['faq_articles'], filename)
            self.vars_list['faq_article_target'].append(target)
            build_depends.append({
                'target': target,
                'depends': ' '.join(faq.get_dependency())
            })

        # Generate FAQ tag page targets
        for tag in FaqTag.list_all():
            if tag.article_count() == 0:
                continue
            filename = f'{tag.id}.rst'
            target = os.path.join(self.dest_dirs['faq_tags'], filename)
            self.vars_list['faq_tagpage_target'].append(target)
            dependency = []
            for faq in self.rel.get_tag_to_faqs(tag):
                dependency.extend(faq.get_dependency())
            build_depends.append({
                'target': target,
                'depends': ' '.join(dependency)
            })

        # Generate info to guidelines targets
        for info in InfoRef.list_has_guidelines():
            if not info.internal:
                continue
            filename = f'{info.ref}.rst'
            target = os.path.join(self.dest_dirs['info2gl'], filename)
            self.vars_list['info_to_gl_target'].append(target)
            build_depends.append({
                'target': target,
                'depends': ' '.join([guideline.src_path for guideline in self.rel.get_info_to_guidelines(info)])
            })

        # Generate info to FAQs targets
        for info in InfoRef.list_has_faqs():
            if not info.internal:
                continue
            filename = f'{info.ref}.rst'
            target = os.path.join(self.dest_dirs['info2faq'], filename)
            self.vars_list['info_to_faq_target'].append(target)
            build_depends.append({
                'target': target,
                'depends': ' '.join([faq.src_path for faq in self.rel.get_info_to_faqs(info)])
            })

        # Join all list variables
        for key, value in self.vars_list.items():
            self.vars[key] = ' '.join(value)

        # Combine all variables
        result = {**self.vars, **self.makefile_vars}
        result['depends'] = build_depends
        
        return result
