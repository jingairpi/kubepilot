"""
ReAct agent using structured JSON outputs.

The agent uses the 'diagnose' prompt by default to guide
the LLM in calling K8s tools and eventually producing an answer.
"""

import json
import re
from kubepilot.agent.base import Agent
from kubepilot.prompts.diagnose_prompt import DIAGNOSE_PROMPT
from kubepilot.tools.k8s import run_tool_by_name
from jsonschema import validate, ValidationError


TOOL_CALL_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": ["tool_call"]},
        "tool": {"type": "string"},
        "args": {"type": "object"},
    },
    "required": ["type", "tool", "args"],
}

ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": ["answer"]},
        "diagnosis": {"type": "string"},
        "recommendation": {"type": "string"},
    },
    "required": ["type", "diagnosis", "recommendation"],
}

MAX_AGENT_STEPS = 6


class ReActAgent(Agent):
    """
    ReAct agent using structured JSON outputs.
    """

    def __init__(self, llm, prompt: str = DIAGNOSE_PROMPT):
        """
        :param llm: An LLM instance (subclass of kubepilot.llm.base.LLM).
        :param prompt: The system prompt or instructions to guide the conversation.
        """
        super().__init__(llm)
        self.prompt = prompt

    def run(self, user_input: str) -> str:
        """
        Execute the multi-step reasoning loop.
        :param user_input: E.g. "Diagnose the 'orders' deployment in 'production' namespace."
        :return: Final result string containing diagnosis & recommendation.
        """
        conversation = self._build_initial_prompt(user_input)
        self.logger.debug(f"Initial Conversation:\n{conversation}")

        for step in range(1, MAX_AGENT_STEPS + 1):
            self.logger.info(f"\n--- Step {step} ---")
            # 1) Ask the LLM for the next JSON response.
            llm_output = self.llm.generate_response(conversation)
            self.logger.debug(f"Raw LLM Output:\n{llm_output}")

            # 2) Parse the JSON output.
            parsed = self._parse_json(llm_output)
            if not parsed:
                # If not valid JSON, append a corrective instruction and loop again.
                corrective_message = (
                    "\nResponse was not valid JSON. Please respond in valid JSON.\n"
                )
                self.logger.warning(
                    "Invalid JSON received from LLM. Appending corrective message."
                )
                conversation += corrective_message
                continue

            resp_type = parsed.get("type", "")
            self.logger.debug(f"Parsed Response Type: {resp_type}")

            if resp_type == "tool_call":
                # LLM wants to call a K8s tool for more data.
                tool_name = parsed.get("tool", "")
                args = parsed.get("args", {})
                self.logger.info(f"Tool Call Requested: {tool_name} with args {args}")
                tool_output = run_tool_by_name(tool_name, args)
                self.logger.debug(f"Tool Output:\n{tool_output}")
                # Provide the tool's output as new context
                conversation += f"\nTool output:\n{tool_output}\n"

            elif resp_type == "answer":
                # We have a final diagnosis. Return it.
                diagnosis = parsed.get("diagnosis", "No diagnosis provided.")
                recommendation = parsed.get(
                    "recommendation", "No recommendation provided."
                )
                self.logger.info(
                    f"Final Answer:\nDiagnosis: {diagnosis}\nRecommendation: {recommendation}"
                )
                return f"Diagnosis: {diagnosis}\nRecommendation: {recommendation}"

            else:
                # Unknown or malformed type
                unrecognized_message = (
                    "\nUnrecognized response type. Expect 'tool_call' or 'answer'.\n"
                )
                self.logger.warning(
                    "Unrecognized response type received from LLM. Appending unrecognized message."
                )
                conversation += unrecognized_message

        # If we exit the loop without an answer, time out
        timeout_message = "Error: Agent timed out without providing a final 'answer'."
        self.logger.error(timeout_message)
        return timeout_message

    def _build_initial_prompt(self, user_input: str) -> str:
        """
        Combine the system instructions (DIAGNOSE_PROMPT) with user input.
        """
        return f"{self.prompt}\n\nUSER QUERY:\n{user_input}\n"

    def _parse_json(self, text: str):
        """
        Extract and parse the first JSON object from the text.
        Validate against predefined schemas.
        """
        try:
            # Use regex to find the first JSON object
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                raise json.JSONDecodeError("No JSON object found", text, 0)
            json_text = match.group(0)
            data = json.loads(json_text)

            # Validate the JSON structure
            if data.get("type") == "tool_call":
                validate(instance=data, schema=TOOL_CALL_SCHEMA)
            elif data.get("type") == "answer":
                validate(instance=data, schema=ANSWER_SCHEMA)
            else:
                raise ValidationError("Invalid 'type' field in JSON.")

            return data
        except (json.JSONDecodeError, ValidationError) as e:
            self.logger.error(f"JSON parsing/validation error: {e}")
            return None
