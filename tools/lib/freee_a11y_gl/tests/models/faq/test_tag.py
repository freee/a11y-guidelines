import pytest
from freee_a11y_gl.models.faq.tag import FaqTag
from freee_a11y_gl.models.faq.article import Faq
from freee_a11y_gl.relationship_manager import RelationshipManager

class TestFaqTag:
    @pytest.fixture(autouse=True)
    def setup(self, setup_faq_tags):
        """Setup FAQ tags for testing."""
        pass

    def test_init(self):
        """Test initialization of FaqTag."""
        tag_data = {
            "id": "axe",
            "names": {"en": "axe", "ja": "axe"}
        }
        tag = FaqTag("axe", tag_data)
        assert tag.id == "axe"
        assert tag.object_type == "faq_tag"
        assert tag.data.names == {"en": "axe", "ja": "axe"}

    def test_get_name(self):
        """Test getting name in specified language."""
        tag = FaqTag.get_by_id("axe")
        assert tag.get_name("ja") == "axe"
        assert tag.get_name("en") == "axe"

    def test_article_count(self, setup_categories):
        """Test counting articles with this tag."""
        tag = FaqTag.get_by_id("axe")
        # Create a FAQ with the tag
        mock_faq = {
            "id": "faq1",
            "sortKey": "1",
            "src_path": "path/to/faq1.yaml",
            "updated": "2023-10-01",
            "title": {"ja": "FAQタイトル", "en": "FAQ Title"},
            "problem": {"ja": "問題", "en": "Problem"},
            "solution": {"ja": "解決策", "en": "Solution"},
            "explanation": {"ja": "説明", "en": "Explanation"},
            "tags": ["axe"]
        }
        Faq(mock_faq)
        assert tag.article_count() == 1

    def test_template_data(self, setup_categories):
        """Test generating template data."""
        tag = FaqTag.get_by_id("axe")
        # Create a FAQ with the tag
        mock_faq = {
            "id": "faq1",
            "sortKey": "1",
            "src_path": "path/to/faq1.yaml",
            "updated": "2023-10-01",
            "title": {"ja": "FAQタイトル", "en": "FAQ Title"},
            "problem": {"ja": "問題", "en": "Problem"},
            "solution": {"ja": "解決策", "en": "Solution"},
            "explanation": {"ja": "説明", "en": "Explanation"},
            "tags": ["axe"]
        }
        Faq(mock_faq)
        
        template_data = tag.get_template_data("ja")
        assert template_data["id"] == "axe"
        assert template_data["name"] == "axe"
        assert len(template_data["articles"]) == 1
        assert template_data["articles"][0]["id"] == "faq1"

    def test_template_data_no_articles(self):
        """Test template data generation when no articles are associated."""
        tag = FaqTag.get_by_id("axe")
        template_data = tag.get_template_data("ja")
        assert template_data["id"] == "axe"
        assert template_data["name"] == "axe"
        assert len(template_data["articles"]) == 0

    def test_list_all(self):
        """Test listing all FAQ tags."""
        tags = FaqTag.list_all()
        assert len(tags) > 0
        assert all(isinstance(tag, FaqTag) for tag in tags)
        # タグの中にaxeが含まれていることを確認
        tag_ids = [tag.id for tag in tags]
        assert "axe" in tag_ids
