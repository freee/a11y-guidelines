"""Pytest configuration and fixtures for freee_a11y_gl tests."""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime

# Add src directory to Python path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import after path setup
from freee_a11y_gl.models.faq.tag import FaqTag
from freee_a11y_gl.models.faq.article import Faq
from freee_a11y_gl.models.content import Guideline, Category
from freee_a11y_gl.models.check import Check, CheckTool
from freee_a11y_gl.models.reference import InfoRef, WcagSc
from freee_a11y_gl.relationship_manager import RelationshipManager


@pytest.fixture(autouse=True)
def clear_instances():
    """Clear all model instances before each test."""
    # Clear all model instance stores
    for model_class in [Faq, FaqTag, Guideline, Category, Check, CheckTool, InfoRef, WcagSc]:
        if hasattr(model_class, '_instances'):
            model_class._instances.clear()

    # Clear RelationshipManager singleton
    RelationshipManager._instance = None

    yield

    # Clear again after test
    for model_class in [Faq, FaqTag, Guideline, Category, Check, CheckTool, InfoRef, WcagSc]:
        if hasattr(model_class, '_instances'):
            model_class._instances.clear()

    # Clear RelationshipManager singleton
    RelationshipManager._instance = None


@pytest.fixture
def setup_categories():
    """Setup test categories."""
    categories_data = [
        ("form", {"ja": "フォーム", "en": "Form"}),
        ("markup", {"ja": "マークアップと実装", "en": "Markup and Implementation"}),
        ("input_device", {"ja": "入力ディバイス", "en": "Input Device"}),
        ("link", {"ja": "リンク", "en": "Link"}),
        ("dynamic_content", {"ja": "動的コンテンツ", "en": "Dynamic Content"}),
        ("text", {"ja": "テキスト", "en": "Text"})
    ]

    categories = []
    for category_id, names in categories_data:
        category = Category(category_id, names)
        categories.append(category)

    return categories


@pytest.fixture
def setup_faq_tags():
    """Setup test FAQ tags."""
    tags_data = [
        ("axe", {"ja": "axe", "en": "axe"}),
        ("keyboard-operation", {"ja": "キーボード操作", "en": "Keyboard Operation"}),
        ("screen-reader", {"ja": "スクリーンリーダー", "en": "Screen Reader"})
    ]

    tags = []
    for tag_id, names in tags_data:
        tag = FaqTag(tag_id, names)
        tags.append(tag)

    return tags


@pytest.fixture
def setup_wcag_sc():
    """Setup test WCAG Success Criteria."""
    wcag_data = [
        ("1.1.1", {
            "id": "1.1.1",
            "sortKey": "1.1.1",
            "level": "A",
            "localPriority": "A",
            "ja": {
                "title": "非テキストコンテンツ",
                "url": "https://waic.jp/translations/WCAG21/#non-text-content"
            },
            "en": {
                "title": "Non-text Content",
                "url": "https://www.w3.org/WAI/WCAG21/Understanding/non-text-content/"
            }
        }),
        ("2.1.1", {
            "id": "2.1.1",
            "sortKey": "2.1.1",
            "level": "A",
            "localPriority": "A",
            "ja": {
                "title": "キーボード",
                "url": "https://waic.jp/translations/WCAG21/#keyboard"
            },
            "en": {
                "title": "Keyboard",
                "url": "https://www.w3.org/WAI/WCAG21/Understanding/keyboard/"
            }
        })
    ]

    wcag_scs = []
    for sc_id, data in wcag_data:
        wcag_sc = WcagSc(sc_id, data)
        wcag_scs.append(wcag_sc)

    return wcag_scs


