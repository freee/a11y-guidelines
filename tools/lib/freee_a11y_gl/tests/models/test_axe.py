"""Tests for axe model."""

import pytest
from unittest.mock import patch, MagicMock

from freee_a11y_gl.models.axe import AxeRule, AxeMessage
from freee_a11y_gl.relationship_manager import RelationshipManager


class TestAxeMessage:
    """Test cases for AxeMessage dataclass."""

    def test_axe_message_creation(self):
        """Test AxeMessage can be created with help and description."""
        help_dict = {'en': 'English help', 'ja': 'Japanese help'}
        desc_dict = {'en': 'English description', 'ja': 'Japanese description'}
        
        message = AxeMessage(help=help_dict, description=desc_dict)
        
        assert message.help == help_dict
        assert message.description == desc_dict

    def test_axe_message_access_properties(self):
        """Test AxeMessage properties can be accessed."""
        help_dict = {'en': 'Help text', 'ja': 'ヘルプテキスト'}
        desc_dict = {'en': 'Description text', 'ja': '説明テキスト'}
        
        message = AxeMessage(help=help_dict, description=desc_dict)
        
        assert message.help['en'] == 'Help text'
        assert message.help['ja'] == 'ヘルプテキスト'
        assert message.description['en'] == 'Description text'
        assert message.description['ja'] == '説明テキスト'


