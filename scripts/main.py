import argparse
import sys

from kubepilot.llm.factory import create_llm_client
from kubepilot.agent.react_agent import ReActAgent


def main():
    parser = argparse.ArgumentParser(description="Run the kubepilot ReAct agent.")
    parser.add_argument(
        "--provider",
        choices=["ollama"],
        default="ollama",
        help="LLM provider to use (default: 'ollama'). Currently, only 'ollama' is supported.",
    )
    parser.add_argument(
        "--model",
        default="deepseek-r1:8b",
        help="Name of the model to use (e.g., 'deepseek-r1:8b').",
    )
    parser.add_argument(
        "--query",
        required=True,
        help="User query to send to the ReAct agent (e.g., 'Diagnose the orders deployment in production namespace.')",
    )
    args = parser.parse_args()

    try:
        llm = create_llm_client(provider=args.provider, model_name=args.model)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    agent = ReActAgent(llm)

    result = agent.run(args.query)
    print("\n--- Result ---")
    print(result)


if __name__ == "__main__":
    main()
