import pytest
from unittest.mock import patch, MagicMock
from freee_a11y_gl.models.check import (
    Check, Condition, Procedure, Implementation, Method, CheckTool, YouTube
)
from tests.models.base_test import BaseModelTest


class TestCheck(BaseModelTest):
    """Test cases for Check model."""

    model_class = Check
    sample_data = {
        "id": "test-check-001",
        "sortKey": "001",
        "check": {"ja": "テストチェック", "en": "Test Check"},
        "severity": "normal",
        "target": "code",
        "platform": ["web", "mobile"],
        "src_path": "test/check.yaml"
    }

    def setup_method(self):
        """Setup for each test method."""
        # Clear all instances before each test
        Check._instances.clear()
        CheckTool._instances.clear()

    def test_init_basic(self):
        """Test basic Check initialization."""
        check = Check(self.sample_data)
        assert check.id == "test-check-001"
        assert check.sort_key == "001"
        assert check.check_text == {"ja": "テストチェック", "en": "Test Check"}
        assert check.severity == "normal"
        assert check.target == "code"
        assert check.platform == ["web", "mobile"]
        assert check.src_path == "test/check.yaml"
        assert check.conditions == []
        assert check.implementations == []

    def test_init_with_conditions(self):
        """Test Check initialization with conditions."""
        condition_data = {
            "type": "simple",
            "platform": "web",
            "id": "test-proc-001",
            "tool": "axe",
            "procedure": {"ja": "テスト手順", "en": "Test procedure"}
        }
        check_data = {**self.sample_data, "conditions": [condition_data]}

        # Mock CheckTool to avoid dependency issues
        with patch('freee_a11y_gl.models.check.CheckTool.list_all_ids',
                   return_value=['axe']):
            with patch('freee_a11y_gl.models.check.CheckTool.get_by_id') \
                    as mock_get_tool:
                mock_tool = MagicMock()
                mock_tool.add_example = MagicMock()
                mock_get_tool.return_value = mock_tool

                check = Check(check_data)
                assert len(check.conditions) == 1
                assert isinstance(check.conditions[0], Condition)

    def test_init_with_implementations(self):
        """Test Check initialization with implementations."""
        impl_data = {
            "title": {"ja": "実装タイトル", "en": "Implementation Title"},
            "methods": [
                {
                    "platform": "web",
                    "method": {"ja": "実装方法", "en": "Implementation method"}
                }
            ]
        }
        check_data = {**self.sample_data, "implementations": [impl_data]}

        check = Check(check_data)
        assert len(check.implementations) == 1
        assert isinstance(check.implementations[0], Implementation)

    def test_duplicate_id_error(self):
        """Test duplicate ID raises ValueError."""
        Check(self.sample_data)
        with pytest.raises(ValueError,
                           match="Duplicate check ID: test-check-001"):
            Check(self.sample_data)

    def test_duplicate_sort_key_error(self):
        """Test duplicate sort key raises ValueError."""
        Check(self.sample_data)
        duplicate_data = {**self.sample_data, "id": "test-check-002"}
        with pytest.raises(ValueError, match="Duplicate check sortKey: 001"):
            Check(duplicate_data)

    def test_condition_platforms(self):
        """Test getting unique platforms from conditions."""
        # Mock condition objects
        mock_cond1 = MagicMock()
        mock_cond1.platform = "web"
        mock_cond2 = MagicMock()
        mock_cond2.platform = "mobile"
        mock_cond3 = MagicMock()
        mock_cond3.platform = "web"  # Duplicate

        check = Check(self.sample_data)
        check.conditions = [mock_cond1, mock_cond2, mock_cond3]

        result = check.condition_platforms()
        assert result == ["mobile", "web"]  # Sorted and unique

    @patch('freee_a11y_gl.models.check.Config')
    def test_template_data(self, mock_config):
        """Test template data generation."""
        mock_config.get_severity_tag.return_value = '[NORMAL]'
        mock_config.get_check_target_name.return_value = 'コード'

        check = Check(self.sample_data)

        # Mock the relationship manager method
        mock_rel = MagicMock()
        mock_rel.get_related_objects.return_value = []
        mock_rel.get_sorted_related_objects.return_value = []
        check._get_relationship_manager = MagicMock(return_value=mock_rel)

        # Mock the join_platform_items method from mixin
        check.join_platform_items = MagicMock(return_value='Web、モバイル')

        result = check.template_data("ja")

        expected = {
            'id': 'test-check-001',
            'check': 'テストチェック',
            'severity': '[NORMAL]',
            'target': 'コード',
            'platform': 'Web、モバイル',
            'guidelines': []
        }

        for key, value in expected.items():
            assert result[key] == value

    def test_join_platform_items_method(self):
        """Test join_platform_items method from mixin."""
        check = Check(self.sample_data)

        with patch('freee_a11y_gl.mixins.template_mixin.join_items') \
                as mock_join:
            mock_join.return_value = "Web、モバイル"

            result = check.join_platform_items(["web", "mobile"], "ja")
            assert result == "Web、モバイル"
            mock_join.assert_called_once_with(["web", "mobile"], "ja")

    def test_list_all_src_paths(self):
        """Test listing all source paths."""
        Check(self.sample_data)
        check2_data = {**self.sample_data, "id": "test-check-002",
                       "sortKey": "002", "src_path": "test/check2.yaml"}
        Check(check2_data)

        result = Check.list_all_src_paths()
        assert set(result) == {"test/check.yaml", "test/check2.yaml"}

    def test_object_data(self):
        """Test object data generation."""
        mock_rel = MagicMock()
        mock_rel.get_related_objects.return_value = []
        mock_rel.get_sorted_related_objects.return_value = []

        check = Check(self.sample_data)

        with patch.object(check, '_get_relationship_manager',
                          return_value=mock_rel):
            result = check.object_data()

        expected = {
            'id': 'test-check-001',
            'sortKey': '001',
            'check': {'ja': 'テストチェック', 'en': 'Test Check'},
            'severity': '[NORMAL]',
            'target': 'code',
            'platform': ['web', 'mobile'],
            'guidelines': []
        }

        for key, value in expected.items():
            assert result[key] == value

    def test_object_data_all(self):
        """Test getting object data for all checks."""
        Check(self.sample_data)
        check2_data = {**self.sample_data, "id": "test-check-002",
                       "sortKey": "002"}
        Check(check2_data)

        with patch.object(Check, 'object_data', return_value={'test': 'data'}):
            result = Check.object_data_all()
            assert len(result) == 2
            assert 'test-check-001' in result
            assert 'test-check-002' in result

    def test_template_data_all(self):
        """Test getting template data for all checks."""
        Check(self.sample_data)
        check2_data = {**self.sample_data, "id": "test-check-002",
                       "sortKey": "002"}
        Check(check2_data)

        with patch.object(Check, 'template_data',
                          return_value={'test': 'data'}):
            result = list(Check.template_data_all("ja"))
            assert len(result) == 2


