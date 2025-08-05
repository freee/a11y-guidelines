"""Tests for template resolution system."""
import pytest
from pathlib import Path
from unittest.mock import patch

from yaml2rst.template_resolver import TemplateResolver, TemplateNotFoundError
from yaml2rst.template_config import TemplateConfig


class TestTemplateResolver:
    """Test cases for TemplateResolver class."""

    def test_init_default(self):
        """Test initialization with default parameters."""
        resolver = TemplateResolver()

        assert resolver.custom_template_dir is None
        assert isinstance(resolver.template_config, TemplateConfig)
        assert resolver._template_cache == {}
        assert resolver._search_paths_cache is None

    def test_init_with_custom_dir(self):
        """Test initialization with custom template directory."""
        custom_dir = "/custom/templates"
        resolver = TemplateResolver(custom_template_dir=custom_dir)

        assert resolver.custom_template_dir == custom_dir

    def test_init_with_template_config(self):
        """Test initialization with custom TemplateConfig."""
        config = TemplateConfig()
        resolver = TemplateResolver(template_config=config)

        assert resolver.template_config is config

    def test_get_search_paths_caching(self):
        """Test that search paths are cached."""
        resolver = TemplateResolver()

        with patch.object(resolver.template_config,
                          'get_template_search_paths') as mock_get:
            mock_get.return_value = ['/path1', '/path2']

            # First call
            paths1 = resolver.get_search_paths()
            # Second call should use cache
            paths2 = resolver.get_search_paths()

            assert paths1 == paths2
            assert mock_get.call_count == 1

    def test_get_search_paths_with_custom_dir(self):
        """Test search paths with custom directory."""
        custom_dir = "/custom/templates"
        resolver = TemplateResolver(custom_template_dir=custom_dir)

        with patch.object(resolver.template_config,
                          'get_template_search_paths') as mock_get:
            mock_get.return_value = [custom_dir, '/user/templates',
                                     '/builtin/templates']

            paths = resolver.get_search_paths()

            mock_get.assert_called_once_with(custom_dir=custom_dir)
            assert paths == [custom_dir, '/user/templates',
                             '/builtin/templates']

    def test_resolve_template_success(self, tmp_path):
        """Test successful template resolution."""
        # Create test template
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        template_file = template_dir / "test.rst"
        template_file.write_text("test template content")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(template_dir)]

            result = resolver.resolve_template("test.rst")

            assert result == str(template_file.resolve())
            # Should be cached
            assert "test.rst" in resolver._template_cache

    def test_resolve_template_from_cache(self, tmp_path):
        """Test template resolution from cache."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        template_file = template_dir / "test.rst"
        template_file.write_text("test template content")

        resolver = TemplateResolver()

        # Pre-populate cache
        resolver._template_cache["test.rst"] = str(template_file)

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            # This shouldn't be called due to cache hit
            mock_paths.return_value = []

            result = resolver.resolve_template("test.rst")

            assert result == str(template_file)
            assert mock_paths.call_count == 0

    def test_resolve_template_cache_invalidation(self, tmp_path):
        """Test cache invalidation when cached file no longer exists."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        template_file = template_dir / "test.rst"
        template_file.write_text("test template content")

        resolver = TemplateResolver()

        # Pre-populate cache with non-existent file
        resolver._template_cache["test.rst"] = "/nonexistent/file.rst"

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(template_dir)]

            result = resolver.resolve_template("test.rst")

            # Should resolve to actual file, not cached path
            assert result == str(template_file.resolve())
            # Cache should be updated
            assert resolver._template_cache["test.rst"] == str(
                template_file.resolve())

    def test_resolve_template_not_found(self):
        """Test template resolution when template doesn't exist."""
        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = ['/nonexistent/path1',
                                       '/nonexistent/path2']

            with pytest.raises(TemplateNotFoundError) as exc_info:
                resolver.resolve_template("nonexistent.rst")

            assert "nonexistent.rst" in str(exc_info.value)
            assert "/nonexistent/path1" in str(exc_info.value)
            assert "/nonexistent/path2" in str(exc_info.value)

    def test_resolve_template_priority_order(self, tmp_path):
        """Test that templates are resolved in priority order."""
        # Create multiple template directories
        dir1 = tmp_path / "dir1"
        dir2 = tmp_path / "dir2"
        dir1.mkdir()
        dir2.mkdir()

        # Create same template in both directories
        template1 = dir1 / "test.rst"
        template2 = dir2 / "test.rst"
        template1.write_text("template from dir1")
        template2.write_text("template from dir2")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            # dir1 has higher priority
            mock_paths.return_value = [str(dir1), str(dir2)]

            result = resolver.resolve_template("test.rst")

            # Should resolve to template from dir1 (higher priority)
            assert result == str(template1.resolve())

    def test_resolve_all_templates_success(self, tmp_path):
        """Test resolving multiple templates successfully."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        # Create multiple templates
        template1 = template_dir / "test1.rst"
        template2 = template_dir / "test2.rst"
        template1.write_text("template 1")
        template2.write_text("template 2")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(template_dir)]

            result = resolver.resolve_all_templates(["test1.rst",
                                                     "test2.rst"])

            expected = {
                "test1.rst": str(template1.resolve()),
                "test2.rst": str(template2.resolve())
            }
            assert result == expected

    def test_resolve_all_templates_partial_failure(self, tmp_path):
        """Test resolving multiple templates with some missing."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        # Create only one template
        template1 = template_dir / "test1.rst"
        template1.write_text("template 1")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(template_dir)]

            with pytest.raises(TemplateNotFoundError) as exc_info:
                resolver.resolve_all_templates(["test1.rst", "missing.rst"])

            assert "missing.rst" in str(exc_info.value)

    def test_check_template_exists_true(self, tmp_path):
        """Test checking template existence when it exists."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        template_file = template_dir / "test.rst"
        template_file.write_text("test template")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(template_dir)]

            result = resolver.check_template_exists("test.rst")

            assert result is True

    def test_check_template_exists_false(self):
        """Test checking template existence when it doesn't exist."""
        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = ['/nonexistent/path']

            result = resolver.check_template_exists("missing.rst")

            assert result is False

    def test_list_available_templates(self, tmp_path):
        """Test listing available templates."""
        # Create template directories with files
        dir1 = tmp_path / "dir1"
        dir2 = tmp_path / "dir2"
        dir1.mkdir()
        dir2.mkdir()

        # Create templates in dir1
        (dir1 / "template1.rst").write_text("template 1")
        (dir1 / "subdir").mkdir()
        (dir1 / "subdir" / "template2.rst").write_text("template 2")

        # Create templates in dir2
        (dir2 / "template3.rst").write_text("template 3")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(dir1), str(dir2)]

            result = resolver.list_available_templates()

            expected = {
                str(dir1): ["subdir/template2.rst", "template1.rst"],
                str(dir2): ["template3.rst"]
            }
            assert result == expected

    def test_list_available_templates_nonexistent_path(self):
        """Test listing templates with nonexistent search path."""
        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = ['/nonexistent/path']

            result = resolver.list_available_templates()

            assert result == {'/nonexistent/path': []}

    def test_list_available_templates_permission_error(self, tmp_path, caplog):
        """Test listing templates with permission error."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(template_dir)]

            # Mock rglob to raise PermissionError
            with patch.object(Path, 'rglob',
                              side_effect=PermissionError("Access denied")):
                result = resolver.list_available_templates()

                assert result == {str(template_dir): []}
                assert "Cannot list templates" in caplog.text

    def test_get_template_source_info_custom(self, tmp_path):
        """Test getting template source info for custom template."""
        custom_dir = tmp_path / "custom"
        custom_dir.mkdir()
        template_file = custom_dir / "test.rst"
        template_file.write_text("custom template")

        resolver = TemplateResolver(custom_template_dir=str(custom_dir))

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(custom_dir)]

            result = resolver.get_template_source_info("test.rst")

            expected = {
                'template_name': 'test.rst',
                'resolved_path': str(template_file.resolve()),
                'source_path': str(custom_dir),
                'source_type': 'custom'
            }
            assert result == expected

    def test_get_template_source_info_user(self, tmp_path):
        """Test getting template source info for user template."""
        user_dir = tmp_path / "user"
        user_dir.mkdir()
        template_file = user_dir / "test.rst"
        template_file.write_text("user template")

        resolver = TemplateResolver()

        with patch.object(resolver.template_config,
                          'get_user_template_dir_expanded') as mock_user_dir:
            with patch.object(resolver, 'get_search_paths') as mock_paths:
                mock_user_dir.return_value = user_dir
                mock_paths.return_value = [str(user_dir)]

                result = resolver.get_template_source_info("test.rst")

                expected = {
                    'template_name': 'test.rst',
                    'resolved_path': str(template_file.resolve()),
                    'source_path': str(user_dir),
                    'source_type': 'user'
                }
                assert result == expected

    def test_get_template_source_info_builtin(self, tmp_path):
        """Test getting template source info for builtin template."""
        builtin_dir = tmp_path / "builtin"
        builtin_dir.mkdir()
        template_file = builtin_dir / "test.rst"
        template_file.write_text("builtin template")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(builtin_dir)]

            result = resolver.get_template_source_info("test.rst")

            expected = {
                'template_name': 'test.rst',
                'resolved_path': str(template_file.resolve()),
                'source_path': str(builtin_dir),
                'source_type': 'builtin'
            }
            assert result == expected

    def test_validate_templates(self, tmp_path):
        """Test template validation."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        # Create one template
        (template_dir / "exists.rst").write_text("exists")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(template_dir)]

            result = resolver.validate_templates(["exists.rst",
                                                  "missing.rst"])

            expected = {
                "exists.rst": True,
                "missing.rst": False
            }
            assert result == expected

    def test_clear_cache(self):
        """Test clearing resolver cache."""
        resolver = TemplateResolver()

        # Populate caches
        resolver._template_cache["test.rst"] = "/path/to/test.rst"
        resolver._search_paths_cache = ["/path1", "/path2"]

        resolver.clear_cache()

        assert resolver._template_cache == {}
        assert resolver._search_paths_cache is None

    def test_get_cache_info(self):
        """Test getting cache information."""
        resolver = TemplateResolver()

        # Initially empty
        info = resolver.get_cache_info()
        expected = {
            'cached_templates': 0,
            'search_paths_cached': False
        }
        assert info == expected

        # Populate caches
        resolver._template_cache["test.rst"] = "/path/to/test.rst"
        resolver._search_paths_cache = ["/path1"]

        info = resolver.get_cache_info()
        expected = {
            'cached_templates': 1,
            'search_paths_cached': True
        }
        assert info == expected

    def test_find_template_conflicts(self, tmp_path):
        """Test finding template conflicts."""
        # Create multiple directories with overlapping templates
        dir1 = tmp_path / "dir1"
        dir2 = tmp_path / "dir2"
        dir1.mkdir()
        dir2.mkdir()

        # Create conflicting templates
        (dir1 / "conflict.rst").write_text("from dir1")
        (dir2 / "conflict.rst").write_text("from dir2")

        # Create unique templates
        (dir1 / "unique1.rst").write_text("unique to dir1")
        (dir2 / "unique2.rst").write_text("unique to dir2")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(dir1), str(dir2)]

            result = resolver.find_template_conflicts()

            expected = {
                "conflict.rst": [str(dir1), str(dir2)]
            }
            assert result == expected

    def test_find_template_conflicts_permission_error(self, tmp_path, caplog):
        """Test finding conflicts with permission error."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            mock_paths.return_value = [str(template_dir)]

            # Mock rglob to raise PermissionError
            with patch.object(Path, 'rglob',
                              side_effect=PermissionError("Access denied")):
                result = resolver.find_template_conflicts()

                assert result == {}
                assert "Cannot scan templates" in caplog.text

    def test_get_effective_templates(self, tmp_path):
        """Test getting effective template paths."""
        # Create multiple directories
        dir1 = tmp_path / "dir1"
        dir2 = tmp_path / "dir2"
        dir1.mkdir()
        dir2.mkdir()

        # Create templates
        template1_dir1 = dir1 / "template1.rst"
        template1_dir2 = dir2 / "template1.rst"  # Will be shadowed
        template2_dir2 = dir2 / "template2.rst"

        template1_dir1.write_text("template1 from dir1")
        template1_dir2.write_text("template1 from dir2")
        template2_dir2.write_text("template2 from dir2")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            # dir1 has priority
            mock_paths.return_value = [str(dir1), str(dir2)]

            result = resolver.get_effective_templates()

            expected = {
                # From higher priority dir
                "template1.rst": str(template1_dir1.resolve()),
                "template2.rst": str(template2_dir2.resolve())
            }
            assert result == expected

    def test_get_effective_templates_resolution_error(self, tmp_path, caplog):
        """Test getting effective templates with resolution error."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        (template_dir / "test.rst").write_text("test")

        resolver = TemplateResolver()

        with patch.object(resolver, 'get_search_paths') as mock_paths:
            with patch.object(resolver,
                              'list_available_templates') as mock_list:
                with patch.object(resolver,
                                  'resolve_template') as mock_resolve:
                    mock_paths.return_value = [str(template_dir)]
                    mock_list.return_value = {str(template_dir): ["test.rst"]}
                    mock_resolve.side_effect = TemplateNotFoundError(
                        "Test error")

                    result = resolver.get_effective_templates()

                    assert result == {}
                    assert "found in listing but not resolvable" in caplog.text

    def test_integration_full_workflow(self, tmp_path):
        """Test complete workflow with multiple template sources."""
        # Set up directory structure
        custom_dir = tmp_path / "custom"
        user_dir = tmp_path / "user"
        builtin_dir = tmp_path / "builtin"

        for directory in [custom_dir, user_dir, builtin_dir]:
            directory.mkdir()

        # Create templates with different priorities
        (custom_dir / "template.rst").write_text("custom template")
        (user_dir / "template.rst").write_text("user template")
        (builtin_dir / "template.rst").write_text("builtin template")

        (user_dir / "user_only.rst").write_text("user only")
        (builtin_dir / "builtin_only.rst").write_text("builtin only")

        # Create resolver with custom config
        config = TemplateConfig()
        resolver = TemplateResolver(
            custom_template_dir=str(custom_dir),
            template_config=config
        )

        with patch.object(config,
                          'get_user_template_dir_expanded') as mock_user_dir:
            with patch.object(config,
                              'should_fallback_to_builtin') as mock_fallback:
                with patch.object(config,
                                  'get_template_search_paths') as mock_paths:
                    mock_user_dir.return_value = user_dir
                    mock_fallback.return_value = True
                    mock_paths.return_value = [str(custom_dir),
                                               str(user_dir),
                                               str(builtin_dir)]

                    # Test resolution priority
                    template_path = resolver.resolve_template("template.rst")
                    assert template_path == str(
                        (custom_dir / "template.rst").resolve())

                    # Test user-only template
                    user_only_path = resolver.resolve_template("user_only.rst")
                    assert user_only_path == str(
                        (user_dir / "user_only.rst").resolve())

                    # Test builtin-only template
                    builtin_only_path = resolver.resolve_template(
                        "builtin_only.rst")
                    assert builtin_only_path == str(
                        (builtin_dir / "builtin_only.rst").resolve())

                # Test conflict detection
                conflicts = resolver.find_template_conflicts()
                assert "template.rst" in conflicts
                assert len(conflicts["template.rst"]) == 3

                # Test source info
                source_info = resolver.get_template_source_info("template.rst")
                assert source_info['source_type'] == 'custom'

                # Test validation
                validation = resolver.validate_templates([
                    "template.rst", "user_only.rst", "missing.rst"
                ])
                expected_validation = {
                    "template.rst": True,
                    "user_only.rst": True,
                    "missing.rst": False
                }
                assert validation == expected_validation
