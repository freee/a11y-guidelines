import pytest
from pathlib import Path
from freee_a11y_gl.models.content import Guideline
from freee_a11y_gl.relationship_manager import RelationshipManager
from freee_a11y_gl.models.faq.article import Faq
from .base_test import BaseModelTest

@pytest.mark.usefixtures("all_check_data")
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
        "checks": ["0171", "0172"],
        "sc": ["1.1.1", "2.1.1"],
        "info": ["exp-markup-semantics", "exp-link-tab-order"],
        "src_path": "path/to/guideline.yaml"
    }

    def test_init_specific(self, all_check_data, setup_categories, setup_wcag_sc):
        """Test Guideline-specific initialization attributes."""
        guideline = Guideline(self.sample_data)
        
        # Test basic data attributes
        assert guideline.data.title == {"ja": "ガイドラインタイトル", "en": "Guideline Title"}
        assert guideline.data.guideline == {"ja": "ガイドラインの内容", "en": "Guideline content"}
        assert guideline.data.intent == {"ja": "ガイドラインの意図", "en": "Guideline intent"}
        assert guideline.data.platform == ["web", "mobile"]
        assert guideline.object_type == "guideline"
        
        # Test that relationships are established (basic check)
        rel = RelationshipManager()
        
        # Check that category relationship exists
        categories = rel.get_related_objects(guideline, "category")
        assert len(categories) > 0
        category = categories[0]
        assert category.names == {"ja": "マークアップと実装", "en": "Markup and Implementation"}
        
        # Check that WCAG SC relationships exist (we know there are some from setup)
        scs = rel.get_related_objects(guideline, "wcag_sc")
        assert len(scs) >= 2  # At least the ones we expect
        
        # Check that info references exist
        inforefs = rel.get_related_objects(guideline, "info_ref")
        assert len(inforefs) >= 2  # At least the ones we expect

    def test_template_data(self, guideline_factory, setup_faq_tags):
        """Test generating template data."""
        from unittest.mock import patch, MagicMock
        
        # Create a mock category
        mock_category = MagicMock()
        mock_category.names = {"ja": "マークアップと実装", "en": "Markup and Implementation"}
        
        # Create mock FAQ
        mock_faq = MagicMock()
        mock_faq.id = "faq1"
        
        # Create mock Config
        mock_config = MagicMock()
        mock_config.get_platform_name.return_value = "Web"
        mock_config.get_list_separator.return_value = "、"
        
        with patch('freee_a11y_gl.models.content.RelationshipManager') as mock_rel_manager, \
             patch('freee_a11y_gl.models.content.Config', mock_config):
            
            mock_rel = MagicMock()
            mock_rel_manager.return_value = mock_rel
            
            def mock_get_related_objects(obj, relation_type):
                if relation_type == "category":
                    return [mock_category]
                elif relation_type == "info_ref":
                    return []
                return []
            
            def mock_get_sorted_related_objects(obj, relation_type, key=None):
                if relation_type == "check":
                    return []
                elif relation_type == "wcag_sc":
                    return []
                elif relation_type == "faq":
                    return [mock_faq]  # Return FAQ to ensure "faqs" key is added
                return []
            
            mock_rel.get_related_objects.side_effect = mock_get_related_objects
            mock_rel.get_sorted_related_objects.side_effect = mock_get_sorted_related_objects
            
            sample_guideline = guideline_factory("markup/semantics")
            template_data = sample_guideline.template_data("ja")
            
            # Basic checks that the template data structure is correct
            assert "id" in template_data
            assert "title" in template_data
            assert "platform" in template_data
            assert "guideline" in template_data
            assert "intent" in template_data
            assert "category" in template_data
            assert "faqs" in template_data
            assert "checks" in template_data
            
            assert template_data["id"] == "gl-markup-semantics"
            assert template_data["category"] == "マークアップと実装"
            assert template_data["faqs"] == ["faq1"]

    def test_get_category_and_id(self, guideline_factory):
        """Test getting category and ID."""
        from unittest.mock import patch, MagicMock
        
        # Create mock category
        mock_category = MagicMock()
        mock_category.get_name.return_value = "マークアップと実装"
        
        with patch('freee_a11y_gl.models.content.RelationshipManager') as mock_rel_manager:
            mock_rel = MagicMock()
            mock_rel_manager.return_value = mock_rel
            mock_rel.get_related_objects.return_value = [mock_category]
            
            sample_guideline = guideline_factory("text/heading-label")
            category_data = sample_guideline.get_category_and_id("ja")
            assert category_data["category"] == "マークアップと実装"
            assert category_data["guideline"] == "gl-text-heading-label"

    def test_link_data(self, guideline_factory):
        """Test generating link data."""
        from unittest.mock import patch, MagicMock
        
        # Create mock category
        mock_category = MagicMock()
        mock_category.id = "form"
        mock_category.get_name.side_effect = lambda lang: {"ja": "フォーム", "en": "Form"}[lang]
        
        # Create mock Config
        mock_config = MagicMock()
        mock_config.get_text_separator.side_effect = lambda lang: {"ja": "：", "en": ": "}[lang]
        mock_config.get_guidelines_path.return_value = "/categories/"
        mock_config.get_base_url.side_effect = lambda lang: {"ja": "", "en": "/en"}[lang]
        
        with patch('freee_a11y_gl.models.content.RelationshipManager') as mock_rel_manager, \
             patch('freee_a11y_gl.models.content.Config', mock_config):
            
            mock_rel = MagicMock()
            mock_rel_manager.return_value = mock_rel
            mock_rel.get_related_objects.return_value = [mock_category]
            
            sample_guideline = guideline_factory("form/tab-order")
            baseurl = "https://example.com"
            
            link_data = sample_guideline.link_data(baseurl)
            
            # Check that the basic structure is correct
            assert "text" in link_data
            assert "url" in link_data
            assert "ja" in link_data["text"]
            assert "en" in link_data["text"]
            assert "ja" in link_data["url"]
            assert "en" in link_data["url"]
            
            # Check that the text contains the expected elements
            assert "フォーム" in link_data["text"]["ja"]
            assert sample_guideline.data.title["ja"] in link_data["text"]["ja"]
            assert "Form" in link_data["text"]["en"]
            assert sample_guideline.data.title["en"] in link_data["text"]["en"]
            
            # Check that URLs contain the expected elements
            assert baseurl in link_data["url"]["ja"]
            assert sample_guideline.id in link_data["url"]["ja"]
            assert baseurl in link_data["url"]["en"]
            assert sample_guideline.id in link_data["url"]["en"]