@pytest.fixture
def all_check_data():
    """Setup test check data."""
    checks_data = [
        {
            "id": "0171",
            "sortKey": "0171",
            "src_path": "test/checks/0171.yaml",
            "check": {"ja": "テストチェック0171", "en": "Test Check 0171"},
            "severity": "normal",
            "target": "code",
            "platform": ["web"],
            "conditions": []
        },
        {
            "id": "0172",
            "sortKey": "0172",
            "src_path": "test/checks/0172.yaml", 
            "check": {"ja": "テストチェック0172", "en": "Test Check 0172"},
            "severity": "high",
            "target": "design",
            "platform": ["mobile"],
            "conditions": []
        }
    ]

    # Mock Config to avoid dependency issues
    with patch('freee_a11y_gl.models.check.Config') as mock_config:
        mock_config.get_severity_tag.side_effect = lambda severity, lang: {
            ('normal', 'ja'): '[NORMAL]',
            ('high', 'ja'): '[HIGH]'
        }.get((severity, lang), f'[{severity.upper()}]')

        mock_config.get_check_target_name.side_effect = lambda target, lang: {
            ('code', 'ja'): 'コード',
            ('design', 'ja'): 'デザイン'
        }.get((target, lang), target)

        mock_config.get_platform_name.side_effect = lambda platform, lang: {
            ('web', 'ja'): 'Web',
            ('mobile', 'ja'): 'モバイル'
        }.get((platform, lang), platform)

        mock_config.get_list_separator.return_value = '、'

        # Mock RelationshipManager
        with patch('freee_a11y_gl.models.base.BaseModel._get_relationship_manager') as mock_get_rel:
            mock_rel = MagicMock()
            mock_get_rel.return_value = mock_rel
            mock_rel.get_related_objects.return_value = []
            mock_rel.get_sorted_related_objects.return_value = []

            checks = []
            for data in checks_data:
                check = Check(data)
                checks.append(check)

    return checks


@pytest.fixture
def all_guideline_data(setup_categories):
    """Setup test guideline data."""
    guidelines_data = [
        {
            "id": "gl-markup-semantics",
            "sortKey": "gl-markup-semantics",
            "src_path": "test/guidelines/gl-markup-semantics.yaml",
            "title": {"ja": "セマンティックなマークアップ", "en": "Semantic Markup"},
            "platform": ["web"],
            "guideline": {"ja": "セマンティックなマークアップ", "en": "Semantic Markup"},
            "intent": {"ja": "意図", "en": "Intent"},
            "category": "markup"
        },
        {
            "id": "gl-input-device-keyboard-operable",
            "sortKey": "gl-input-device-keyboard-operable", 
            "src_path": "test/guidelines/gl-input-device-keyboard-operable.yaml",
            "title": {"ja": "キーボード操作可能", "en": "Keyboard Operable"},
            "platform": ["web"],
            "guideline": {"ja": "キーボード操作可能", "en": "Keyboard Operable"},
            "intent": {"ja": "意図", "en": "Intent"},
            "category": "input_device"
        },
        {
            "id": "gl-input-device-focus",
            "sortKey": "gl-input-device-focus",
            "src_path": "test/guidelines/gl-input-device-focus.yaml", 
            "title": {"ja": "フォーカス", "en": "Focus"},
            "platform": ["web"],
            "guideline": {"ja": "フォーカス", "en": "Focus"},
            "intent": {"ja": "意図", "en": "Intent"},
            "category": "input_device"
        },
        {
            "id": "gl-input-device-focus-indicator",
            "sortKey": "gl-input-device-focus-indicator",
            "src_path": "test/guidelines/gl-input-device-focus-indicator.yaml",
            "title": {"ja": "フォーカスインジケーター", "en": "Focus Indicator"},
            "platform": ["web"],
            "guideline": {"ja": "フォーカスインジケーター", "en": "Focus Indicator"}, 
            "intent": {"ja": "意図", "en": "Intent"},
            "category": "input_device"
        },
        {
            "id": "gl-link-tab-order",
            "sortKey": "gl-link-tab-order",
            "src_path": "test/guidelines/gl-link-tab-order.yaml",
            "title": {"ja": "リンクのタブ順序", "en": "Link Tab Order"},
            "platform": ["web"],
            "guideline": {"ja": "リンクのタブ順序", "en": "Link Tab Order"},
            "intent": {"ja": "意図", "en": "Intent"}, 
            "category": "link"
        },
        {
            "id": "gl-form-keyboard-operable",
            "sortKey": "gl-form-keyboard-operable",
            "src_path": "test/guidelines/gl-form-keyboard-operable.yaml",
            "title": {"ja": "フォームのキーボード操作", "en": "Form Keyboard Operation"},
            "platform": ["web"],
            "guideline": {"ja": "フォームのキーボード操作", "en": "Form Keyboard Operation"},
            "intent": {"ja": "意図", "en": "Intent"},
            "category": "form"
        },
        {
            "id": "gl-form-tab-order", 
            "sortKey": "gl-form-tab-order",
            "src_path": "test/guidelines/gl-form-tab-order.yaml",
            "title": {"ja": "フォームのタブ順序", "en": "Form Tab Order"},
            "platform": ["web"],
            "guideline": {"ja": "フォームのタブ順序", "en": "Form Tab Order"},
            "intent": {"ja": "意図", "en": "Intent"},
            "category": "form"
        },
        {
            "id": "gl-form-dynamic-content-focus",
            "sortKey": "gl-form-dynamic-content-focus", 
            "src_path": "test/guidelines/gl-form-dynamic-content-focus.yaml",
            "title": {"ja": "フォームの動的コンテンツフォーカス", "en": "Form Dynamic Content Focus"},
            "platform": ["web"],
            "guideline": {"ja": "フォームの動的コンテンツフォーカス", "en": "Form Dynamic Content Focus"},
            "intent": {"ja": "意図", "en": "Intent"},
            "category": "form"
        },
        {
            "id": "gl-dynamic-content-focus",
            "sortKey": "gl-dynamic-content-focus",
            "src_path": "test/guidelines/gl-dynamic-content-focus.yaml", 
            "title": {"ja": "動的コンテンツフォーカス", "en": "Dynamic Content Focus"},
            "platform": ["web"],
            "guideline": {"ja": "動的コンテンツフォーカス", "en": "Dynamic Content Focus"},
            "intent": {"ja": "意図", "en": "Intent"},
            "category": "dynamic_content"
        }
    ]

    # Don't mock RelationshipManager for guidelines to allow real relationships
    guidelines = []
    for data in guidelines_data:
        guideline = Guideline(data)
        guidelines.append(guideline)

    return guidelines