class TestAxeRule:
    """Test cases for AxeRule model."""

    def setUp(self):
        """Set up test fixtures."""
        # Clear instances before each test
        AxeRule._instances.clear()
        RelationshipManager._instance = None

    def tearDown(self):
        """Clean up after each test."""
        AxeRule._instances.clear()
        RelationshipManager._instance = None

    def test_axe_rule_basic_initialization(self):
        """Test basic AxeRule initialization."""
        self.setUp()
        
        rule_data = {
            'id': 'test-rule',
            'metadata': {
                'help': 'Test help text',
                'description': 'Test description'
            },
            'tags': ['wcag2a', 'section508']
        }
        
        messages_ja = {
            'rules': {
                'test-rule': {
                    'help': 'テストヘルプ',
                    'description': 'テスト説明'
                }
            }
        }
        
        with patch('freee_a11y_gl.models.axe.RelationshipManager') as mock_rel_manager:
            mock_rel_instance = MagicMock()
            mock_rel_manager.return_value = mock_rel_instance
            
            rule = AxeRule(rule_data, messages_ja)
            
            assert rule.id == 'test-rule'
            assert rule.translated is True
            assert rule.message.help['en'] == 'Test help text'
            assert rule.message.help['ja'] == 'テストヘルプ'
            assert rule.message.description['en'] == 'Test description'
            assert rule.message.description['ja'] == 'テスト説明'
            assert rule.has_wcag_sc is False
            assert rule.has_guideline is False

        self.tearDown()

    def test_axe_rule_without_japanese_translation(self):
        """Test AxeRule initialization without Japanese translation."""
        self.setUp()
        
        rule_data = {
            'id': 'untranslated-rule',
            'metadata': {
                'help': 'English help only',
                'description': 'English description only'
            },
            'tags': ['wcag2a']
        }
        
        messages_ja = {
            'rules': {}  # No translation for this rule
        }
        
        with patch('freee_a11y_gl.models.axe.RelationshipManager') as mock_rel_manager:
            mock_rel_instance = MagicMock()
            mock_rel_manager.return_value = mock_rel_instance
            
            rule = AxeRule(rule_data, messages_ja)
            
            assert rule.id == 'untranslated-rule'
            assert rule.translated is False
            assert rule.message.help['en'] == 'English help only'
            assert rule.message.help['ja'] == 'English help only'  # Falls back to English
            assert rule.message.description['en'] == 'English description only'
            assert rule.message.description['ja'] == 'English description only'

        self.tearDown()

    def test_axe_rule_duplicate_id_error(self):
        """Test AxeRule raises error for duplicate IDs."""
        self.setUp()
        
        rule_data = {
            'id': 'duplicate-rule',
            'metadata': {
                'help': 'Test help',
                'description': 'Test description'
            },
            'tags': []
        }
        
        messages_ja = {'rules': {}}
        
        with patch('freee_a11y_gl.models.axe.RelationshipManager') as mock_rel_manager:
            mock_rel_instance = MagicMock()
            mock_rel_manager.return_value = mock_rel_instance
            
            # Create first rule
            AxeRule(rule_data, messages_ja)
            
            # Attempt to create duplicate should raise error
            with pytest.raises(ValueError) as exc_info:
                AxeRule(rule_data, messages_ja)
            
            assert 'Duplicate rule ID: duplicate-rule' in str(exc_info.value)

        self.tearDown()

    def test_axe_rule_with_wcag_tags(self):
        """Test AxeRule with WCAG success criteria tags."""
        self.setUp()
        
        rule_data = {
            'id': 'wcag-rule',
            'metadata': {
                'help': 'WCAG rule help',
                'description': 'WCAG rule description'
            },
            'tags': ['wcag111', 'wcag21aa', 'section508']
        }
        
        messages_ja = {'rules': {}}
        
        # Mock WcagSc instances
        mock_wcag_sc = MagicMock()
        mock_wcag_sc.sort_key = '1.1.1'
        
        with patch('freee_a11y_gl.models.axe.RelationshipManager') as mock_rel_manager, \
             patch('freee_a11y_gl.models.axe.tag2sc') as mock_tag2sc, \
             patch('freee_a11y_gl.models.reference.WcagSc') as mock_wcag_sc_class:
            
            mock_rel_instance = MagicMock()
            mock_rel_manager.return_value = mock_rel_instance
            
            # Mock tag2sc to return success criteria IDs
            mock_tag2sc.side_effect = lambda tag: '1.1.1' if tag == 'wcag111' else '2.1.1' if tag == 'wcag21aa' else None
            
            # Mock WcagSc class
            mock_wcag_sc_class._instances = {'1.1.1': mock_wcag_sc, '2.1.1': mock_wcag_sc}
            mock_wcag_sc_class.get_by_id.return_value = mock_wcag_sc
            
            # Mock relationship manager to return guidelines
            mock_rel_instance.get_related_objects.return_value = []
            
            rule = AxeRule(rule_data, messages_ja)
            
            assert rule.has_wcag_sc is True
            # Should have called associate_objects for WCAG SC
            assert mock_rel_instance.associate_objects.call_count >= 1

        self.tearDown()

    def test_axe_rule_template_data_basic(self):
        """Test AxeRule template_data method basic functionality."""
        self.setUp()
        
        rule_data = {
            'id': 'template-rule',
            'metadata': {
                'help': 'Template help',
                'description': 'Template description'
            },
            'tags': []
        }
        
        messages_ja = {
            'rules': {
                'template-rule': {
                    'help': 'テンプレートヘルプ',
                    'description': 'テンプレート説明'
                }
            }
        }
        
        with patch('freee_a11y_gl.models.axe.RelationshipManager') as mock_rel_manager:
            mock_rel_instance = MagicMock()
            mock_rel_manager.return_value = mock_rel_instance
            
            rule = AxeRule(rule_data, messages_ja)
            
            template_data = rule.template_data('ja')
            
            assert template_data['id'] == 'template-rule'
            assert template_data['help']['en'] == 'Template help'
            assert template_data['help']['ja'] == 'テンプレートヘルプ'
            assert template_data['description']['en'] == 'Template description'
            assert template_data['description']['ja'] == 'テンプレート説明'
            assert template_data['translated'] is True

        self.tearDown()

    def test_axe_rule_template_data_with_wcag_sc(self):
        """Test AxeRule template_data with WCAG success criteria."""
        self.setUp()
        
        rule_data = {
            'id': 'wcag-template-rule',
            'metadata': {
                'help': 'WCAG template help',
                'description': 'WCAG template description'
            },
            'tags': ['wcag111']
        }
        
        messages_ja = {'rules': {}}
        
        # Mock WcagSc and related objects
        mock_wcag_sc = MagicMock()
        mock_wcag_sc.sort_key = '1.1.1'
        mock_wcag_sc.template_data.return_value = {'id': '1.1.1', 'title': 'Non-text Content'}
        
        mock_guideline = MagicMock()
        mock_guideline.sort_key = 'image-001'
        mock_guideline.get_category_and_id.return_value = {'category': 'image', 'id': '001'}
        
        with patch('freee_a11y_gl.models.axe.RelationshipManager') as mock_rel_manager, \
             patch('freee_a11y_gl.models.axe.tag2sc') as mock_tag2sc, \
             patch('freee_a11y_gl.models.reference.WcagSc') as mock_wcag_sc_class:
            
            mock_rel_instance = MagicMock()
            mock_rel_manager.return_value = mock_rel_instance
            
            mock_tag2sc.return_value = '1.1.1'
            mock_wcag_sc_class._instances = {'1.1.1': mock_wcag_sc}
            mock_wcag_sc_class.get_by_id.return_value = mock_wcag_sc
            
            # Mock relationship manager responses
            def mock_get_related_objects(obj, obj_type):
                if obj_type == 'wcag_sc':
                    return [mock_wcag_sc]
                elif obj_type == 'guideline':
                    return [mock_guideline]
                return []
            
            mock_rel_instance.get_related_objects.side_effect = mock_get_related_objects
            
            rule = AxeRule(rule_data, messages_ja)
            rule.has_wcag_sc = True
            rule.has_guideline = True
            
            template_data = rule.template_data('ja')
            
            assert 'scs' in template_data
            assert 'guidelines' in template_data
            assert len(template_data['scs']) == 1
            assert len(template_data['guidelines']) == 1

        self.tearDown()

    def test_axe_rule_list_all_sorting(self):
        """Test AxeRule list_all method sorting."""
        self.setUp()
        
        # Create multiple rules with different characteristics
        rules_data = [
            {
                'id': 'z-rule-no-guideline',
                'metadata': {'help': 'Help Z', 'description': 'Desc Z'},
                'tags': []
            },
            {
                'id': 'a-rule-with-guideline',
                'metadata': {'help': 'Help A', 'description': 'Desc A'},
                'tags': ['wcag111']
            },
            {
                'id': 'm-rule-with-sc-only',
                'metadata': {'help': 'Help M', 'description': 'Desc M'},
                'tags': ['wcag211']
            }
        ]
        
        messages_ja = {'rules': {}}
        
        with patch('freee_a11y_gl.models.axe.RelationshipManager') as mock_rel_manager, \
             patch('freee_a11y_gl.models.axe.tag2sc') as mock_tag2sc, \
             patch('freee_a11y_gl.models.reference.WcagSc') as mock_wcag_sc_class:
            
            mock_rel_instance = MagicMock()
            mock_rel_manager.return_value = mock_rel_instance
            
            # Mock tag2sc responses
            def mock_tag2sc_func(tag):
                if tag == 'wcag111':
                    return '1.1.1'
                elif tag == 'wcag211':
                    return '2.1.1'
                return None
            
            mock_tag2sc.side_effect = mock_tag2sc_func
            
            # Mock WcagSc instances
            mock_wcag_sc_class._instances = {'1.1.1': MagicMock(), '2.1.1': MagicMock()}
            mock_wcag_sc_class.get_by_id.return_value = MagicMock()
            
            # Mock relationship responses
            def mock_get_related_objects(obj, obj_type):
                if obj.id == 'a-rule-with-guideline' and obj_type == 'guideline':
                    return [MagicMock()]  # Has guidelines
                return []
            
            mock_rel_instance.get_related_objects.side_effect = mock_get_related_objects
            
            # Create rules
            rules = []
            for rule_data in rules_data:
                rule = AxeRule(rule_data, messages_ja)
                rules.append(rule)
            
            # Set has_guideline and has_wcag_sc flags manually for testing
            rules[1].has_guideline = True  # a-rule-with-guideline
            rules[1].has_wcag_sc = True
            rules[2].has_wcag_sc = True    # m-rule-with-sc-only
            
            sorted_rules = AxeRule.list_all()
            
            # Should be sorted: with_guidelines, with_sc, without_sc
            # Within each group, sorted by ID
            assert len(sorted_rules) == 3
            assert sorted_rules[0].id == 'a-rule-with-guideline'  # Has guidelines
            assert sorted_rules[1].id == 'm-rule-with-sc-only'    # Has SC only
            assert sorted_rules[2].id == 'z-rule-no-guideline'    # No SC

        self.tearDown()

    def test_axe_rule_class_metadata(self):
        """Test AxeRule class-level metadata."""
        # Reset class variables to ensure clean state
        AxeRule.timestamp = None
        AxeRule.version = None
        AxeRule.major_version = None
        AxeRule.deque_url = None
        
        # Test initial state
        assert AxeRule.timestamp is None
        assert AxeRule.version is None
        assert AxeRule.major_version is None
        assert AxeRule.deque_url is None
        
        # Test setting metadata
        AxeRule.timestamp = "2023-01-01 12:00:00+0000"
        AxeRule.version = "4.6.3"
        AxeRule.major_version = "4.6"
        AxeRule.deque_url = "https://deque.com"
        
        assert AxeRule.timestamp == "2023-01-01 12:00:00+0000"
        assert AxeRule.version == "4.6.3"
        assert AxeRule.major_version == "4.6"
        assert AxeRule.deque_url == "https://deque.com"
        
        # Reset for other tests
        AxeRule.timestamp = None
        AxeRule.version = None
        AxeRule.major_version = None
        AxeRule.deque_url = None

    def test_axe_rule_object_type(self):
        """Test AxeRule object_type class attribute."""
        assert AxeRule.object_type == "axe_rule"

    def test_axe_rule_instances_tracking(self):
        """Test AxeRule instances are properly tracked."""
        self.setUp()
        
        rule_data = {
            'id': 'tracked-rule',
            'metadata': {
                'help': 'Tracked help',
                'description': 'Tracked description'
            },
            'tags': []
        }
        
        messages_ja = {'rules': {}}
        
        with patch('freee_a11y_gl.models.axe.RelationshipManager') as mock_rel_manager:
            mock_rel_instance = MagicMock()
            mock_rel_manager.return_value = mock_rel_instance
            
            # Initially no instances
            assert len(AxeRule._instances) == 0
            
            rule = AxeRule(rule_data, messages_ja)
            
            # Should be tracked in instances
            assert len(AxeRule._instances) == 1
            assert 'tracked-rule' in AxeRule._instances
            assert AxeRule._instances['tracked-rule'] is rule

        self.tearDown()
