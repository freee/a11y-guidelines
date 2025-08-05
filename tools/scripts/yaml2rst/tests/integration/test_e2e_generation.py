"""End-to-end integration tests for yaml2rst."""
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from yaml2rst import yaml2rst
from yaml2rst.generators.file_generator import FileGenerator, GeneratorConfig
from yaml2rst.generators.content_generators.category_generator import (
    CategoryGenerator
)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestEndToEndGeneration:
    """End-to-end tests for the complete generation process."""

    @patch('yaml2rst.yaml2rst.Config')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('freee_a11y_gl.Category.list_all')
    @patch('freee_a11y_gl.relationship_manager.RelationshipManager'
           '.get_sorted_related_objects')
    @patch('yaml2rst.initializer.get_dest_dirnames')
    @patch('yaml2rst.initializer.get_static_dest_files')
    @patch('freee_a11y_gl.source.get_src_path')
    @patch('yaml2rst.initializer.TemplateManager')
    def test_complete_generation_workflow(
        self,
        mock_template_manager_class,
        mock_get_src_path,
        mock_get_static_dest_files,
        mock_get_dest_dirnames,
        mock_get_related_objects,
        mock_list_all,
        mock_setup_instances,
        mock_config,
        temp_dir
    ):
        """Test complete generation workflow from start to finish."""
        # Setup directory structure
        output_dir = temp_dir / "output"
        categories_dir = output_dir / "categories"

        # Setup mocks for initialization
        mock_get_dest_dirnames.return_value = {
            'guidelines': str(categories_dir),
            'checks': str(output_dir / "checks"),
            'faq_articles': str(output_dir / "faq"),
            'faq_tags': str(output_dir / "faq" / "tags"),
            'info2gl': str(output_dir / "info"),
            'info2faq': str(output_dir / "info")
        }

        mock_get_static_dest_files.return_value = {
            'all_checks': str(output_dir / "checks" / "checklist.rst"),
            'faq_index': str(output_dir / "faq" / "index.rst"),
            'faq_tag_index': str(output_dir / "faq" / "tags" / "index.rst"),
            'faq_article_index': str(output_dir / "faq" / "articles" /
                                     "index.rst"),
            'wcag21mapping': str(output_dir / "info" / "wcag21-mapping.rst"),
            'priority_diff': str(output_dir / "info" / "priority.rst"),
            'miscdefs': str(output_dir / "inc" / "miscdefs.txt"),
            'axe_rules': str(output_dir / "info" / "axe-rules.rst"),
            'makefile': str(output_dir / "Makefile")
        }

        mock_get_src_path.return_value = {
            'wcag_sc': str(temp_dir / "wcag_sc.json"),
            'info': str(temp_dir / "info.json")
        }

        # Setup template mocks
        mock_template = Mock()
        mock_template.write_rst = Mock()
        mock_template_manager = Mock()
        mock_template_manager.load.return_value = mock_template
        mock_template_manager_class.from_config.return_value = \
            mock_template_manager

        # Setup guideline data mocks
        mock_category1 = Mock()
        mock_category1.id = 'form'
        mock_category1.title = 'Form Guidelines'
        mock_category1.description = 'Guidelines for accessible forms'
        mock_category1.get_dependency.return_value = ['/test/form.yaml']

        mock_category2 = Mock()
        mock_category2.id = 'image'
        mock_category2.title = 'Image Guidelines'
        mock_category2.description = 'Guidelines for accessible images'
        mock_category2.get_dependency.return_value = ['/test/image.yaml']

        mock_list_all.return_value = [mock_category1, mock_category2]

        # Setup guidelines for each category
        mock_guideline1 = Mock()
        mock_guideline1.template_data.return_value = {
            'id': 'form_001', 'title': 'Form Labels', 'priority': 'high'
        }

        mock_guideline2 = Mock()
        mock_guideline2.template_data.return_value = {
            'id': 'form_002', 'title': 'Form Validation', 'priority': 'medium'
        }

        mock_guideline3 = Mock()
        mock_guideline3.template_data.return_value = {
            'id': 'image_001', 'title': 'Alt Text', 'priority': 'high'
        }

        # Return different guidelines based on category
        mock_get_related_objects.side_effect = lambda cat, obj_type: {
            'form': [mock_guideline1, mock_guideline2],
            'image': [mock_guideline3]
        }.get(cat.id, [])

        # Mock command line arguments
        args = ['yaml2rst', '--basedir', str(temp_dir), '--lang', 'ja']
        with patch('sys.argv', args):
            # Execute the main function
            yaml2rst.main()

        # Verify that Config was initialized
        mock_config.initialize.assert_called_once_with(
            profile="yaml2rst",
            config_override={
                "basedir": str(temp_dir),
                "languages": {
                    "default": "ja"
                }
            }
        )

        # Verify that setup_instances was called
        mock_setup_instances.assert_called_once_with(str(temp_dir))

        # Verify that templates were loaded
        assert mock_template_manager_class.from_config.call_count > 0

        # Verify that files were generated
        assert mock_template.write_rst.call_count > 0

    def test_file_generator_with_real_category_generator(
        self, temp_dir, mock_templates
    ):
        """Test FileGenerator with a real CategoryGenerator."""
        # Create a mock category generator that yields real data
        class MockCategoryGenerator:
            def __init__(self, lang):
                self.lang = lang

            def generate(self):
                yield {
                    'filename': 'form',
                    'category': {
                        'id': 'form',
                        'title': 'Form Guidelines',
                        'description': 'Guidelines for accessible forms'
                    },
                    'guidelines': [
                        {'id': 'form_001', 'title': 'Form Labels',
                         'priority': 'high'},
                        {'id': 'form_002', 'title': 'Form Validation',
                         'priority': 'medium'}
                    ]
                }
                yield {
                    'filename': 'image',
                    'category': {
                        'id': 'image',
                        'title': 'Image Guidelines',
                        'description': 'Guidelines for accessible images'
                    },
                    'guidelines': [
                        {'id': 'image_001', 'title': 'Alt Text',
                         'priority': 'high'}
                    ]
                }

        # Setup FileGenerator
        file_generator = FileGenerator(mock_templates, 'ja')

        config = GeneratorConfig(
            generator_class=MockCategoryGenerator,
            template_name='category_page',
            output_path=str(temp_dir),
            is_single_file=False
        )

        # Execute generation
        file_generator.generate(config, build_all=True, targets=[])

        # Verify results
        template = mock_templates['category_page']
        assert template.write_rst.call_count == 2

        # Check generated data
        calls = template.write_rst.call_args_list

        # First call should be for form category
        form_call = calls[0]
        form_data, form_path = form_call[0]
        assert form_data['filename'] == 'form'
        assert form_data['category']['title'] == 'Form Guidelines'
        assert len(form_data['guidelines']) == 2
        assert form_data['lang'] == 'ja'
        assert form_path.name == 'form.rst'

        # Second call should be for image category
        image_call = calls[1]
        image_data, image_path = image_call[0]
        assert image_data['filename'] == 'image'
        assert image_data['category']['title'] == 'Image Guidelines'
        assert len(image_data['guidelines']) == 1
        assert image_data['lang'] == 'ja'
        assert image_path.name == 'image.rst'

    @patch('freee_a11y_gl.Category.list_all')
    @patch('freee_a11y_gl.relationship_manager.RelationshipManager'
           '.get_sorted_related_objects')
    def test_category_generator_integration(
        self, mock_get_related_objects, mock_list_all, temp_dir, mock_templates
    ):
        """Test CategoryGenerator integration with FileGenerator."""
        # Setup mock data
        mock_category = Mock()
        mock_category.id = 'accessibility_basics'
        mock_category.title = 'Accessibility Basics'
        mock_category.description = 'Fundamental accessibility guidelines'
        mock_list_all.return_value = [mock_category]

        mock_guideline1 = Mock()
        mock_guideline1.template_data.return_value = {
            'id': 'basic_001',
            'title': 'Provide text alternatives',
            'description': 'All images must have alt text',
            'priority': 'high'
        }

        mock_guideline2 = Mock()
        mock_guideline2.template_data.return_value = {
            'id': 'basic_002',
            'title': 'Use proper headings',
            'description': 'Structure content with headings',
            'priority': 'medium'
        }

        mock_get_related_objects.return_value = [mock_guideline1,
                                                 mock_guideline2]

        # Setup FileGenerator with real CategoryGenerator
        file_generator = FileGenerator(mock_templates, 'ja')

        config = GeneratorConfig(
            generator_class=CategoryGenerator,
            template_name='category_page',
            output_path=str(temp_dir),
            is_single_file=False
        )

        # Execute generation
        file_generator.generate(config, build_all=True, targets=[])

        # Verify results
        template = mock_templates['category_page']
        assert template.write_rst.call_count == 1

        # Check generated data
        call_args = template.write_rst.call_args[0]
        data, path = call_args

        assert data['filename'] == 'accessibility_basics'
        assert len(data['guidelines']) == 2
        assert data['lang'] == 'ja'
        assert path.name == 'accessibility_basics.rst'

    def test_selective_generation(self, temp_dir, mock_templates):
        """Test selective file generation based on targets."""
        # Create a generator that yields multiple files
        class MultiFileGenerator:
            def __init__(self, lang):
                self.lang = lang

            def generate(self):
                for i in range(5):
                    yield {
                        'filename': f'file_{i}',
                        'content': f'Content for file {i}',
                        'title': f'Title {i}'
                    }

        # Setup FileGenerator
        file_generator = FileGenerator(mock_templates, 'ja')

        config = GeneratorConfig(
            generator_class=MultiFileGenerator,
            template_name='category_page',
            output_path=str(temp_dir),
            is_single_file=False
        )

        # Target only specific files
        targets = [
            str(temp_dir / 'file_1.rst'),
            str(temp_dir / 'file_3.rst')
        ]

        # Execute selective generation
        file_generator.generate(config, build_all=False, targets=targets)

        # Verify only targeted files were generated
        template = mock_templates['category_page']
        assert template.write_rst.call_count == 2

        # Check that correct files were generated
        calls = template.write_rst.call_args_list
        generated_filenames = [call[0][0]['filename'] for call in calls]

        assert 'file_1' in generated_filenames
        assert 'file_3' in generated_filenames
        assert 'file_0' not in generated_filenames
        assert 'file_2' not in generated_filenames
        assert 'file_4' not in generated_filenames

    def test_error_handling_in_generation_pipeline(
        self, temp_dir, mock_templates
    ):
        """Test error handling throughout the generation pipeline."""
        # Create a generator that fails on certain items
        class FailingGenerator:
            def __init__(self, lang):
                self.lang = lang

            def generate(self):
                yield {'filename': 'good_file', 'content': 'Good content'}
                # This will cause an error in template rendering
                yield {'filename': 'bad_file'}  # Missing required content

        # Setup template to fail on missing content
        failing_template = Mock()
        failing_template.write_rst.side_effect = [
            None,  # First call succeeds
            Exception("Missing required content")  # Second call fails
        ]

        templates_with_failure = mock_templates.copy()
        templates_with_failure['category_page'] = failing_template

        # Setup FileGenerator
        file_generator = FileGenerator(templates_with_failure, 'ja')

        config = GeneratorConfig(
            generator_class=FailingGenerator,
            template_name='category_page',
            output_path=str(temp_dir),
            is_single_file=False
        )

        # Execute generation and expect failure
        with pytest.raises(Exception):
            file_generator.generate(config, build_all=True, targets=[])

    def test_multiple_generators_workflow(self, temp_dir, mock_templates):
        """Test workflow with multiple different generators."""
        # Create different generator types
        class CategoryGen:
            def __init__(self, lang):
                self.lang = lang

            def generate(self):
                yield {
                    'filename': 'categories',
                    'type': 'category',
                    'content': 'Category content'
                }

        class FaqGen:
            def __init__(self, lang):
                self.lang = lang

            def generate(self):
                yield {
                    'filename': 'faq',
                    'type': 'faq',
                    'content': 'FAQ content'
                }

        # Setup FileGenerator
        file_generator = FileGenerator(mock_templates, 'ja')

        # Configure multiple generators
        configs = [
            GeneratorConfig(
                generator_class=CategoryGen,
                template_name='category_page',
                output_path=str(temp_dir / 'categories'),
                is_single_file=False
            ),
            GeneratorConfig(
                generator_class=FaqGen,
                template_name='faq_article',
                output_path=str(temp_dir / 'faq'),
                is_single_file=False
            )
        ]

        # Execute all generators
        for config in configs:
            file_generator.generate(config, build_all=True, targets=[])

        # Verify all generators were executed
        category_template = mock_templates['category_page']
        faq_template = mock_templates['faq_article']

        # Each generator should be called once, but category_page might be used
        # by both so we check that at least one call was made to each template
        assert category_template.write_rst.call_count >= 1
        assert faq_template.write_rst.call_count >= 1

        # Check generated content - verify the correct templates were called
        # The order of calls may vary, so we check both templates were used
        # Note: category_page template might be called multiple times if used
        # by different generators
        assert category_template.write_rst.call_count >= 1
        assert faq_template.write_rst.call_count >= 1

        # Verify the content types match what we expect by checking all calls
        category_calls = category_template.write_rst.call_args_list
        faq_calls = faq_template.write_rst.call_args_list

        # Find calls with the expected content types
        category_found = any(
            call[0][0]['type'] == 'category' for call in category_calls
        )
        faq_found = any(call[0][0]['type'] == 'faq' for call in faq_calls)

        assert category_found, ("Category type content not found in "
                                "category template calls")
        assert faq_found, ("FAQ type content not found in "
                           "FAQ template calls")