class TestCondition:
    """Test cases for Condition class."""

    def setup_method(self):
        """Setup for each test method."""
        Check._instances.clear()
        CheckTool._instances.clear()

    def test_init_simple_condition(self):
        """Test simple condition initialization."""
        check_data = {
            "id": "test-check",
            "sortKey": "001",
            "check": {"ja": "テスト", "en": "Test"},
            "severity": "normal",
            "target": "code",
            "platform": ["web"],
            "src_path": "test.yaml"
        }
        check = Check(check_data)

        condition_data = {
            "type": "simple",
            "platform": "web",
            "id": "test-proc",
            "tool": "axe",
            "procedure": {"ja": "手順", "en": "Procedure"}
        }

        with patch('freee_a11y_gl.models.check.CheckTool.list_all_ids',
                   return_value=['axe']):
            with patch('freee_a11y_gl.models.check.CheckTool.get_by_id') \
                    as mock_get_tool:
                mock_tool = MagicMock()
                mock_tool.add_example = MagicMock()
                mock_get_tool.return_value = mock_tool

                condition = Condition(condition_data, check)
                assert condition.type == "simple"
                assert condition.platform == "web"
                assert isinstance(condition.procedure, Procedure)

    def test_init_complex_condition(self):
        """Test complex condition initialization."""
        check_data = {
            "id": "test-check",
            "sortKey": "001",
            "check": {"ja": "テスト", "en": "Test"},
            "severity": "normal",
            "target": "code",
            "platform": ["web"],
            "src_path": "test.yaml"
        }
        check = Check(check_data)

        simple_condition = {
            "type": "simple",
            "platform": "web",
            "id": "test-proc",
            "tool": "axe",
            "procedure": {"ja": "手順", "en": "Procedure"}
        }

        condition_data = {
            "type": "and",
            "conditions": [simple_condition, simple_condition.copy()]
        }

        with patch('freee_a11y_gl.models.check.CheckTool.list_all_ids',
                   return_value=['axe']):
            with patch('freee_a11y_gl.models.check.CheckTool.get_by_id') \
                    as mock_get_tool:
                mock_tool = MagicMock()
                mock_tool.add_example = MagicMock()
                mock_get_tool.return_value = mock_tool

                condition = Condition(condition_data, check)
                assert condition.type == "and"
                assert len(condition.conditions) == 2

    def test_procedures(self):
        """Test getting all procedures from condition."""
        check_data = {
            "id": "test-check",
            "sortKey": "001",
            "check": {"ja": "テスト", "en": "Test"},
            "severity": "normal",
            "target": "code",
            "platform": ["web"],
            "src_path": "test.yaml"
        }
        check = Check(check_data)

        condition_data = {
            "type": "simple",
            "platform": "web",
            "id": "test-proc",
            "tool": "axe",
            "procedure": {"ja": "手順", "en": "Procedure"}
        }

        with patch('freee_a11y_gl.models.check.CheckTool.list_all_ids',
                   return_value=['axe']):
            with patch('freee_a11y_gl.models.check.CheckTool.get_by_id') \
                    as mock_get_tool:
                mock_tool = MagicMock()
                mock_tool.add_example = MagicMock()
                mock_get_tool.return_value = mock_tool

                condition = Condition(condition_data, check)
                procedures = condition.procedures()
                assert len(procedures) == 1
                assert isinstance(procedures[0], Procedure)

    @patch('freee_a11y_gl.models.check.Config')
    def test_summary_simple(self, mock_config):
        """Test summary for simple condition."""
        mock_config.get_pass_singular_text.return_value = "を満たしている"

        check_data = {
            "id": "test-check",
            "sortKey": "001",
            "check": {"ja": "テスト", "en": "Test"},
            "severity": "normal",
            "target": "code",
            "platform": ["web"],
            "src_path": "test.yaml"
        }
        check = Check(check_data)

        condition_data = {
            "type": "simple",
            "platform": "web",
            "id": "test-proc",
            "tool": "axe",
            "procedure": {"ja": "手順", "en": "Procedure"}
        }

        with patch('freee_a11y_gl.models.check.CheckTool.list_all_ids',
                   return_value=['axe']):
            with patch('freee_a11y_gl.models.check.CheckTool.get_by_id') \
                    as mock_get_tool:
                mock_tool = MagicMock()
                mock_tool.add_example = MagicMock()
                mock_get_tool.return_value = mock_tool

                condition = Condition(condition_data, check)
                summary = condition.summary("ja")
                assert summary == "test-procを満たしている"


