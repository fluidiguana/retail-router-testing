"""ReACT (Reasoning + Acting) Agent implementation."""

import json
import re
from typing import Any, Dict, List, Optional
from openai import OpenAI
from tools.base import BaseTool, ToolRegistry, ToolResult


class ReACTAgent:
    """A ReACT agent that can reason and act using tools."""

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.tool_registry = ToolRegistry()
        self.conversation_history = []
        self.max_iterations = 10

    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool with the agent."""
        self.tool_registry.register(tool)

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        tool_schemas = self.tool_registry.get_tool_schemas()
        tools_description = "\n".join(
            [f"- {tool['name']}: {tool['description']}" for tool in tool_schemas]
        )

        return f"""You are a ReACT (Reasoning + Acting) agent. You can use tools to help solve problems.

Available tools:
{tools_description}

You should follow this format:
Thought: [Your reasoning about what to do next]
Action: [The action to take, should be one of the available tools]
Action Input: [The input to the action, as a JSON object]
Observation: [The result of the action]

When you have enough information to answer the user's question, you should respond with:
Final Answer: [Your final answer to the user]

Always think step by step and use tools when needed to gather information or perform actions."""

    def _parse_agent_response(self, response: str) -> Dict[str, Any]:
        """Parse the agent's response to extract thought, action, and action input."""
        result = {"thought": "", "action": "", "action_input": {}, "final_answer": ""}

        # Extract thought
        thought_match = re.search(
            r"Thought:\s*(.*?)(?=Action:|Final Answer:|$)", response, re.DOTALL
        )
        if thought_match:
            result["thought"] = thought_match.group(1).strip()

        # Extract action
        action_match = re.search(
            r"Action:\s*(.*?)(?=Action Input:|$)", response, re.DOTALL
        )
        if action_match:
            result["action"] = action_match.group(1).strip()

        # Extract action input
        action_input_match = re.search(
            r"Action Input:\s*(.*?)(?=Observation:|$)", response, re.DOTALL
        )
        if action_input_match:
            try:
                action_input_str = action_input_match.group(1).strip()
                result["action_input"] = json.loads(action_input_str)
            except json.JSONDecodeError:
                result["action_input"] = {"input": action_input_str}

        # Extract final answer
        final_answer_match = re.search(r"Final Answer:\s*(.*?)$", response, re.DOTALL)
        if final_answer_match:
            result["final_answer"] = final_answer_match.group(1).strip()

        return result

    def _execute_tool(self, action: str, action_input: Dict[str, Any]) -> ToolResult:
        """Execute a tool with the given input."""
        tool = self.tool_registry.get_tool(action)
        if not tool:
            return ToolResult(
                success=False, result=None, error=f"Tool '{action}' not found"
            )

        return tool.execute(**action_input)

    def _build_messages(
        self, user_input: str, observation: str = ""
    ) -> List[Dict[str, str]]:
        """Build messages for the OpenAI API."""
        messages = [{"role": "system", "content": self._get_system_prompt()}]

        # Add conversation history
        for entry in self.conversation_history:
            messages.append(entry)

        # Add current user input
        messages.append({"role": "user", "content": user_input})

        # Add observation if provided
        if observation:
            messages.append(
                {"role": "assistant", "content": f"Observation: {observation}"}
            )

        return messages

    def run(self, user_input: str) -> str:
        """Run the ReACT loop to process user input."""
        self.conversation_history = []
        current_input = user_input
        observation = ""

        for iteration in range(self.max_iterations):
            # Build messages for this iteration
            messages = self._build_messages(current_input, observation)

            # Get response from the model
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.1
            )

            agent_response = response.choices[0].message.content
            print(f"\n--- Iteration {iteration + 1} ---")
            print(f"Agent Response: {agent_response}")

            # Parse the response
            parsed = self._parse_agent_response(agent_response)

            # Add to conversation history
            self.conversation_history.append(
                {"role": "assistant", "content": agent_response}
            )

            # Check if we have a final answer
            if parsed["final_answer"]:
                return parsed["final_answer"]

            # Execute action if present
            if parsed["action"]:
                print(
                    f"Executing action: {parsed['action']} with input: {parsed['action_input']}"
                )
                tool_result = self._execute_tool(
                    parsed["action"], parsed["action_input"]
                )

                if tool_result.success:
                    observation = f"Tool '{parsed['action']}' executed successfully. Result: {tool_result.result}"
                else:
                    observation = (
                        f"Tool '{parsed['action']}' failed. Error: {tool_result.error}"
                    )

                print(f"Observation: {observation}")

                # Add observation to conversation history
                self.conversation_history.append(
                    {"role": "user", "content": f"Observation: {observation}"}
                )
            else:
                # No action specified, ask for clarification
                observation = "No action specified. Please provide a valid action."
                print(f"Observation: {observation}")

        return "Maximum iterations reached. Unable to complete the task."

