import time
from freee_a11y_gl.yaml_processor.rst_processor import (
    normalize_text, process_rst_text, process_rst_condition
)


class TestNormalizeText:
    """Test cases for normalize_text function.

    The normalize_text function is responsible for:
    1. Preserving fullwidth spaces (U+3000) in all contexts
    2. Removing regular spaces between different character types (Japanese/English/Numbers)
    3. Preserving bullet point formatting and indentation
    4. Handling various Unicode space characters appropriately

    Test Categories:
    - Basic functionality tests
    - Space preservation tests (fullwidth spaces)
    - Space removal tests (regular spaces between character types)
    - Edge case tests (empty strings, special characters)
    - Performance tests
    """

    def test_normalize_text_preserve_fullwidth_spaces_comprehensive(self):
        """Test comprehensive fullwidth space preservation in various contexts."""
        # Basic Japanese text with fullwidth spaces
        text1 = "これは　テスト　です"
        result1 = normalize_text(text1)
        assert result1 == text1

        # Complex mixed content with numbers and English
        text2 = "これは　123　テスト　abc　です"
        result2 = normalize_text(text2)
        assert result2 == text2

        # Explicit U+3000 fullwidth space testing
        text3 = "これは\u3000テスト\u3000です"
        result3 = normalize_text(text3)
        assert result3 == text3

        # Fullwidth spaces between same character types (Japanese)
        text4 = "これは\u3000テスト\u3000です"
        result4 = normalize_text(text4)
        assert result4 == text4

        # Fullwidth spaces between English characters
        text5 = "test\u3000hello\u3000world"
        result5 = normalize_text(text5)
        assert result5 == text5

    def test_normalize_text_leading_trailing_spaces(self):
        """Test removal of leading and trailing spaces."""
        text = "  これはテストです  "
        result = normalize_text(text)
        assert result == "これはテストです"

    def test_normalize_text_fullwidth_chars(self):
        """Test normalization with special fullwidth characters (numbers, symbols, letters)."""
        text = "テスト１２３！＠＃ＡＢＣ"
        result = normalize_text(text)
        # Special fullwidth characters should be preserved as-is
        assert result == text

    def test_normalize_text_remove_spaces_between_different_character_types(self):
        """Test space removal between different character types (Japanese/English/Numbers)."""
        # Japanese-English pattern
        text1 = "これは test です"
        result1 = normalize_text(text1)
        assert result1 == "これはtestです"

        # English-Japanese-English pattern
        text2 = "test これは test"
        result2 = normalize_text(text2)
        assert result2 == "testこれはtest"

        # Numbers and Japanese pattern
        text3 = "価格は 100 円です"
        result3 = normalize_text(text3)
        assert result3 == "価格は100円です"

    def test_normalize_text_preserve_newlines(self):
        """Test that newlines are preserved."""
        text = "これは\nテスト\nです"
        result = normalize_text(text)
        assert result == text

    def test_normalize_text_preserve_bullet_point_formatting_comprehensive(self):
        """Test comprehensive bullet point formatting preservation."""
        # Basic bullet points with different types
        text1 = "* これは\n  テストです\n- もう一つの\n  テスト"
        result1 = normalize_text(text1)
        assert result1 == text1  # Ensure formatting is preserved

        # Indented bullet points
        text2 = "  * インデントされた\n    項目です"
        result2 = normalize_text(text2)
        assert result2 == text2

        # Mixed bullet types
        text3 = "* アスタリスク\n- ハイフン\n+ プラス"
        result3 = normalize_text(text3)
        assert result3 == text3

        # Multi-level indented bullets
        text4 = "* レベル1\n  * レベル2\n    * レベル3\n      項目です"
        result4 = normalize_text(text4)
        assert result4 == text4

        # Tab-indented bullets
        text5 = "\t* タブインデント\n\t  項目です"
        result5 = normalize_text(text5)
        assert result5 == text5

        # Mixed space and tab indentation
        text6 = "  * スペース\n\t- タブ\n    + 混合"
        result6 = normalize_text(text6)
        assert result6 == text6

        # Fullwidth spaces in bullet content
        text7 = "* これは\u3000テスト\u3000です\n  * 次の\u3000項目"
        result7 = normalize_text(text7)
        assert result7 == text7

    def test_normalize_text_empty_string(self):
        """Test empty string input."""
        result = normalize_text("")
        assert result == ""

    def test_normalize_text_only_spaces(self):
        """Test string with only spaces."""
        result = normalize_text("   ")
        assert result == ""

    def test_normalize_text_remove_unicode_spaces(self):
        """Test removal of various Unicode space characters (excluding fullwidth space)."""
        # En quad, Em quad
        text1 = "これは\u2000テスト\u2001です"
        result1 = normalize_text(text1)
        assert result1 == "これはテストです"

        # En space, Em space, Thin space
        text2 = "これは\u2002test\u2003です\u2009end"
        result2 = normalize_text(text2)
        assert result2 == "これはtestですend"

        # Mixed Unicode spaces between character types
        text3 = "test\u2004これは\u2005です"  # Three-per-em space, Four-per-em space
        result3 = normalize_text(text3)
        assert result3 == "testこれはです"

    def test_normalize_text_mixed_spaces(self):
        """Test mixed regular and fullwidth spaces."""
        text = "これは テスト\u3000です"  # Regular space + fullwidth space
        result = normalize_text(text)
        assert result == "これはテスト\u3000です"  # Regular space removed, fullwidth preserved

    def test_normalize_text_multiple_and_mixed_spaces(self):
        """Test removal of multiple consecutive and mixed whitespace types between character types."""
        # Multiple consecutive regular spaces
        text1 = "これは   test   です"
        result1 = normalize_text(text1)
        assert result1 == "これはtestです"

        # Mixed regular and fullwidth spaces (fullwidth should be preserved)
        text2 = "これは   test\u3000\u3000です   end"
        result2 = normalize_text(text2)
        assert result2 == "これはtest\u3000\u3000ですend"

        # Tab characters between different character types
        text3 = "これは\ttest\tです"
        result3 = normalize_text(text3)
        assert result3 == "これはtestです"

        # Mixed spaces and tabs
        text4 = "これは \t test \t です"
        result4 = normalize_text(text4)
        assert result4 == "これはtestです"

    def test_normalize_text_numbers_and_symbols(self):
        """Test space removal between numbers, symbols, and Japanese text."""
        text = "価格は 100 円です"  # Numbers with spaces
        result = normalize_text(text)
        assert result == "価格は100円です"

    def test_normalize_text_english_punctuation(self):
        """Test space removal between English punctuation and Japanese text."""
        text = "これは , test です ."  # Punctuation with spaces
        result = normalize_text(text)
        assert result == "これは, testです."  # Space after comma is preserved

    def test_normalize_text_performance_small_text(self):
        """Test performance with small text (< 100 characters)."""
        text = "これは　テスト　です。" * 5  # ~50 characters

        start_time = time.time()
        for _ in range(1000):  # Run 1000 times
            normalize_text(text)
        end_time = time.time()

        # Should complete 1000 iterations in less than 1 second
        assert (end_time - start_time) < 1.0

    def test_normalize_text_performance_medium_text(self):
        """Test performance with medium text (1000+ characters)."""
        text = "これは　テスト　です。English text with spaces. 数字123も含む。" * 20  # ~1000+ characters

        start_time = time.time()
        for _ in range(100):  # Run 100 times
            normalize_text(text)
        end_time = time.time()

        # Should complete 100 iterations in less than 1 second
        assert (end_time - start_time) < 1.0

    def test_normalize_text_performance_large_text(self):
        """Test performance with large text (10000+ characters)."""
        text = "これは　テスト　です。English text with spaces. 数字123も含む。\n* 箇条書き\n  - サブ項目\n" * 200  # ~10000+ characters

        start_time = time.time()
        for _ in range(10):  # Run 10 times
            normalize_text(text)
        end_time = time.time()

        # Should complete 10 iterations in less than 1 second
        assert (end_time - start_time) < 1.0

    def test_normalize_text_consistency_multiple_runs(self):
        """Test that normalize_text produces consistent results across multiple runs."""
        text = "これは test です　with　fullwidth　spaces"

        # Run the function multiple times and ensure consistent results
        results = []
        for _ in range(10):
            results.append(normalize_text(text))

        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            assert result == first_result

    def test_normalize_text_memory_efficiency(self):
        """Test that normalize_text doesn't cause memory leaks with repeated calls."""
        import gc

        text = "これは　テスト　です。" * 100  # Medium-sized text

        # Force garbage collection before test
        gc.collect()
        initial_objects = len(gc.get_objects())

        # Run function many times
        for _ in range(1000):
            result = normalize_text(text)
            del result  # Explicitly delete result

        # Force garbage collection after test
        gc.collect()
        final_objects = len(gc.get_objects())

        # Object count should not increase significantly (allow some variance)
        object_increase = final_objects - initial_objects
        assert object_increase < 100  # Allow some increase but not excessive


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
        text = ":kbd:`Ctrl+C` でコピー、 :kbd:`Ctrl+V` でペースト"
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

    def test_process_rst_text_language_specific_normalization(self):
        """Test that normalization only occurs for Japanese language processing."""

        # Test Japanese text with space normalization (spaces between character types should be removed)
        japanese_mixed_text = "これは test です"  # Regular space between Japanese and English
        result_ja_mixed = process_rst_text(japanese_mixed_text, {}, "ja")
        assert result_ja_mixed == "これはtestです"  # Space removed between different character types

        # Test English text with English processing (should not normalize - return as-is)
        english_text = "This is a test"
        result_en = process_rst_text(english_text, {}, "en")
        assert result_en == english_text  # Use variable to confirm input unchanged

        # Test fullwidth space preservation in Japanese (should not change)
        fullwidth_text = "これは　テスト　です"  # Fullwidth spaces (U+3000)
        result_fullwidth = process_rst_text(fullwidth_text, {}, "ja")
        assert result_fullwidth == fullwidth_text  # Use variable to confirm input unchanged

        # Test that Japanese text with English processing is not normalized (return as-is)
        japanese_text_en_processing = "これは test です"
        result_ja_text_en_lang = process_rst_text(japanese_text_en_processing, {}, "en")
        assert result_ja_text_en_lang == japanese_text_en_processing  # Use variable to confirm input unchanged

    def test_process_rst_text_no_markup(self):
        """Test text with no RST markup."""
        text = "これは普通のテキストです"
        info = {}
        result = process_rst_text(text, info, "ja")
        assert result == text

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
                },
                {
                    "type": "simple",
                    "procedure": {
                        "procedure": {
                            "ja": ":kbd:`Shift+Tab` キーを使用",
                            "en": "Use :kbd:`Shift+Tab` key"
                        }
                    }
                }
            ]
        }
        info = {}

        result = process_rst_condition(condition, info)

        assert result["type"] == "or"
        assert len(result["conditions"]) == 2
        assert result["conditions"][0]["procedure"]["procedure"]["ja"] == "Tabキーを使用"  # Space between English and Japanese is normalized
        assert result["conditions"][0]["procedure"]["procedure"]["en"] == "Use Tab key"
        assert result["conditions"][1]["procedure"]["procedure"]["ja"] == "Shift+Tabキーを使用"  # Space between English and Japanese is normalized
        assert result["conditions"][1]["procedure"]["procedure"]["en"] == "Use Shift+Tab key"

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
