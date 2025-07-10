"""Configuration management system for freee_a11y_gl module."""
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, List, Literal
import yaml
from pydantic import BaseModel, Field, field_validator
from .message_catalog import MessageCatalog

# Python 3.9+ has importlib.resources.files, 3.8 needs importlib_resources
if sys.version_info >= (3, 9):
    from importlib import resources
else:
    try:
        import importlib_resources as resources
    except ImportError:
        import importlib.resources as resources


class LanguageConfig(BaseModel):
    """Language configuration."""
    available: list[str]
    default: str

class PathConfig(BaseModel):
    """Path configuration."""
    guidelines: str = Field(description="Guidelines path (must start and end with /)")
    faq: str = Field(description="FAQ path (must start and end with /)")

    @field_validator("guidelines", "faq")
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Validate path string.
        
        Args:
            v: Path string to validate
            
        Returns:
            Validated path string
            
        Raises:
            ValueError: If path is invalid
        """
        if not v:
            raise ValueError("Path cannot be empty")
        if not v.startswith("/"):
            raise ValueError("Path must start with /")
        if not v.endswith("/"):
            raise ValueError("Path must end with /")
        return v


class GlobalConfig(BaseModel):
    """Global configuration model."""
    languages: LanguageConfig
    base_url: str
    paths: PathConfig

class Settings:
    """設定値を階層的に管理するクラス。
    優先順位: 
    1. プログラムによる直接指定 (Config.initialize())
    2. プロファイル設定 (~/.config/freee_a11y_gl/profiles/{profile}.yaml)
    3. デフォルトプロファイル (~/.config/freee_a11y_gl/profiles/default.yaml)
    4. ライブラリデフォルト (~/.config/freee_a11y_gl/lib/config.yaml)
    5. 内蔵デフォルト設定 (data/config.yaml)
    6. 緊急時フォールバック（最小限のハードコード値）
    """
    
    def __init__(self, profile: Optional[str] = None):
        self._settings: Dict[str, Any] = {}
        self._config_model: Optional[GlobalConfig] = None
        self._message_catalog: Optional[MessageCatalog] = None
        self._profile = profile or "default"
        
        # デフォルト値の読み込み
        self.load_defaults()
        
        # 設定ファイルの読み込み（プロファイルベース）
        self.load_from_profile()
        
        # メッセージカタログの読み込み
        self.load_message_catalog()
        
        # 設定値の検証
        self.validate()

    def load_defaults(self) -> None:
        """デフォルト設定の読み込み"""
        # 内蔵デフォルト設定ファイルから読み込み
        try:
            # importlib.resources を使用してパッケージリソースにアクセス
            if sys.version_info >= (3, 9):
                config_files = resources.files("freee_a11y_gl.data")
                config_file = config_files / "config.yaml"
                if config_file.is_file():
                    config_data = yaml.safe_load(config_file.read_text(encoding='utf-8'))
                    if config_data:
                        self._settings = config_data
                    else:
                        self._settings = self._get_minimal_defaults()
                else:
                    self._settings = self._get_minimal_defaults()
            else:
                # Python 3.8 compatibility
                with resources.open_text("freee_a11y_gl.data", "config.yaml", encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                    if config_data:
                        self._settings = config_data
                    else:
                        self._settings = self._get_minimal_defaults()
        except (FileNotFoundError, ModuleNotFoundError, yaml.YAMLError):
            # リソースが見つからない場合やYAMLエラーの場合は、従来の方法でフォールバック
            try:
                default_config_path = Path(__file__).parent / "data" / "config.yaml"
                if default_config_path.exists():
                    with default_config_path.open(encoding='utf-8') as f:
                        config_data = yaml.safe_load(f)
                        if config_data:
                            self._settings = config_data
                        else:
                            self._settings = self._get_minimal_defaults()
                else:
                    self._settings = self._get_minimal_defaults()
            except (OSError, PermissionError, yaml.YAMLError):
                # 最終フォールバック: 最小限のデフォルト値を設定
                self._settings = self._get_minimal_defaults()

    def _get_minimal_defaults(self) -> Dict[str, Any]:
        """最小限のデフォルト値を取得（緊急時フォールバック用）"""
        return {
            "languages": {
                "available": ["ja", "en"],
                "default": "ja"
            },
            "base_url": "https://a11y-guidelines.freee.co.jp",
            "paths": {
                "guidelines": "/categories/",
                "faq": "/faq/articles/"
            }
        }

    def _get_config_base_dir(self) -> Path:
        """Get base configuration directory.
        
        Returns:
            Base configuration directory path
        """
        return Path.home() / ".config" / "freee_a11y_gl"

    def _get_profile_config_paths(self) -> List[Path]:
        """Get list of profile configuration file paths to search.
        
        Returns:
            List of paths to search, in order of precedence
        """
        config_dir = self._get_config_base_dir()
        
        search_paths = []
        
        # 1. プロファイル設定
        if self._profile != "default":
            search_paths.append(config_dir / "profiles" / f"{self._profile}.yaml")
        
        # 2. デフォルトプロファイル
        search_paths.append(config_dir / "profiles" / "default.yaml")
        
        # 3. ライブラリデフォルト
        search_paths.append(config_dir / "lib" / "config.yaml")
        
        return search_paths

    def load_from_profile(self) -> None:
        """プロファイルベース設定ファイルからの読み込み"""
        for path in self._get_profile_config_paths():
            try:
                if path.exists() and path.is_file():
                    with path.open(encoding='utf-8') as f:
                        config_data = yaml.safe_load(f)
                        if config_data:
                            self.update(config_data)
                            break  # 最初に見つかった設定ファイルを使用
            except (OSError, PermissionError, yaml.YAMLError):
                continue  # 読み取り権限がない場合やYAMLエラーの場合は次を試す

    def load_message_catalog(self) -> None:
        """メッセージカタログの読み込み"""
        config_dir = self._get_config_base_dir()
        
        # メッセージカタログの探索パス
        catalog_paths = []
        
        # 1. プロファイル固有のメッセージカタログ
        if self._profile != "default":
            catalog_paths.append(config_dir / "messages" / f"{self._profile}.yaml")
        
        # 2. デフォルトメッセージカタログ
        catalog_paths.append(config_dir / "messages" / "default.yaml")
        
        # 3. ライブラリ内蔵のデフォルトメッセージカタログ（importlib.resources使用）
        lib_messages_path = None
        try:
            # importlib.resources を使用してパッケージリソースにアクセス
            if sys.version_info >= (3, 9):
                message_files = resources.files("freee_a11y_gl.data")
                message_file = message_files / "messages.yaml"
                if message_file.is_file():
                    # 一時的にPathオブジェクトを作成（MessageCatalog.load_with_fallbackとの互換性のため）
                    lib_messages_path = Path(__file__).parent / "data" / "messages.yaml"
            else:
                # Python 3.8 compatibility - リソースが存在するかチェック
                try:
                    resources.open_text("freee_a11y_gl.data", "messages.yaml")
                    lib_messages_path = Path(__file__).parent / "data" / "messages.yaml"
                except FileNotFoundError:
                    pass
        except (ModuleNotFoundError, FileNotFoundError):
            # フォールバック: 従来の方法
            fallback_path = Path(__file__).parent / "data" / "messages.yaml"
            if fallback_path.exists():
                lib_messages_path = fallback_path
        
        if lib_messages_path:
            catalog_paths.append(lib_messages_path)
        
        # メッセージカタログの読み込み
        for primary_path in catalog_paths:
            try:
                self._message_catalog = MessageCatalog.load_with_fallback(
                    primary_path=primary_path,
                    fallback_path=lib_messages_path if primary_path != lib_messages_path else None
                )
                break
            except Exception:
                continue
        
        # フォールバック: デフォルトのメッセージカタログ
        if self._message_catalog is None:
            self._message_catalog = MessageCatalog()

    def get(self, key: str, default: Any = None) -> Any:
        """設定値の取得
        
        Args:
            key: ドット区切りのキー (例: "urls.base.ja")
            default: キーが存在しない場合のデフォルト値
            
        Returns:
            設定値
        """
        try:
            return self.get_nested(key.split("."))
        except KeyError:
            return default

    def set(self, key: str, value: Any) -> None:
        """設定値の動的な更新
        
        Args:
            key: ドット区切りのキー
            value: 設定値
        """
        self.set_nested(key.split("."), value)
        self.validate()

    def get_nested(self, keys: list) -> Any:
        """ネストされた設定値の取得"""
        current = self._settings
        for key in keys:
            current = current[key]
        return current

    def set_nested(self, keys: list, value: Any) -> None:
        """ネストされた設定値の設定"""
        current = self._settings
        for key in keys[:-1]:
            current = current.setdefault(key, {})
        current[keys[-1]] = value

    def update(self, settings: Optional[Dict[str, Any]] = None) -> None:
        """設定値の一括更新
        
        Args:
            settings: 更新する設定値。Noneの場合は更新しない
        """
        if settings:
            # 深い階層でもデフォルト値を保持したまま更新
            def deep_update(base: dict, update: dict) -> dict:
                for key, value in update.items():
                    if isinstance(value, dict) and isinstance(base.get(key, {}), dict):
                        base[key] = deep_update(base.get(key, {}), value)
                    else:
                        base[key] = value
                return base
            
            deep_update(self._settings, settings)
        self.validate()

    def validate(self) -> None:
        """設定値の検証"""
        self._config_model = GlobalConfig(**self._settings)

    @property
    def config(self) -> GlobalConfig:
        """型チェック済みの設定オブジェクトを取得"""
        if self._config_model is None:
            self.validate()
        return self._config_model

    @property
    def message_catalog(self) -> MessageCatalog:
        """メッセージカタログを取得"""
        if self._message_catalog is None:
            self.load_message_catalog()
        return self._message_catalog

    def initialize(self, profile: Optional[str] = None, config_override: Optional[Dict[str, Any]] = None) -> None:
        """設定の初期化（プログラムによる直接指定）
        
        Args:
            profile: 使用するプロファイル名
            config_override: 設定の上書き値
        """
        if profile and profile != self._profile:
            self._profile = profile
            # プロファイルが変更された場合は再読み込み
            self.load_defaults()
            self.load_from_profile()
            self.load_message_catalog()
        
        if config_override:
            self.update(config_override)

# シングルトンインスタンス
settings = Settings()
