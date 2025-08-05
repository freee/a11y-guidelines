"""Tests for check generator module."""
import pytest
from unittest.mock import Mock, patch

from yaml2rst.generators.content_generators.check_generator import (
    CheckGeneratorBase, AllChecksGenerator, CheckExampleGenerator
)


@pytest.fixture
def mock_check():
    """Mock Check object."""
    mock_check = Mock()
    mock_check.id = 'test_check'
    mock_check.src_path = 'data/yaml/checks/test_check.yaml'
    return mock_check


@pytest.fixture
def mock_check_tool():
    """Mock CheckTool object."""
    mock_tool = Mock()
    mock_tool.id = 'test_tool'
    mock_tool.src_path = 'data/yaml/checks/tools/test_tool.yaml'
    mock_tool.example_template_data.return_value = {
        'examples': [
            {'title': 'Example 1', 'content': 'Example content 1'},
            {'title': 'Example 2', 'content': 'Example content 2'}
        ]
    }
    return mock_tool


class MockCheckGeneratorBase(CheckGeneratorBase):
    """Mock implementation of CheckGeneratorBase for testing."""

    def generate(self):
        """Mock generate method."""
        return iter([])


class TestCheckGeneratorBase:
    """Test CheckGeneratorBase class."""

    def test_init(self):
        """Test base generator initialization."""
        generator = MockCheckGeneratorBase('ja')
        assert generator.lang == 'ja'

    @patch('yaml2rst.generators.content_generators.check_generator.Check')
    def test_get_dependencies(self, mock_check_class):
        """Test getting check file dependencies."""
        mock_check_class.list_all_src_paths.return_value = [
            'data/yaml/checks/check1.yaml',
            'data/yaml/checks/check2.yaml'
        ]

        generator = MockCheckGeneratorBase('ja')
        deps = generator.get_dependencies()

        assert len(deps) == 2
        assert 'data/yaml/checks/check1.yaml' in deps
        assert 'data/yaml/checks/check2.yaml' in deps

    @patch('yaml2rst.generators.content_generators.check_generator.Check')
    def test_get_dependencies_empty(self, mock_check_class):
        """Test getting dependencies with no checks."""
        mock_check_class.list_all_src_paths.return_value = []

        generator = MockCheckGeneratorBase('ja')
        deps = generator.get_dependencies()

        assert deps == []

    def test_validate_data_default(self):
        """Test default validation always returns True."""
        generator = MockCheckGeneratorBase('ja')

        # Should return True for any data
        assert generator.validate_data({}) is True
        assert generator.validate_data({'any': 'data'}) is True
        assert generator.validate_data(None) is True


class TestAllChecksGenerator:
    """Test AllChecksGenerator class."""

    def test_init(self):
        """Test generator initialization."""
        generator = AllChecksGenerator('ja')
        assert generator.lang == 'ja'

    @patch('yaml2rst.generators.content_generators.check_generator.Check')
    def test_get_template_data(self, mock_check_class):
        """Test template data generation."""
        # Mock the generator returned by template_data_all
        mock_generator = iter([
            {'id': 'check1', 'title': 'Check 1'},
            {'id': 'check2', 'title': 'Check 2'}
        ])
        mock_check_class.template_data_all.return_value = mock_generator

        generator = AllChecksGenerator('ja')

        # Mock the logger to avoid actual logging during tests
        generator.logger = Mock()

        data = generator.get_template_data()

        assert 'allchecks' in data
        assert len(data['allchecks']) == 2
        assert data['allchecks'][0]['id'] == 'check1'
        assert data['allchecks'][1]['id'] == 'check2'

        # Verify logging calls
        generator.logger.info.assert_any_call("Generating all checks data")
        generator.logger.info.assert_any_call("Generated 2 checks")

    @patch('yaml2rst.generators.content_generators.check_generator.Check')
    def test_get_template_data_empty(self, mock_check_class):
        """Test template data generation with no checks."""
        mock_check_class.template_data_all.return_value = iter([])

        generator = AllChecksGenerator('ja')
        generator.logger = Mock()

        data = generator.get_template_data()

        assert 'allchecks' in data
        assert data['allchecks'] == []

        generator.logger.info.assert_any_call("Generated 0 checks")

    @pytest.mark.parametrize("data,expected", [
        # Valid data cases
        ({
            'allchecks': [
                {'id': 'check1', 'title': 'Check 1'},
                {'id': 'check2', 'title': 'Check 2'}
            ]
        }, True),
        # Empty list case
        ({'allchecks': []}, True),
        # Missing field case
        ({'other_field': 'value'}, False),
        # Invalid type case
        ({'allchecks': 'not_a_list'}, False),
    ])
    def test_validate_data_allchecks(self, data, expected):
        """Test AllChecksGenerator data validation with various inputs."""
        generator = AllChecksGenerator('ja')
        assert generator.validate_data(data) == expected


