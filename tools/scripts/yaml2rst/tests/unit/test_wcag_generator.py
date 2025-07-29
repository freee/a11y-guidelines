"""Tests for WCAG generator module."""
import pytest
from unittest.mock import Mock, patch

from yaml2rst.generators.content_generators.wcag_generator import (
    WcagGeneratorBase, WcagMappingGenerator, PriorityDiffGenerator
)


@pytest.fixture
def mock_wcag_sc():
    """Mock WcagSc object."""
    mock_sc = Mock()
    mock_sc.id = 'test_sc'
    mock_sc.src_path = 'data/json/wcag_sc.json'
    mock_sc.level = 'AA'
    mock_sc.local_priority = 'AA'
    mock_sc.template_data.return_value = {
        'id': 'test_sc',
        'level': 'AA',
        'local_priority': 'AA',
        'title': 'Test Success Criterion'
    }
    return mock_sc


@pytest.fixture
def mock_wcag_sc_diff():
    """Mock WcagSc object with different priority."""
    mock_sc = Mock()
    mock_sc.id = 'diff_sc'
    mock_sc.src_path = 'data/json/wcag_sc.json'
    mock_sc.level = 'AAA'
    mock_sc.local_priority = 'AA'  # Different from level
    mock_sc.template_data.return_value = {
        'id': 'diff_sc',
        'level': 'AAA',
        'local_priority': 'AA',
        'title': 'Different Priority SC'
    }
    return mock_sc


@pytest.fixture
def mock_guideline():
    """Mock Guideline object."""
    mock_gl = Mock()
    mock_gl.get_category_and_id.return_value = {
        'category': 'test_category',
        'id': 'test_guideline'
    }
    return mock_gl


class MockWcagGeneratorBase(WcagGeneratorBase):
    """Mock implementation of WcagGeneratorBase for testing."""

    def generate(self):
        """Mock generate method."""
        return iter([])


