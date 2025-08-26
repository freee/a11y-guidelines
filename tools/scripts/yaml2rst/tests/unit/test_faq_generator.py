"""Tests for FAQ generator module."""
import pytest
from unittest.mock import Mock, patch

from yaml2rst.generators.content_generators.faq_generator import (
    FaqGeneratorBase, FaqArticleGenerator, FaqIndexGenerator,
    FaqTagPageGenerator, FaqTagIndexGenerator, FaqArticleIndexGenerator
)


@pytest.fixture
def mock_faq():
    """Mock Faq object."""
    mock_faq = Mock()
    mock_faq.id = 'test_faq'
    mock_faq.src_path = 'data/yaml/faq/test_faq.yaml'
    mock_faq.template_data.return_value = {
        'id': 'test_faq',
        'title': 'Test FAQ',
        'question': 'What is this?',
        'answer': 'This is a test FAQ'
    }
    return mock_faq


@pytest.fixture
def mock_faq_tag():
    """Mock FaqTag object."""
    mock_tag = Mock()
    mock_tag.id = 'test_tag'
    mock_tag.article_count.return_value = 2
    mock_tag.names = {'ja': 'テストタグ', 'en': 'Test Tag'}
    mock_tag.template_data.return_value = {
        'id': 'test_tag',
        'name': 'Test Tag',
        'article_count': 2
    }
    return mock_tag


@pytest.fixture
def mock_faq_tag_empty():
    """Mock FaqTag object with no articles."""
    mock_tag = Mock()
    mock_tag.id = 'empty_tag'
    mock_tag.article_count.return_value = 0
    mock_tag.names = {'ja': '空タグ', 'en': 'Empty Tag'}
    return mock_tag


class MockFaqGeneratorBase(FaqGeneratorBase):
    """Mock implementation of FaqGeneratorBase for testing."""

    def generate(self):
        """Mock generate method."""
        return iter([])


