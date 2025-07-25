"""Tests for reference generator module."""
import pytest
from unittest.mock import Mock, patch, MagicMock

from yaml2rst.generators.content_generators.reference_generator import (
    InfoToGuidelinesGenerator, InfoToFaqsGenerator, AxeRulesGenerator, MiscDefinitionsGenerator
)


@pytest.fixture
def mock_info_ref():
    """Mock InfoRef object."""
    mock_info = Mock()
    mock_info.ref = 'test_ref'
    mock_info.internal = True
    mock_info.src_path = 'data/json/info.json'
    return mock_info


@pytest.fixture
def mock_info_ref_external():
    """Mock external InfoRef object."""
    mock_info = Mock()
    mock_info.ref = 'external_ref'
    mock_info.internal = False
    mock_info.src_path = 'data/json/external_info.json'
    mock_info.refstring.return_value = 'External Reference'
    mock_info.link_data.return_value = {
        'text': {'ja': 'External Link Text', 'en': 'External Link Text'},
        'url': {'ja': 'https://example.com/ja', 'en': 'https://example.com/en'}
    }
    return mock_info


@pytest.fixture
def mock_guideline():
    """Mock Guideline object."""
    mock_gl = Mock()
    mock_gl.get_category_and_id.return_value = {'category': 'test_category', 'id': 'test_gl'}
    return mock_gl


@pytest.fixture
def mock_faq():
    """Mock Faq object."""
    mock_faq = Mock()
    mock_faq.id = 'test_faq'
    return mock_faq


@pytest.fixture
def mock_axe_rule():
    """Mock AxeRule object."""
    mock_rule = Mock()
    mock_rule.src_path = 'data/json/axe_rules.json'
    mock_rule.template_data.return_value = {
        'id': 'test_rule',
        'description': 'Test rule description'
    }
    return mock_rule


