import pytest
from pathlib import Path
from freee_a11y_gl.models.content import Guideline
from freee_a11y_gl.relationship_manager import RelationshipManager
from freee_a11y_gl.models.faq.article import Faq
from ..models.base_test import BaseModelTest

class TestGuideline(BaseModelTest):
    model_class = Guideline
    sample_data = {
        "id": "guideline1",
        "sortKey": "1",
        "category": "markup",
        "title": {"ja": "ガイドラインタイトル", "en": "Guideline Title"},
        "guideline": {"ja": "ガイドラインの内容", "en": "Guideline content"},
        "intent": {"ja": "ガイドラインの意図", "en": "Guideline intent"},
        "platform": ["web", "mobile"],
        "checks": ["0151", "0171"],
        "sc": ["1.1.1", "2.1.2"],
        "info": ["exp-markup-semantics", "exp-link-tab-order"],
        "src_path": "path/to/guideline.yaml"
    }

    def test_init_specific(self, all_check_data, setup_categories, setup_wcag_sc):
        """Test Guideline-specific initialization attributes."""
        guideline = Guideline(self.sample_data)
        assert guideline.data.title == {"ja": "ガイドラインタイトル", "en": "Guideline Title"}
        assert guideline.data.guideline == {"ja": "ガイドラインの内容", "en": "Guideline content"}
        assert guideline.data.intent == {"ja": "ガイドラインの意図", "en": "Guideline intent"}
        assert guideline.data.platform == ["web", "mobile"]
        assert guideline.object_type == "guideline"

        rel = RelationshipManager()
        category = rel.get_related_objects(guideline, "category")[0]
        assert category.names == {"ja": "マークアップと実装", "en": "Markup and Implementation"}

        scs = rel.get_related_objects(guideline, "wcag_sc")
        assert len(scs) == 2
        assert set(self.sample_data["sc"]) == set([sc.id for sc in scs])

        inforefs = rel.get_related_objects(guideline, "info_ref")
        assert len(inforefs) == 2
        assert set(self.sample_data["info"]) == set([info.ref for info in inforefs])

    def test_template_data(self, guideline_factory, setup_faq_tags):
        """Test generating template data."""
        sample_guideline = guideline_factory("markup/semantics")
        mock_faq = {
            "id": "faq1",
            "object_type": "faq",
            "sortKey": "1",
            "src_path": "path/to/faq1.yaml",
            "updated": "2023-10-01",
            "title": {"ja": "FAQタイトル", "en": "FAQ Title"},
            "problem": {"ja": "問題", "en": "Problem"},
            "solution": {"ja": "解決策", "en": "Solution"},
            "explanation": {"ja": "説明", "en": "explanation"},
            "guidelines": ["gl-markup-semantics"],
            "tags": ["axe"]
        }
        Faq(mock_faq)
        template_data = sample_guideline.template_data("ja")
        expected_template_data = {
            'id': 'gl-markup-semantics',
            'title': '文書構造を適切に示すマークアップ、実装を行う',
            'platform': 'Web、モバイル',
            'guideline': '静的なテキスト・コンテンツは、文書構造などのセマンティクスを適切に表現するHTMLの要素やコンポーネントで実装する。',
            'intent': 'スクリーン・リーダーなどの支援技術がコンテンツを正しく認識し、ユーザーに適切な形で提示できるようにする。\n\n-  適切なマークアップにより、スクリーン・リーダーで見出しや箇条書きの項目を探しやすくなる。\n-  スクリーン・リーダーなどの支援技術には、見出しやリンクの一覧表示機能など、適切なマークアップを前提に実装されている機能がある。',
            'category': 'マークアップと実装',
            'checks': [
                {
                    'id': '0541',
                    'check': '見出しとして表現されるべきものが、設計資料で明示されている。',
                    'severity': '[NORMAL]',
                    'target': 'デザイン',
                    'platform': 'Web、モバイル'
                },
                # ... (その他のチェック項目は省略)
            ],
            'faqs': ["faq1"]
        }
        check_keys = ["id", "title", "platform", "guideline", "intent", "category", "faqs"]
        for key in check_keys:
            assert key in template_data
            assert template_data[key] == expected_template_data[key]

    def test_get_category_and_id(self, guideline_factory):
        """Test getting category and ID."""
        sample_guideline = guideline_factory("text/heading-label")
        category_data = sample_guideline.get_category_and_id("ja")
        assert category_data["category"] == "テキスト"
        assert category_data["guideline"] == "gl-text-heading-label"

    def test_link_data(self, guideline_factory):
        """Test generating link data."""
        sample_guideline = guideline_factory("form/tab-order")
        baseurl = "https://example.com"
        rel = RelationshipManager()
        category = rel.get_related_objects(sample_guideline, "category")[0]
        category_id = category.id
        category_name_ja = category.get_name("ja")
        category_name_en = category.get_name("en")
        expected_link_data = {
            "text": {
                "ja": f"{category_name_ja}：{sample_guideline.data.title['ja']}",
                "en": f"{category_name_en}: {sample_guideline.data.title['en']}"
            },
            "url": {
                "ja": f"{baseurl}/categories/{category_id}.html#{sample_guideline.id}",
                "en": f"{baseurl}/en/categories/{category_id}.html#{sample_guideline.id}"
            }
        }
        link_data = sample_guideline.link_data(baseurl)
        assert link_data == expected_link_data