class TestFaqGeneratorBase:
    """Test FaqGeneratorBase class."""

    def test_init(self):
        """Test base generator initialization."""
        generator = MockFaqGeneratorBase('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_dependencies(self, mock_faq_class, mock_faq):
        """Test getting FAQ file dependencies."""
        mock_faq_class.list_all.return_value = [mock_faq]

        generator = MockFaqGeneratorBase('ja')
        deps = generator.get_dependencies()

        assert len(deps) == 1
        assert deps[0] == 'data/yaml/faq/test_faq.yaml'

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_dependencies_multiple(self, mock_faq_class):
        """Test getting dependencies for multiple FAQs."""
        mock_faq1 = Mock()
        mock_faq1.src_path = 'path1.yaml'
        mock_faq2 = Mock()
        mock_faq2.src_path = 'path2.yaml'

        mock_faq_class.list_all.return_value = [mock_faq1, mock_faq2]

        generator = MockFaqGeneratorBase('ja')
        deps = generator.get_dependencies()

        assert len(deps) == 2
        assert 'path1.yaml' in deps
        assert 'path2.yaml' in deps

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_dependencies_empty(self, mock_faq_class):
        """Test getting dependencies with no FAQs."""
        mock_faq_class.list_all.return_value = []

        generator = MockFaqGeneratorBase('ja')
        deps = generator.get_dependencies()

        assert deps == []

    @patch('yaml2rst.generators.content_generators.faq_generator.FaqTag')
    def test_get_sorted_tags(self, mock_faq_tag_class, mock_faq_tag,
                             mock_faq_tag_empty):
        """Test getting sorted tags with articles."""
        mock_faq_tag_class.list_all.return_value = [mock_faq_tag,
                                                    mock_faq_tag_empty]

        generator = MockFaqGeneratorBase('ja')
        sorted_tags = generator.get_sorted_tags()

        # Should only include tags with articles (article_count > 0)
        assert len(sorted_tags) == 1
        assert sorted_tags[0] == mock_faq_tag

    @patch('yaml2rst.generators.content_generators.faq_generator.FaqTag')
    def test_get_sorted_tags_empty(self, mock_faq_tag_class):
        """Test getting sorted tags with no tags."""
        mock_faq_tag_class.list_all.return_value = []

        generator = MockFaqGeneratorBase('ja')
        sorted_tags = generator.get_sorted_tags()

        assert sorted_tags == []

    @patch('yaml2rst.generators.content_generators.faq_generator.FaqTag')
    def test_get_sorted_tags_sorting(self, mock_faq_tag_class):
        """Test that tags are sorted by name."""
        mock_tag1 = Mock()
        mock_tag1.article_count.return_value = 1
        mock_tag1.names = {'ja': 'Zタグ', 'en': 'Z Tag'}

        mock_tag2 = Mock()
        mock_tag2.article_count.return_value = 1
        mock_tag2.names = {'ja': 'Aタグ', 'en': 'A Tag'}

        mock_faq_tag_class.list_all.return_value = [mock_tag1, mock_tag2]

        generator = MockFaqGeneratorBase('ja')
        sorted_tags = generator.get_sorted_tags()

        # Should be sorted by Japanese name
        assert len(sorted_tags) == 2
        assert sorted_tags[0] == mock_tag2  # 'Aタグ' comes first
        assert sorted_tags[1] == mock_tag1  # 'Zタグ' comes second

    @pytest.mark.parametrize("data", [
        {},
        {'any': 'data'},
        None,
    ])
    def test_validate_data_default(self, data):
        """Test default validation always returns True."""
        generator = MockFaqGeneratorBase('ja')
        assert generator.validate_data(data)


class TestFaqArticleGenerator:
    """Test FaqArticleGenerator class."""

    def test_init(self):
        """Test generator initialization."""
        generator = FaqArticleGenerator('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_items(self, mock_faq_class, mock_faq):
        """Test getting FAQ items."""
        mock_faq_class.list_all.return_value = [mock_faq]

        generator = FaqArticleGenerator('ja')
        items = generator.get_items()

        assert len(items) == 1
        assert items[0] == mock_faq

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_items_empty(self, mock_faq_class):
        """Test getting items with no FAQs."""
        mock_faq_class.list_all.return_value = []

        generator = FaqArticleGenerator('ja')
        items = generator.get_items()

        assert items == []

    def test_process_item(self, mock_faq):
        """Test processing a single FAQ article."""
        generator = FaqArticleGenerator('ja')
        result = generator.process_item(mock_faq)

        assert result['filename'] == 'test_faq'
        assert result['id'] == 'test_faq'
        assert result['title'] == 'Test FAQ'
        assert result['question'] == 'What is this?'
        assert result['answer'] == 'This is a test FAQ'

    @pytest.mark.parametrize("data,expected", [
        # Valid data
        ({
            'filename': 'test_faq',
            'title': 'Test FAQ'
        }, True),
        # Missing filename
        ({
            'title': 'Test FAQ'
        }, False),
        # Missing title
        ({
            'filename': 'test_faq'
        }, False),
    ])
    def test_validate_data(self, data, expected):
        """Test data validation with various inputs."""
        generator = FaqArticleGenerator('ja')
        assert generator.validate_data(data) == expected


class TestFaqIndexGenerator:
    """Test FaqIndexGenerator class."""

    def test_init(self):
        """Test generator initialization."""
        generator = FaqIndexGenerator('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_template_data(self, mock_faq_class, mock_faq):
        """Test template data generation."""
        mock_faq_class.list_all.return_value = [mock_faq]

        generator = FaqIndexGenerator('ja')
        generator.get_sorted_tags = Mock(return_value=[])

        data = generator.get_template_data()

        assert 'tags' in data
        assert 'articles' in data
        assert len(data['articles']) == 1
        mock_faq_class.list_all.assert_called_once_with(sort_by='date')

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_template_data_with_tags(self, mock_faq_class, mock_faq,
                                         mock_faq_tag):
        """Test template data generation with tags."""
        mock_faq_class.list_all.return_value = [mock_faq]

        generator = FaqIndexGenerator('ja')
        generator.get_sorted_tags = Mock(return_value=[mock_faq_tag])

        data = generator.get_template_data()

        assert 'tags' in data
        assert 'articles' in data
        assert len(data['tags']) == 1
        assert len(data['articles']) == 1

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_template_data_empty(self, mock_faq_class):
        """Test template data generation with no FAQs."""
        mock_faq_class.list_all.return_value = []

        generator = FaqIndexGenerator('ja')
        generator.get_sorted_tags = Mock(return_value=[])

        data = generator.get_template_data()

        assert 'tags' in data
        assert 'articles' in data
        assert data['tags'] == []
        assert data['articles'] == []


class TestFaqTagPageGenerator:
    """Test FaqTagPageGenerator class."""

    def test_init(self):
        """Test generator initialization."""
        generator = FaqTagPageGenerator('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None

    @patch('yaml2rst.generators.content_generators.faq_generator.FaqTag')
    def test_get_items(self, mock_faq_tag_class, mock_faq_tag,
                       mock_faq_tag_empty):
        """Test getting tag items with articles."""
        mock_faq_tag_class.list_all.return_value = [mock_faq_tag,
                                                    mock_faq_tag_empty]

        generator = FaqTagPageGenerator('ja')
        items = generator.get_items()

        # Should only include tags with articles
        assert len(items) == 1
        assert items[0] == mock_faq_tag

    @patch('yaml2rst.generators.content_generators.faq_generator.FaqTag')
    def test_get_items_empty(self, mock_faq_tag_class):
        """Test getting items with no tags."""
        mock_faq_tag_class.list_all.return_value = []

        generator = FaqTagPageGenerator('ja')
        items = generator.get_items()

        assert items == []

    def test_process_item(self, mock_faq_tag, mock_faq):
        """Test processing a single FAQ tag."""
        generator = FaqTagPageGenerator('ja')
        generator.relationship_manager.get_sorted_related_objects = Mock(
            return_value=[mock_faq])

        result = generator.process_item(mock_faq_tag)

        assert result['filename'] == 'test_tag'
        assert result['tag'] == 'test_tag'
        assert result['label'] == 'テストタグ'
        assert result['articles'] == ['test_faq']
        generator.relationship_manager.get_sorted_related_objects.\
            assert_called_once_with(mock_faq_tag, 'faq', key='sort_key')

    def test_process_item_no_articles(self, mock_faq_tag):
        """Test processing tag with no articles."""
        generator = FaqTagPageGenerator('ja')
        generator.relationship_manager.get_sorted_related_objects = Mock(
            return_value=[])

        result = generator.process_item(mock_faq_tag)

        assert result['filename'] == 'test_tag'
        assert result['tag'] == 'test_tag'
        assert result['label'] == 'テストタグ'
        assert result['articles'] == []

    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        generator = FaqTagPageGenerator('ja')

        valid_data = {
            'filename': 'test_tag',
            'tag': 'test_tag',
            'label': 'Test Tag',
            'articles': ['faq1', 'faq2']
        }

        assert generator.validate_data(valid_data) is True

    def test_validate_data_missing_fields(self):
        """Test data validation with missing required fields."""
        generator = FaqTagPageGenerator('ja')

        # Missing filename
        invalid_data1 = {
            'tag': 'test_tag',
            'label': 'Test Tag',
            'articles': []
        }
        assert generator.validate_data(invalid_data1) is False

        # Missing tag
        invalid_data2 = {
            'filename': 'test_tag',
            'label': 'Test Tag',
            'articles': []
        }
        assert generator.validate_data(invalid_data2) is False

        # Missing label
        invalid_data3 = {
            'filename': 'test_tag',
            'tag': 'test_tag',
            'articles': []
        }
        assert generator.validate_data(invalid_data3) is False

        # Missing articles
        invalid_data4 = {
            'filename': 'test_tag',
            'tag': 'test_tag',
            'label': 'Test Tag'
        }
        assert generator.validate_data(invalid_data4) is False


class TestFaqTagIndexGenerator:
    """Test FaqTagIndexGenerator class."""

    def test_init(self):
        """Test generator initialization."""
        generator = FaqTagIndexGenerator('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None

    def test_get_template_data(self, mock_faq_tag):
        """Test template data generation."""
        generator = FaqTagIndexGenerator('ja')
        generator.get_sorted_tags = Mock(return_value=[mock_faq_tag])

        data = generator.get_template_data()

        assert 'tags' in data
        assert len(data['tags']) == 1
        assert data['tags'][0] == mock_faq_tag.template_data.return_value

    def test_get_template_data_empty(self):
        """Test template data generation with no tags."""
        generator = FaqTagIndexGenerator('ja')
        generator.get_sorted_tags = Mock(return_value=[])

        data = generator.get_template_data()

        assert 'tags' in data
        assert data['tags'] == []

    @pytest.mark.parametrize("data,expected", [
        # Valid data with tags
        ({
            'tags': [
                {'id': 'tag1', 'name': 'Tag 1'},
                {'id': 'tag2', 'name': 'Tag 2'}
            ]
        }, True),
        # Valid data with empty tags
        ({
            'tags': []
        }, True),
        # Missing tags field
        ({
            'other_field': 'value'
        }, False),
        # Invalid tags type
        ({
            'tags': 'not_a_list'
        }, False),
    ])
    def test_validate_data(self, data, expected):
        """Test data validation with various inputs."""
        generator = FaqTagIndexGenerator('ja')
        assert generator.validate_data(data) == expected


class TestFaqArticleIndexGenerator:
    """Test FaqArticleIndexGenerator class."""

    def test_init(self):
        """Test generator initialization."""
        generator = FaqArticleIndexGenerator('ja')
        assert generator.lang == 'ja'
        assert generator.relationship_manager is not None

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_template_data(self, mock_faq_class, mock_faq):
        """Test template data generation."""
        mock_faq_class.list_all.return_value = [mock_faq]

        generator = FaqArticleIndexGenerator('ja')
        data = generator.get_template_data()

        assert 'articles' in data
        assert len(data['articles']) == 1
        assert data['articles'][0] == mock_faq.template_data.return_value
        mock_faq_class.list_all.assert_called_once_with(
            sort_by='sortKey')

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_template_data_empty(self, mock_faq_class):
        """Test template data generation with no articles."""
        mock_faq_class.list_all.return_value = []

        generator = FaqArticleIndexGenerator('ja')
        data = generator.get_template_data()

        assert 'articles' in data
        assert data['articles'] == []

    @patch('yaml2rst.generators.content_generators.faq_generator.Faq')
    def test_get_template_data_multiple(self, mock_faq_class):
        """Test template data generation with multiple articles."""
        mock_faq1 = Mock()
        mock_faq1.template_data.return_value = {'id': 'faq1', 'title': 'FAQ 1'}
        mock_faq2 = Mock()
        mock_faq2.template_data.return_value = {'id': 'faq2', 'title': 'FAQ 2'}

        mock_faq_class.list_all.return_value = [mock_faq1, mock_faq2]

        generator = FaqArticleIndexGenerator('ja')
        data = generator.get_template_data()

        assert 'articles' in data
        assert len(data['articles']) == 2
        assert data['articles'][0]['id'] == 'faq1'
        assert data['articles'][1]['id'] == 'faq2'

    @pytest.mark.parametrize("data,expected", [
        # Valid data with articles
        ({
            'articles': [
                {'id': 'faq1', 'title': 'FAQ 1'},
                {'id': 'faq2', 'title': 'FAQ 2'}
            ]
        }, True),
        # Valid data with empty articles
        ({
            'articles': []
        }, True),
        # Missing articles field
        ({
            'other_field': 'value'
        }, False),
        # Invalid articles type
        ({
            'articles': 'not_a_list'
        }, False),
    ])
    def test_validate_data(self, data, expected):
        """Test data validation with various inputs."""
        generator = FaqArticleIndexGenerator('ja')
        assert generator.validate_data(data) == expected
