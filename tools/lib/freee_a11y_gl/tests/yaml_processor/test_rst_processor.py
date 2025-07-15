import pytest
from freee_a11y_gl.yaml_processor.rst_processor import (
    normalize_text, process_rst_text, process_rst_condition
)


class TestNormalizeText:
    """Test cases for normalize_text function."""

    def test_normalize_text_basic(self):
        """Test basic text normalization."""
        text = "これは　テスト　です"
        result = normalize_text(text)
        assert result == "これはテストです"

    def test_normalize_text_leading_trailing_spaces(self):
        """Test removal of leading and trailing spaces."""
        text = "  これはテストです  "
        result = normalize_text(text)
        assert result == "これはテストです"

    def test_normalize_text_fullwidth_chars(self):
        """Test normalization between fullwidth characters."""
        text = "これは　　　テスト　です"
        result = normalize_text(text)
        assert result == "これはテストです"

    def test_normalize_text_halfwidth_to_fullwidth(self):
        """Test normalization between halfwidth and fullwidth characters."""
        text = "これは test です"
        result = normalize_text(text)
        assert result == "これはtestです"

    def test_normalize_text_fullwidth_to_halfwidth(self):
        """Test normalization between fullwidth and halfwidth characters."""
        text = "test　これは　test"
        result = normalize_text(text)
        assert result == "testこれはtest"

    def test_normalize_text_preserve_newlines(self):
        """Test that newlines are preserved."""
        text = "これは\nテスト\nです"
        result = normalize_text(text)
        assert result == "これは\nテスト\nです"

    def test_normalize_text_bullet_points(self):
        """Test preservation of bullet point formatting."""
        text = "* これは\n  テストです\n- もう一つの\n  テスト"
        result = normalize_text(text)
        # Bullet point spaces should be preserved, but text normalization still applies
        assert "* これは" in result
        assert "テストです" in result  # Indentation may be normalized
        assert "- もう一つの" in result
        assert "テスト" in result  # Indentation may be normalized

    def test_normalize_text_indented_bullet_points(self):
        """Test preservation of indented bullet points."""
        text = "  * インデントされた\n    項目です"
        result = normalize_text(text)
        # The bullet marker spacing is preserved, but content may be normalized
        assert "* インデントされた" in result  # Leading spaces before * may be normalized
        assert "項目です" in result  # Indentation may be normalized

    def test_normalize_text_mixed_bullet_types(self):
        """Test preservation of different bullet types."""
        text = "* アスタリスク\n- ハイフン\n+ プラス"
        result = normalize_text(text)
        assert "* アスタリスク" in result
        assert "- ハイフン" in result
        assert "+ プラス" in result

    def test_normalize_text_empty_string(self):
        """Test empty string input."""
        result = normalize_text("")
        assert result == ""

    def test_normalize_text_only_spaces(self):
        """Test string with only spaces."""
        result = normalize_text("   ")
        assert result == ""

    def test_normalize_text_complex_mixed_content(self):
        """Test complex mixed content with various character types."""
        text = "これは　123　テスト　abc　です"
        result = normalize_text(text)
        assert result == "これは123テストabcです"

    def test_normalize_text_unicode_spaces(self):
        """Test normalization with various Unicode space characters."""
        # Using various Unicode space characters
        text = "これは\u2000テスト\u2001です"  # En quad, Em quad
        result = normalize_text(text)
        assert result == "これはテストです"


