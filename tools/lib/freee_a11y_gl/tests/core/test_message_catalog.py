import pytest
import tempfile
import yaml
from pathlib import Path
from freee_a11y_gl.message_catalog import MessageCatalog


from unittest.mock import patch, MagicMock


class TestMessageCatalog:
    """Test cases for MessageCatalog class."""

    def test_init_default(self):
        """Test MessageCatalog initialization with defaults."""
        catalog = MessageCatalog()

        assert catalog.severity_tags == {}
        assert catalog.check_targets == {}
        assert catalog.check_tools == {}
        assert catalog.platform_names == {}
        assert catalog.separators == {}
        assert catalog.conjunctions == {}
        assert catalog.pass_texts == {}
        assert catalog.date_formats == {}

    def test_init_with_data(self):
        """Test MessageCatalog initialization with data."""
        data = {
            'severity_tags': {'minor': {'ja': '軽微', 'en': 'MINOR'}},
            'check_targets': {'design': {'ja': 'デザイン', 'en': 'Design'}},
            'platform_names': {'web': {'ja': 'Web', 'en': 'Web'}}
        }

        catalog = MessageCatalog(**data)

        assert catalog.severity_tags == data['severity_tags']
        assert catalog.check_targets == data['check_targets']
        assert catalog.platform_names == data['platform_names']

    def test_load_from_file_success(self):
        """Test successful loading from file."""
        test_data = {
            'severity_tags': {'minor': {'ja': '軽微', 'en': 'MINOR'}},
            'check_targets': {'design': {'ja': 'デザイン', 'en': 'Design'}}
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            temp_path = Path(f.name)

        try:
            catalog = MessageCatalog.load_from_file(temp_path)
            assert catalog.severity_tags == test_data['severity_tags']
            assert catalog.check_targets == test_data['check_targets']
        finally:
            temp_path.unlink()

    def test_load_from_file_not_found(self):
        """Test loading from non-existent file."""
        non_existent_path = Path("/non/existent/file.yaml")

        with pytest.raises(FileNotFoundError, match="Message catalog file not found"):
            MessageCatalog.load_from_file(non_existent_path)

    def test_load_from_file_invalid_yaml(self):
        """Test loading from file with invalid YAML."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            temp_path = Path(f.name)

        try:
            with pytest.raises(yaml.YAMLError):
                MessageCatalog.load_from_file(temp_path)
        finally:
            temp_path.unlink()

    def test_load_from_file_empty_file(self):
        """Test loading from empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("")
            temp_path = Path(f.name)

        try:
            catalog = MessageCatalog.load_from_file(temp_path)
            assert catalog.severity_tags == {}
        finally:
            temp_path.unlink()

    def test_load_with_fallback_primary_success(self):
        """Test load_with_fallback using primary path successfully."""
        test_data = {'severity_tags': {'minor': {'ja': '軽微'}}}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            primary_path = Path(f.name)

        try:
            catalog = MessageCatalog.load_with_fallback(primary_path=primary_path)
            assert catalog.severity_tags == test_data['severity_tags']
        finally:
            primary_path.unlink()

    def test_load_with_fallback_fallback_success(self):
        """Test load_with_fallback using fallback path."""
        test_data = {'check_targets': {'design': {'ja': 'デザイン'}}}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            fallback_path = Path(f.name)

        try:
            non_existent = Path("/non/existent/primary.yaml")
            catalog = MessageCatalog.load_with_fallback(
                primary_path=non_existent,
                fallback_path=fallback_path
            )
            assert catalog.check_targets == test_data['check_targets']
        finally:
            fallback_path.unlink()

    @patch('freee_a11y_gl.message_catalog.MessageCatalog.load_from_package_resource')
    def test_load_with_fallback_package_resource(self, mock_load_resource):
        """Test load_with_fallback using package resource."""
        mock_catalog = MessageCatalog(severity_tags={'test': {'ja': 'テスト'}})
        mock_load_resource.return_value = mock_catalog

        non_existent = Path("/non/existent/file.yaml")
        catalog = MessageCatalog.load_with_fallback(
            primary_path=non_existent,
            fallback_path=non_existent
        )

        mock_load_resource.assert_called_once()
        assert catalog.severity_tags == {'test': {'ja': 'テスト'}}

    @patch('freee_a11y_gl.message_catalog.MessageCatalog.load_from_package_resource')
    def test_load_with_fallback_all_fail(self, mock_load_resource):
        """Test load_with_fallback when all methods fail."""
        mock_load_resource.side_effect = Exception("Resource not found")

        non_existent = Path("/non/existent/file.yaml")
        catalog = MessageCatalog.load_with_fallback(
            primary_path=non_existent,
            fallback_path=non_existent
        )

        # Should return default instance
        assert catalog.severity_tags == {}

    def test_load_with_fallback_primary_invalid_yaml(self):
        """Test load_with_fallback with invalid YAML in primary file."""
        test_data = {'check_targets': {'design': {'ja': 'デザイン'}}}

        # Create invalid primary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: [")
            primary_path = Path(f.name)

        # Create valid fallback file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            fallback_path = Path(f.name)

        try:
            catalog = MessageCatalog.load_with_fallback(
                primary_path=primary_path,
                fallback_path=fallback_path
            )
            assert catalog.check_targets == test_data['check_targets']
        finally:
            primary_path.unlink()
            fallback_path.unlink()

    @patch('freee_a11y_gl.message_catalog.resources')
    def test_load_from_package_resource_success(self, mock_resources):
        """Test loading from package resource successfully."""
        test_data = {'severity_tags': {'minor': {'ja': '軽微'}}}

        # Mock the resources.files() chain
        mock_files = MagicMock()
        mock_message_file = MagicMock()
        mock_message_file.is_file.return_value = True
        mock_message_file.read_text.return_value = yaml.dump(test_data)
        mock_files.__truediv__.return_value = mock_message_file
        mock_resources.files.return_value = mock_files

        catalog = MessageCatalog.load_from_package_resource()

        mock_resources.files.assert_called_once_with("freee_a11y_gl.data")
        mock_files.__truediv__.assert_called_once_with("messages.yaml")
        assert catalog.severity_tags == test_data['severity_tags']

    @patch('freee_a11y_gl.message_catalog.resources')
    def test_load_from_package_resource_file_not_found(self, mock_resources):
        """Test loading from package resource when file doesn't exist."""
        mock_files = MagicMock()
        mock_message_file = MagicMock()
        mock_message_file.is_file.return_value = False
        mock_files.__truediv__.return_value = mock_message_file
        mock_resources.files.return_value = mock_files

        with pytest.raises(FileNotFoundError, match="messages.yaml not found in package resources"):
            MessageCatalog.load_from_package_resource()

    @patch('freee_a11y_gl.message_catalog.resources')
    def test_load_from_package_resource_module_not_found(self, mock_resources):
        """Test loading from package resource when module is not found."""
        mock_resources.files.side_effect = ModuleNotFoundError("Module not found")

        with pytest.raises(FileNotFoundError, match="Message catalog resource not found"):
            MessageCatalog.load_from_package_resource()

    def test_get_severity_tag_success(self):
        """Test successful severity tag retrieval."""
        catalog = MessageCatalog(
            severity_tags={'minor': {'ja': '軽微', 'en': 'MINOR'}}
        )

        assert catalog.get_severity_tag('minor', 'ja') == '軽微'
        assert catalog.get_severity_tag('minor', 'en') == 'MINOR'

    def test_get_severity_tag_missing_severity(self):
        """Test severity tag retrieval with missing severity."""
        catalog = MessageCatalog()

        assert catalog.get_severity_tag('nonexistent', 'ja') == 'nonexistent'

    def test_get_severity_tag_missing_language(self):
        """Test severity tag retrieval with missing language."""
        catalog = MessageCatalog(
            severity_tags={'minor': {'ja': '軽微'}}
        )

        assert catalog.get_severity_tag('minor', 'fr') == 'minor'

    def test_get_severity_tag_default_language(self):
        """Test severity tag retrieval with default language."""
        catalog = MessageCatalog(
            severity_tags={'minor': {'ja': '軽微', 'en': 'MINOR'}}
        )

        assert catalog.get_severity_tag('minor') == '軽微'

    def test_get_check_target_success(self):
        """Test successful check target retrieval."""
        catalog = MessageCatalog(
            check_targets={'design': {'ja': 'デザイン', 'en': 'Design'}}
        )

        assert catalog.get_check_target('design', 'ja') == 'デザイン'
        assert catalog.get_check_target('design', 'en') == 'Design'

    def test_get_check_target_missing(self):
        """Test check target retrieval with missing target."""
        catalog = MessageCatalog()

        assert catalog.get_check_target('nonexistent', 'ja') == 'nonexistent'

    def test_get_check_tool_success(self):
        """Test successful check tool retrieval."""
        catalog = MessageCatalog(
            check_tools={'axe': {'ja': 'axe-core', 'en': 'axe-core'}}
        )

        assert catalog.get_check_tool('axe', 'ja') == 'axe-core'
        assert catalog.get_check_tool('axe', 'en') == 'axe-core'

    def test_get_check_tool_missing(self):
        """Test check tool retrieval with missing tool."""
        catalog = MessageCatalog()

        assert catalog.get_check_tool('nonexistent', 'ja') == 'nonexistent'

    def test_get_platform_name_success(self):
        """Test successful platform name retrieval."""
        catalog = MessageCatalog(
            platform_names={'web': {'ja': 'Web', 'en': 'Web'}, 'mobile': {'ja': 'モバイル', 'en': 'Mobile'}}
        )

        assert catalog.get_platform_name('web', 'ja') == 'Web'
        assert catalog.get_platform_name('mobile', 'ja') == 'モバイル'
        assert catalog.get_platform_name('mobile', 'en') == 'Mobile'

    def test_get_platform_name_missing(self):
        """Test platform name retrieval with missing platform."""
        catalog = MessageCatalog()

        assert catalog.get_platform_name('nonexistent', 'ja') == 'nonexistent'

    def test_get_separator_success(self):
        """Test successful separator retrieval."""
        catalog = MessageCatalog(
            separators={'text': {'ja': '、', 'en': ', '}, 'list': {'ja': '・', 'en': '• '}}
        )

        assert catalog.get_separator('text', 'ja') == '、'
        assert catalog.get_separator('text', 'en') == ', '
        assert catalog.get_separator('list', 'ja') == '・'

    def test_get_separator_missing(self):
        """Test separator retrieval with missing separator."""
        catalog = MessageCatalog()

        assert catalog.get_separator('nonexistent', 'ja') == 'nonexistent'

    def test_get_conjunction_success(self):
        """Test successful conjunction retrieval."""
        catalog = MessageCatalog(
            conjunctions={'and': {'ja': 'かつ', 'en': 'and'}, 'or': {'ja': 'または', 'en': 'or'}}
        )

        assert catalog.get_conjunction('and', 'ja') == 'かつ'
        assert catalog.get_conjunction('and', 'en') == 'and'
        assert catalog.get_conjunction('or', 'ja') == 'または'

    def test_get_conjunction_missing(self):
        """Test conjunction retrieval with missing conjunction."""
        catalog = MessageCatalog()

        assert catalog.get_conjunction('nonexistent', 'ja') == 'nonexistent'

    def test_get_pass_text_success(self):
        """Test successful pass text retrieval."""
        catalog = MessageCatalog(
            pass_texts={'singular': {'ja': '合格', 'en': 'Pass'}, 'plural': {'ja': '合格', 'en': 'Passes'}}
        )

        assert catalog.get_pass_text('singular', 'ja') == '合格'
        assert catalog.get_pass_text('singular', 'en') == 'Pass'
        assert catalog.get_pass_text('plural', 'en') == 'Passes'

    def test_get_pass_text_missing(self):
        """Test pass text retrieval with missing text type."""
        catalog = MessageCatalog()

        assert catalog.get_pass_text('nonexistent', 'ja') == 'nonexistent'

    def test_get_date_format_success(self):
        """Test successful date format retrieval."""
        catalog = MessageCatalog(
            date_formats={'default': {'ja': '%Y年%m月%d日', 'en': '%Y-%m-%d'}}
        )

        assert catalog.get_date_format('default', 'ja') == '%Y年%m月%d日'
        assert catalog.get_date_format('default', 'en') == '%Y-%m-%d'

    def test_get_date_format_default_params(self):
        """Test date format retrieval with default parameters."""
        catalog = MessageCatalog(
            date_formats={'default': {'ja': '%Y年%m月%d日', 'en': '%Y-%m-%d'}}
        )

        assert catalog.get_date_format() == '%Y年%m月%d日'

    def test_get_date_format_missing(self):
        """Test date format retrieval with missing format."""
        catalog = MessageCatalog()

        assert catalog.get_date_format('nonexistent', 'ja') == 'nonexistent'

    def test_all_methods_with_empty_catalog(self):
        """Test all getter methods with empty catalog."""
        catalog = MessageCatalog()

        assert catalog.get_severity_tag('test') == 'test'
        assert catalog.get_check_target('test') == 'test'
        assert catalog.get_check_tool('test') == 'test'
        assert catalog.get_platform_name('test') == 'test'
        assert catalog.get_separator('test') == 'test'
        assert catalog.get_conjunction('test') == 'test'
        assert catalog.get_pass_text('test') == 'test'
        assert catalog.get_date_format('test') == 'test'

    def test_comprehensive_data_structure(self):
        """Test with comprehensive data structure."""
        comprehensive_data = {
            'severity_tags': {
                'minor': {'ja': '軽微', 'en': 'MINOR'},
                'normal': {'ja': '通常', 'en': 'NORMAL'},
                'major': {'ja': '重要', 'en': 'MAJOR'},
                'critical': {'ja': '致命的', 'en': 'CRITICAL'}
            },
            'check_targets': {
                'design': {'ja': 'デザイン', 'en': 'Design'},
                'code': {'ja': 'コード', 'en': 'Code'},
                'product': {'ja': 'プロダクト', 'en': 'Product'}
            },
            'check_tools': {
                'axe': {'ja': 'axe-core', 'en': 'axe-core'},
                'lighthouse': {'ja': 'Lighthouse', 'en': 'Lighthouse'},
                'wave': {'ja': 'WAVE', 'en': 'WAVE'}
            },
            'platform_names': {
                'web': {'ja': 'Web', 'en': 'Web'},
                'mobile': {'ja': 'モバイル', 'en': 'Mobile'},
                'ios': {'ja': 'iOS', 'en': 'iOS'},
                'android': {'ja': 'Android', 'en': 'Android'}
            },
            'separators': {
                'text': {'ja': '、', 'en': ', '},
                'list': {'ja': '・', 'en': '• '}
            },
            'conjunctions': {
                'and': {'ja': 'かつ', 'en': 'and'},
                'or': {'ja': 'または', 'en': 'or'}
            },
            'pass_texts': {
                'singular': {'ja': '合格', 'en': 'Pass'},
                'plural': {'ja': '合格', 'en': 'Passes'}
            },
            'date_formats': {
                'default': {'ja': '%Y年%m月%d日', 'en': '%Y-%m-%d'}
            }
        }

        catalog = MessageCatalog(**comprehensive_data)

        # Test all categories
        assert catalog.get_severity_tag('critical', 'ja') == '致命的'
        assert catalog.get_check_target('product', 'en') == 'Product'
        assert catalog.get_check_tool('lighthouse', 'ja') == 'Lighthouse'
        assert catalog.get_platform_name('android', 'en') == 'Android'
        assert catalog.get_separator('list', 'ja') == '・'
        assert catalog.get_conjunction('or', 'en') == 'or'
        assert catalog.get_pass_text('plural', 'en') == 'Passes'
        assert catalog.get_date_format('default', 'ja') == '%Y年%m月%d日'
