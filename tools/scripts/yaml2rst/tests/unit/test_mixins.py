"""Unit tests for mixin classes."""
import pytest
from unittest.mock import Mock, patch

from yaml2rst.generators.mixins import (
    RelationshipMixin, ValidationMixin, UtilityMixin
)


class TestRelationshipMixin:
    """Test RelationshipMixin functionality."""

    def test_relationship_manager_lazy_loading(self):
        """Test that RelationshipManager is lazy-loaded."""
        class TestClass(RelationshipMixin):
            pass

        instance = TestClass()

        # Should not have _relationship_manager initially
        assert not hasattr(instance, '_relationship_manager')

        # Mock the RelationshipManager import
        with patch('freee_a11y_gl.relationship_manager.'
                   'RelationshipManager') as mock_rm:
            mock_instance = Mock()
            mock_rm.return_value = mock_instance

            # First access should create the instance
            result = instance.relationship_manager
            assert result is mock_instance
            mock_rm.assert_called_once()

            # Second access should return the same instance
            result2 = instance.relationship_manager
            assert result2 is mock_instance
            # Should not call RelationshipManager() again
            mock_rm.assert_called_once()


class TestValidationMixin:
    """Test ValidationMixin functionality."""

    @pytest.mark.parametrize("data,required_fields,expected", [
        # Success case - all required fields present
        ({'field1': 'value1', 'field2': 'value2', 'field3': 'value3'},
         ['field1', 'field2'], True),
        # Failure case - missing required field
        ({'field1': 'value1'}, ['field1', 'field2'], False),
    ])
    def test_validate_required_fields(self, data, required_fields, expected):
        """Test validation of required fields with various inputs."""
        class TestClass(ValidationMixin):
            pass

        instance = TestClass()
        assert instance.validate_required_fields(
            data, required_fields) == expected

    @pytest.mark.parametrize("data,field_name,expected", [
        # Success case - valid list
        ({'items': [1, 2, 3]}, 'items', True),
        # Failure case - missing field
        ({}, 'items', False),
        # Failure case - not a list
        ({'items': 'not a list'}, 'items', False),
    ])
    def test_validate_list_field(self, data, field_name, expected):
        """Test validation of list fields with various inputs."""
        class TestClass(ValidationMixin):
            pass

        instance = TestClass()
        assert instance.validate_list_field(data, field_name) == expected

    @pytest.mark.parametrize("data,field_name,allow_empty,expected", [
        # Success case - valid string
        ({'text': 'hello world'}, 'text', False, True),
        # Failure case - missing field
        ({}, 'text', False, False),
        # Failure case - not a string
        ({'text': 123}, 'text', False, False),
        # Failure case - empty string not allowed
        ({'text': '   '}, 'text', False, False),
        # Success case - empty string allowed
        ({'text': ''}, 'text', True, True),
    ])
    def test_validate_string_field(self, data, field_name, allow_empty,
                                   expected):
        """Test validation of string fields with various inputs."""
        class TestClass(ValidationMixin):
            pass

        instance = TestClass()
        result = instance.validate_string_field(
            data, field_name, allow_empty=allow_empty)
        assert result == expected


class TestUtilityMixin:
    """Test UtilityMixin functionality."""

    def test_get_sorted_objects_default_key(self):
        """Test sorting objects with default sort key."""
        class TestClass(UtilityMixin):
            pass

        class MockObject:
            def __init__(self, sort_key):
                self.sort_key = sort_key

        instance = TestClass()
        objects = [MockObject('c'), MockObject('a'), MockObject('b')]

        result = instance.get_sorted_objects(objects)

        assert len(result) == 3
        assert result[0].sort_key == 'a'
        assert result[1].sort_key == 'b'
        assert result[2].sort_key == 'c'

    def test_get_sorted_objects_custom_key(self):
        """Test sorting objects with custom sort key."""
        class TestClass(UtilityMixin):
            pass

        class MockObject:
            def __init__(self, name):
                self.name = name

        instance = TestClass()
        objects = [MockObject('zebra'), MockObject('apple'),
                   MockObject('banana')]

        result = instance.get_sorted_objects(objects, 'name')

        assert len(result) == 3
        assert result[0].name == 'apple'
        assert result[1].name == 'banana'
        assert result[2].name == 'zebra'

    def test_get_sorted_objects_by_lang_name(self):
        """Test sorting objects by localized name."""
        class TestClass(UtilityMixin):
            pass

        class MockObject:
            def __init__(self, names):
                self.names = names

        instance = TestClass()
        objects = [
            MockObject({'en': 'zebra', 'ja': 'シマウマ'}),
            MockObject({'en': 'apple', 'ja': 'りんご'}),
            MockObject({'en': 'banana', 'ja': 'バナナ'})
        ]

        result = instance.get_sorted_objects_by_lang_name(objects, 'en')

        assert len(result) == 3
        assert result[0].names['en'] == 'apple'
        assert result[1].names['en'] == 'banana'
        assert result[2].names['en'] == 'zebra'

    def test_process_template_data(self):
        """Test processing object into template data."""
        class TestClass(UtilityMixin):
            pass

        class MockObject:
            def template_data(self, lang):
                return {'title': f'Title in {lang}', 'content': 'Content'}

        instance = TestClass()
        obj = MockObject()

        result = instance.process_template_data(obj, 'en')

        assert result == {'title': 'Title in en', 'content': 'Content'}

    def test_process_template_data_no_method(self):
        """Test processing object without template_data method."""
        class TestClass(UtilityMixin):
            pass

        class MockObject:
            pass

        instance = TestClass()
        obj = MockObject()

        result = instance.process_template_data(obj, 'en')

        assert result == {}

    def test_process_template_data_list(self):
        """Test processing list of objects into template data."""
        class TestClass(UtilityMixin):
            pass

        class MockObject:
            def __init__(self, title):
                self.title = title

            def template_data(self, lang):
                return {'title': f'{self.title} in {lang}'}

        instance = TestClass()
        objects = [MockObject('First'), MockObject('Second')]

        result = instance.process_template_data_list(objects, 'en')

        assert len(result) == 2
        assert result[0] == {'title': 'First in en'}
        assert result[1] == {'title': 'Second in en'}

    def test_filter_objects_with_articles(self):
        """Test filtering objects that have articles."""
        class TestClass(UtilityMixin):
            pass

        class MockObject:
            def __init__(self, count):
                self._count = count

            def article_count(self):
                return self._count

        instance = TestClass()
        objects = [MockObject(0), MockObject(5), MockObject(0),
                   MockObject(3)]

        result = instance.filter_objects_with_articles(objects)

        assert len(result) == 2
        assert result[0].article_count() == 5
        assert result[1].article_count() == 3

    def test_filter_objects_with_articles_no_method(self):
        """Test filtering objects without article_count method."""
        class TestClass(UtilityMixin):
            pass

        class MockObject:
            pass

        instance = TestClass()
        objects = [MockObject(), MockObject()]

        result = instance.filter_objects_with_articles(objects)

        assert len(result) == 0
