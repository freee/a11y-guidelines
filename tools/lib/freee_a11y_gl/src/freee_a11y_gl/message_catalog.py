"""Message catalog system for internationalization."""
from pathlib import Path
from typing import Dict, Optional
import yaml
from pydantic import BaseModel, Field

from importlib import resources


class MessageCatalog(BaseModel):
    """Message catalog for internationalization."""

    severity_tags: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    check_targets: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    check_tools: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    platform_names: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    implementation_targets: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    separators: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    conjunctions: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    pass_texts: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    date_formats: Dict[str, Dict[str, str]] = Field(default_factory=dict)

    @classmethod
    def load_from_file(cls, file_path: Path) -> "MessageCatalog":
        """Load message catalog from YAML file.

        Args:
            file_path: Path to the YAML file

        Returns:
            MessageCatalog instance

        Raises:
            FileNotFoundError: If file doesn't exist
            yaml.YAMLError: If YAML is invalid
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Message catalog file not found: {file_path}")

        with file_path.open(encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        return cls(**data)

    @classmethod
    def load_with_fallback(cls, primary_path: Optional[Path] = None,
                           fallback_path: Optional[Path] = None) -> "MessageCatalog":
        """Load message catalog with fallback.

        Args:
            primary_path: Primary message catalog file path
            fallback_path: Fallback message catalog file path

        Returns:
            MessageCatalog instance
        """
        # Try primary path first
        if primary_path and primary_path.exists():
            try:
                return cls.load_from_file(primary_path)
            except (yaml.YAMLError, ValueError):
                pass  # Fall back to default or fallback file

        # Try fallback path
        if fallback_path and fallback_path.exists():
            try:
                return cls.load_from_file(fallback_path)
            except (yaml.YAMLError, ValueError):
                pass  # Fall back to default

        # Try loading from package resources as final fallback
        try:
            return cls.load_from_package_resource()
        except Exception:
            pass

        # Return default instance
        return cls()

    @classmethod
    def load_from_package_resource(cls) -> "MessageCatalog":
        """Load message catalog from package resources.

        Returns:
            MessageCatalog instance

        Raises:
            FileNotFoundError: If resource doesn't exist
            yaml.YAMLError: If YAML is invalid
        """
        try:
            # importlib.resources を使用してパッケージリソースにアクセス
            message_files = resources.files("freee_a11y_gl.data")
            message_file = message_files / "messages.yaml"
            if message_file.is_file():
                data = yaml.safe_load(message_file.read_text(encoding='utf-8')) or {}
                return cls(**data)
            else:
                raise FileNotFoundError("messages.yaml not found in package resources")
        except (ModuleNotFoundError, FileNotFoundError) as e:
            raise FileNotFoundError(f"Message catalog resource not found: {e}")

    def get_severity_tag(self, severity: str, lang: str = "ja") -> str:
        """Get localized severity tag.

        Args:
            severity: Severity level (minor, normal, major, critical)
            lang: Language code (ja, en)

        Returns:
            Localized severity tag
        """
        try:
            return self.severity_tags[severity][lang]
        except KeyError:
            return severity

    def get_check_target(self, target: str, lang: str = "ja") -> str:
        """Get localized check target name.

        Args:
            target: Target type (design, code, product)
            lang: Language code (ja, en)

        Returns:
            Localized check target name
        """
        try:
            return self.check_targets[target][lang]
        except KeyError:
            return target

    def get_check_tool(self, tool: str, lang: str = "ja") -> str:
        """Get localized check tool name.

        Args:
            tool: Tool identifier (axe, lighthouse, wave)
            lang: Language code (ja, en)

        Returns:
            Localized check tool name
        """
        try:
            return self.check_tools[tool][lang]
        except KeyError:
            return tool

    def get_platform_name(self, platform: str, lang: str = "ja") -> str:
        """Get localized platform name.

        Args:
            platform: Platform identifier (web, mobile, etc.)
            lang: Language code (ja, en)

        Returns:
            Localized platform name
        """
        try:
            return self.platform_names[platform][lang]
        except KeyError:
            return platform

    def get_implementation_target(self, target: str, lang: str = "ja") -> str:
        """Get localized implementation target name.

        Args:
            target: Implementation target identifier (web, android, ios)
            lang: Language code (ja, en)

        Returns:
            Localized implementation target name
        """
        try:
            return self.implementation_targets[target][lang]
        except KeyError:
            return target

    def get_separator(self, separator_type: str, lang: str = "ja") -> str:
        """Get localized separator.

        Args:
            separator_type: Separator type (text, list, and, or)
            lang: Language code (ja, en)

        Returns:
            Localized separator
        """
        try:
            return self.separators[separator_type][lang]
        except KeyError:
            return separator_type

    def get_conjunction(self, conjunction_type: str, lang: str = "ja") -> str:
        """Get localized conjunction.

        Args:
            conjunction_type: Conjunction type (and, or)
            lang: Language code (ja, en)

        Returns:
            Localized conjunction
        """
        try:
            return self.conjunctions[conjunction_type][lang]
        except KeyError:
            return conjunction_type

    def get_pass_text(self, text_type: str, lang: str = "ja") -> str:
        """Get localized pass text.

        Args:
            text_type: Text type (singular, plural)
            lang: Language code (ja, en)

        Returns:
            Localized pass text
        """
        try:
            return self.pass_texts[text_type][lang]
        except KeyError:
            return text_type

    def get_date_format(self, format_type: str = "default", lang: str = "ja") -> str:
        """Get localized date format.

        Args:
            format_type: Format type (default)
            lang: Language code (ja, en)

        Returns:
            Localized date format string
        """
        try:
            return self.date_formats[format_type][lang]
        except KeyError:
            # Fallback to format_type if not found
            return format_type