class TestCheckTool:
    """Test cases for CheckTool class."""

    def setup_method(self):
        """Setup for each test method."""
        CheckTool._instances.clear()

    def test_init(self):
        """Test CheckTool initialization."""
        names = {"ja": "テストツール", "en": "Test Tool"}
        tool = CheckTool("test-tool", names)

        assert tool.id == "test-tool"
        assert tool.names == names
        assert tool.examples == []
        assert CheckTool._instances["test-tool"] == tool

    def test_get_name(self):
        """Test getting localized name."""
        names = {"ja": "テストツール", "en": "Test Tool"}
        tool = CheckTool("test-tool", names)

        assert tool.get_name("ja") == "テストツール"
        assert tool.get_name("en") == "Test Tool"
        assert tool.get_name("fr") == "テストツール"  # Falls back to Japanese

    def test_add_example(self):
        """Test adding example to tool."""
        names = {"ja": "テストツール", "en": "Test Tool"}
        tool = CheckTool("test-tool", names)

        mock_example = MagicMock()
        tool.add_example(mock_example)

        assert len(tool.examples) == 1
        assert tool.examples[0] == mock_example

    def test_list_all(self):
        """Test listing all tools."""
        tool1 = CheckTool("tool1", {"ja": "ツール1", "en": "Tool 1"})
        tool2 = CheckTool("tool2", {"ja": "ツール2", "en": "Tool 2"})

        all_tools = CheckTool.list_all()
        assert len(all_tools) == 2
        assert tool1 in all_tools
        assert tool2 in all_tools

    def test_list_all_ids(self):
        """Test listing all tool IDs."""
        CheckTool("tool1", {"ja": "ツール1", "en": "Tool 1"})
        CheckTool("tool2", {"ja": "ツール2", "en": "Tool 2"})

        all_ids = CheckTool.list_all_ids()
        assert set(all_ids) == {"tool1", "tool2"}

    def test_get_by_id(self):
        """Test getting tool by ID."""
        tool = CheckTool("test-tool", {"ja": "テストツール", "en": "Test Tool"})

        assert CheckTool.get_by_id("test-tool") == tool
        assert CheckTool.get_by_id("nonexistent") is None


