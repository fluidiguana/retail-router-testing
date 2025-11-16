"""Main entry point for the ReACT agent."""

import sys
from agent.react_agent import ReACTAgent
from tools.basic_tools import (
    CalculatorTool,
    FileReadTool,
    FileWriteTool,
    ListDirectoryTool,
    WebSearchTool,
)
from utils.config import config


def setup_agent() -> ReACTAgent:
    """Set up the ReACT agent with all available tools."""
    # Validate configuration
    if not config.validate():
        print("Configuration validation failed. Please check your .env file.")
        sys.exit(1)

    # Create agent
    agent = ReACTAgent(api_key=config.OPENAI_API_KEY, model=config.DEFAULT_MODEL)

    # Register tools
    agent.register_tool(CalculatorTool())
    agent.register_tool(FileReadTool())
    agent.register_tool(FileWriteTool())
    agent.register_tool(ListDirectoryTool())

    if config.ENABLE_WEB_SEARCH:
        agent.register_tool(WebSearchTool())

    return agent


def main():
    """Main function to run the ReACT agent."""
    print("=== ReACT Agent ===")
    print("Type 'quit' or 'exit' to stop the agent.\n")

    # Set up the agent
    try:
        agent = setup_agent()
        print("✓ Agent initialized successfully!")
        print(f"✓ Available tools: {len(agent.tool_registry.list_tools())}")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        sys.exit(1)

    # Interactive loop
    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if not user_input:
                continue

            print("\nAgent is thinking...")
            response = agent.run(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