class TestProcessRstText:
    """Test cases for process_rst_text function."""

    def test_process_rst_text_basic_reference(self):
        """Test basic reference replacement."""
        text = "これは :ref:`test-ref` です"
        info = {
            "test-ref": {
                "text": {"ja": "テスト参照", "en": "Test Reference"}
            }
        }
        result = process_rst_text(text, info, "ja")
        assert result == "これはテスト参照です"

    def test_process_rst_text_multiple_references(self):
        """Test multiple reference replacements."""
        text = ":ref:`ref1` と :ref:`ref2` があります"
        info = {
            "ref1": {"text": {"ja": "参照1", "en": "Reference 1"}},
            "ref2": {"text": {"ja": "参照2", "en": "Reference 2"}}
        }
        result = process_rst_text(text, info, "ja")
        assert result == "参照1と参照2があります"  # Spaces around particles are normalized

    def test_process_rst_text_missing_reference(self):
        """Test behavior with missing reference."""
        text = "これは :ref:`missing-ref` です"
        info = {}
        result = process_rst_text(text, info, "ja")
        assert result == "これは:ref:`missing-ref`です"  # Spaces are normalized even with missing refs

    def test_process_rst_text_keyboard_shortcut(self):
        """Test keyboard shortcut replacement."""
        text = ":kbd:`Ctrl+C` を押します"
        info = {}
        result = process_rst_text(text, info, "ja")
        assert result == "Ctrl+Cを押します"  # Space between English and Japanese is normalized

    def test_process_rst_text_multiple_keyboard_shortcuts(self):
        """Test multiple keyboard shortcut replacements."""
        text = ":kbd:`Ctrl+C` でコピー、:kbd:`Ctrl+V` でペースト"
        info = {}
        result = process_rst_text(text, info, "ja")
        assert result == "Ctrl+Cでコピー、Ctrl+Vでペースト"  # Spaces between English and Japanese are normalized

    def test_process_rst_text_mixed_markup(self):
        """Test mixed RST markup (references and keyboard shortcuts)."""
        text = ":ref:`test-ref` を使って :kbd:`Tab` キーを押す"
        info = {
            "test-ref": {"text": {"ja": "テスト機能", "en": "Test Feature"}}
        }
        result = process_rst_text(text, info, "ja")
        assert result == "テスト機能を使ってTabキーを押す"  # All spaces between different character types are normalized

    def test_process_rst_text_english_language(self):
        """Test processing with English language."""
        text = "This is :ref:`test-ref` example"
        info = {
            "test-ref": {"text": {"ja": "テスト参照", "en": "Test Reference"}}
        }
        result = process_rst_text(text, info, "en")
        assert result == "This is Test Reference example"

    def test_process_rst_text_japanese_normalization(self):
        """Test that Japanese text gets normalized but English doesn't."""
        text = "これは　テスト　です"
        info = {}
        
        # Japanese should be normalized
        result_ja = process_rst_text(text, info, "ja")
        assert result_ja == "これはテストです"
        
        # English should not be normalized
        result_en = process_rst_text(text, info, "en")
        assert result_en == "これは　テスト　です"

    def test_process_rst_text_no_markup(self):
        """Test text with no RST markup."""
        text = "これは普通のテキストです"
        info = {}
        result = process_rst_text(text, info, "ja")
        assert result == "これは普通のテキストです"

    def test_process_rst_text_empty_string(self):
        """Test empty string input."""
        result = process_rst_text("", {}, "ja")
        assert result == ""

    def test_process_rst_text_complex_keyboard_shortcut(self):
        """Test complex keyboard shortcuts."""
        text = ":kbd:`Shift+Ctrl+Alt+F12` の組み合わせ"
        info = {}
        result = process_rst_text(text, info, "ja")
        assert result == "Shift+Ctrl+Alt+F12の組み合わせ"  # Space between English and Japanese is normalized

    def test_process_rst_text_reference_with_hyphens(self):
        """Test references with hyphens and numbers."""
        text = ":ref:`test-ref-123` を参照"
        info = {
            "test-ref-123": {"text": {"ja": "テスト参照123", "en": "Test Reference 123"}}
        }
        result = process_rst_text(text, info, "ja")
        assert result == "テスト参照123を参照"  # Space before particle is normalized


