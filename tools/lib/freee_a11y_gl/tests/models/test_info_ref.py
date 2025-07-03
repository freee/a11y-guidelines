import pytest
from freee_a11y_gl.models.reference import InfoRef
from freee_a11y_gl.relationship_manager import RelationshipManager
from freee_a11y_gl.models.content import Guideline
from freee_a11y_gl.models.faq.article import Faq

class TestInfoRef:
    def test_singleton_behavior(self):
        """Test singleton behavior."""
        ref1 = InfoRef("exp-test")
        ref2 = InfoRef("exp-test")
        assert ref1 is ref2

    def test_init_internal_reference(self):
        """Test initialization of internal reference."""
        ref = InfoRef("exp-test")
        assert ref.ref == "exp-test"
        assert ref.ref_type == "internal"
        assert ref.link is None

    def test_init_external_reference(self):
        """Test initialization of external reference."""
        ref = InfoRef("ext-test")
        assert ref.ref == "ext-test"
        assert ref.ref_type == "external"
        assert ref.link is None

    def test_refstring(self):
        """Test generating reference string."""
        ref = InfoRef("exp-test")
        assert ref.get_refstring() == ":ref:`exp-test`"

    @pytest.mark.usefixtures("mock_infolabels")
    def test_link_data_internal(self):
        """Test getting link data for internal reference."""
        ref = InfoRef("exp-tab-order-check")
        ref.set_link({"text": {"ja": "タイトル", "en": "Title"}})
        link_data = ref.get_link_data("ja")
        assert link_data["text"] == "タイトル"
        assert "url" in link_data

    def test_link_data_external(self):
        """Test getting link data for external reference."""
        ref = InfoRef("ext-wcag-1-1-1")
        ref.set_link({
            "text": {"ja": "外部リンク", "en": "External Link"},
            "url": "https://example.com"
        })
        link_data = ref.get_link_data("ja")
        assert link_data["text"] == "外部リンク"
        assert link_data["url"] == "https://example.com"

    def test_set_link(self):
        """Test setting link data."""
        ref = InfoRef("exp-test")
        link_data = {"text": {"ja": "タイトル", "en": "Title"}}
        ref.set_link(link_data)
        assert ref.link == link_data

    def test_list_all_internal(self):
        """Test listing all internal references."""
        refs = InfoRef.list_all_internal()
        assert isinstance(refs, list)
        assert all(isinstance(ref, InfoRef) for ref in refs)
        assert all(ref.ref_type == "internal" for ref in refs)

    def test_list_all_external(self):
        """Test listing all external references."""
        refs = InfoRef.list_all_external()
        assert isinstance(refs, list)
        assert all(isinstance(ref, InfoRef) for ref in refs)
        assert all(ref.ref_type == "external" for ref in refs)

    def test_list_has_guidelines(self, setup_categories, all_guideline_data):
        """Test listing references that have guidelines."""
        # Setup a guideline with info references
        guideline_data = {
            "id": "gl-test",
            "sortKey": "1",
            "category": "form",
            "title": {"ja": "テスト", "en": "Test"},
            "guideline": {"ja": "ガイドライン", "en": "Guideline"},
            "intent": {"ja": "意図", "en": "Intent"},
            "platform": ["web"],
            "info": ["exp-tab-order-check"],
            "src_path": "path/to/test.yaml"
        }
        Guideline(guideline_data)
        
        # Test the method
        refs = InfoRef.list_has_guidelines()
        assert isinstance(refs, list)
        assert len(refs) > 0
        assert all(isinstance(ref, InfoRef) for ref in refs)

    def test_list_has_faqs(self, setup_categories, setup_faq_tags):
        """Test listing references that have FAQs."""
        # Setup a FAQ with info references
        faq_data = {
            "id": "faq1",
            "sortKey": "1",
            "src_path": "path/to/faq1.yaml",
            "updated": "2023-10-01",
            "title": {"ja": "FAQタイトル", "en": "FAQ Title"},
            "problem": {"ja": "問題", "en": "Problem"},
            "solution": {"ja": "解決策", "en": "Solution"},
            "explanation": {"ja": "説明", "en": "explanation"},
            "info": ["exp-tab-order-check"],
            "tags": ["axe"]
        }
        Faq(faq_data)

        # Test the method
        refs = InfoRef.list_has_faqs()
        assert isinstance(refs, list)
        assert len(refs) > 0
        assert all(isinstance(ref, InfoRef) for ref in refs)