class TestImplementation:
    """Test cases for Implementation class."""

    def test_init(self):
        """Test Implementation initialization."""
        title = {"ja": "実装タイトル", "en": "Implementation Title"}
        methods = [
            {
                "platform": "web",
                "method": {"ja": "実装方法", "en": "Implementation method"}
            }
        ]

        impl = Implementation(title=title, methods=methods)
        assert impl.title == title
        assert len(impl.methods) == 1
        assert isinstance(impl.methods[0], Method)

    @patch('freee_a11y_gl.models.check.Config')
    def test_template_data(self, mock_config):
        """Test template data generation."""
        mock_config.get_platform_name.return_value = "Web"

        title = {"ja": "実装タイトル", "en": "Implementation Title"}
        methods = [
            {
                "platform": "web",
                "method": {"ja": "実装方法", "en": "Implementation method"}
            }
        ]

        impl = Implementation(title=title, methods=methods)
        result = impl.template_data("ja")

        assert result['title'] == "実装タイトル"
        assert len(result['methods']) == 1


class TestMethod:
    """Test cases for Method class."""

    @patch('freee_a11y_gl.models.check.Config')
    def test_template_data(self, mock_config):
        """Test template data generation."""
        mock_config.get_platform_name.return_value = "Web"

        method = Method(
            platform="web",
            method={"ja": "実装方法", "en": "Implementation method"}
        )

        result = method.template_data("ja")
        assert result['platform'] == "Web"
        assert result['method'] == "実装方法"


class TestYouTube:
    """Test cases for YouTube class."""

    def test_template_data(self):
        """Test template data generation."""
        youtube = YouTube(id="test-video", title="Test Video")
        result = youtube.template_data()

        assert result['id'] == "test-video"
        assert result['title'] == "Test Video"


