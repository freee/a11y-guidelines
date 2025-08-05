"""Common test fixtures and configuration for yaml2rst tests."""
import pytest
import tempfile
import shutil
import sys
from pathlib import Path
from unittest.mock import Mock

from yaml2rst.template_manager import TemplateManager
from yaml2rst.generators.base_generator import GeneratorContext

# Add src directory to Python path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(autouse=True)
def setup_test_path():
    """Automatically setup Python path for all tests."""
    # This fixture runs automatically for all tests
    # Path is already set above, but this ensures consistency
    pass


@pytest.fixture
def mock_generator_base():
    """Base mock generator for common testing patterns."""
    mock_gen = Mock()
    mock_gen.lang = 'ja'
    mock_gen.generate.return_value = iter([
        {'filename': 'test', 'content': 'test content'}
    ])
    mock_gen.validate_data.return_value = True
    mock_gen.get_dependencies.return_value = []
    return mock_gen


@pytest.fixture
def mock_relationship_manager():
    """Mock relationship manager for generator tests."""
    mock_rm = Mock()
    mock_rm.get_sorted_related_objects.return_value = []
    mock_rm.get_related_objects.return_value = []
    return mock_rm


@pytest.fixture
def common_mock_patches():
    """Common patches used across multiple test files."""
    return {
        'config_patch': 'yaml2rst.yaml2rst.Config',
        'setup_instances_patch': 'yaml2rst.yaml2rst.setup_instances',
        'file_generator_patch': 'yaml2rst.yaml2rst.FileGenerator',
        'makedirs_patch': 'os.makedirs',
        'category_list_patch': (
            'yaml2rst.generators.content_generators.'
            'category_generator.Category.list_all'
        ),
        'relationship_manager_patch': (
            'freee_a11y_gl.relationship_manager.RelationshipManager'
        )
    }


@pytest.fixture
def mock_patch_helper():
    """Helper for standardized mock patching patterns."""
    from unittest.mock import patch, Mock

    def create_mock_with_patches(patches_dict):
        """Create a context manager with multiple patches."""
        mocks = {}
        patch_objects = []

        for name, target in patches_dict.items():
            mock_obj = Mock()
            patch_obj = patch(target, mock_obj)
            patch_objects.append(patch_obj)
            mocks[name] = mock_obj

        class MockContext:
            def __enter__(self):
                for patch_obj in patch_objects:
                    patch_obj.__enter__()
                return mocks

            def __exit__(self, exc_type, exc_val, exc_tb):
                for patch_obj in reversed(patch_objects):
                    patch_obj.__exit__(exc_type, exc_val, exc_tb)

        return MockContext()

    return create_mock_with_patches


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_settings():
    """Sample settings for testing."""
    return {
        'build_all': True,
        'targets': [],
        'lang': 'ja',
        'basedir': '/test/basedir'
    }


@pytest.fixture
def mock_templates():
    """Mock templates dictionary."""
    mock_template = Mock(spec=TemplateManager)
    mock_template.write_rst = Mock()

    return {
        'category_page': mock_template,
        'allchecks_text': mock_template,
        'tool_example': mock_template,
        'faq_article': mock_template,
        'faq_tagpage': mock_template,
        'faq_index': mock_template,
        'faq_tag_index': mock_template,
        'faq_article_index': mock_template,
        'info_to_gl': mock_template,
        'info_to_faq': mock_template,
        'wcag21mapping': mock_template,
        'priority_diff': mock_template,
        'miscdefs': mock_template,
        'axe_rules': mock_template,
        'makefile': mock_template
    }


@pytest.fixture
def generator_context():
    """Sample generator context."""
    return GeneratorContext(
        lang='ja',
        base_dir=Path('/test/basedir')
    )


@pytest.fixture
def sample_dest_dirs():
    """Sample destination directories."""
    return {
        'guidelines': '/test/output/categories',
        'checks': '/test/output/checks/examples',
        'faq_articles': '/test/output/faq',
        'faq_tags': '/test/output/faq/tags',
        'info2gl': '/test/output/info',
        'info2faq': '/test/output/info'
    }


@pytest.fixture
def sample_static_files():
    """Sample static file paths."""
    return {
        'all_checks': '/test/output/checks/checklist.rst',
        'faq_index': '/test/output/faq/index.rst',
        'faq_tag_index': '/test/output/faq/tags/index.rst',
        'faq_article_index': '/test/output/faq/articles/index.rst',
        'wcag21mapping': '/test/output/info/wcag21-mapping.rst',
        'priority_diff': '/test/output/info/priority.rst',
        'miscdefs': '/test/output/inc/miscdefs.txt',
        'axe_rules': '/test/output/info/axe-rules.rst',
        'makefile': '/test/output/Makefile'
    }


@pytest.fixture
def mock_freee_a11y_gl():
    """Mock freee_a11y_gl module."""
    with pytest.MonkeyPatch().context() as m:
        mock_config = Mock()
        mock_config.initialize = Mock()

        mock_setup = Mock()

        m.setattr("yaml2rst.yaml2rst.Config", mock_config)
        m.setattr("yaml2rst.yaml2rst.setup_instances", mock_setup)

        yield {
            'config': mock_config,
            'setup_instances': mock_setup
        }


@pytest.fixture
def capture_logs(caplog):
    """Capture logs for testing."""
    return caplog


@pytest.fixture
def mock_generator_class():
    """Mock generator class."""
    mock_class = Mock()
    mock_instance = Mock()
    mock_instance.generate.return_value = [
        {'filename': 'test', 'content': 'test content'}
    ]
    mock_class.return_value = mock_instance
    return mock_class


# Test data fixtures - consolidated
@pytest.fixture
def sample_test_data():
    """Consolidated sample data for testing."""
    return {
        'guideline': {
            'id': 'gl_001',
            'title': 'Sample Guideline',
            'description': 'This is a sample guideline for testing',
            'priority': 'high',
            'category': 'accessibility',
            'checks': ['check_001', 'check_002'],
            'filename': 'sample_guideline'
        },
        'faq': {
            'id': 'faq_001',
            'title': 'Sample FAQ',
            'question': 'What is accessibility?',
            'answer': (
                'Accessibility is the practice of making websites usable by '
                'everyone.'
            ),
            'tags': ['accessibility', 'basics'],
            'filename': 'sample_faq'
        },
        'check': {
            'id': 'check_001',
            'title': 'Sample Check',
            'description': 'This is a sample check for testing',
            'procedure': 'Follow these steps to perform the check',
            'implementation': 'Implementation details here',
            'filename': 'sample_check'
        }
    }
