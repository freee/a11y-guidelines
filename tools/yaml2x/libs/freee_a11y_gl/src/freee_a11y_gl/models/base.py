"""Base model classes."""
from typing import Any, Dict, List, Optional, Type, TypeVar

T = TypeVar('T', bound='BaseModel')

class BaseModel:
    """Base class for all models."""
    
    object_type: str = ""
    _instances: Dict[str, Any] = {}

    def __init__(self, id: str):
        """Initialize base model.
        
        Args:
            id: Unique identifier for the model instance
        """
        self.id = id
        if not hasattr(self.__class__, '_instances'):
            self.__class__._instances = {}

    @classmethod
    def get_by_id(cls: Type[T], id: str) -> Optional[T]:
        """Get model instance by ID.
        
        Args:
            id: Instance identifier
            
        Returns:
            Model instance if found, None otherwise
        """
        return cls._instances.get(id)