class TestWcagGeneratorBase:
    """Test WcagGeneratorBase class."""

    def test_init(self):
        """Test base generator initialization."""
        generator = MockWcagGeneratorBase('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_dependencies(self, mock_wcag_sc_class, mock_wcag_sc):
        """Test getting WCAG SC file dependencies."""
        mock_wcag_sc_class.get_all.return_value = {
            'test_sc': mock_wcag_sc
        }

        generator = MockWcagGeneratorBase('ja')
        deps = generator.get_dependencies()

        assert len(deps) == 1
        assert deps[0] == 'data/json/wcag_sc.json'

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_dependencies_multiple(self, mock_wcag_sc_class):
        """Test getting dependencies for multiple WCAG SCs."""
        mock_sc1 = Mock()
        mock_sc1.src_path = 'path1.json'
        mock_sc2 = Mock()
        mock_sc2.src_path = 'path2.json'

        mock_wcag_sc_class.get_all.return_value = {
            'sc1': mock_sc1,
            'sc2': mock_sc2
        }

        generator = MockWcagGeneratorBase('ja')
        deps = generator.get_dependencies()

        assert len(deps) == 2
        assert 'path1.json' in deps
        assert 'path2.json' in deps

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_dependencies_empty(self, mock_wcag_sc_class):
        """Test getting dependencies with no WCAG SCs."""
        mock_wcag_sc_class.get_all.return_value = {}

        generator = MockWcagGeneratorBase('ja')
        deps = generator.get_dependencies()

        assert deps == []

    def test_get_guidelines_for_sc(self, mock_wcag_sc, mock_guideline):
        """Test getting guidelines for a success criterion."""
        generator = MockWcagGeneratorBase('ja')
        generator.relationship_manager.get_sorted_related_objects = (
            Mock(return_value=[mock_guideline]))

        guidelines = generator.get_guidelines_for_sc(mock_wcag_sc)

        assert len(guidelines) == 1
        assert guidelines[0] == {
            'category': 'test_category', 'id': 'test_guideline'}
        generator.relationship_manager.get_sorted_related_objects.\
            assert_called_once_with(mock_wcag_sc, 'guideline', 'sort_key')

    def test_get_guidelines_for_sc_no_guidelines(self, mock_wcag_sc):
        """Test getting guidelines for SC with no guidelines."""
        generator = MockWcagGeneratorBase('ja')
        generator.relationship_manager.get_sorted_related_objects = (
            Mock(return_value=[]))

        guidelines = generator.get_guidelines_for_sc(mock_wcag_sc)

        assert guidelines == []

    def test_get_guidelines_for_sc_multiple(self, mock_wcag_sc):
        """Test getting multiple guidelines for a success criterion."""
        mock_gl1 = Mock()
        mock_gl1.get_category_and_id.return_value = {
            'category': 'cat1', 'id': 'gl1'}
        mock_gl2 = Mock()
        mock_gl2.get_category_and_id.return_value = {
            'category': 'cat2', 'id': 'gl2'}

        generator = MockWcagGeneratorBase('ja')
        generator.relationship_manager.get_sorted_related_objects = (
            Mock(return_value=[mock_gl1, mock_gl2]))

        guidelines = generator.get_guidelines_for_sc(mock_wcag_sc)

        assert len(guidelines) == 2
        assert guidelines[0] == {'category': 'cat1', 'id': 'gl1'}
        assert guidelines[1] == {'category': 'cat2', 'id': 'gl2'}


class TestWcagMappingGenerator:
    """Test WcagMappingGenerator class."""

    def test_init(self):
        """Test generator initialization."""
        generator = WcagMappingGenerator('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_template_data(self, mock_wcag_sc_class, mock_wcag_sc,
                               mock_guideline):
        """Test template data generation."""
        mock_wcag_sc_class.get_all.return_value = {'test_sc': mock_wcag_sc}

        generator = WcagMappingGenerator('ja')
        generator.get_guidelines_for_sc = Mock(return_value=[
            {'category': 'test_category', 'id': 'test_guideline'}
        ])

        data = generator.get_template_data()

        assert 'mapping' in data
        assert len(data['mapping']) == 1
        mapping = data['mapping'][0]
        assert mapping['id'] == 'test_sc'
        assert mapping['level'] == 'AA'
        assert 'guidelines' in mapping
        assert len(mapping['guidelines']) == 1

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_template_data_no_guidelines(self, mock_wcag_sc_class,
                                             mock_wcag_sc):
        """Test template data generation with SC having no guidelines."""
        mock_wcag_sc_class.get_all.return_value = {'test_sc': mock_wcag_sc}

        generator = WcagMappingGenerator('ja')
        generator.get_guidelines_for_sc = Mock(return_value=[])

        data = generator.get_template_data()

        assert 'mapping' in data
        assert len(data['mapping']) == 1
        mapping = data['mapping'][0]
        assert mapping['id'] == 'test_sc'
        # Should not have guidelines field when empty
        assert 'guidelines' not in mapping

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_template_data_multiple_scs(self, mock_wcag_sc_class):
        """Test template data generation with multiple SCs."""
        mock_sc1 = Mock()
        mock_sc1.template_data.return_value = {'id': 'sc1', 'level': 'A'}
        mock_sc2 = Mock()
        mock_sc2.template_data.return_value = {'id': 'sc2', 'level': 'AA'}

        mock_wcag_sc_class.get_all.return_value = {
            'sc1': mock_sc1,
            'sc2': mock_sc2
        }

        generator = WcagMappingGenerator('ja')
        generator.get_guidelines_for_sc = Mock(return_value=[])

        data = generator.get_template_data()

        assert 'mapping' in data
        assert len(data['mapping']) == 2
        assert data['mapping'][0]['id'] == 'sc1'
        assert data['mapping'][1]['id'] == 'sc2'

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_template_data_empty(self, mock_wcag_sc_class):
        """Test template data generation with no SCs."""
        mock_wcag_sc_class.get_all.return_value = {}

        generator = WcagMappingGenerator('ja')
        data = generator.get_template_data()

        assert 'mapping' in data
        assert data['mapping'] == []

    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        generator = WcagMappingGenerator('ja')

        valid_data = {
            'mapping': [
                {'id': 'sc1', 'level': 'A'},
                {'id': 'sc2', 'level': 'AA', 'guidelines': []}
            ]
        }

        assert generator.validate_data(valid_data) is True

    def test_validate_data_empty_mapping(self):
        """Test data validation with empty mapping."""
        generator = WcagMappingGenerator('ja')

        valid_data = {
            'mapping': []
        }

        assert generator.validate_data(valid_data) is True

    def test_validate_data_missing_mapping(self):
        """Test data validation with missing mapping field."""
        generator = WcagMappingGenerator('ja')

        invalid_data = {
            'other_field': 'value'
        }

        assert generator.validate_data(invalid_data) is False

    def test_validate_data_invalid_mapping_type(self):
        """Test data validation with invalid mapping type."""
        generator = WcagMappingGenerator('ja')

        invalid_data = {
            'mapping': 'not_a_list'
        }

        assert generator.validate_data(invalid_data) is False


class TestPriorityDiffGenerator:
    """Test PriorityDiffGenerator class."""

    def test_init(self):
        """Test generator initialization."""
        generator = PriorityDiffGenerator('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_template_data_with_diffs(self, mock_wcag_sc_class,
                                          mock_wcag_sc_diff):
        """Test template data generation with priority differences."""
        # Mock SC with different level and local_priority
        mock_wcag_sc_class.get_all.return_value = {
            'diff_sc': mock_wcag_sc_diff}

        generator = PriorityDiffGenerator('ja')
        data = generator.get_template_data()

        assert 'diffs' in data
        assert len(data['diffs']) == 1
        diff = data['diffs'][0]
        assert diff['id'] == 'diff_sc'
        assert diff['level'] == 'AAA'
        assert diff['local_priority'] == 'AA'

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_template_data_no_diffs(self, mock_wcag_sc_class,
                                        mock_wcag_sc):
        """Test template data generation with no priority differences."""
        # Mock SC with same level and local_priority
        mock_wcag_sc_class.get_all.return_value = {'test_sc': mock_wcag_sc}

        generator = PriorityDiffGenerator('ja')
        data = generator.get_template_data()

        assert 'diffs' in data
        assert data['diffs'] == []

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_template_data_mixed(self, mock_wcag_sc_class, mock_wcag_sc,
                                     mock_wcag_sc_diff):
        """Test template data generation with mixed SCs."""
        mock_wcag_sc_class.get_all.return_value = {
            'test_sc': mock_wcag_sc,  # No diff (level == local_priority)
            'diff_sc': mock_wcag_sc_diff  # Has diff (level != local_priority)
        }

        generator = PriorityDiffGenerator('ja')
        data = generator.get_template_data()

        assert 'diffs' in data
        assert len(data['diffs']) == 1  # Only the one with difference
        assert data['diffs'][0]['id'] == 'diff_sc'

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_template_data_multiple_diffs(self, mock_wcag_sc_class):
        """Test template data generation with multiple priority differences."""
        mock_sc1 = Mock()
        mock_sc1.level = 'AAA'
        mock_sc1.local_priority = 'AA'
        mock_sc1.template_data.return_value = {
            'id': 'sc1', 'level': 'AAA', 'local_priority': 'AA'}

        mock_sc2 = Mock()
        mock_sc2.level = 'AA'
        mock_sc2.local_priority = 'A'
        mock_sc2.template_data.return_value = {
            'id': 'sc2', 'level': 'AA', 'local_priority': 'A'}

        mock_wcag_sc_class.get_all.return_value = {
            'sc1': mock_sc1,
            'sc2': mock_sc2
        }

        generator = PriorityDiffGenerator('ja')
        data = generator.get_template_data()

        assert 'diffs' in data
        assert len(data['diffs']) == 2
        assert data['diffs'][0]['id'] == 'sc1'
        assert data['diffs'][1]['id'] == 'sc2'

    @patch('yaml2rst.generators.content_generators.wcag_generator.WcagSc')
    def test_get_template_data_empty(self, mock_wcag_sc_class):
        """Test template data generation with no SCs."""
        mock_wcag_sc_class.get_all.return_value = {}

        generator = PriorityDiffGenerator('ja')
        data = generator.get_template_data()

        assert 'diffs' in data
        assert data['diffs'] == []

    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        generator = PriorityDiffGenerator('ja')

        valid_data = {
            'diffs': [
                {'id': 'sc1', 'level': 'AAA', 'local_priority': 'AA'},
                {'id': 'sc2', 'level': 'AA', 'local_priority': 'A'}
            ]
        }

        assert generator.validate_data(valid_data) is True

    def test_validate_data_empty_diffs(self):
        """Test data validation with empty diffs."""
        generator = PriorityDiffGenerator('ja')

        valid_data = {
            'diffs': []
        }

        assert generator.validate_data(valid_data) is True

    def test_validate_data_missing_diffs(self):
        """Test data validation with missing diffs field."""
        generator = PriorityDiffGenerator('ja')

        invalid_data = {
            'other_field': 'value'
        }

        assert generator.validate_data(invalid_data) is False

    def test_validate_data_invalid_diffs_type(self):
        """Test data validation with invalid diffs type."""
        generator = PriorityDiffGenerator('ja')

        invalid_data = {
            'diffs': 'not_a_list'
        }

        assert generator.validate_data(invalid_data) is False