@pytest.fixture
def sample_dir(tmp_path):
    """Create a temporary directory for test files."""
    return tmp_path


@pytest.fixture
def faq_factory(setup_faq_tags, all_guideline_data):
    """Factory for creating FAQ instances with test data."""
    def _create_faq(faq_id):
        faq_data = {
            "p0009": {
                "id": "p0009",
                "sortKey": "p0009",
                "src_path": "test/faq/p0009.yaml",
                "updated": "2025-03-25",
                "title": {
                    "ja": "Safariでのみ、Tabキーによるフォーカス移動の挙動がおかしい",
                    "en": "Focus Movement by Tab Key Is Strange Only in Safari"
                },
                "problem": {
                    "ja": "SafariでWebページを表示して、 :kbd:`Tab` キーや :kbd:`Shift+Tab` キーでフォーカスを移動すると、本来フォーカスされるべきなのにスキップされる要素がある。\nGoogle Chromeや他のブラウザーでは適切にフォーカス移動できているが、コンテンツ側で何らかの対応が必要か。",
                    "en": "Problem description in English"
                },
                "solution": {
                    "ja": "デフォルト設定でSafariを使用している場合の挙動なので対処は不要。\n:kbd:`option+Tab` と :kbd:`Shift+option+Tab` キーを使用すると他のブラウザーと同様の挙動になる。",
                    "en": "Solution description in English"
                },
                "explanation": {
                    "ja": "デフォルト設定でSafariを使用している場合、リンクやボタンなど、本来 :kbd:`Tab` キーや :kbd:`Shift+Tab` キーでフォーカスを移動できるはずの要素の一部に、フォーカスが移動できません。\n代わりに、 :kbd:`option+Tab` キーや :kbd:`Shift+option+Tab` キーを使用すると、他のブラウザーと同様にフォーカスを移動できます。\n\nフォーカス順序のチェックをする場合、通常は他のブラウザーで確認して問題なければ問題はありません。\nもしSafariでチェックを実施する必要がある場合は、 :kbd:`option+Tab` キーと :kbd:`Shift+option+Tab` キーを使用して確認します。\n\nなお、macOS上のSafariを使用している場合は、以下のいずれかの設定をすることで、 :kbd:`Tab` キーと :kbd:`Shift+Tab` キーの挙動が他のブラウザーと同様になります。\n\n*  Safariの :menuselection:`設定 --> 詳細` で、「Tabキーを押したときにWebページ上の各項目を強調表示」にチェックを入れる\n*  macOSの :menuselection:`環境設定 --> アクセシビリティ --> キーボード` で「フルキーボードアクセス」を有効にする",
                    "en": "Explanation in English"
                },
                "tags": ["keyboard-operation"],
                "guidelines": [
                    "gl-input-device-keyboard-operable",
                    "gl-input-device-focus", 
                    "gl-input-device-focus-indicator",
                    "gl-link-tab-order",
                    "gl-form-keyboard-operable",
                    "gl-form-tab-order",
                    "gl-form-dynamic-content-focus",
                    "gl-dynamic-content-focus"
                ]
            },
            "d0001": {
                "id": "d0001",
                "sortKey": "d0001", 
                "src_path": "test/faq/d0001.yaml",
                "updated": "2025-01-01",
                "title": {"ja": "デザインFAQ", "en": "Design FAQ"},
                "problem": {"ja": "デザイン問題", "en": "Design problem"},
                "solution": {"ja": "デザイン解決策", "en": "Design solution"},
                "explanation": {"ja": "デザイン説明", "en": "Design explanation"},
                "tags": ["screen-reader"],
                "guidelines": []
            }
        }

        if faq_id not in faq_data:
            raise ValueError(f"Unknown FAQ ID: {faq_id}")

        # Don't mock RelationshipManager for FAQ creation to allow real relationships
        return Faq(faq_data[faq_id])

    return _create_faq


