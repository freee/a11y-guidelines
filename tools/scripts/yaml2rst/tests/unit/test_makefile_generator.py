"""Tests for makefile generator module."""
import pytest
from unittest.mock import Mock, patch

from yaml2rst.generators.content_generators.makefile_generator import (
    MakefileGenerator, MakefileConfig
)


@pytest.fixture
def sample_makefile_config():
    """Sample makefile configuration."""
    return MakefileConfig(
        dest_dirs={
            'guidelines': '/test/categories',
            'checks': '/test/checks/examples',
            'faq_articles': '/test/faq',
            'faq_tags': '/test/faq/tags',
            'info2gl': '/test/info',
            'info2faq': '/test/info'
        },
        makefile_vars={
            'SPHINX_BUILD': 'sphinx-build',
            'BUILDDIR': 'build'
        },
        base_vars={
            'SOURCEDIR': 'source',
            'ALLSPHINXOPTS': ('-d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) '
                              '$(SPHINXOPTS) .')
        },
        vars_list={
            'targets': ['html', 'pdf'],
            'languages': ['ja', 'en']
        }
    )


@pytest.fixture
def mock_category():
    """Mock Category object."""
    mock_cat = Mock()
    mock_cat.id = 'test_category'
    mock_cat.get_dependency.return_value = [
        'data/yaml/gl/test_category/test.yaml']
    return mock_cat


@pytest.fixture
def mock_checktool():
    """Mock CheckTool object."""
    mock_tool = Mock()
    mock_tool.id = 'test_tool'
    mock_tool.get_dependency.return_value = ['data/yaml/checks/test_tool.yaml']
    return mock_tool


@pytest.fixture
def mock_faq():
    """Mock Faq object."""
    mock_faq = Mock()
    mock_faq.id = 'test_faq'
    mock_faq.get_dependency.return_value = ['data/yaml/faq/test_faq.yaml']
    return mock_faq


@pytest.fixture
def mock_faq_tag():
    """Mock FaqTag object."""
    mock_tag = Mock()
    mock_tag.id = 'test_tag'
    mock_tag.article_count.return_value = 2
    return mock_tag


@pytest.fixture
def mock_faq_tag_empty():
    """Mock FaqTag object with no articles."""
    mock_tag = Mock()
    mock_tag.id = 'empty_tag'
    mock_tag.article_count.return_value = 0
    return mock_tag


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
    mock_info.src_path = 'data/json/info.json'
    return mock_info


class TestMakefileConfig:
    """Test MakefileConfig dataclass."""

    def test_makefile_config_creation(self, sample_makefile_config):
        """Test MakefileConfig creation."""
        config = sample_makefile_config
        assert config.dest_dirs['guidelines'] == '/test/categories'
        assert config.makefile_vars['SPHINX_BUILD'] == 'sphinx-build'
        assert config.base_vars['SOURCEDIR'] == 'source'
        assert config.vars_list['targets'] == ['html', 'pdf']


