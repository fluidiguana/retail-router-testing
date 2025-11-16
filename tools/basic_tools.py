"""Basic tools for the ReACT agent."""

import json
import os
import time
from typing import Any, List
from .base import BaseTool, ToolParameter, ToolResult


class CalculatorTool(BaseTool):
    """Tool for performing basic mathematical calculations."""

    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform basic mathematical calculations (addition, subtraction, multiplication, division)",
        )

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="expression",
                type="string",
                description="Mathematical expression to evaluate (e.g., '2 + 3 * 4')",
                required=True,
            )
        ]

    def execute(self, **kwargs) -> ToolResult:
        try:
            expression = kwargs.get("expression", "")
            # Simple evaluation for basic operations
            # In production, use a proper math parser for security
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return ToolResult(
                    success=False,
                    result=None,
                    error="Expression contains invalid characters",
                )

            result = eval(expression)
            return ToolResult(success=True, result=result)
        except Exception as e:
            return ToolResult(success=False, result=None, error=str(e))


class FileReadTool(BaseTool):
    """Tool for reading files."""

    def __init__(self):
        super().__init__(name="read_file", description="Read the contents of a file")

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="file_path",
                type="string",
                description="Path to the file to read",
                required=True,
            )
        ]

    def execute(self, **kwargs) -> ToolResult:
        try:
            file_path = kwargs.get("file_path", "")
            if not os.path.exists(file_path):
                return ToolResult(
                    success=False, result=None, error=f"File not found: {file_path}"
                )

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            return ToolResult(success=True, result=content)
        except Exception as e:
            return ToolResult(success=False, result=None, error=str(e))


class FileWriteTool(BaseTool):
    """Tool for writing to files."""

    def __init__(self):
        super().__init__(name="write_file", description="Write content to a file")

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="file_path",
                type="string",
                description="Path to the file to write",
                required=True,
            ),
            ToolParameter(
                name="content",
                type="string",
                description="Content to write to the file",
                required=True,
            ),
        ]

    def execute(self, **kwargs) -> ToolResult:
        try:
            file_path = kwargs.get("file_path", "")
            content = kwargs.get("content", "")

            # Create directory if it doesn't exist
            dir_path = os.path.dirname(file_path)
            if dir_path:  # Only create directory if there's a directory path
                os.makedirs(dir_path, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return ToolResult(success=True, result=f"Successfully wrote to {file_path}")
        except Exception as e:
            return ToolResult(success=False, result=None, error=str(e))


class ListDirectoryTool(BaseTool):
    """Tool for listing directory contents."""

    def __init__(self):
        super().__init__(
            name="list_directory", description="List the contents of a directory"
        )

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="directory_path",
                type="string",
                description="Path to the directory to list",
                required=True,
            )
        ]

    def execute(self, **kwargs) -> ToolResult:
        try:
            directory_path = kwargs.get("directory_path", "")
            if not os.path.exists(directory_path):
                return ToolResult(
                    success=False,
                    result=None,
                    error=f"Directory not found: {directory_path}",
                )

            if not os.path.isdir(directory_path):
                return ToolResult(
                    success=False,
                    result=None,
                    error=f"Path is not a directory: {directory_path}",
                )

            contents = os.listdir(directory_path)
            return ToolResult(success=True, result=contents)
        except Exception as e:
            return ToolResult(success=False, result=None, error=str(e))


class WebSearchTool(BaseTool):
    """Tool for performing web searches (mock implementation)."""

    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information (mock implementation)",
        )

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="query", type="string", description="Search query", required=True
            )
        ]

    def execute(self, **kwargs) -> ToolResult:
        try:
            query = kwargs.get("query", "")
            # Mock implementation - in real scenario, integrate with search API
            mock_results = [
                f"Mock search result 1 for '{query}'",
                f"Mock search result 2 for '{query}'",
                f"Mock search result 3 for '{query}'",
            ]

            return ToolResult(success=True, result=mock_results)
        except Exception as e:
            return ToolResult(success=False, result=None, error=str(e))
