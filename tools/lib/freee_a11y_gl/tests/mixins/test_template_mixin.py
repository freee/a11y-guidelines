"""Tests for TemplateDataMixin."""
import pytest
from unittest.mock import Mock, MagicMock

from freee_a11y_gl.mixins.template_mixin import TemplateDataMixin
from freee_a11y_gl.models.base import BaseModel


class MockModel(BaseModel, TemplateDataMixin):
    """Mock model that combines BaseModel and TemplateDataMixin."""
    
    object_type = "test_model"
    _instances = {}
    
    def __init__(self, id_val: str, title: dict = None):
        super().__init__(id_val)
        self.title = title or {'ja': 'テストタイトル', 'en': 'Test Title'}


class TestTemplateDataMixin:
    """Test TemplateDataMixin functionality."""

    def test_get_base_template_data_with_title(self):
        """Test basic template data generation with title."""
        model = MockModel("test_001")
        data = model.get_base_template_data("ja")
        
        assert data['id'] == "test_001"
        assert data['title'] == 'テストタイトル'

    def test_get_base_template_data_english(self):
        """Test basic template data generation with English title."""
        model = MockModel("test_002")
        data = model.get_base_template_data("en")
        
        assert data['id'] == "test_002"
        assert data['title'] == 'Test Title'

    def test_get_base_template_data_without_title(self):
        """Test basic template data generation without title attribute."""
        model = MockModel("test_003", title=None)
        # Remove title attribute completely
        delattr(model, 'title')
        
        data = model.get_base_template_data("ja")
        assert data['id'] == "test_003"
        assert data.get('title', '') == ''

    def test_add_related_objects_with_data(self):
        """Test adding related objects when they exist."""
        model = MockModel("test_004")
        
        # Mock relationship manager and related objects
        mock_rel = Mock()
        mock_obj1 = Mock()
        mock_obj1.id = "related_001"
        mock_obj2 = Mock()
        mock_obj2.id = "related_002"
        mock_rel.get_sorted_related_objects.return_value = [mock_obj1, mock_obj2]
        
        # Mock the _get_relationship_manager method
        model._get_relationship_manager = Mock(return_value=mock_rel)
        
        data = {}
        model.add_related_objects(data, 'faq')
        
        assert 'faqs' in data
        assert data['faqs'] == ['related_001', 'related_002']
        mock_rel.get_sorted_related_objects.assert_called_once_with(model, 'faq')

    def test_add_related_objects_info_ref_special_handling(self):
        """Test special handling for info_ref objects."""
        model = MockModel("test_005")
        
        # Mock relationship manager and info_ref objects
        mock_rel = Mock()
        mock_info1 = Mock()
        mock_info1.refstring.return_value = "ref_001"
        mock_info2 = Mock()
        mock_info2.refstring.return_value = "ref_002"
        mock_rel.get_sorted_related_objects.return_value = [mock_info1, mock_info2]
        
        model._get_relationship_manager = Mock(return_value=mock_rel)
        
        data = {}
        model.add_related_objects(data, 'info_ref')
        
        assert 'info_refs' in data
        assert data['info_refs'] == ['ref_001', 'ref_002']

    def test_add_related_objects_empty_list(self):
        """Test adding related objects when none exist."""
        model = MockModel("test_006")
        
        # Mock relationship manager with empty result
        mock_rel = Mock()
        mock_rel.get_sorted_related_objects.return_value = []
        model._get_relationship_manager = Mock(return_value=mock_rel)
        
        data = {}
        model.add_related_objects(data, 'faq')
        
        # Should not add any key when no related objects exist
        assert 'faqs' not in data

    def test_add_link_data(self):
        """Test adding link data to template data."""
        model = MockModel("test_007")
        data = {}
        
        model.add_link_data(data, 'ja', 'https://example.com/', 
                           'path/{id}.html')
        
        assert 'text' in data
        assert 'url' in data
        assert data['text']['ja'] == 'テストタイトル'
        assert data['url']['ja'] == 'https://example.com/path/test_007.html'

    def test_add_link_data_existing_structure(self):
        """Test adding link data when text/url structure already exists."""
        model = MockModel("test_008")
        data = {
            'text': {'en': 'Existing'},
            'url': {'en': 'https://existing.com'}
        }
        
        model.add_link_data(data, 'ja', 'https://example.com/', 
                           'path/{id}.html')
        
        # Should preserve existing data and add new language
        assert data['text']['en'] == 'Existing'
        assert data['text']['ja'] == 'テストタイトル'
        assert data['url']['en'] == 'https://existing.com'
        assert data['url']['ja'] == 'https://example.com/path/test_008.html'

    def test_join_platform_items(self):
        """Test joining platform items with localized separator."""
        model = MockModel("test_009")
        
        # Test with actual data - should use the real join_items function
        result = model.join_platform_items(['web', 'mobile'], 'ja')
        
        # The actual result depends on Config.get_platform_name and 
        # Config.get_list_separator, which should return localized values
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_relationship_manager_caching(self):
        """Test relationship manager caching behavior."""
        model = MockModel("test_010")
        
        # First call should create and cache the relationship manager
        rel1 = model._get_relationship_manager()
        rel2 = model._get_relationship_manager()
        
        # Should return the same instance (cached)
        assert rel1 is rel2
        assert model._relationship_manager is rel1

    def test_get_relationship_manager_fallback(self):
        """Test fallback behavior when no cached relationship manager."""
        model = MockModel("test_011")
        
        # Ensure no cached relationship manager
        model._relationship_manager = None
        
        rel = model._get_relationship_manager()
        
        # Should create a new RelationshipManager instance
        assert rel is not None
        assert model._relationship_manager is rel


class TestTemplateDataMixinIntegration:
    """Integration tests for TemplateDataMixin with actual models."""

    def test_mixin_inheritance_check(self):
        """Verify that the mixin is properly inherited by test model."""
        model = MockModel("integration_001")
        
        # Check that all mixin methods are available
        assert hasattr(model, 'get_base_template_data')
        assert hasattr(model, 'add_related_objects')
        assert hasattr(model, 'add_link_data')
        assert hasattr(model, 'join_platform_items')
        assert hasattr(model, '_get_relationship_manager')

    def test_model_and_mixin_interaction(self):
        """Test interaction between BaseModel and TemplateDataMixin."""
        model = MockModel("integration_002")
        
        # Should have properties from both BaseModel and TemplateDataMixin
        assert model.id == "integration_002"
        assert model.object_type == "test_model"
        
        # Should be able to use mixin methods
        data = model.get_base_template_data("ja")
        assert data['id'] == "integration_002"
        assert 'title' in data