"""
Base Tool Class - Foundation for all tools
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from loguru import logger


class BaseTool(ABC):
    """Base class for all tools"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.logger = logger.bind(tool=name)

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute tool"""
        pass

    def get_info(self) -> Dict[str, Any]:
        """Get tool information"""
        return {
            "name": self.name,
            "description": self.description,
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get tool statistics"""
        return {
            "tool": self.name,
            "description": self.description,
        }
