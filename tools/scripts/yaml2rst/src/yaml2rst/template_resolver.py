"""Template resolution system for yaml2rst.

This module provides the TemplateResolver class that handles finding and
resolving template files from multiple sources with fallback support.
It integrates with TemplateConfig to provide a complete template
customization system.
"""
from pathlib import Path
from typing import Dict, List, Optional, Set
import logging

from .template_config import TemplateConfig


class TemplateNotFoundError(Exception):
    """Raised when a template file cannot be found in any search path."""
    pass


class TemplateResolver:
    """Resolves template files from multiple sources with fallback support.

    The TemplateResolver handles the logic of finding template files across
    multiple directories in priority order. It supports:

    1. Custom template directories (highest priority)
    2. User template directories (~/.config/freee_a11y_gl/templates)
    3. Built-in package templates (fallback)

    The resolver caches template paths for performance and provides
    validation and debugging capabilities.

    Example:
        >>> resolver = TemplateResolver()
        >>> template_path = resolver.resolve_template('gl-category.rst')
        >>> print(template_path)  # /path/to/template/gl-category.rst

        >>> # With custom directory
        >>> resolver = TemplateResolver(
            custom_template_dir='/custom/templates')
        >>> template_path = resolver.resolve_template('gl-category.rst')
    """

    def __init__(self, custom_template_dir: Optional[str] = None,
                 template_config: Optional[TemplateConfig] = None):
        """Initialize the template resolver.

        Args:
            custom_template_dir: Optional custom template directory path
            template_config: Optional TemplateConfig instance. If None,
                           creates a new instance.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.custom_template_dir = custom_template_dir
        self.template_config = template_config or TemplateConfig()

        # Cache for resolved template paths
        self._template_cache: Dict[str, str] = {}

        # Cache for search paths (invalidated when config changes)
        self._search_paths_cache: Optional[List[str]] = None

    def get_search_paths(self) -> List[str]:
        """Get template search paths in priority order.

        Returns:
            List of directory paths to search for templates
        """
        if self._search_paths_cache is None:
            self._search_paths_cache = (
                self.template_config.get_template_search_paths(
                    custom_dir=self.custom_template_dir))
            self.logger.debug(
                f"Template search paths: {self._search_paths_cache}")

        return self._search_paths_cache

    def resolve_template(self, template_name: str) -> str:
        """Resolve a template file to its full path.

        Searches for the template file in all configured search paths
        and returns the path to the first match found.

        Args:
            template_name: Name of the template file (e.g., 'gl-category.rst')

        Returns:
            Full path to the resolved template file

        Raises:
            TemplateNotFoundError: If template is not found in any search path

        Example:
            >>> resolver = TemplateResolver()
            >>> path = resolver.resolve_template('gl-category.rst')
            >>> print(path)  # '/home/user/.config/freee_a11y_gl/templates/
            ...              #  gl-category.rst'
        """
        # Check cache first
        if template_name in self._template_cache:
            cached_path = self._template_cache[template_name]
            # Verify cached path still exists
            if Path(cached_path).exists():
                return cached_path
            else:
                # Remove invalid cache entry
                del self._template_cache[template_name]
                self.logger.debug(
                    f"Removed invalid cache entry for {template_name}"
                )

        # Search in all paths
        search_paths = self.get_search_paths()

        for search_path in search_paths:
            template_path = Path(search_path) / template_name

            if template_path.exists() and template_path.is_file():
                resolved_path = str(template_path.resolve())
                self._template_cache[template_name] = resolved_path
                self.logger.debug(
                    f"Resolved {template_name} to {resolved_path}"
                )
                return resolved_path

        # Template not found in any path
        self.logger.error(f"Template not found: {template_name}")
        self.logger.error(f"Searched paths: {search_paths}")

        raise TemplateNotFoundError(
            f"Template '{template_name}' not found in any of the "
            f"search paths: {', '.join(search_paths)}"
        )

    def resolve_all_templates(
            self, template_names: List[str]) -> Dict[str, str]:
        """Resolve multiple templates at once.

        Args:
            template_names: List of template names to resolve

        Returns:
            Dictionary mapping template names to their resolved paths

        Raises:
            TemplateNotFoundError: If any template is not found
        """
        resolved = {}
        missing = []

        for template_name in template_names:
            try:
                resolved[template_name] = self.resolve_template(template_name)
            except TemplateNotFoundError:
                missing.append(template_name)

        if missing:
            raise TemplateNotFoundError(
                f"Templates not found: {', '.join(missing)}"
            )

        return resolved

    def check_template_exists(self, template_name: str) -> bool:
        """Check if a template exists without resolving it.

        Args:
            template_name: Name of the template file

        Returns:
            True if template exists in any search path
        """
        try:
            self.resolve_template(template_name)
            return True
        except TemplateNotFoundError:
            return False

    def list_available_templates(self) -> Dict[str, List[str]]:
        """List all available templates by search path.

        Returns:
            Dictionary mapping search paths to lists of available templates
        """
        available = {}
        search_paths = self.get_search_paths()

        for search_path in search_paths:
            path_obj = Path(search_path)
            if not path_obj.exists():
                available[search_path] = []
                continue

            templates = []
            try:
                # Find all template files (recursively)
                for template_file in path_obj.rglob('*'):
                    if template_file.is_file():
                        # Get relative path from search directory
                        rel_path = template_file.relative_to(path_obj)
                        templates.append(str(rel_path))

                templates.sort()
                available[search_path] = templates

            except (OSError, PermissionError) as e:
                self.logger.warning(
                    f"Cannot list templates in {search_path}: {e}"
                )
                available[search_path] = []

        return available

    def get_template_source_info(self, template_name: str) -> Dict[str, str]:
        """Get information about where a template is resolved from.

        Args:
            template_name: Name of the template file

        Returns:
            Dictionary with template source information

        Raises:
            TemplateNotFoundError: If template is not found
        """
        resolved_path = self.resolve_template(template_name)
        search_paths = self.get_search_paths()

        # Find which search path contains this template
        source_path = None
        for search_path in search_paths:
            if resolved_path.startswith(str(Path(search_path).resolve())):
                source_path = search_path
                break

        # Determine source type
        source_type = "unknown"
        if source_path:
            if source_path == self.custom_template_dir:
                source_type = "custom"
            elif source_path == str(
                self.template_config.get_user_template_dir_expanded()
            ):
                source_type = "user"
            else:
                source_type = "builtin"

        return {
            'template_name': template_name,
            'resolved_path': resolved_path,
            'source_path': source_path or "unknown",
            'source_type': source_type
        }

    def validate_templates(self, template_names: List[str]) -> Dict[str, bool]:
        """Validate that all specified templates exist.

        Args:
            template_names: List of template names to validate

        Returns:
            Dictionary mapping template names to existence status
        """
        validation_results = {}

        for template_name in template_names:
            validation_results[template_name] = self.check_template_exists(
                template_name
            )

        return validation_results

    def clear_cache(self) -> None:
        """Clear all cached template paths and search paths.

        This forces the resolver to re-search for templates on the next
        resolution request. Useful when template directories change.
        """
        self._template_cache.clear()
        self._search_paths_cache = None
        self.logger.debug("Cleared template resolver cache")

    def get_cache_info(self) -> Dict[str, int]:
        """Get information about the current cache state.

        Returns:
            Dictionary with cache statistics
        """
        return {
            'cached_templates': len(self._template_cache),
            'search_paths_cached': self._search_paths_cache is not None
        }

    def find_template_conflicts(self) -> Dict[str, List[str]]:
        """Find templates that exist in multiple search paths.

        This can help identify potential conflicts where a user template
        might be shadowing a built-in template, or vice versa.

        Returns:
            Dictionary mapping template names to lists of paths where they
            exist
        """
        conflicts = {}
        search_paths = self.get_search_paths()

        # Collect all templates from all paths
        all_templates: Dict[str, List[str]] = {}

        for search_path in search_paths:
            path_obj = Path(search_path)
            if not path_obj.exists():
                continue

            try:
                for template_file in path_obj.rglob('*'):
                    if template_file.is_file():
                        rel_path = str(template_file.relative_to(path_obj))

                        if rel_path not in all_templates:
                            all_templates[rel_path] = []

                        all_templates[rel_path].append(search_path)

            except (OSError, PermissionError) as e:
                self.logger.warning(
                    f"Cannot scan templates in {search_path}: {e}"
                )

        # Find conflicts (templates in multiple paths)
        for template_name, paths in all_templates.items():
            if len(paths) > 1:
                conflicts[template_name] = paths

        return conflicts

    def get_effective_templates(self) -> Dict[str, str]:
        """Get the effective template paths that would be used.

        This shows which template file would actually be used for each
        template name, taking into account the search path priority.

        Returns:
            Dictionary mapping template names to their effective paths
        """
        effective = {}
        available = self.list_available_templates()

        # Collect all unique template names
        all_template_names: Set[str] = set()
        for templates in available.values():
            all_template_names.update(templates)

        # Resolve each template to see which path wins
        for template_name in sorted(all_template_names):
            try:
                effective[template_name] = self.resolve_template(template_name)
            except TemplateNotFoundError:
                # This shouldn't happen since we got the name from
                # available templates
                self.logger.warning(
                    f"Template {template_name} found in listing but "
                    f"not resolvable")

        return effective