class TestCheckAdditional:
    """Additional comprehensive tests for Check model coverage."""

    def setup_method(self):
        """Set up test fixtures."""
        Check._instances.clear()
        CheckTool._instances.clear()
        from freee_a11y_gl.settings import settings

        check_tools = settings.message_catalog.check_tools
        for tool_id, names in check_tools.items():
            CheckTool(tool_id, names)

        self.sample_data = {
            'id': 'test-check-comprehensive-001',
            'sortKey': 'comp-001',
            'check': {
                'ja': 'テストチェック項目追加',
                'en': 'Test Check Item Additional'
            },
            'severity': 'major',
            'target': 'designer',
            'platform': ['web', 'mobile'],
            'src_path': '/test/path/check_comp.yaml'
        }

    def test_template_data_japanese_language(self):
        """Test template_data method with Japanese language."""
        check = Check(self.sample_data)

        with patch('freee_a11y_gl.models.check.Config') as mock_config:
            mock_config.get_check_target_name.return_value = 'デザイナー'
            mock_config.get_severity_tag.return_value = '[重要]'
            mock_config.get_platform_name.return_value = 'ウェブ'
            mock_config.get_list_separator.return_value = '、'

            template_data = check.template_data('ja')

            assert isinstance(template_data, dict)
            assert template_data['check'] == 'テストチェック項目追加'

    def test_template_data_with_platform_filter(self):
        """Test template_data with platform filtering."""
        data_with_conditions = self.sample_data.copy()
        data_with_conditions['conditions'] = [
            {
                'type': 'simple',
                'platform': 'web',
                'id': 'proc-001',
                'tool': 'axe',
                'procedure': {
                    'ja': 'ウェブ手順',
                    'en': 'Web procedure'
                }
            },
            {
                'type': 'simple',
                'platform': 'mobile',
                'id': 'proc-002',
                'tool': 'axe',
                'procedure': {
                    'ja': 'モバイル手順',
                    'en': 'Mobile procedure'
                }
            }
        ]

        check = Check(data_with_conditions)

        with patch('freee_a11y_gl.models.check.Config') as mock_config:
            mock_config.get_check_target_name.return_value = 'Designer'
            mock_config.get_severity_tag.return_value = '[MAJOR]'
            mock_config.get_platform_name.return_value = 'Web'
            mock_config.get_list_separator.return_value = ', '

            # Test with platform filter
            template_data = check.template_data('en', platform=['web'])

            assert 'conditions' in template_data

    def test_with_empty_conditions_and_implementations(self):
        """Test Check with empty conditions and implementations lists."""
        data_empty = self.sample_data.copy()
        data_empty['conditions'] = []
        data_empty['implementations'] = []

        check = Check(data_empty)

        assert check.conditions == []
        assert check.implementations == []
        assert check.condition_platforms() == []

    def test_string_representation(self):
        """Test Check string representation."""
        check = Check(self.sample_data)
        str_repr = str(check)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_inheritance_from_base_model(self):
        """Test Check inherits from BaseModel correctly."""
        check = Check(self.sample_data)

        # Test BaseModel methods
        assert hasattr(check, 'id')
        assert hasattr(check, 'object_type')
        assert check.object_type == 'check'

    def test_instances_tracking(self):
        """Test Check instances are tracked correctly."""
        Check._instances.clear()

        check1 = Check(self.sample_data)
        assert 'test-check-comprehensive-001' in Check._instances
        assert Check._instances['test-check-comprehensive-001'] == check1

    def test_with_complex_nested_conditions(self):
        """Test Check with complex nested conditions."""
        data_complex = self.sample_data.copy()
        data_complex['conditions'] = [
            {
                'type': 'and',
                'conditions': [
                    {
                        'type': 'simple',
                        'platform': 'web',
                        'id': 'proc-001',
                        'tool': 'axe',
                        'procedure': {
                            'ja': '手順1',
                            'en': 'Procedure 1'
                        }
                    },
                    {
                        'type': 'simple',
                        'platform': 'web',
                        'id': 'proc-002',
                        'tool': 'manual',
                        'procedure': {
                            'ja': '手順2',
                            'en': 'Procedure 2'
                        }
                    }
                ]
            }
        ]

        check = Check(data_complex)

        assert len(check.conditions) == 1
        assert check.conditions[0].type == 'and'
        assert len(check.conditions[0].conditions) == 2

    def test_join_items_static_method(self):
        """Test Check join_items static method."""
        items = ['web', 'mobile', 'desktop']

        with patch('freee_a11y_gl.utils.Config') as mock_config:
            mock_config.get_list_separator.return_value = ', '
            mock_config.get_platform_name.side_effect = \
                lambda item, lang: f'{item.title()}'

            result = Check.join_items(items, 'en')

            assert isinstance(result, str)
            assert 'Web' in result
            assert 'Mobile' in result
            assert 'Desktop' in result

    def teardown_method(self):
        """Clean up after each test."""
        Check._instances.clear()
        CheckTool._instances.clear()
