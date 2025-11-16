"""Base tool class and tool registry for the ReACT agent."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ToolParameter(BaseModel):
    """Schema for tool parameters."""

    name: str
    type: str
    description: str
    required: bool = True


class ToolResult(BaseModel):
    """Result from tool execution."""

    success: bool
    result: Any
    error: Optional[str] = None


class BaseTool(ABC):
    """Base class for all tools."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.parameters = self._define_parameters()

    @abstractmethod
    def _define_parameters(self) -> List[ToolParameter]:
        """Define the parameters for this tool."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters."""
        pass

    def get_schema(self) -> Dict[str, Any]:
        """Get the tool schema for the agent."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    param.name: {"type": param.type, "description": param.description}
                    for param in self.parameters
                },
                "required": [param.name for param in self.parameters if param.required],
            },
        }


class ToolRegistry:
    """Registry for managing available tools."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[BaseTool]:
        """List all registered tools."""
        return list(self._tools.values())

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get schemas for all tools."""
        return [tool.get_schema() for tool in self._tools.values()]