class TestInfoToGuidelinesGenerator:
    """Test InfoToGuidelinesGenerator class."""
    
    def test_init(self):
        """Test generator initialization."""
        generator = InfoToGuidelinesGenerator('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_items(self, mock_info_class, mock_info_ref):
        """Test getting items with internal info refs."""
        mock_info_class.list_has_guidelines.return_value = [mock_info_ref]
        
        generator = InfoToGuidelinesGenerator('ja')
        items = generator.get_items()
        
        assert len(items) == 1
        assert items[0] == mock_info_ref
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_items_filters_external(self, mock_info_class, mock_info_ref_external):
        """Test that external info refs are filtered out."""
        mock_info_ref_external.internal = False
        mock_info_class.list_has_guidelines.return_value = [mock_info_ref_external]
        
        generator = InfoToGuidelinesGenerator('ja')
        items = generator.get_items()
        
        assert len(items) == 0
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_items_mixed_internal_external(self, mock_info_class, mock_info_ref, mock_info_ref_external):
        """Test filtering with mixed internal and external refs."""
        mock_info_ref_external.internal = False
        mock_info_class.list_has_guidelines.return_value = [mock_info_ref, mock_info_ref_external]
        
        generator = InfoToGuidelinesGenerator('ja')
        items = generator.get_items()
        
        assert len(items) == 1
        assert items[0] == mock_info_ref
    
    def test_process_item(self, mock_info_ref, mock_guideline):
        """Test processing a single info reference."""
        generator = InfoToGuidelinesGenerator('ja')
        generator.relationship_manager.get_sorted_related_objects = Mock(return_value=[mock_guideline])
        
        result = generator.process_item(mock_info_ref)
        
        assert result['filename'] == 'test_ref'
        assert len(result['guidelines']) == 1
        assert result['guidelines'][0] == {'category': 'test_category', 'id': 'test_gl'}
    
    def test_process_item_no_guidelines(self, mock_info_ref):
        """Test processing info ref with no guidelines."""
        generator = InfoToGuidelinesGenerator('ja')
        generator.relationship_manager.get_sorted_related_objects = Mock(return_value=[])
        
        result = generator.process_item(mock_info_ref)
        
        assert result['filename'] == 'test_ref'
        assert result['guidelines'] == []
    
    def test_process_item_multiple_guidelines(self, mock_info_ref):
        """Test processing info ref with multiple guidelines."""
        mock_gl1 = Mock()
        mock_gl1.get_category_and_id.return_value = {'category': 'cat1', 'id': 'gl1'}
        mock_gl2 = Mock()
        mock_gl2.get_category_and_id.return_value = {'category': 'cat2', 'id': 'gl2'}
        
        generator = InfoToGuidelinesGenerator('ja')
        generator.relationship_manager.get_sorted_related_objects = Mock(return_value=[mock_gl1, mock_gl2])
        
        result = generator.process_item(mock_info_ref)
        
        assert result['filename'] == 'test_ref'
        assert len(result['guidelines']) == 2
        assert result['guidelines'][0] == {'category': 'cat1', 'id': 'gl1'}
        assert result['guidelines'][1] == {'category': 'cat2', 'id': 'gl2'}
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        generator = InfoToGuidelinesGenerator('ja')
        
        valid_data = {
            'filename': 'test_ref',
            'guidelines': [{'category': 'test', 'id': 'gl1'}]
        }
        
        assert generator.validate_data(valid_data) is True
    
    def test_validate_data_missing_filename(self):
        """Test data validation with missing filename."""
        generator = InfoToGuidelinesGenerator('ja')
        
        invalid_data = {
            'guidelines': [{'category': 'test', 'id': 'gl1'}]
        }
        
        assert generator.validate_data(invalid_data) is False
    
    def test_validate_data_missing_guidelines(self):
        """Test data validation with missing guidelines."""
        generator = InfoToGuidelinesGenerator('ja')
        
        invalid_data = {
            'filename': 'test_ref'
        }
        
        assert generator.validate_data(invalid_data) is False
    
    def test_validate_data_invalid_guidelines_type(self):
        """Test data validation with invalid guidelines type."""
        generator = InfoToGuidelinesGenerator('ja')
        
        invalid_data = {
            'filename': 'test_ref',
            'guidelines': 'not_a_list'
        }
        
        assert generator.validate_data(invalid_data) is False
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_dependencies(self, mock_info_class, mock_info_ref):
        """Test getting file dependencies."""
        mock_info_class.list_has_guidelines.return_value = [mock_info_ref]
        
        generator = InfoToGuidelinesGenerator('ja')
        deps = generator.get_dependencies()
        
        assert len(deps) == 1
        assert deps[0] == 'data/json/info.json'


class TestInfoToFaqsGenerator:
    """Test InfoToFaqsGenerator class."""
    
    def test_init(self):
        """Test generator initialization."""
        generator = InfoToFaqsGenerator('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_items(self, mock_info_class, mock_info_ref):
        """Test getting items with internal info refs."""
        mock_info_class.list_has_faqs.return_value = [mock_info_ref]
        
        generator = InfoToFaqsGenerator('ja')
        items = generator.get_items()
        
        assert len(items) == 1
        assert items[0] == mock_info_ref
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_items_filters_external(self, mock_info_class, mock_info_ref_external):
        """Test that external info refs are filtered out."""
        mock_info_ref_external.internal = False
        mock_info_class.list_has_faqs.return_value = [mock_info_ref_external]
        
        generator = InfoToFaqsGenerator('ja')
        items = generator.get_items()
        
        assert len(items) == 0
    
    def test_process_item(self, mock_info_ref, mock_faq):
        """Test processing a single info reference."""
        generator = InfoToFaqsGenerator('ja')
        generator.relationship_manager.get_sorted_related_objects = Mock(return_value=[mock_faq])
        
        result = generator.process_item(mock_info_ref)
        
        assert result['filename'] == 'test_ref'
        assert len(result['faqs']) == 1
        assert result['faqs'][0] == 'test_faq'
    
    def test_process_item_no_faqs(self, mock_info_ref):
        """Test processing info ref with no FAQs."""
        generator = InfoToFaqsGenerator('ja')
        generator.relationship_manager.get_sorted_related_objects = Mock(return_value=[])
        
        result = generator.process_item(mock_info_ref)
        
        assert result['filename'] == 'test_ref'
        assert result['faqs'] == []
    
    def test_process_item_multiple_faqs(self, mock_info_ref):
        """Test processing info ref with multiple FAQs."""
        mock_faq1 = Mock()
        mock_faq1.id = 'faq1'
        mock_faq2 = Mock()
        mock_faq2.id = 'faq2'
        
        generator = InfoToFaqsGenerator('ja')
        generator.relationship_manager.get_sorted_related_objects = Mock(return_value=[mock_faq1, mock_faq2])
        
        result = generator.process_item(mock_info_ref)
        
        assert result['filename'] == 'test_ref'
        assert len(result['faqs']) == 2
        assert result['faqs'][0] == 'faq1'
        assert result['faqs'][1] == 'faq2'
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        generator = InfoToFaqsGenerator('ja')
        
        valid_data = {
            'filename': 'test_ref',
            'faqs': ['faq1', 'faq2']
        }
        
        assert generator.validate_data(valid_data) is True
    
    def test_validate_data_missing_filename(self):
        """Test data validation with missing filename."""
        generator = InfoToFaqsGenerator('ja')
        
        invalid_data = {
            'faqs': ['faq1', 'faq2']
        }
        
        assert generator.validate_data(invalid_data) is False
    
    def test_validate_data_missing_faqs(self):
        """Test data validation with missing faqs."""
        generator = InfoToFaqsGenerator('ja')
        
        invalid_data = {
            'filename': 'test_ref'
        }
        
        assert generator.validate_data(invalid_data) is False
    
    def test_validate_data_invalid_faqs_type(self):
        """Test data validation with invalid faqs type."""
        generator = InfoToFaqsGenerator('ja')
        
        invalid_data = {
            'filename': 'test_ref',
            'faqs': 'not_a_list'
        }
        
        assert generator.validate_data(invalid_data) is False
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_dependencies(self, mock_info_class, mock_info_ref):
        """Test getting file dependencies."""
        mock_info_class.list_has_faqs.return_value = [mock_info_ref]
        
        generator = InfoToFaqsGenerator('ja')
        deps = generator.get_dependencies()
        
        assert len(deps) == 1
        assert deps[0] == 'data/json/info.json'


class TestAxeRulesGenerator:
    """Test AxeRulesGenerator class."""
    
    def test_init(self):
        """Test generator initialization."""
        generator = AxeRulesGenerator('ja')
        assert generator.lang == 'ja'
    
    @patch('yaml2rst.generators.content_generators.reference_generator.AxeRule')
    def test_get_template_data(self, mock_axe_rule_class, mock_axe_rule):
        """Test template data generation."""
        mock_axe_rule_class.version = '4.4.0'
        mock_axe_rule_class.major_version = '4'
        mock_axe_rule_class.deque_url = 'https://deque.com'
        mock_axe_rule_class.timestamp = '2023-01-01'
        mock_axe_rule_class.list_all.return_value = [mock_axe_rule]
        
        generator = AxeRulesGenerator('ja')
        data = generator.get_template_data()
        
        assert data['version'] == '4.4.0'
        assert data['major_version'] == '4'
        assert data['deque_url'] == 'https://deque.com'
        assert data['timestamp'] == '2023-01-01'
        assert len(data['rules']) == 1
        assert data['rules'][0] == {'id': 'test_rule', 'description': 'Test rule description'}
    
    @patch('yaml2rst.generators.content_generators.reference_generator.AxeRule')
    def test_get_template_data_no_rules(self, mock_axe_rule_class):
        """Test template data generation with no rules."""
        mock_axe_rule_class.version = '4.4.0'
        mock_axe_rule_class.major_version = '4'
        mock_axe_rule_class.deque_url = 'https://deque.com'
        mock_axe_rule_class.timestamp = '2023-01-01'
        mock_axe_rule_class.list_all.return_value = []
        
        generator = AxeRulesGenerator('ja')
        data = generator.get_template_data()
        
        assert data['version'] == '4.4.0'
        assert data['rules'] == []
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        generator = AxeRulesGenerator('ja')
        
        valid_data = {
            'version': '4.4.0',
            'major_version': '4',
            'deque_url': 'https://deque.com',
            'timestamp': '2023-01-01',
            'rules': [{'id': 'test_rule'}]
        }
        
        assert generator.validate_data(valid_data) is True
    
    def test_validate_data_missing_version(self):
        """Test data validation with missing version."""
        generator = AxeRulesGenerator('ja')
        
        invalid_data = {
            'major_version': '4',
            'deque_url': 'https://deque.com',
            'timestamp': '2023-01-01',
            'rules': []
        }
        
        assert generator.validate_data(invalid_data) is False
    
    def test_validate_data_missing_rules(self):
        """Test data validation with missing rules."""
        generator = AxeRulesGenerator('ja')
        
        invalid_data = {
            'version': '4.4.0',
            'major_version': '4',
            'deque_url': 'https://deque.com',
            'timestamp': '2023-01-01'
        }
        
        assert generator.validate_data(invalid_data) is False
    
    def test_validate_data_invalid_rules_type(self):
        """Test data validation with invalid rules type."""
        generator = AxeRulesGenerator('ja')
        
        invalid_data = {
            'version': '4.4.0',
            'major_version': '4',
            'deque_url': 'https://deque.com',
            'timestamp': '2023-01-01',
            'rules': 'not_a_list'
        }
        
        assert generator.validate_data(invalid_data) is False
    
    @patch('yaml2rst.generators.content_generators.reference_generator.AxeRule')
    def test_get_dependencies(self, mock_axe_rule_class, mock_axe_rule):
        """Test getting file dependencies."""
        mock_axe_rule_class.list_all.return_value = [mock_axe_rule]
        
        generator = AxeRulesGenerator('ja')
        deps = generator.get_dependencies()
        
        assert len(deps) == 1
        assert deps[0] == 'data/json/axe_rules.json'


class TestMiscDefinitionsGenerator:
    """Test MiscDefinitionsGenerator class."""
    
    def test_init(self):
        """Test generator initialization."""
        generator = MiscDefinitionsGenerator('ja')
        assert generator.lang == 'ja'
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_template_data(self, mock_info_class, mock_info_ref_external):
        """Test template data generation."""
        mock_info_class.list_all_external.return_value = [mock_info_ref_external]
        
        generator = MiscDefinitionsGenerator('ja')
        data = generator.get_template_data()
        
        assert 'links' in data
        assert len(data['links']) == 1
        link = data['links'][0]
        assert link['label'] == 'External Reference'
        assert link['text'] == 'External Link Text'
        assert link['url'] == 'https://example.com/ja'
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_template_data_no_external_refs(self, mock_info_class):
        """Test template data generation with no external refs."""
        mock_info_class.list_all_external.return_value = []
        
        generator = MiscDefinitionsGenerator('ja')
        data = generator.get_template_data()
        
        assert 'links' in data
        assert data['links'] == []
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_template_data_multiple_refs(self, mock_info_class):
        """Test template data generation with multiple external refs."""
        mock_ref1 = Mock()
        mock_ref1.refstring.return_value = 'Ref 1'
        mock_ref1.link_data.return_value = {
            'text': {'ja': 'Text 1', 'en': 'Text 1'},
            'url': {'ja': 'https://example1.com', 'en': 'https://example1.com'}
        }
        
        mock_ref2 = Mock()
        mock_ref2.refstring.return_value = 'Ref 2'
        mock_ref2.link_data.return_value = {
            'text': {'ja': 'Text 2', 'en': 'Text 2'},
            'url': {'ja': 'https://example2.com', 'en': 'https://example2.com'}
        }
        
        mock_info_class.list_all_external.return_value = [mock_ref1, mock_ref2]
        
        generator = MiscDefinitionsGenerator('ja')
        data = generator.get_template_data()
        
        assert len(data['links']) == 2
        assert data['links'][0]['label'] == 'Ref 1'
        assert data['links'][1]['label'] == 'Ref 2'
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        generator = MiscDefinitionsGenerator('ja')
        
        valid_data = {
            'links': [
                {
                    'label': 'Test Link',
                    'text': 'Test Text',
                    'url': 'https://example.com'
                }
            ]
        }
        
        assert generator.validate_data(valid_data) is True
    
    def test_validate_data_empty_links(self):
        """Test data validation with empty links."""
        generator = MiscDefinitionsGenerator('ja')
        
        valid_data = {
            'links': []
        }
        
        assert generator.validate_data(valid_data) is True
    
    def test_validate_data_missing_links(self):
        """Test data validation with missing links."""
        generator = MiscDefinitionsGenerator('ja')
        
        invalid_data = {}
        
        assert generator.validate_data(invalid_data) is False
    
    def test_validate_data_invalid_links_type(self):
        """Test data validation with invalid links type."""
        generator = MiscDefinitionsGenerator('ja')
        
        invalid_data = {
            'links': 'not_a_list'
        }
        
        assert generator.validate_data(invalid_data) is False
    
    def test_validate_data_invalid_link_structure(self):
        """Test data validation with invalid link structure."""
        generator = MiscDefinitionsGenerator('ja')
        
        # Missing 'label'
        invalid_data1 = {
            'links': [
                {
                    'text': 'Test Text',
                    'url': 'https://example.com'
                }
            ]
        }
        assert generator.validate_data(invalid_data1) is False
        
        # Missing 'text'
        invalid_data2 = {
            'links': [
                {
                    'label': 'Test Link',
                    'url': 'https://example.com'
                }
            ]
        }
        assert generator.validate_data(invalid_data2) is False
        
        # Missing 'url'
        invalid_data3 = {
            'links': [
                {
                    'label': 'Test Link',
                    'text': 'Test Text'
                }
            ]
        }
        assert generator.validate_data(invalid_data3) is False
    
    @patch('yaml2rst.generators.content_generators.reference_generator.InfoRef')
    def test_get_dependencies(self, mock_info_class, mock_info_ref_external):
        """Test getting file dependencies."""
        mock_info_class.list_all_external.return_value = [mock_info_ref_external]
        
        generator = MiscDefinitionsGenerator('ja')
        deps = generator.get_dependencies()
        
        assert len(deps) == 1
        assert deps[0] == 'data/json/external_info.json'