class TestCheckExampleGenerator:
    """Test CheckExampleGenerator class."""

    def test_init(self):
        """Test generator initialization."""
        generator = CheckExampleGenerator('ja')
        assert generator.lang == 'ja'

    @patch('yaml2rst.generators.content_generators.check_generator.CheckTool')
    def test_get_items(self, mock_checktool_class, mock_check_tool):
        """Test getting check tool items."""
        mock_checktool_class.list_all.return_value = [mock_check_tool]

        generator = CheckExampleGenerator('ja')
        items = generator.get_items()

        assert len(items) == 1
        assert items[0] == mock_check_tool

    @patch('yaml2rst.generators.content_generators.check_generator.CheckTool')
    def test_get_items_empty(self, mock_checktool_class):
        """Test getting items with no check tools."""
        mock_checktool_class.list_all.return_value = []

        generator = CheckExampleGenerator('ja')
        items = generator.get_items()

        assert items == []

    @patch('yaml2rst.generators.content_generators.check_generator.CheckTool')
    def test_get_items_multiple(self, mock_checktool_class):
        """Test getting multiple check tool items."""
        mock_tool1 = Mock()
        mock_tool1.id = 'tool1'
        mock_tool2 = Mock()
        mock_tool2.id = 'tool2'

        mock_checktool_class.list_all.return_value = [mock_tool1, mock_tool2]

        generator = CheckExampleGenerator('ja')
        items = generator.get_items()

        assert len(items) == 2
        assert items[0] == mock_tool1
        assert items[1] == mock_tool2

    def test_process_item(self, mock_check_tool):
        """Test processing a single check tool."""
        generator = CheckExampleGenerator('ja')
        result = generator.process_item(mock_check_tool)

        assert result['filename'] == 'examples-test_tool'
        assert 'examples' in result
        assert result['examples'] == {
            'examples': [
                {'title': 'Example 1', 'content': 'Example content 1'},
                {'title': 'Example 2', 'content': 'Example content 2'}
            ]
        }

    def test_process_item_no_examples(self):
        """Test processing check tool with no examples."""
        mock_tool = Mock()
        mock_tool.id = 'empty_tool'
        mock_tool.example_template_data.return_value = {'examples': []}

        generator = CheckExampleGenerator('ja')
        result = generator.process_item(mock_tool)

        assert result['filename'] == 'examples-empty_tool'
        assert result['examples'] == {'examples': []}

    @pytest.mark.parametrize("data,expected", [
        # Valid data cases
        ({
            'filename': 'examples-test_tool',
            'examples': {'examples': [{'title': 'Test', 'content': 'Content'}]}
        }, True),
        # Valid with empty examples
        ({
            'filename': 'examples-test_tool',
            'examples': {'examples': []},
            'extra_field': 'ignored'  # Extra fields should be ignored
        }, True),
        # Missing filename
        ({'examples': {'examples': []}}, False),
        # Missing examples
        ({'filename': 'examples-test_tool'}, False),
    ])
    def test_validate_data_check_examples(self, data, expected):
        """Test CheckExampleGenerator data validation with various inputs."""
        generator = CheckExampleGenerator('ja')
        assert generator.validate_data(data) == expected

    @patch('yaml2rst.generators.content_generators.check_generator.CheckTool')
    def test_get_dependencies(self, mock_checktool_class, mock_check_tool):
        """Test getting check tool file dependencies."""
        mock_checktool_class.list_all.return_value = [mock_check_tool]

        generator = CheckExampleGenerator('ja')
        deps = generator.get_dependencies()

        assert len(deps) == 1
        assert deps[0] == 'data/yaml/checks/tools/test_tool.yaml'

    @patch('yaml2rst.generators.content_generators.check_generator.CheckTool')
    def test_get_dependencies_multiple_tools(self, mock_checktool_class):
        """Test getting dependencies for multiple check tools."""
        mock_tool1 = Mock()
        mock_tool1.src_path = 'path1.yaml'
        mock_tool2 = Mock()
        mock_tool2.src_path = 'path2.yaml'

        mock_checktool_class.list_all.return_value = [mock_tool1, mock_tool2]

        generator = CheckExampleGenerator('ja')
        deps = generator.get_dependencies()

        assert len(deps) == 2
        assert 'path1.yaml' in deps
        assert 'path2.yaml' in deps

    @patch('yaml2rst.generators.content_generators.check_generator.CheckTool')
    def test_get_dependencies_empty(self, mock_checktool_class):
        """Test getting dependencies with no check tools."""
        mock_checktool_class.list_all.return_value = []

        generator = CheckExampleGenerator('ja')
        deps = generator.get_dependencies()

        assert deps == []
