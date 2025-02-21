import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
import logging
import yaml
import toml
import configparser

logger = logging.getLogger(__name__)

@dataclass
class ApplicationConfig:
    """Application configuration settings"""
    credentials_path: str
    token_path: str
    development_spreadsheet_id: str
    production_spreadsheet_id: str
    log_level: str = "INFO"
    
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

    @classmethod
    def from_dict(cls, config_data: Dict[str, Any]) -> 'ApplicationConfig':
        """Create config from dictionary with validation
        
        Args:
            config_data: Configuration dictionary
            
        Returns:
            ApplicationConfig: Validated configuration object
            
        Raises:
            ValueError: If required settings are missing
        """
        # Set defaults
        defaults = {
            'credentials_path': 'credentials.json',
            'token_path': 'token.json'
        }
        
        # Merge with provided data
        merged_data = {**defaults, **config_data}
        
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
                merged_data[config_key] = env_value
                logger.debug(f"Using environment variable for {config_key}")
        
        # Validate minimal required settings
        required_fields = {'credentials_path', 'token_path'}
        missing_fields = required_fields - set(merged_data.keys())
        if missing_fields:
            raise ValueError(f"Missing required configuration fields: {', '.join(missing_fields)}")
            
        return cls(**merged_data)

class ConfigLoader(ABC):
    """Abstract base class for configuration loaders"""
    
    @abstractmethod
    def load(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from file
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dict[str, Any]: Loaded configuration
        """
        pass
        
    @abstractmethod
    def save(self, config: Dict[str, Any], config_path: str) -> None:
        """Save configuration to file
        
        Args:
            config: Configuration to save
            config_path: Path to save configuration file
        """
        pass

class YAMLConfigLoader(ConfigLoader):
    """YAML configuration loader"""
    
    def load(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
            
    def save(self, config: Dict[str, Any], config_path: str) -> None:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)

class TOMLConfigLoader(ConfigLoader):
    """TOML configuration loader"""
    
    def load(self, config_path: str) -> Dict[str, Any]:
        return toml.load(config_path)
            
    def save(self, config: Dict[str, Any], config_path: str) -> None:
        with open(config_path, 'w', encoding='utf-8') as f:
            toml.dump(config, f)

class INIConfigLoader(ConfigLoader):
    """INI configuration loader"""
    
    def load(self, config_path: str) -> Dict[str, Any]:
        config = configparser.ConfigParser()
        config.read(config_path)
        
        if 'General' not in config:
            return {}
            
        return dict(config['General'])
            
    def save(self, config: Dict[str, Any], config_path: str) -> None:
        cfg = configparser.ConfigParser()
        cfg['General'] = config
        with open(config_path, 'w', encoding='utf-8') as f:
            cfg.write(f)

def get_config_loader(config_path: str) -> ConfigLoader:
    """Get appropriate config loader based on file extension
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        ConfigLoader: Appropriate loader instance
        
    Raises:
        ValueError: If file extension is not supported
    """
    ext = os.path.splitext(config_path)[1].lower()
    loaders = {
        '.yaml': YAMLConfigLoader(),
        '.yml': YAMLConfigLoader(),
        '.toml': TOMLConfigLoader(),
        '.ini': INIConfigLoader()
    }
    
    if ext not in loaders:
        raise ValueError(f"Unsupported configuration file format: {ext}")
        
    return loaders[ext]

def load_configuration(config_path: str = 'config.yaml') -> ApplicationConfig:
    """Load application configuration from file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        ApplicationConfig: Loaded configuration
        
    Raises:
        FileNotFoundError: If config file is not found
        ValueError: If format is not supported or required settings are missing
    """
    if not os.path.exists(config_path):
        logger.warning(f"Configuration file not found: {config_path}")
        return ApplicationConfig.from_dict({})
        
    try:
        loader = get_config_loader(config_path)
        config_data = loader.load(config_path)
        logger.info(f"Loaded configuration from {config_path}")
        return ApplicationConfig.from_dict(config_data)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise
