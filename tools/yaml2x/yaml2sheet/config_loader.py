import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Literal, Union
import logging
from pathlib import Path
from pydantic import BaseModel, Field, model_validator, field_validator, ValidationError
import yaml
import toml
import configparser

logger = logging.getLogger(__name__)

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def validate_readable_file(path: Union[str, Path]) -> Path:
    """Validate that a file exists and is readable
    
    Args:
        path: File path to validate
        
    Returns:
        Path: Validated Path object
        
    Raises:
        ValueError: If file doesn't exist or isn't readable
    """
    try:
        path_obj = Path(path)
        if not path_obj.is_file():
            raise ValueError(f"File does not exist: {path}")
        if not os.access(path_obj, os.R_OK):
            raise ValueError(f"File is not readable: {path}")
        return path_obj
    except Exception as e:
        raise ValueError(f"Invalid file path: {e}")

class ApplicationConfig(BaseModel):
    """Application configuration settings"""
    credentials_path: Path = Field(default=Path("credentials.json"), description="Path to Google credentials file")
    token_path: Path = Field(default=Path("token.json"), description="Path to Google token file")
    development_spreadsheet_id: str = Field("", description="Development environment spreadsheet ID")
    production_spreadsheet_id: str = Field("", description="Production environment spreadsheet ID")
    log_level: LogLevel = Field(default="INFO", description="Logging level")
    basedir: Optional[Path] = Field(None, description="Base directory for YAML files")
    base_url: str = Field(default="https://a11y-guidelines.freee.co.jp", description="Base URL for documentation")

    def get_base_url(self, cmd_base_url: Optional[str] = None) -> str:
        """Get base URL for documentation, resolving from command line or config
        
        Args:
            cmd_base_url: Base URL from command line (overrides config)
            
        Returns:
            str: Resolved base URL
        """
        # Command line takes precedence if provided
        if cmd_base_url is not None:
            return cmd_base_url
        return self.base_url

    def get_basedir(self, cmd_basedir: Optional[Union[str, Path]] = None) -> Path:
        """Get base directory for YAML files, resolving from command line or config
        
        Args:
            cmd_basedir: Base directory from command line (overrides config)
            
        Returns:
            Path: Resolved and validated base directory
            
        Raises:
            ValueError: If path is invalid or directory is not accessible
        """
        try:
            # Command line takes precedence if explicitly set (not default CWD)
            if cmd_basedir is not None and str(cmd_basedir) != str(Path.cwd()):
                path_obj = Path(cmd_basedir)
            # Then try config file value
            elif self.basedir is not None:
                path_obj = self.basedir
            # Finally fall back to CWD
            else:
                path_obj = Path.cwd()

            # Make relative paths relative to CWD
            if not path_obj.is_absolute():
                path_obj = Path.cwd() / path_obj
                
            # Validate directory
            if not path_obj.is_dir():
                raise ValueError(f"Base directory does not exist: {path_obj}")
            if not os.access(path_obj, os.R_OK):
                raise ValueError(f"Base directory is not readable: {path_obj}")
            
            return path_obj.resolve()
        except Exception as e:
            raise ValueError(f"Invalid base directory: {e}")

    @field_validator('basedir')
    @classmethod
    def _validate_basedir(cls, path: Optional[Path]) -> Optional[Path]:
        """Validate base directory from config file
        
        Args:
            path: Directory path to validate
            
        Returns:
            Optional[Path]: Validated path or None if not provided
        """
        if path is None:
            return None
            
        # Relative paths will be handled in get_basedir
        return Path(path)

    @field_validator('credentials_path', 'token_path')
    @classmethod
    def validate_path(cls, path: Path) -> Path:
        """Validate that paths exist and are readable
        
        Args:
            path: Path to validate
            
        Returns:
            Path: Validated path
            
        Raises:
            ValueError: If path is invalid or file is not readable
        """
        return validate_readable_file(path)
    
    def get_log_level(self) -> int:
        """Convert string log level to logging constant
        
        Returns:
            int: Logging level constant
        """
        return getattr(logging, self.log_level.upper(), logging.INFO)
    
    def get_spreadsheet_id(self, production: bool = False) -> str:
        """Get appropriate spreadsheet ID based on environment
        
        Args:
            production: Whether to use production spreadsheet
            
        Returns:
            str: Spreadsheet ID to use
            
        Raises:
            ValueError: If required spreadsheet ID is not set
        """
        if production:
            if not self.production_spreadsheet_id:
                raise ValueError(
                    "Production spreadsheet ID is not set in config. "
                    "Please set 'production_spreadsheet_id' in your config file or "
                    "PROD_CHECKSHEET_ID environment variable."
                )
            return self.production_spreadsheet_id
        else:
            if not self.development_spreadsheet_id:
                raise ValueError(
                    "Development spreadsheet ID is not set in config. "
                    "Please set 'development_spreadsheet_id' in your config file or "
                    "DEV_CHECKSHEET_ID environment variable."
                )
            return self.development_spreadsheet_id

    @model_validator(mode='before')
    @classmethod
    def check_environment_variables(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Load and validate configuration with environment variables
        
        Args:
            data: Raw configuration dictionary
            
        Returns:
            Dict[str, Any]: Validated configuration dictionary
        """
        # Override with environment variables if set
        env_mappings = {
            'GOOGLE_CREDENTIALS_PATH': 'credentials_path',
            'GOOGLE_TOKEN_PATH': 'token_path',
            'DEV_CHECKSHEET_ID': 'development_spreadsheet_id',
            'PROD_CHECKSHEET_ID': 'production_spreadsheet_id',
            'LOG_LEVEL': 'log_level'
        }
        
        for env_var, config_key in env_mappings.items():
            if env_value := os.getenv(env_var):
                data[config_key] = env_value
                logger.debug(f"Using environment variable for {config_key}")
                
        return data

class ConfigLoader(ABC):
    """Abstract base class for configuration loaders"""
    
    @abstractmethod
    def load(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from file
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dict[str, Any]: Loaded configuration
        """
        pass
        
    @abstractmethod
    def save(self, config: Dict[str, Any], config_path: Path) -> None:
        """Save configuration to file
        
        Args:
            config: Configuration to save
            config_path: Path to save configuration file
        """
        pass

class YAMLConfigLoader(ConfigLoader):
    """YAML configuration loader"""
    
    def load(self, config_path: Path) -> Dict[str, Any]:
        with config_path.open('r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
            
    def save(self, config: Dict[str, Any], config_path: Path) -> None:
        with config_path.open('w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)

class TOMLConfigLoader(ConfigLoader):
    """TOML configuration loader"""
    
    def load(self, config_path: Path) -> Dict[str, Any]:
        return toml.load(str(config_path))
            
    def save(self, config: Dict[str, Any], config_path: Path) -> None:
        with config_path.open('w', encoding='utf-8') as f:
            toml.dump(config, f)

class INIConfigLoader(ConfigLoader):
    """INI configuration loader"""
    
    def load(self, config_path: Path) -> Dict[str, Any]:
        config = configparser.ConfigParser()
        config.read(config_path)
        
        if 'General' not in config:
            return {}
            
        return dict(config['General'])
            
    def save(self, config: Dict[str, Any], config_path: Path) -> None:
        cfg = configparser.ConfigParser()
        cfg['General'] = config
        with config_path.open('w', encoding='utf-8') as f:
            cfg.write(f)

def get_config_loader(config_path: Path) -> ConfigLoader:
    """Get appropriate config loader based on file extension
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        ConfigLoader: Appropriate loader instance
        
    Raises:
        ValueError: If file extension is not supported
    """
    ext = config_path.suffix.lower()
    loaders = {
        '.yaml': YAMLConfigLoader(),
        '.yml': YAMLConfigLoader(),
        '.toml': TOMLConfigLoader(),
        '.ini': INIConfigLoader()
    }
    
    if ext not in loaders:
        raise ValueError(f"Unsupported configuration file format: {ext}")
        
    return loaders[ext]

def find_config_file(config_path: Optional[Union[str, Path]] = None) -> Path:
    """設定ファイルを探索する
    
    Args:
        config_path: コマンドラインで指定された設定ファイルパス
        
    Returns:
        Path: 見つかった設定ファイルの絶対パス
        
    Raises:
        FileNotFoundError: 設定ファイルが見つからない場合
    """
    try:
        # Convert to Path if string provided
        config_path_obj = Path(config_path) if config_path else None
    except Exception as e:
        raise ValueError(f"Invalid config path: {e}")

    # -c オプションで指定された場合
    if config_path_obj:
        if config_path_obj.is_absolute():
            # 絶対パスの場合はそのまま使用
            if not config_path_obj.exists():
                raise FileNotFoundError(f"Specified configuration file not found: {config_path_obj}")
            return validate_readable_file(config_path_obj)
        else:
            # 相対パスの場合は以下の順で探す:
            # 1. カレントディレクトリからの相対パス
            # 2. スクリプトディレクトリからの相対パス
            search_dirs = [
                Path.cwd(),  # Current working directory first
                Path(__file__).parent.absolute()  # Script directory second
            ]
            
            tried_paths = []
            for dir_path in search_dirs:
                try_path = dir_path / config_path_obj
                tried_paths.append(try_path)
                if try_path.exists():
                    return validate_readable_file(try_path)
            
            raise FileNotFoundError(
                "Specified configuration file not found. Searched in:\n" +
                "\n".join(f"- {p}" for p in tried_paths)
            )
    
    # File types in order of precedence
    config_types = ["yaml", "toml", "ini"]
    search_dirs = [
        Path.cwd(),  # Current working directory first
        Path(__file__).parent.absolute()  # Script directory second
    ]
    
    # Try all config types in current directory first
    for ext in config_types:
        config_path = Path.cwd() / f"config.{ext}"
        if config_path.exists():
            return validate_readable_file(config_path)
            
    # If not found, try all config types in script directory
    script_dir = Path(__file__).parent.absolute()
    for ext in config_types:
        config_path = script_dir / f"config.{ext}"
        if config_path.exists():
            return validate_readable_file(config_path)
    
    # Build search paths list for error message, maintaining search order
    search_paths = [
        Path.cwd() / f"config.{ext}"
        for ext in config_types
    ] + [
        Path(__file__).parent.absolute() / f"config.{ext}"
        for ext in config_types
    ]
    
    raise FileNotFoundError(
        "No configuration file found. Searched in order of precedence:\n" +
        "\n".join(f"- {p}" for p in search_paths)
    )

def load_configuration(config_path: Optional[Union[str, Path]] = None) -> ApplicationConfig:
    """Load application configuration from file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        ApplicationConfig: Loaded configuration
        
    Raises:
        FileNotFoundError: If config file is not found
        ValueError: If format is not supported or required settings are missing
        ValidationError: If configuration validation fails
    """
    try:
        actual_config_path = find_config_file(config_path)
        logger.info(f"Using configuration file: {actual_config_path}")
        
        loader = get_config_loader(actual_config_path)
        config_data = loader.load(actual_config_path)
        return ApplicationConfig.model_validate(config_data)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise
