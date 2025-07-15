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
        assert ref.internal == True
        assert ref.ref_data is None

    def test_init_external_reference(self):
        """Test initialization of external reference."""
        ref = InfoRef("https://example.com")
        assert ref.ref == "https://example.com"
        assert ref.internal == False
        assert ref.ref_data is None

    def test_refstring(self):
        """Test generating reference string."""
        ref = InfoRef("exp-test")
        assert ref.refstring() == ":ref:`exp-test`"

    def test_refstring_external_url(self):
        """Test generating reference string for external URL."""
        ref = InfoRef("https://example.com")
        assert ref.refstring() == "https://example.com"

    def test_refstring_pipe_reference(self):
        """Test generating reference string for |name| style reference."""
        ref = InfoRef("|example|")
        assert ref.refstring() == "|example|"

    def test_link_data_internal(self):
        """Test getting link data for internal reference."""
        ref = InfoRef("exp-tab-order-check")
        link_data = ref.link_data()
        assert "text" in link_data
        assert "url" in link_data
        assert link_data["text"]["ja"] == ":ref:`exp-tab-order-check`"
        assert link_data["url"]["ja"] == ""

    def test_link_data_external_url(self):
        """Test getting link data for external URL reference."""
        ref = InfoRef("https://example.com")
        link_data = ref.link_data()
        assert "text" in link_data
        assert "url" in link_data
        assert link_data["text"]["ja"] == "https://example.com"
        assert link_data["url"]["ja"] == "https://example.com"

    def test_link_data_with_ref_data(self):
        """Test getting link data when ref_data is set."""
        ref = InfoRef("exp-test")
        test_data = {
            "text": {"ja": "テストタイトル", "en": "Test Title"},
            "url": {"ja": "https://ja.example.com", "en": "https://en.example.com"}
        }
        ref.ref_data = test_data
        link_data = ref.link_data()
        assert link_data["text"]["ja"] == "テストタイトル"
        assert link_data["url"]["ja"] == "https://ja.example.com"

    def test_set_link(self):
        """Test setting link data."""
        ref = InfoRef("exp-test")
        link_data = {
            "text": {"ja": "タイトル", "en": "Title"},
            "url": {"ja": "https://ja.example.com", "en": "https://en.example.com"}
        }
        ref.set_link(link_data)
        assert ref.ref_data == link_data

    def test_list_all_internal(self):
        """Test listing all internal references."""
        refs = InfoRef.list_all_internal()
        assert isinstance(refs, list)
        assert all(isinstance(ref, InfoRef) for ref in refs)
        assert all(ref.internal == True for ref in refs)

    def test_list_all_external(self):
        """Test listing all external references."""
        refs = InfoRef.list_all_external()
        assert isinstance(refs, list)
        assert all(isinstance(ref, InfoRef) for ref in refs)
        assert all(ref.internal == False for ref in refs)

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
