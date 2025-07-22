import pytest
from unittest.mock import patch, MagicMock
from freee_a11y_gl.models.content import Category, GuidelineData
from freee_a11y_gl.relationship_manager import RelationshipManager


class TestGuidelineData:
    """Test cases for GuidelineData dataclass."""

    def test_guideline_data_creation(self):
        """Test GuidelineData creation with all fields."""
        data = GuidelineData(
            title={'ja': 'タイトル', 'en': 'Title'},
            platform=['web', 'mobile'],
            guideline={'ja': 'ガイドライン', 'en': 'Guideline'},
            intent={'ja': '意図', 'en': 'Intent'}
        )
        
        assert data.title == {'ja': 'タイトル', 'en': 'Title'}
        assert data.platform == ['web', 'mobile']
        assert data.guideline == {'ja': 'ガイドライン', 'en': 'Guideline'}
        assert data.intent == {'ja': '意図', 'en': 'Intent'}

    def test_guideline_data_empty_fields(self):
        """Test GuidelineData with empty fields."""
        data = GuidelineData(
            title={},
            platform=[],
            guideline={},
            intent={}
        )
        
        assert data.title == {}
        assert data.platform == []
        assert data.guideline == {}
        assert data.intent == {}


class TestCategory:
    """Test cases for Category class."""

    def setup_method(self):
        """Clear instances before each test."""
        Category._instances.clear()

    def test_init_basic(self):
        """Test basic Category initialization."""
        names = {'ja': 'テストカテゴリ', 'en': 'Test Category'}
        category = Category('test-category', names)
        
        assert category.id == 'test-category'
        assert category.names == names
        assert category.object_type == 'category'
        assert Category._instances['test-category'] == category

    def test_init_multiple_categories(self):
        """Test creating multiple categories."""
        category1 = Category('cat1', {'ja': 'カテゴリ1', 'en': 'Category 1'})
        category2 = Category('cat2', {'ja': 'カテゴリ2', 'en': 'Category 2'})
        
        assert len(Category._instances) == 2
        assert Category._instances['cat1'] == category1
        assert Category._instances['cat2'] == category2

    def test_get_name_japanese(self):
        """Test getting Japanese name."""
        names = {'ja': 'テストカテゴリ', 'en': 'Test Category'}
        category = Category('test', names)
        
        assert category.get_name('ja') == 'テストカテゴリ'

    def test_get_name_english(self):
        """Test getting English name."""
        names = {'ja': 'テストカテゴリ', 'en': 'Test Category'}
        category = Category('test', names)
        
        assert category.get_name('en') == 'Test Category'

    def test_get_name_fallback_to_japanese(self):
        """Test fallback to Japanese when language not found."""
        names = {'ja': 'テストカテゴリ', 'en': 'Test Category'}
        category = Category('test', names)
        
        assert category.get_name('fr') == 'テストカテゴリ'

    def test_get_name_missing_japanese_fallback(self):
        """Test behavior when Japanese is also missing."""
        names = {'en': 'Test Category'}
        category = Category('test', names)
        
        # Should raise KeyError when 'ja' key doesn't exist (current behavior)
        with pytest.raises(KeyError):
            category.get_name('fr')

    def test_get_name_empty_names(self):
        """Test behavior with empty names dictionary."""
        category = Category('test', {})
        
        # Should raise KeyError when 'ja' key doesn't exist (current behavior)
        with pytest.raises(KeyError):
            category.get_name('ja')

    @patch('freee_a11y_gl.models.content.RelationshipManager')
    @patch('freee_a11y_gl.models.content.uniq')
    def test_get_dependency_basic(self, mock_uniq, mock_rel_manager):
        """Test getting dependencies with basic setup."""
        # Setup mocks
        mock_rel = MagicMock()
        mock_rel_manager.return_value = mock_rel
        
        # Mock guideline with src_path
        mock_guideline = MagicMock()
        mock_guideline.src_path = 'guideline1.yaml'
        
        # Mock check with src_path
        mock_check = MagicMock()
        mock_check.src_path = 'check1.yaml'
        
        # Mock FAQ with src_path
        mock_faq = MagicMock()
        mock_faq.src_path = 'faq1.yaml'
        
        # Setup relationship manager behavior
        def mock_get_sorted_related_objects(obj, obj_type):
            if obj_type == 'guideline':
                return [mock_guideline]
            return []
        
        def mock_get_related_objects(obj, obj_type):
            if obj_type == 'check':
                return [mock_check]
            elif obj_type == 'faq':
                return [mock_faq]
            return []
        
        mock_rel.get_sorted_related_objects.side_effect = mock_get_sorted_related_objects
        mock_rel.get_related_objects.side_effect = mock_get_related_objects
        
        # Mock uniq to return the input list
        mock_uniq.side_effect = lambda x: x
        
        category = Category('test', {'ja': 'テスト', 'en': 'Test'})
        dependencies = category.get_dependency()
        
        # Verify RelationshipManager was called
        mock_rel_manager.assert_called_once()
        mock_rel.get_sorted_related_objects.assert_called_once_with(category, 'guideline')
        
        # Verify uniq was called to remove duplicates
        mock_uniq.assert_called_once()
        
        # Check that dependencies include expected paths
        expected_deps = ['guideline1.yaml', 'check1.yaml', 'faq1.yaml']
        assert dependencies == expected_deps

    @patch('freee_a11y_gl.models.content.RelationshipManager')
    @patch('freee_a11y_gl.models.content.uniq')
    def test_get_dependency_multiple_guidelines(self, mock_uniq, mock_rel_manager):
        """Test getting dependencies with multiple guidelines."""
        mock_rel = MagicMock()
        mock_rel_manager.return_value = mock_rel
        
        # Mock multiple guidelines
        mock_guideline1 = MagicMock()
        mock_guideline1.src_path = 'guideline1.yaml'
        mock_guideline2 = MagicMock()
        mock_guideline2.src_path = 'guideline2.yaml'
        
        # Mock checks for each guideline
        mock_check1 = MagicMock()
        mock_check1.src_path = 'check1.yaml'
        mock_check2 = MagicMock()
        mock_check2.src_path = 'check2.yaml'
        
        # Mock FAQs for each guideline
        mock_faq1 = MagicMock()
        mock_faq1.src_path = 'faq1.yaml'
        mock_faq2 = MagicMock()
        mock_faq2.src_path = 'faq2.yaml'
        
        def mock_get_sorted_related_objects(obj, obj_type):
            if obj_type == 'guideline':
                return [mock_guideline1, mock_guideline2]
            return []
        
        def mock_get_related_objects(obj, obj_type):
            if obj_type == 'check':
                if obj == mock_guideline1:
                    return [mock_check1]
                elif obj == mock_guideline2:
                    return [mock_check2]
            elif obj_type == 'faq':
                if obj == mock_guideline1:
                    return [mock_faq1]
                elif obj == mock_guideline2:
                    return [mock_faq2]
            return []
        
        mock_rel.get_sorted_related_objects.side_effect = mock_get_sorted_related_objects
        mock_rel.get_related_objects.side_effect = mock_get_related_objects
        mock_uniq.side_effect = lambda x: x
        
        category = Category('test', {'ja': 'テスト', 'en': 'Test'})
        dependencies = category.get_dependency()
        
        expected_deps = [
            'guideline1.yaml', 'check1.yaml', 'faq1.yaml',
            'guideline2.yaml', 'check2.yaml', 'faq2.yaml'
        ]
        assert dependencies == expected_deps

    @patch('freee_a11y_gl.models.content.RelationshipManager')
    @patch('freee_a11y_gl.models.content.uniq')
    def test_get_dependency_no_guidelines(self, mock_uniq, mock_rel_manager):
        """Test getting dependencies when no guidelines exist."""
        mock_rel = MagicMock()
        mock_rel_manager.return_value = mock_rel
        mock_rel.get_sorted_related_objects.return_value = []
        mock_uniq.side_effect = lambda x: x
        
        category = Category('test', {'ja': 'テスト', 'en': 'Test'})
        dependencies = category.get_dependency()
        
        assert dependencies == []
        mock_uniq.assert_called_once_with([])

    @patch('freee_a11y_gl.models.content.RelationshipManager')
    @patch('freee_a11y_gl.models.content.uniq')
    def test_get_dependency_no_checks_or_faqs(self, mock_uniq, mock_rel_manager):
        """Test getting dependencies when guidelines have no checks or FAQs."""
        mock_rel = MagicMock()
        mock_rel_manager.return_value = mock_rel
        
        mock_guideline = MagicMock()
        mock_guideline.src_path = 'guideline1.yaml'
        
        def mock_get_sorted_related_objects(obj, obj_type):
            if obj_type == 'guideline':
                return [mock_guideline]
            return []
        
        def mock_get_related_objects(obj, obj_type):
            return []  # No checks or FAQs
        
        mock_rel.get_sorted_related_objects.side_effect = mock_get_sorted_related_objects
        mock_rel.get_related_objects.side_effect = mock_get_related_objects
        mock_uniq.side_effect = lambda x: x
        
        category = Category('test', {'ja': 'テスト', 'en': 'Test'})
        dependencies = category.get_dependency()
        
        assert dependencies == ['guideline1.yaml']

    @patch('freee_a11y_gl.models.content.RelationshipManager')
    @patch('freee_a11y_gl.models.content.uniq')
    def test_get_dependency_with_duplicates(self, mock_uniq, mock_rel_manager):
        """Test that uniq is called to remove duplicates."""
        mock_rel = MagicMock()
        mock_rel_manager.return_value = mock_rel
        
        mock_guideline = MagicMock()
        mock_guideline.src_path = 'guideline1.yaml'
        
        mock_check = MagicMock()
        mock_check.src_path = 'check1.yaml'
        
        def mock_get_sorted_related_objects(obj, obj_type):
            if obj_type == 'guideline':
                return [mock_guideline]
            return []
        
        def mock_get_related_objects(obj, obj_type):
            if obj_type == 'check':
                return [mock_check]
            elif obj_type == 'faq':
                return []
            return []
        
        mock_rel.get_sorted_related_objects.side_effect = mock_get_sorted_related_objects
        mock_rel.get_related_objects.side_effect = mock_get_related_objects
        
        # Mock uniq to simulate removing duplicates
        mock_uniq.return_value = ['guideline1.yaml', 'check1.yaml']
        
        category = Category('test', {'ja': 'テスト', 'en': 'Test'})
        dependencies = category.get_dependency()
        
        # Verify uniq was called with the expected list
        mock_uniq.assert_called_once_with(['guideline1.yaml', 'check1.yaml'])
        assert dependencies == ['guideline1.yaml', 'check1.yaml']

    def test_list_all_empty(self):
        """Test list_all when no categories exist."""
        assert Category.list_all() == []

    def test_list_all_single_category(self):
        """Test list_all with single category."""
        category = Category('test', {'ja': 'テスト', 'en': 'Test'})
        
        all_categories = Category.list_all()
        assert len(all_categories) == 1
        assert all_categories[0] == category

    def test_list_all_multiple_categories(self):
        """Test list_all with multiple categories."""
        category1 = Category('cat1', {'ja': 'カテゴリ1', 'en': 'Category 1'})
        category2 = Category('cat2', {'ja': 'カテゴリ2', 'en': 'Category 2'})
        category3 = Category('cat3', {'ja': 'カテゴリ3', 'en': 'Category 3'})
        
        all_categories = Category.list_all()
        assert len(all_categories) == 3
        assert category1 in all_categories
        assert category2 in all_categories
        assert category3 in all_categories

    def test_instances_isolation(self):
        """Test that Category instances are properly isolated."""
        # Create categories
        category1 = Category('cat1', {'ja': 'カテゴリ1', 'en': 'Category 1'})
        category2 = Category('cat2', {'ja': 'カテゴリ2', 'en': 'Category 2'})
        
        # Verify they're in instances
        assert len(Category._instances) == 2
        assert Category._instances['cat1'] == category1
        assert Category._instances['cat2'] == category2
        
        # Clear instances
        Category._instances.clear()
        
        # Verify they're cleared
        assert len(Category._instances) == 0
        assert Category.list_all() == []

    def test_get_by_id_existing(self):
        """Test getting category by existing ID."""
        category = Category('test', {'ja': 'テスト', 'en': 'Test'})
        
        retrieved = Category.get_by_id('test')
        assert retrieved == category

    def test_get_by_id_nonexistent(self):
        """Test getting category by non-existent ID."""
        Category('test', {'ja': 'テスト', 'en': 'Test'})
        
        retrieved = Category.get_by_id('nonexistent')
        assert retrieved is None

    def test_object_type_attribute(self):
        """Test that object_type is correctly set."""
        category = Category('test', {'ja': 'テスト', 'en': 'Test'})
        assert category.object_type == 'category'
        assert Category.object_type == 'category'

    def test_inheritance_from_base_model(self):
        """Test that Category properly inherits from BaseModel."""
        from freee_a11y_gl.models.base import BaseModel
        
        category = Category('test', {'ja': 'テスト', 'en': 'Test'})
        assert isinstance(category, BaseModel)
        assert hasattr(category, 'id')
        assert category.id == 'test'

    def test_names_attribute_modification(self):
        """Test that names can be accessed and modified."""
        names = {'ja': 'テスト', 'en': 'Test'}
        category = Category('test', names)
        
        # Test initial names
        assert category.names == names
        
        # Test that modifying the original dict affects the category (they share the same reference)
        names['fr'] = 'Test French'
        assert 'fr' in category.names  # The reference is shared
        
        # Test that we can modify the category's names
        category.names['de'] = 'Test Deutsch'
        assert category.names['de'] == 'Test Deutsch'

    def test_category_with_minimal_names(self):
        """Test category with minimal name data."""
        category = Category('minimal', {'ja': 'ミニマル'})
        
        assert category.get_name('ja') == 'ミニマル'
        assert category.get_name('en') == 'ミニマル'  # Falls back to Japanese
