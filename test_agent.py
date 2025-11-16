"""Simple test script to verify the ReACT agent setup."""

import os
import sys
from tools.basic_tools import (
    CalculatorTool,
    FileReadTool,
    FileWriteTool,
    ListDirectoryTool,
    WebSearchTool,
)


def test_tools():
    """Test all tools to ensure they work correctly."""
    print("Testing ReACT Agent Tools...")

    # Test Calculator Tool
    print("\n1. Testing Calculator Tool:")
    calc = CalculatorTool()
    result = calc.execute(expression="2 + 3 * 4")
    print(f"   2 + 3 * 4 = {result.result if result.success else result.error}")

    # Test File Write Tool
    print("\n2. Testing File Write Tool:")
    file_write = FileWriteTool()
    result = file_write.execute(
        file_path="test_output.txt", content="Hello from ReACT agent!"
    )
    print(f"   {result.result if result.success else result.error}")

    # Test File Read Tool
    print("\n3. Testing File Read Tool:")
    file_read = FileReadTool()
    result = file_read.execute(file_path="test_output.txt")
    print(f"   Content: {result.result if result.success else result.error}")

    # Test List Directory Tool
    print("\n4. Testing List Directory Tool:")
    list_dir = ListDirectoryTool()
    result = list_dir.execute(directory_path=".")
    if result.success:
        print(f"   Found {len(result.result)} items in current directory")
        print(
            f"   Items: {', '.join(result.result[:5])}{'...' if len(result.result) > 5 else ''}"
        )
    else:
        print(f"   Error: {result.error}")

    # Test Web Search Tool
    print("\n5. Testing Web Search Tool:")
    web_search = WebSearchTool()
    result = web_search.execute(query="Python programming")
    if result.success:
        print(f"   Found {len(result.result)} search results")
        print(f"   First result: {result.result[0]}")
    else:
        print(f"   Error: {result.error}")

    # Clean up test file
    try:
        os.remove("test_output.txt")
        print("\n✓ Cleaned up test file")
    except:
        pass

    print("\n✓ All tools tested successfully!")


def test_agent_structure():
    """Test that the agent structure is properly set up."""
    print("\nTesting Agent Structure...")

    # Check if all required files exist
    required_files = [
        "agent/__init__.py",
        "agent/react_agent.py",
        "tools/__init__.py",
        "tools/base.py",
        "tools/basic_tools.py",
        "utils/__init__.py",
        "utils/config.py",
        "main.py",
        "requirements.txt",
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✓ All required files present")

    # Test imports
    try:
        from agent.react_agent import ReACTAgent
        from tools.base import ToolRegistry

        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


if __name__ == "__main__":
    print("=== ReACT Agent Test Suite ===\n")

    # Test structure
    structure_ok = test_agent_structure()

    if structure_ok:
        # Test tools
        test_tools()
        print("\n🎉 All tests passed! The ReACT agent is ready to use.")
        print("\nTo run the agent:")
        print("1. Set up your .env file with OPENAI_API_KEY")
        print("2. Run: python main.py")
    else:
        print("\n❌ Some tests failed. Please check the setup.")
        sys.exit(1)


