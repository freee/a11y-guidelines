import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Literal, Union
import logging
from pathlib import Path
from pydantic import BaseModel, Field, model_validator, field_validator, ValidationError, ValidationInfo
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
    sheet_editor_email: str = Field("", description="Email (Google account) of the user allowed to edit protected ranges")
    log_level: LogLevel = Field(default="INFO", description="Logging level")
    basedir: Optional[Path] = Field(None, description="Base directory for YAML files")
    base_url: str = Field(default="https://a11y-guidelines.freee.co.jp", description="Base URL for documentation")

    @model_validator(mode='after')
    def resolve_credential_paths(self, info: ValidationInfo) -> 'ApplicationConfig':
        """Resolve credential and token paths relative to the config file."""
        # load_configurationからcontext経由で設定ファイルのパスを取得
        config_file_path = info.context.get('config_file_path') if info.context else None

        if config_file_path:
            config_dir = config_file_path.parent
            
            # 1. credentials_path が相対パスの場合、設定ファイルのディレクトリからの相対パスとして解決
            if not self.credentials_path.is_absolute():
                self.credentials_path = config_dir / self.credentials_path
            
            # 2. token_path が相対パスの場合、同様に解決
            if not self.token_path.is_absolute():
                self.token_path = config_dir / self.token_path
        
        return self

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

    @field_validator('credentials_path')
    @classmethod
    def validate_credentials_path(cls, path: Path) -> Path:
        """Validate credentials path format
        
        Args:
            path: Path to validate
            
        Returns:
            Path: Validated path
        """
        # Only validate format, not existence
        try:
            return Path(path)
        except Exception as e:
            raise ValueError(f"Invalid credentials path: {e}")

    @field_validator('token_path')
    @classmethod
    def validate_token_path(cls, path: Path) -> Path:
        """Token file path validator - only validates path format
        
        Args:
            path: Path to validate
            
        Returns:
            Path: Path object
        """
        try:
            return Path(path)
        except Exception as e:
            raise ValueError(f"Invalid token path: {e}")
    
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
                    "set the PROD_CHECKSHEET_ID environment variable."
                )
            return self.production_spreadsheet_id
        else:
            if not self.development_spreadsheet_id:
                raise ValueError(
                    "Development spreadsheet ID is not set in config. "
                    "Please set 'development_spreadsheet_id' in your config file or "
                    "set the DEV_CHECKSHEET_ID environment variable."
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
            'SHEET_EDITOR_EMAIL': 'sheet_editor_email',
            'LOG_LEVEL': 'log_level',
            'BASE_URL': 'base_url'
        }
        
        for env_var, config_key in env_mappings.items():
            if env_value := os.getenv(env_var):
                data[config_key] = env_value
                logger.debug(f"Using environment variable for {config_key}: {env_var}={env_value}")
                
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
        try:
            with config_path.open('r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                logger.debug(f"Loaded YAML config with {len(data)} keys")
                return data
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {config_path}: {e}")
            raise ValueError(f"Invalid YAML in config file: {e}")
            
    def save(self, config: Dict[str, Any], config_path: Path) -> None:
        with config_path.open('w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)
            logger.debug(f"Saved config to YAML file: {config_path}")

class TOMLConfigLoader(ConfigLoader):
    """TOML configuration loader"""
    
    def load(self, config_path: Path) -> Dict[str, Any]:
        try:
            data = toml.load(str(config_path))
            logger.debug(f"Loaded TOML config with {len(data)} keys")
            return data
        except toml.TomlDecodeError as e:
            logger.error(f"TOML parsing error in {config_path}: {e}")
            raise ValueError(f"Invalid TOML in config file: {e}")
            
    def save(self, config: Dict[str, Any], config_path: Path) -> None:
        with config_path.open('w', encoding='utf-8') as f:
            toml.dump(config, f)
            logger.debug(f"Saved config to TOML file: {config_path}")

class INIConfigLoader(ConfigLoader):
    """INI configuration loader"""
    
    def load(self, config_path: Path) -> Dict[str, Any]:
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            
            if 'General' not in config:
                logger.warning(f"No 'General' section found in INI file {config_path}")
                return {}
                
            data = dict(config['General'])
            logger.debug(f"Loaded INI config with {len(data)} keys")
            return data
        except configparser.Error as e:
            logger.error(f"INI parsing error in {config_path}: {e}")
            raise ValueError(f"Invalid INI in config file: {e}")
            
    def save(self, config: Dict[str, Any], config_path: Path) -> None:
        cfg = configparser.ConfigParser()
        cfg['General'] = config
        with config_path.open('w', encoding='utf-8') as f:
            cfg.write(f)
            logger.debug(f"Saved config to INI file: {config_path}")

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
        supported = ", ".join(loaders.keys())
        raise ValueError(f"Unsupported configuration file format: {ext}. Supported formats: {supported}")
        
    return loaders[ext]

def find_config_file(config_path: Optional[Union[str, Path]] = None) -> Path:
    """Find configuration file from specified path or default locations.

    Search logic:
    1. If -c option is used:
        a. If absolute path, use it directly.
        b. If relative path, search only in the current working directory.
    2. If -c option is NOT used, search in order:
        a. In `${HOME}/.config/freee_a11y_gl/` for `yaml2sheet.{yaml,yml,ini,toml}`
        b. In the current working directory for `.yaml2sheet.{yaml,yml,ini,toml}`

    Args:
        config_path: Command-line specified configuration file path.

    Returns:
        Path: Absolute path to the found configuration file.

    Raises:
        FileNotFoundError: If configuration file is not found.
    """
    # When -c option is specified, use the provided path directly
    if config_path:
        path_obj = Path(config_path)
        
        # a. When the path is absolute
        if path_obj.is_absolute():
            if not path_obj.exists():
                raise FileNotFoundError(f"Specified configuration file not found: {path_obj}")
            return validate_readable_file(path_obj)
        
        # b. When the path is relative (only serach in current directory)
        else:
            search_path = Path.cwd() / path_obj
            if search_path.exists():
                return validate_readable_file(search_path)
            else:
                raise FileNotFoundError(
                    "Specified configuration file not found in the current directory.\n"
                    f"- Searched for: {search_path}"
                )

    # Default  search logic when -c option is not used
    search_locations = [
        {
            "dir": Path.home() / ".config" / "freee_a11y_gl",
            "basename": "yaml2sheet"
        },
        {
            "dir": Path.cwd(),
            "basename": ".yaml2sheet"
        }
    ]
    
    config_types = ["yaml", "yml", "ini", "toml"]
    
    tried_paths = []
    for loc in search_locations:
        if not loc["dir"].is_dir():
            continue
        for ext in config_types:
            path_to_check = loc["dir"] / f"{loc['basename']}.{ext}"
            tried_paths.append(path_to_check)
            if path_to_check.exists():
                logger.debug(f"Found config file: {path_to_check}")
                return validate_readable_file(path_to_check)

    # If no config file found, raise FileNotFoundError
    raise FileNotFoundError(
        "No configuration file found. Searched in order of precedence:\n" +
        "\n".join(f"- {p}" for p in tried_paths) +
        "\n\nTo create a config file, save as "
        f"'{Path.home() / '.config' / 'freee_a11y_gl' / 'yaml2sheet.yaml'}' "
        "with the following content:\n" +
        "---\n" +
        "development_spreadsheet_id: YOUR_DEV_SPREADSHEET_ID\n" +
        "production_spreadsheet_id: YOUR_PROD_SPREADSHEET_ID\n"
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
        
        # Validate and return config
        try:
            validation_context = {"config_file_path": actual_config_path}
            validated_config = ApplicationConfig.model_validate(
                config_data,
                context=validation_context
            )
            
            return validated_config
        except ValidationError as e:
            logger.error(f"Configuration validation error: {e}")
            raise ValueError(f"Invalid configuration: {e}")
            
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise

def create_default_config(output_path: Optional[Union[str, Path]] = None) -> Path:
    """Create a default configuration file
    
    Args:
        output_path: Path to save configuration file (defaults to ./yaml2sheet.yaml)
        
    Returns:
        Path: Path to created configuration file
    """
    if output_path is None:
        output_path = Path.cwd() / "yaml2sheet.yaml"
    else:
        output_path = Path(output_path)
        
    # Create sample config
    default_config = {
        "credentials_path": "credentials.json",
        "token_path": "token.json",
        "development_spreadsheet_id": "",
        "production_spreadsheet_id": "",
        "log_level": "INFO",
        "base_url": "https://a11y-guidelines.freee.co.jp"
    }
    
    # Determine loader based on file extension
    loader = get_config_loader(output_path)
    
    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save config
    loader.save(default_config, output_path)
    logger.info(f"Created default configuration file at {output_path}")
    
    return output_path