class TestMakefileGenerator:
    """Test MakefileGenerator class."""

    def test_init(self, sample_makefile_config):
        """Test generator initialization."""
        generator = MakefileGenerator('ja', sample_makefile_config)
        assert generator.lang == 'ja'
        assert generator.config == sample_makefile_config
        assert generator.relationship_manager is not None

    @patch('yaml2rst.generators.content_generators.makefile_generator.Check')
    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'Guideline')
    @patch('yaml2rst.generators.content_generators.makefile_generator.Faq')
    def test_get_template_data_basic(self, mock_faq_class,
                                     mock_guideline_class,
                                     mock_check_class, sample_makefile_config):
        """Test basic template data generation."""
        # Mock the class methods
        mock_check_class.list_all_src_paths.return_value = [
            'check1.yaml', 'check2.yaml']
        mock_guideline_class.list_all_src_paths.return_value = [
            'gl1.yaml', 'gl2.yaml']
        mock_faq_class.list_all_src_paths.return_value = [
            'faq1.yaml', 'faq2.yaml']

        generator = MakefileGenerator('ja', sample_makefile_config)

        # Mock the processing methods to return empty results
        generator._process_category_targets = Mock(
            return_value=([], []))
        generator._process_checktool_targets = Mock(
            return_value=([], []))
        generator._process_faq_targets = Mock(
            return_value=([], [], []))
        generator._process_info_targets = Mock(
            return_value=([], [], []))

        data = generator.get_template_data()

        assert 'check_yaml' in data
        assert 'gl_yaml' in data
        assert 'faq_yaml' in data
        assert 'depends' in data
        assert data['check_yaml'] == 'check1.yaml check2.yaml'
        assert data['gl_yaml'] == 'gl1.yaml gl2.yaml'
        assert data['faq_yaml'] == 'faq1.yaml faq2.yaml'

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'Category')
    def test_process_category_targets(self, mock_category_class,
                                      sample_makefile_config, mock_category):
        """Test category target processing."""
        mock_category_class.list_all.return_value = [mock_category]

        generator = MakefileGenerator('ja', sample_makefile_config)
        result = generator._process_category_targets()
        build_depends, category_targets = result

        assert len(build_depends) == 1
        assert len(category_targets) == 1
        assert (build_depends[0]['target'] ==
                '/test/categories/test_category.rst')
        assert (build_depends[0]['depends'] ==
                'data/yaml/gl/test_category/test.yaml')
        expected = '/test/categories/test_category.rst'
        assert category_targets[0] == expected

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'Category')
    def test_process_category_targets_duplicates(self, mock_category_class,
                                                 sample_makefile_config):
        """Test category target processing with duplicate targets."""
        # Create two categories with same ID (edge case)
        mock_cat1 = Mock()
        mock_cat1.id = 'same_category'
        mock_cat1.get_dependency.return_value = ['dep1.yaml']

        mock_cat2 = Mock()
        mock_cat2.id = 'same_category'
        mock_cat2.get_dependency.return_value = ['dep2.yaml']

        mock_category_class.list_all.return_value = [
            mock_cat1, mock_cat2]

        generator = MakefileGenerator('ja', sample_makefile_config)
        build_depends, category_targets = (
            generator._process_category_targets())

        # Should only have one target due to duplicate filtering
        assert len(category_targets) == 1
        assert len(build_depends) == 1

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'CheckTool')
    def test_process_checktool_targets(self, mock_checktool_class,
                                       sample_makefile_config, mock_checktool):
        """Test checktool target processing."""
        mock_checktool_class.list_all.return_value = [mock_checktool]

        generator = MakefileGenerator('ja', sample_makefile_config)
        build_depends, checktool_targets = (
            generator._process_checktool_targets())

        assert len(build_depends) == 1
        assert len(checktool_targets) == 1
        assert (build_depends[0]['target'] ==
                '/test/checks/examples/examples-test_tool.rst')
        assert (build_depends[0]['depends'] ==
                'data/yaml/checks/test_tool.yaml')
        assert (checktool_targets[0] ==
                '/test/checks/examples/examples-test_tool.rst')

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'CheckTool')
    def test_process_checktool_targets_duplicates(self, mock_checktool_class,
                                                  sample_makefile_config):
        """Test checktool target processing with duplicates."""
        mock_tool1 = Mock()
        mock_tool1.id = 'same_tool'
        mock_tool1.get_dependency.return_value = ['dep1.yaml']

        mock_tool2 = Mock()
        mock_tool2.id = 'same_tool'
        mock_tool2.get_dependency.return_value = ['dep2.yaml']

        mock_checktool_class.list_all.return_value = [
            mock_tool1, mock_tool2]

        generator = MakefileGenerator('ja', sample_makefile_config)
        build_depends, checktool_targets = (
            generator._process_checktool_targets())

        # Should only have one target due to duplicate filtering
        assert len(checktool_targets) == 1
        assert len(build_depends) == 1

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'FaqTag')
    @patch('yaml2rst.generators.content_generators.makefile_generator.Faq')
    def test_process_faq_targets(self, mock_faq_class, mock_faq_tag_class,
                                 sample_makefile_config, mock_faq,
                                 mock_faq_tag):
        """Test FAQ target processing."""
        mock_faq_class.list_all.return_value = [mock_faq]
        mock_faq_tag_class.list_all.return_value = [mock_faq_tag]

        generator = MakefileGenerator('ja', sample_makefile_config)
        generator.relationship_manager.get_sorted_related_objects = Mock(
            return_value=[mock_faq])

        build_depends, article_targets, tagpage_targets = (
            generator._process_faq_targets())

        assert len(build_depends) == 2  # One for article, one for tag page
        assert len(article_targets) == 1
        assert len(tagpage_targets) == 1
        assert article_targets[0] == '/test/faq/test_faq.rst'
        assert tagpage_targets[0] == '/test/faq/tags/test_tag.rst'

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'FaqTag')
    @patch('yaml2rst.generators.content_generators.makefile_generator.Faq')
    def test_process_faq_targets_empty_tag(self, mock_faq_class,
                                           mock_faq_tag_class,
                                           sample_makefile_config, mock_faq,
                                           mock_faq_tag_empty):
        """Test FAQ target processing with empty tag (no articles)."""
        mock_faq_class.list_all.return_value = [mock_faq]
        mock_faq_tag_class.list_all.return_value = [
            mock_faq_tag_empty]

        generator = MakefileGenerator('ja', sample_makefile_config)
        build_depends, article_targets, tagpage_targets = (
            generator._process_faq_targets())

        # Should have article but no tag page (empty tag skipped)
        assert len(article_targets) == 1
        assert len(tagpage_targets) == 0
        assert len(build_depends) == 1  # Only article dependency

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'FaqTag')
    @patch('yaml2rst.generators.content_generators.makefile_generator.Faq')
    def test_process_faq_targets_duplicates(self, mock_faq_class,
                                            mock_faq_tag_class,
                                            sample_makefile_config):
        """Test FAQ target processing with duplicate targets."""
        mock_faq1 = Mock()
        mock_faq1.id = 'same_faq'
        mock_faq1.get_dependency.return_value = ['dep1.yaml']

        mock_faq2 = Mock()
        mock_faq2.id = 'same_faq'
        mock_faq2.get_dependency.return_value = ['dep2.yaml']

        mock_tag1 = Mock()
        mock_tag1.id = 'same_tag'
        mock_tag1.article_count.return_value = 1

        mock_tag2 = Mock()
        mock_tag2.id = 'same_tag'
        mock_tag2.article_count.return_value = 1

        mock_faq_class.list_all.return_value = [mock_faq1, mock_faq2]
        mock_faq_tag_class.list_all.return_value = [mock_tag1, mock_tag2]

        generator = MakefileGenerator('ja', sample_makefile_config)
        generator.relationship_manager.get_sorted_related_objects = Mock(
            return_value=[mock_faq1])

        build_depends, article_targets, tagpage_targets = (
            generator._process_faq_targets())

        # Should only have one of each due to duplicate filtering
        assert len(article_targets) == 1
        assert len(tagpage_targets) == 1

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'InfoRef')
    def test_process_info_targets_guidelines(self, mock_info_class,
                                             sample_makefile_config,
                                             mock_info_ref):
        """Test info target processing for guidelines."""
        mock_guideline = Mock()
        mock_guideline.src_path = 'gl_src.yaml'

        mock_info_class.list_has_guidelines.return_value = [mock_info_ref]
        mock_info_class.list_has_faqs.return_value = []

        generator = MakefileGenerator('ja', sample_makefile_config)
        generator.relationship_manager.get_sorted_related_objects = Mock(
            return_value=[mock_guideline])

        build_depends, info_to_gl_targets, info_to_faq_targets = (
            generator._process_info_targets())

        assert len(build_depends) == 1
        assert len(info_to_gl_targets) == 1
        assert len(info_to_faq_targets) == 0
        expected = '/test/info/test_ref.rst'
        assert info_to_gl_targets[0] == expected
        assert build_depends[0]['depends'] == 'gl_src.yaml'

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'InfoRef')
    def test_process_info_targets_faqs(self, mock_info_class,
                                       sample_makefile_config, mock_info_ref):
        """Test info target processing for FAQs."""
        mock_faq = Mock()
        mock_faq.src_path = 'faq_src.yaml'

        mock_info_class.list_has_guidelines.return_value = []
        mock_info_class.list_has_faqs.return_value = [mock_info_ref]

        generator = MakefileGenerator('ja', sample_makefile_config)
        generator.relationship_manager.get_sorted_related_objects = Mock(
            return_value=[mock_faq])

        build_depends, info_to_gl_targets, info_to_faq_targets = (
            generator._process_info_targets())

        assert len(build_depends) == 1
        assert len(info_to_gl_targets) == 0
        assert len(info_to_faq_targets) == 1
        expected = '/test/info/test_ref.rst'
        assert info_to_faq_targets[0] == expected
        assert build_depends[0]['depends'] == 'faq_src.yaml'

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'InfoRef')
    def test_process_info_targets_external_skipped(self, mock_info_class,
                                                   sample_makefile_config,
                                                   mock_info_ref_external):
        """Test that external info references are skipped."""
        mock_info_class.list_has_guidelines.return_value = [
            mock_info_ref_external]
        mock_info_class.list_has_faqs.return_value = [
            mock_info_ref_external]

        generator = MakefileGenerator('ja', sample_makefile_config)
        build_depends, info_to_gl_targets, info_to_faq_targets = (
            generator._process_info_targets())

        # External refs should be skipped
        assert len(build_depends) == 0
        assert len(info_to_gl_targets) == 0
        assert len(info_to_faq_targets) == 0

    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'InfoRef')
    def test_process_info_targets_duplicates(self, mock_info_class,
                                             sample_makefile_config):
        """Test info target processing with duplicates."""
        mock_info1 = Mock()
        mock_info1.ref = 'same_ref'
        mock_info1.internal = True

        mock_info2 = Mock()
        mock_info2.ref = 'same_ref'
        mock_info2.internal = True

        mock_guideline = Mock()
        mock_guideline.src_path = 'gl_src.yaml'

        mock_info_class.list_has_guidelines.return_value = [
            mock_info1, mock_info2]
        mock_info_class.list_has_faqs.return_value = []

        generator = MakefileGenerator('ja', sample_makefile_config)
        generator.relationship_manager.get_sorted_related_objects = Mock(
            return_value=[mock_guideline])

        build_depends, info_to_gl_targets, info_to_faq_targets = (
            generator._process_info_targets())

        # Should only have one target due to duplicate filtering
        assert len(info_to_gl_targets) == 1
        assert len(build_depends) == 1

    @pytest.mark.parametrize("data,expected", [
        # Valid data case
        ({
            'depends': [
                {'target': 'test.rst', 'depends': 'test.yaml'}
            ],
            'gl_yaml': 'gl1.yaml gl2.yaml',
            'check_yaml': 'check1.yaml',
            'faq_yaml': 'faq1.yaml'
        }, True),
        # Missing 'depends' field
        ({
            'gl_yaml': 'gl1.yaml',
            'check_yaml': 'check1.yaml',
            'faq_yaml': 'faq1.yaml'
        }, False),
        # Missing 'gl_yaml' field
        ({
            'depends': [],
            'check_yaml': 'check1.yaml',
            'faq_yaml': 'faq1.yaml'
        }, False),
        # Invalid depends type
        ({
            'depends': 'not_a_list',
            'gl_yaml': 'gl1.yaml',
            'check_yaml': 'check1.yaml',
            'faq_yaml': 'faq1.yaml'
        }, False),
        # Missing 'target' in dependency
        ({
            'depends': [
                {'depends': 'test.yaml'}  # Missing 'target'
            ],
            'gl_yaml': 'gl1.yaml',
            'check_yaml': 'check1.yaml',
            'faq_yaml': 'faq1.yaml'
        }, False),
        # Missing 'depends' in dependency
        ({
            'depends': [
                {'target': 'test.rst'}  # Missing 'depends'
            ],
            'gl_yaml': 'gl1.yaml',
            'check_yaml': 'check1.yaml',
            'faq_yaml': 'faq1.yaml'
        }, False),
        # Non-dict in depends list
        ({
            'depends': [
                'not_a_dict'
            ],
            'gl_yaml': 'gl1.yaml',
            'check_yaml': 'check1.yaml',
            'faq_yaml': 'faq1.yaml'
        }, False),
    ])
    def test_validate_data_makefile(self, data, expected,
                                    sample_makefile_config):
        """Test MakefileGenerator data validation with various inputs."""
        generator = MakefileGenerator('ja', sample_makefile_config)
        assert generator.validate_data(data) == expected

    @patch('yaml2rst.generators.content_generators.makefile_generator.Check')
    @patch('yaml2rst.generators.content_generators.makefile_generator.'
           'Guideline')
    @patch('yaml2rst.generators.content_generators.makefile_generator.Faq')
    def test_generate_success(self, mock_faq_class, mock_guideline_class,
                              mock_check_class, sample_makefile_config):
        """Test successful generate method execution."""
        # Mock the class methods
        mock_check_class.list_all_src_paths.return_value = [
            'check1.yaml']
        mock_guideline_class.list_all_src_paths.return_value = [
            'gl1.yaml']
        mock_faq_class.list_all_src_paths.return_value = ['faq1.yaml']

        generator = MakefileGenerator('ja', sample_makefile_config)

        # Mock the processing methods to return valid data
        generator._process_category_targets = Mock(
            return_value=([], []))
        generator._process_checktool_targets = Mock(
            return_value=([], []))
        generator._process_faq_targets = Mock(
            return_value=([], [], []))
        generator._process_info_targets = Mock(
            return_value=([], [], []))

        # Execute generate method
        results = list(generator.generate())

        # Should yield one result
        assert len(results) == 1
        result = results[0]

        # Verify the result contains expected fields
        assert 'check_yaml' in result
        assert 'gl_yaml' in result
        assert 'faq_yaml' in result
        assert 'depends' in result
        assert result['check_yaml'] == 'check1.yaml'
        assert result['gl_yaml'] == 'gl1.yaml'
        assert result['faq_yaml'] == 'faq1.yaml'

    def test_generate_with_exception(self, sample_makefile_config):
        """Test generate method with exception handling."""
        generator = MakefileGenerator('ja', sample_makefile_config)

        # Mock get_template_data to raise an exception
        generator.get_template_data = Mock(
            side_effect=Exception("Test error"))

        # Should raise the exception
        with pytest.raises(Exception, match="Test error"):
            list(generator.generate())

    def test_generate_with_invalid_data(self, sample_makefile_config):
        """Test generate method with invalid data that fails validation."""
        generator = MakefileGenerator('ja', sample_makefile_config)

        # Mock get_template_data to return invalid data
        invalid_data = {
            'depends': 'not_a_list',  # Invalid - should be list
            'gl_yaml': 'gl1.yaml',
            'check_yaml': 'check1.yaml',
            'faq_yaml': 'faq1.yaml'
        }
        generator.get_template_data = Mock(return_value=invalid_data)

        # Should not yield anything due to validation failure
        results = list(generator.generate())
        assert len(results) == 0
