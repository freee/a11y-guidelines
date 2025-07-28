"""Unit tests for the category generator module."""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from yaml2rst.generators.content_generators.category_generator import CategoryGenerator
from yaml2rst.generators.base_generator import GeneratorError


class TestCategoryGenerator:
    """Test cases for CategoryGenerator class."""

    @patch('yaml2rst.generators.content_generators.category_generator.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_category_generator_initialization(self, mock_list_all, mock_relationship_manager):
        """Test CategoryGenerator initialization."""
        # Setup mock categories
        mock_category = Mock()
        mock_category.id = 'form'
        mock_list_all.return_value = [mock_category]
        
        # Setup mock relationship manager
        mock_rm_instance = Mock()
        mock_relationship_manager.return_value = mock_rm_instance
        
        generator = CategoryGenerator('ja')
        
        assert generator.lang == 'ja'
        assert hasattr(generator, 'relationship_manager')
        assert hasattr(generator, 'categories_by_id')

    @patch('yaml2rst.generators.content_generators.category_generator.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_generate_success(self, mock_list_all, mock_relationship_manager):
        """Test successful generation of category pages."""
        # Setup mock categories
        mock_category1 = Mock()
        mock_category1.id = 'form'
        mock_category2 = Mock()
        mock_category2.id = 'image'
        mock_list_all.return_value = [mock_category1, mock_category2]
        
        # Setup mock guidelines
        mock_guideline1 = Mock()
        mock_guideline1.template_data.return_value = {'id': 'form_001', 'title': 'Form Label'}
        mock_guideline2 = Mock()
        mock_guideline2.template_data.return_value = {'id': 'image_001', 'title': 'Alt Text'}
        
        # Setup relationship manager
        mock_rm_instance = Mock()
        mock_rm_instance.get_sorted_related_objects.side_effect = lambda cat, rel_type: (
            [mock_guideline1] if cat.id == 'form' else [mock_guideline2]
        )
        mock_relationship_manager.return_value = mock_rm_instance
        
        # Execute
        generator = CategoryGenerator('ja')
        results = list(generator.generate())
        
        # Verify
        assert len(results) == 2
        
        # Check results contain expected data
        filenames = [r['filename'] for r in results]
        assert 'form' in filenames
        assert 'image' in filenames

    @patch('yaml2rst.generators.content_generators.category_generator.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_generate_empty_categories(self, mock_list_all, mock_relationship_manager):
        """Test generation with empty categories."""
        mock_list_all.return_value = []
        
        generator = CategoryGenerator('ja')
        results = list(generator.generate())
        
        assert len(results) == 0

    @patch('yaml2rst.generators.content_generators.category_generator.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_generate_category_with_no_guidelines(self, mock_list_all, mock_relationship_manager):
        """Test generation for category with no guidelines."""
        # Setup mock category
        mock_category = Mock()
        mock_category.id = 'empty_category'
        mock_list_all.return_value = [mock_category]
        
        # Setup relationship manager to return no guidelines
        mock_rm_instance = Mock()
        mock_rm_instance.get_sorted_related_objects.return_value = []
        mock_relationship_manager.return_value = mock_rm_instance
        
        generator = CategoryGenerator('ja')
        results = list(generator.generate())
        
        assert len(results) == 1
        result = results[0]
        assert result['filename'] == 'empty_category'
        assert len(result['guidelines']) == 0

    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_generate_exception_handling(self, mock_list_all):
        """Test exception handling during generation."""
        mock_list_all.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            CategoryGenerator('ja')

    @patch('freee_a11y_gl.relationship_manager.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_generate_with_priority_sorting(self, mock_list_all, mock_relationship_manager):
        """Test that guidelines are sorted by priority."""
        # Setup mock category
        mock_category = Mock()
        mock_category.id = 'test_category'
        mock_list_all.return_value = [mock_category]
        
        # Setup mock guidelines with different priorities
        mock_guidelines = []
        for i, priority in enumerate(['low', 'high', 'medium']):
            mock_gl = Mock()
            mock_gl.template_data.return_value = {
                'id': f'{priority}_priority',
                'title': f'{priority.title()} Priority',
                'priority': priority
            }
            mock_guidelines.append(mock_gl)
        
        # Setup relationship manager singleton
        mock_rm_instance = Mock()
        mock_rm_instance.get_sorted_related_objects.return_value = mock_guidelines
        mock_relationship_manager.return_value = mock_rm_instance
        
        generator = CategoryGenerator('ja')
        results = list(generator.generate())
        
        assert len(results) == 1
        guidelines = results[0]['guidelines']
        assert len(guidelines) == 3

    @patch('freee_a11y_gl.relationship_manager.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_generate_data_structure(self, mock_list_all, mock_relationship_manager):
        """Test the structure of generated data."""
        # Setup mock category
        mock_category = Mock()
        mock_category.id = 'test_cat'
        mock_list_all.return_value = [mock_category]
        
        # Setup mock guideline
        mock_guideline = Mock()
        mock_guideline.template_data.return_value = {
            'id': 'test_gl',
            'title': 'Test Guideline',
            'description': 'Test guideline description',
            'priority': 'high'
        }
        
        # Setup relationship manager singleton
        mock_rm_instance = Mock()
        mock_rm_instance.get_sorted_related_objects.return_value = [mock_guideline]
        mock_relationship_manager.return_value = mock_rm_instance
        
        generator = CategoryGenerator('ja')
        results = list(generator.generate())
        
        assert len(results) == 1
        result = results[0]
        
        # Check required fields
        assert 'filename' in result
        assert 'guidelines' in result
        
        # Check guidelines structure
        guidelines = result['guidelines']
        assert isinstance(guidelines, list)
        assert len(guidelines) == 1
        guideline = guidelines[0]
        assert 'id' in guideline
        assert 'title' in guideline

    @patch('yaml2rst.generators.content_generators.category_generator.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_generate_filename_generation(self, mock_list_all, mock_relationship_manager):
        """Test filename generation from category ID."""
        # Setup mock categories
        mock_category1 = Mock()
        mock_category1.id = 'form_validation'
        mock_category2 = Mock()
        mock_category2.id = 'image_alt_text'
        mock_list_all.return_value = [mock_category1, mock_category2]
        
        # Setup relationship manager
        mock_rm_instance = Mock()
        mock_rm_instance.get_sorted_related_objects.return_value = []
        mock_relationship_manager.return_value = mock_rm_instance
        
        generator = CategoryGenerator('ja')
        results = list(generator.generate())
        
        assert len(results) == 2
        filenames = [r['filename'] for r in results]
        
        assert 'form_validation' in filenames
        assert 'image_alt_text' in filenames

    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_get_dependencies(self, mock_list_all):
        """Test get_dependencies method."""
        # Setup mock categories
        mock_category = Mock()
        mock_category.get_dependency.return_value = 'category_dependency'
        mock_list_all.return_value = [mock_category]
        
        generator = CategoryGenerator('ja')
        dependencies = generator.get_dependencies()
        
        assert isinstance(dependencies, list)
        assert 'category_dependency' in dependencies

    def test_validate_data_success(self):
        """Test data validation with valid data."""
        generator = CategoryGenerator('ja')
        
        valid_data = {
            'filename': 'test_category',
            'guidelines': [
                {
                    'id': 'test_gl',
                    'title': 'Test Guideline',
                    'priority': 'high'
                }
            ]
        }
        
        result = generator.validate_data(valid_data)
        assert result is True

    def test_validate_data_missing_required_fields(self):
        """Test data validation with missing required fields."""
        generator = CategoryGenerator('ja')
        
        invalid_data = {
            'filename': 'test_category'
            # Missing 'guidelines'
        }
        
        result = generator.validate_data(invalid_data)
        assert result is False

    @patch('yaml2rst.generators.content_generators.category_generator.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_preprocess_data(self, mock_list_all, mock_relationship_manager):
        """Test data preprocessing."""
        # Setup mocks
        mock_list_all.return_value = []
        
        generator = CategoryGenerator('ja')
        
        original_data = {
            'filename': 'test_category',
            'guidelines': []
        }
        
        processed_data = generator.preprocess_data(original_data)
        
        # Check that preprocessing maintains data integrity
        assert 'filename' in processed_data
        assert 'guidelines' in processed_data

    @patch('yaml2rst.generators.content_generators.category_generator.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_postprocess_data(self, mock_list_all, mock_relationship_manager):
        """Test data postprocessing."""
        # Setup mocks
        mock_list_all.return_value = []
        
        generator = CategoryGenerator('ja')
        
        original_data = {
            'filename': 'test_category',
            'guidelines': []
        }
        
        processed_data = generator.postprocess_data(original_data)
        
        # Check that postprocessing maintains data integrity
        assert processed_data['filename'] == 'test_category'
        assert 'guidelines' in processed_data


class TestCategoryGeneratorIntegration:
    """Integration tests for CategoryGenerator."""

    @patch('freee_a11y_gl.relationship_manager.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_full_generation_workflow(self, mock_list_all, mock_relationship_manager):
        """Test complete generation workflow."""
        # Setup mock category
        mock_category = Mock()
        mock_category.id = 'accessibility_basics'
        mock_list_all.return_value = [mock_category]
        
        # Setup mock guidelines
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
        
        # Setup relationship manager singleton
        mock_rm_instance = Mock()
        mock_rm_instance.get_sorted_related_objects.return_value = [mock_guideline1, mock_guideline2]
        mock_relationship_manager.return_value = mock_rm_instance
        
        # Execute full workflow
        generator = CategoryGenerator('ja')
        
        with generator:
            results = list(generator.generate())
            
            # Validate results
            assert len(results) == 1
            result = results[0]
            
            # Validate data structure
            assert generator.validate_data(result) is True
            
            # Process data through full pipeline
            processed = generator.preprocess_data(result)
            final = generator.postprocess_data(processed)
            
            assert final['filename'] == 'accessibility_basics'
            assert len(final['guidelines']) == 2

    @patch('freee_a11y_gl.relationship_manager.RelationshipManager')
    @patch('yaml2rst.generators.content_generators.category_generator.Category.list_all')
    def test_error_recovery(self, mock_list_all, mock_relationship_manager):
        """Test error recovery during generation."""
        # Setup categories
        mock_category1 = Mock()
        mock_category1.id = 'good_category'
        mock_category2 = Mock()
        mock_category2.id = 'bad_category'
        mock_list_all.return_value = [mock_category1, mock_category2]
        
        # Setup relationship manager to fail for bad_category
        mock_rm_instance = Mock()
        def mock_get_related(category, rel_type):
            if category.id == 'bad_category':
                raise Exception("Failed to load guidelines")
            return [Mock()]
        
        mock_rm_instance.get_sorted_related_objects.side_effect = mock_get_related
        mock_relationship_manager.return_value = mock_rm_instance
        
        generator = CategoryGenerator('ja')
        
        # Should handle partial failures gracefully
        with pytest.raises(Exception):
            list(generator.generate())