@pytest.fixture
def mock_infolabels():
    """Mock info labels for InfoRef tests."""
    # This fixture provides mock data for info reference labels
    # Used by InfoRef tests that need to test link data functionality
    pass


@pytest.fixture
def guideline_factory(setup_categories):
    """Factory for creating Guideline instances with test data."""
    def _create_guideline(guideline_id):
        # Use data from all_guideline_data fixture
        guidelines_data = {
            "gl-markup-semantics": {
                "id": "gl-markup-semantics",
                "sortKey": "gl-markup-semantics",
                "src_path": "test/guidelines/gl-markup-semantics.yaml",
                "title": {"ja": "文書構造を適切に示すマークアップ、実装を行う", "en": "Semantic Markup"},
                "guideline": {"ja": "セマンティックなマークアップ", "en": "Semantic Markup"},
                "intent": {"ja": "意図", "en": "Intent"},
                "category": "markup",
                "platform": ["web"]
            },
            "markup/semantics": {
                "id": "gl-markup-semantics",
                "sortKey": "gl-markup-semantics",
                "src_path": "test/guidelines/gl-markup-semantics.yaml",
                "title": {"ja": "文書構造を適切に示すマークアップ、実装を行う", "en": "Semantic Markup"},
                "guideline": {"ja": "セマンティックなマークアップ", "en": "Semantic Markup"},
                "intent": {"ja": "意図", "en": "Intent"},
                "category": "markup",
                "platform": ["web"]
            },
            "text/heading-label": {
                "id": "gl-text-heading-label",
                "sortKey": "gl-text-heading-label",
                "src_path": "test/guidelines/gl-text-heading-label.yaml",
                "title": {"ja": "見出しラベル", "en": "Heading Label"},
                "guideline": {"ja": "見出しラベルのガイドライン", "en": "Heading Label Guideline"},
                "intent": {"ja": "意図", "en": "Intent"},
                "category": "markup",
                "platform": ["web"]
            },
            "form/tab-order": {
                "id": "gl-form-tab-order",
                "sortKey": "gl-form-tab-order",
                "src_path": "test/guidelines/gl-form-tab-order.yaml",
                "title": {"ja": "フォームのタブ順序", "en": "Form Tab Order"},
                "guideline": {"ja": "フォームのタブ順序ガイドライン", "en": "Form Tab Order Guideline"},
                "intent": {"ja": "意図", "en": "Intent"},
                "category": "form",
                "platform": ["web"]
            }
        }

        if guideline_id not in guidelines_data:
            raise ValueError(f"Unknown Guideline ID: {guideline_id}")

        # Mock RelationshipManager for guideline creation
        with patch('freee_a11y_gl.models.content.RelationshipManager') as mock_rel_manager:
            mock_rel = MagicMock()
            mock_rel_manager.return_value = mock_rel

            # Create mock category based on guideline data
            mock_category = MagicMock()
            guideline_data = guidelines_data[guideline_id]
            category_id = guideline_data["category"]

            if category_id == "markup":
                mock_category.names = {"ja": "マークアップと実装", "en": "Markup and Implementation"}
                mock_category.id = "markup"
                mock_category.get_name.side_effect = lambda lang: {"ja": "マークアップと実装", "en": "Markup and Implementation"}[lang]
            elif category_id == "form":
                mock_category.names = {"ja": "フォーム", "en": "Form"}
                mock_category.id = "form"
                mock_category.get_name.side_effect = lambda lang: {"ja": "フォーム", "en": "Form"}[lang]
            elif category_id == "text":
                mock_category.names = {"ja": "テキスト", "en": "Text"}
                mock_category.id = "text"
                mock_category.get_name.side_effect = lambda lang: {"ja": "テキスト", "en": "Text"}[lang]

            def mock_get_related_objects(obj, relation_type):
                if relation_type == "category":
                    return [mock_category]
                return []

            mock_rel.get_related_objects.side_effect = mock_get_related_objects
            mock_rel.get_sorted_related_objects.return_value = []

            return Guideline(guidelines_data[guideline_id])

    return _create_guideline
