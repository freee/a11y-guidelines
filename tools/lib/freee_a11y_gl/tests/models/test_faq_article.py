import datetime
from freee_a11y_gl.models.faq.article import Faq
from freee_a11y_gl.relationship_manager import RelationshipManager
from tests.models.base_test import BaseModelTest


class TestFaq(BaseModelTest):
    model_class = Faq
    sample_data = {
        "id": "faq1",
        "sortKey": "1",
        "src_path": "path/to/faq1.yaml",
        "updated": "2023-10-01",
        "title": {"ja": "FAQタイトル", "en": "FAQ Title"},
        "problem": {"ja": "問題", "en": "Problem"},
        "solution": {"ja": "解決策", "en": "Solution"},
        "explanation": {"ja": "説明", "en": "explanation"},
        "tags": ["axe"]
    }

    def test_init_specific(self, setup_faq_tags):
        """Test FAQ-specific initialization attributes."""
        faq = Faq(self.sample_data)
        assert faq.title == {"ja": "FAQタイトル", "en": "FAQ Title"}
        assert faq.problem == {"ja": "問題", "en": "Problem"}
        assert faq.solution == {"ja": "解決策", "en": "Solution"}
        assert faq.explanation == {"ja": "説明", "en": "explanation"}
        assert faq.updated == datetime.datetime.fromisoformat("2023-10-01")

        rel = RelationshipManager()
        tags = rel.get_related_objects(faq, "faq_tag")
        assert len(tags) == 1
        assert tags[0].id == "axe"

    def test_create_relationships(self, setup_faq_tags, all_guideline_data, all_check_data):
        """Test creating relationships with other objects."""
        mock_faq = {
            **self.sample_data,
            "guidelines": ["gl-markup-semantics"],
            "tags": ["axe"],
            "info": ["exp-tab-order-check"],
            "checks": ["0171"]
        }
        rel = RelationshipManager()
        faq = Faq(mock_faq)

        guidelines = rel.get_related_objects(faq, 'guideline')
        assert len(guidelines) == 1
        assert guidelines[0].id == 'gl-markup-semantics'

        tags = rel.get_related_objects(faq, 'faq_tag')
        assert len(tags) == 1
        assert tags[0].id == 'axe'

        info_refs = rel.get_related_objects(faq, 'info_ref')
        assert len(info_refs) == 1
        assert info_refs[0].id == 'exp-tab-order-check'

        checks = rel.get_related_objects(faq, 'check')
        assert len(checks) == 1
        assert checks[0].id == '0171'

    def test_link_data(self, faq_factory):
        """Test link data generation for FAQ."""
        faq = faq_factory("p0009")
        link_data = faq.link_data("https://example.com")
        expected_link_data = {
            "text": {
                "ja": "Safariでのみ、Tabキーによるフォーカス移動の挙動がおかしい",
                "en": "Focus Movement by Tab Key Is Strange Only in Safari"
            },
            "url": {
                "ja": "https://example.com/faq/articles/p0009.html",
                "en": "https://example.com/faq/articles/p0009.html"
            }
        }
        assert link_data == expected_link_data

    def test_template_data(self, faq_factory):
        """Test template data generation for FAQ."""
        rel = RelationshipManager()
        faq = faq_factory("p0009")
        faq_factory("d0001")
        rel.resolve_faqs()
        template_data = faq.template_data("ja")
        expected_template_data = {
            'id': 'p0009',
            'title': 'Safariでのみ、Tabキーによるフォーカス移動の挙動がおかしい',
            'problem': 'SafariでWebページを表示して、 :kbd:`Tab` キーや :kbd:`Shift+Tab` キーでフォーカスを移動すると、本来フォーカスされるべきなのにスキップされる要素がある。\nGoogle Chromeや他のブラウザーでは適切にフォーカス移動できているが、コンテンツ側で何らかの対応が必要か。',
            'solution': 'デフォルト設定でSafariを使用している場合の挙動なので対処は不要。\n:kbd:`option+Tab` と :kbd:`Shift+option+Tab` キーを使用すると他のブラウザーと同様の挙動になる。',
            'explanation': 'デフォルト設定でSafariを使用している場合、リンクやボタンなど、本来 :kbd:`Tab` キーや :kbd:`Shift+Tab` キーでフォーカスを移動できるはずの要素の一部に、フォーカスが移動できません。\n代わりに、 :kbd:`option+Tab` キーや :kbd:`Shift+option+Tab` キーを使用すると、他のブラウザーと同様にフォーカスを移動できます。\n\nフォーカス順序のチェックをする場合、通常は他のブラウザーで確認して問題なければ問題はありません。\nもしSafariでチェックを実施する必要がある場合は、 :kbd:`option+Tab` キーと :kbd:`Shift+option+Tab` キーを使用して確認します。\n\nなお、macOS上のSafariを使用している場合は、以下のいずれかの設定をすることで、 :kbd:`Tab` キーと :kbd:`Shift+Tab` キーの挙動が他のブラウザーと同様になります。\n\n*  Safariの :menuselection:`設定 --> 詳細` で、「Tabキーを押したときにWebページ上の各項目を強調表示」にチェックを入れる\n*  macOSの :menuselection:`環境設定 --> アクセシビリティ --> キーボード` で「フルキーボードアクセス」を有効にする',
            'updated_str': '2025年3月25日',
            'tags': ['keyboard-operation'],
            'guidelines': [
                {'category': '動的コンテンツ', 'guideline': 'gl-dynamic-content-focus'},
                {'category': 'フォーム', 'guideline': 'gl-form-dynamic-content-focus'},
                {'category': 'フォーム', 'guideline': 'gl-form-keyboard-operable'},
                {'category': 'フォーム', 'guideline': 'gl-form-tab-order'},
                {'category': '入力ディバイス', 'guideline': 'gl-input-device-focus'},
                {'category': '入力ディバイス', 'guideline': 'gl-input-device-focus-indicator'},
                {'category': '入力ディバイス', 'guideline': 'gl-input-device-keyboard-operable'},
                {'category': 'リンク', 'guideline': 'gl-link-tab-order'}
            ]
        }
        assert_keys = ["id", "title", "problem", "solution", "explanation", "updated_str", "tags", "guidelines"]
        for key in assert_keys:
            assert template_data[key] == expected_template_data[key]

    def test_list_all(self, setup_faq_tags):
        """Test listing all FAQs by date."""
        faq1 = {
            **self.sample_data,
            "updated": "2023-10-01"
        }
        faq2 = {
            **self.sample_data,
            "id": "faq2",
            "sortKey": "2",
            "updated": "2023-09-01",
            "src_path": "path/to/faq2.yaml"
        }
        faq3 = {
            **self.sample_data,
            "id": "faq3",
            "sortKey": "3",
            "updated": "2023-12-01",
            "src_path": "path/to/faq3.yaml"
        }
        Faq(faq1)
        Faq(faq2)
        Faq(faq3)

        # Test sorting by ID
        all_faqs = Faq.list_all()
        assert len(all_faqs) == 3
        assert all_faqs[0].id == "faq1"
        assert all_faqs[1].id == "faq2"
        assert all_faqs[2].id == "faq3"

        # Test sorting by date
        all_faqs_by_date = Faq.list_all(sort_by="date")
        assert len(all_faqs_by_date) == 3
        assert all_faqs_by_date[0].id == "faq3"
        assert all_faqs_by_date[1].id == "faq1"
        assert all_faqs_by_date[2].id == "faq2"
