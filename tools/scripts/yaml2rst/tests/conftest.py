"""Common test fixtures and configuration for yaml2rst tests."""
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import sys
import os

# Add src directory to Python path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from yaml2rst.template_manager import TemplateManager
from yaml2rst.generators.base_generator import GeneratorContext


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_yaml_content():
    """Sample YAML content for testing."""
    return {
        'id': 'test_001',
        'title': 'Test Guideline',
        'description': 'This is a test guideline',
        'priority': 'high',
        'category': 'test_category'
    }


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
def mock_file_system(temp_dir):
    """Mock file system with test data."""
    # Create test YAML files
    yaml_dir = temp_dir / "data" / "yaml"
    yaml_dir.mkdir(parents=True)
    
    # Sample guideline YAML
    gl_dir = yaml_dir / "gl" / "test_category"
    gl_dir.mkdir(parents=True)
    (gl_dir / "test_guideline.yaml").write_text("""
id: test_001
title: Test Guideline
description: This is a test guideline
priority: high
category: test_category
""")
    
    # Sample FAQ YAML
    faq_dir = yaml_dir / "faq"
    faq_dir.mkdir(parents=True)
    (faq_dir / "test_faq.yaml").write_text("""
id: faq_001
title: Test FAQ
question: What is this?
answer: This is a test FAQ
tags: [test, sample]
""")
    
    # Sample check YAML
    check_dir = yaml_dir / "checks" / "test"
    check_dir.mkdir(parents=True)
    (check_dir / "test_check.yaml").write_text("""
id: check_001
title: Test Check
description: This is a test check
procedure: Test procedure
implementation: Test implementation
""")
    
    return temp_dir


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


class MockGenerator:
    """Mock generator for testing."""
    
    def __init__(self, lang, data_to_yield=None):
        self.lang = lang
        self.data_to_yield = data_to_yield or [{'filename': 'test', 'content': 'test content'}]
    
    def generate(self):
        """Generate mock data."""
        for item in self.data_to_yield:
            yield item


@pytest.fixture
def mock_generator_class():
    """Mock generator class."""
    mock_class = Mock()
    mock_instance = Mock()
    mock_instance.generate.return_value = [{'filename': 'test', 'content': 'test content'}]
    mock_class.return_value = mock_instance
    return mock_class


# Test data fixtures
@pytest.fixture
def sample_guideline_data():
    """Sample guideline data."""
    return {
        'id': 'gl_001',
        'title': 'Sample Guideline',
        'description': 'This is a sample guideline for testing',
        'priority': 'high',
        'category': 'accessibility',
        'checks': ['check_001', 'check_002'],
        'filename': 'sample_guideline'
    }


@pytest.fixture
def sample_faq_data():
    """Sample FAQ data."""
    return {
        'id': 'faq_001',
        'title': 'Sample FAQ',
        'question': 'What is accessibility?',
        'answer': 'Accessibility is the practice of making websites usable by everyone.',
        'tags': ['accessibility', 'basics'],
        'filename': 'sample_faq'
    }


@pytest.fixture
def sample_check_data():
    """Sample check data."""
    return {
        'id': 'check_001',
        'title': 'Sample Check',
        'description': 'This is a sample check for testing',
        'procedure': 'Follow these steps to perform the check',
        'implementation': 'Implementation details here',
        'filename': 'sample_check'
    }