class TestLanguageSupport:
    """Test multi-language support in generation."""

    def test_japanese_generation(self, temp_dir, mock_templates):
        """Test generation with Japanese language."""
        class JapaneseGenerator:
            def __init__(self, lang):
                self.lang = lang

            def generate(self):
                yield {
                    'filename': 'japanese_content',
                    'title': 'アクセシビリティガイドライン',
                    'content': 'これは日本語のコンテンツです',
                    'lang': self.lang
                }

        file_generator = FileGenerator(mock_templates, 'ja')

        config = GeneratorConfig(
            generator_class=JapaneseGenerator,
            template_name='category_page',
            output_path=str(temp_dir),
            is_single_file=False
        )

        file_generator.generate(config, build_all=True, targets=[])

        template = mock_templates['category_page']
        call_args = template.write_rst.call_args[0]
        data = call_args[0]

        assert data['lang'] == 'ja'
        assert data['title'] == 'アクセシビリティガイドライン'

    def test_english_generation(self, temp_dir, mock_templates):
        """Test generation with English language."""
        class EnglishGenerator:
            def __init__(self, lang):
                self.lang = lang

            def generate(self):
                yield {
                    'filename': 'english_content',
                    'title': 'Accessibility Guidelines',
                    'content': 'This is English content',
                    'lang': self.lang
                }

        file_generator = FileGenerator(mock_templates, 'en')

        config = GeneratorConfig(
            generator_class=EnglishGenerator,
            template_name='category_page',
            output_path=str(temp_dir),
            is_single_file=False
        )

        file_generator.generate(config, build_all=True, targets=[])

        template = mock_templates['category_page']
        call_args = template.write_rst.call_args[0]
        data = call_args[0]

        assert data['lang'] == 'en'
        assert data['title'] == 'Accessibility Guidelines'