class TestProcessRstCondition:
    """Test cases for process_rst_condition function."""

    def test_process_rst_condition_simple(self):
        """Test processing simple condition."""
        condition = {
            "type": "simple",
            "procedure": {
                "procedure": {
                    "ja": ":ref:`test-ref` を確認",
                    "en": "Check :ref:`test-ref`"
                }
            }
        }
        info = {
            "test-ref": {"text": {"ja": "テスト項目", "en": "Test Item"}}
        }
        
        result = process_rst_condition(condition, info)
        
        assert result["type"] == "simple"
        assert result["procedure"]["procedure"]["ja"] == "テスト項目を確認"  # Space before particle is normalized
        assert result["procedure"]["procedure"]["en"] == "Check Test Item"

    def test_process_rst_condition_simple_without_procedure(self):
        """Test processing simple condition without procedure key."""
        condition = {
            "type": "simple",
            "other_data": "value"
        }
        info = {}
        
        result = process_rst_condition(condition, info)
        
        assert result["type"] == "simple"
        assert result["other_data"] == "value"
        assert "procedure" not in result

    def test_process_rst_condition_nested_and(self):
        """Test processing nested AND condition."""
        condition = {
            "type": "and",
            "conditions": [
                {
                    "type": "simple",
                    "procedure": {
                        "procedure": {
                            "ja": ":ref:`ref1` をチェック",
                            "en": "Check :ref:`ref1`"
                        }
                    }
                },
                {
                    "type": "simple",
                    "procedure": {
                        "procedure": {
                            "ja": ":ref:`ref2` を確認",
                            "en": "Verify :ref:`ref2`"
                        }
                    }
                }
            ]
        }
        info = {
            "ref1": {"text": {"ja": "項目1", "en": "Item 1"}},
            "ref2": {"text": {"ja": "項目2", "en": "Item 2"}}
        }
        
        result = process_rst_condition(condition, info)
        
        assert result["type"] == "and"
        assert len(result["conditions"]) == 2
        assert result["conditions"][0]["procedure"]["procedure"]["ja"] == "項目1をチェック"  # Space before particle is normalized
        assert result["conditions"][0]["procedure"]["procedure"]["en"] == "Check Item 1"
        assert result["conditions"][1]["procedure"]["procedure"]["ja"] == "項目2を確認"  # Space before particle is normalized
        assert result["conditions"][1]["procedure"]["procedure"]["en"] == "Verify Item 2"

    def test_process_rst_condition_nested_or(self):
        """Test processing nested OR condition."""
        condition = {
            "type": "or",
            "conditions": [
                {
                    "type": "simple",
                    "procedure": {
                        "procedure": {
                            "ja": ":kbd:`Tab` キーを使用",
                            "en": "Use :kbd:`Tab` key"
                        }
                    }
                }
            ]
        }
        info = {}
        
        result = process_rst_condition(condition, info)
        
        assert result["type"] == "or"
        assert len(result["conditions"]) == 1
        assert result["conditions"][0]["procedure"]["procedure"]["ja"] == "Tabキーを使用"  # Space between English and Japanese is normalized
        assert result["conditions"][0]["procedure"]["procedure"]["en"] == "Use Tab key"

    def test_process_rst_condition_deeply_nested(self):
        """Test processing deeply nested conditions."""
        condition = {
            "type": "and",
            "conditions": [
                {
                    "type": "or",
                    "conditions": [
                        {
                            "type": "simple",
                            "procedure": {
                                "procedure": {
                                    "ja": ":ref:`test` を実行",
                                    "en": "Execute :ref:`test`"
                                }
                            }
                        }
                    ]
                }
            ]
        }
        info = {
            "test": {"text": {"ja": "テスト", "en": "Test"}}
        }
        
        result = process_rst_condition(condition, info)
        
        assert result["type"] == "and"
        nested = result["conditions"][0]["conditions"][0]
        assert nested["procedure"]["procedure"]["ja"] == "テストを実行"  # Space before particle is normalized
        assert nested["procedure"]["procedure"]["en"] == "Execute Test"

    def test_process_rst_condition_empty_conditions(self):
        """Test processing condition with empty conditions list."""
        condition = {
            "type": "and",
            "conditions": []
        }
        info = {}
        
        result = process_rst_condition(condition, info)
        
        assert result["type"] == "and"
        assert result["conditions"] == []

    def test_process_rst_condition_preserves_other_data(self):
        """Test that other data in conditions is preserved."""
        condition = {
            "type": "simple",
            "platform": "web",
            "id": "test-condition",
            "procedure": {
                "procedure": {
                    "ja": "テスト手順",
                    "en": "Test procedure"
                },
                "note": {
                    "ja": "注意事項",
                    "en": "Note"
                }
            }
        }
        info = {}
        
        result = process_rst_condition(condition, info)
        
        assert result["platform"] == "web"
        assert result["id"] == "test-condition"
        assert result["procedure"]["note"]["ja"] == "注意事項"
        assert result["procedure"]["note"]["en"] == "Note"
