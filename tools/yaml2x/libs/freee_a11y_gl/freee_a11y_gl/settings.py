"""Configuration management system for freee_a11y_gl module."""
import os
import platform
from pathlib import Path
from typing import Any, Dict, Optional, Set, List
import yaml
from pydantic import BaseModel, Field

class UrlConfig(BaseModel):
    """URL configuration for each language."""
    ja: str = ""
    en: str = ""

class SeparatorConfig(BaseModel):
    """Separator configuration for each language."""
    ja: str = ""
    en: str = ""

class LanguageConfig(BaseModel):
    """Language configuration."""
    available: list[str] = Field(default_factory=lambda: ["ja", "en"])
    default: str = "ja"
    required: Set[str] = Field(default_factory=lambda: {"ja", "en"})

class GlobalConfig(BaseModel):
    """Global configuration model."""
    languages: LanguageConfig = Field(default_factory=lambda: LanguageConfig())
    base_url: str = Field(default="https://a11y-guidelines.freee.co.jp")
    separators: Dict[str, SeparatorConfig] = Field(default_factory=dict)

class Settings:
    """設定値を階層的に管理するクラス。
    優先順位: 
    1. プログラムによる設定
    2. 環境変数
    3. 設定ファイル
    4. デフォルト値
    """
    
    def __init__(self):
        self._settings: Dict[str, Any] = {}
        self._env_prefix = "FREEE_A11Y_GL_"
        self._config_model: Optional[GlobalConfig] = None
        
        # デフォルト値の読み込み
        self.load_defaults()
        
        # 設定ファイルの読み込み
        self.load_from_file()
        
        # 環境変数の読み込み
        self.load_from_env()
        
        # 設定値の検証
        self.validate()

    def load_defaults(self) -> None:
        """デフォルト設定の読み込み"""
        self._settings = {
            "languages": {
                "available": ["ja", "en"],
                "default": "ja",
                "required": ["ja", "en"]
            },
            "base_url": "https://a11y-guidelines.freee.co.jp",
            "paths": {
                "guidelines": "/categories/",
                "faq": "/faq/articles/"
            },
            "separators": {
                "text": {
                    "ja": "：",
                    "en": ": "
                },
                "list": {
                    "ja": "、",
                    "en": ", "
                },
                "and": {
                    "ja": "と",
                    "en": " and "
                },
                "or": {
                    "ja": "または",
                    "en": " or "
                },
                "and_conjunction": {
                    "ja": "、かつ",
                    "en": ", and "
                },
                "or_conjunction": {
                    "ja": "、または",
                    "en": ", or "
                },
                "pass_text": {
                    "ja": "_を満たしている",
                    "en": " is true"
                }
            },
            "formats": {
                "date": {
                    "ja": "%Y年%-m月%-d日",
                    "en": "%B %-d, %Y"
                }
            }
        }

    def _get_config_search_paths(self) -> List[Path]:
        """Get list of paths to search for config files.
        
        Returns:
            List of paths to search, in order of precedence
        """
        search_paths = []
        
        # 1. 明示的に指定されたパス
        explicit_path = os.environ.get(f"{self._env_prefix}CONFIG")
        if explicit_path:
            search_paths.append(Path(explicit_path))

        # 2. カレントディレクトリ
        search_paths.extend([
            Path.cwd() / "config.yaml",
            Path.cwd() / "config.yml"
        ])

        # 3. プラットフォーム固有の標準的な設定ディレクトリ
        if platform.system() == "Windows":
            if appdata := os.environ.get("APPDATA"):
                search_paths.append(Path(appdata) / "freee_a11y_gl" / "config.yaml")
        else:  # Unix-like
            # ユーザー固有の設定
            search_paths.append(Path.home() / ".config" / "freee_a11y_gl" / "config.yaml")
            
            # システム全体の設定
            if platform.system() == "Darwin":  # macOS
                search_paths.append(Path("/Library/Application Support/freee_a11y_gl/config.yaml"))
            else:  # Linux/BSD
                search_paths.append(Path("/etc/freee_a11y_gl/config.yaml"))

        return search_paths

    def load_from_file(self, file_path: Optional[str] = None) -> None:
        """設定ファイルからの読み込み
        
        Args:
            file_path: 設定ファイルのパス。未指定の場合は標準の場所を探索
        """
        # 明示的なパスが指定された場合
        if file_path:
            path = Path(file_path).resolve()
            if path.is_file():
                with path.open() as f:
                    self.update(yaml.safe_load(f))
                return
            raise FileNotFoundError(f"Config file not found: {file_path}")

        # 標準的な場所を探索
        for path in self._get_config_search_paths():
            try:
                if path.is_file():
                    with path.open() as f:
                        self.update(yaml.safe_load(f))
                        return
            except (OSError, PermissionError):
                continue  # 読み取り権限がない場合など

    def load_from_env(self) -> None:
        """環境変数からの読み込み"""
        for key, value in os.environ.items():
            if key.startswith(self._env_prefix):
                # FREEE_A11Y_GL_URLS_BASE_JA -> ["urls"]["base"]["ja"]
                config_key = key[len(self._env_prefix):].lower()
                self.set_nested(config_key.split("_"), value)

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

# シングルトンインスタンス
settings = Settings()
