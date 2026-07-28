"""Command-line entry point.

Usage:
    python main.py "your question"
    python main.py
"""

import sys

from src.config import KNOWLEDGE_BASE_PATH
from src.graph.workflow import build_workflow


def read_question() -> str:
    """Read the question from the command line, or prompt for it.

    Returns:
        The question text.
    """
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    try:
        return input("Question: ")
    except (EOFError, KeyboardInterrupt):
        return ""


def main() -> int:
    """Run one question through the workflow and print the result.

    Returns:
        Process exit code.
    """
    question = read_question().strip()
    if not question:
        print("No question provided.", file=sys.stderr)
        return 1

    if not KNOWLEDGE_BASE_PATH.is_file():
        print(f"Error: knowledge base file not found: {KNOWLEDGE_BASE_PATH}", file=sys.stderr)
        return 1

    try:
        result = build_workflow().invoke({"question": question})
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        # Provider and transport failures (invalid key, quota, network) surface here.
        print(f"Error calling the model: {error}", file=sys.stderr)
        return 1

    print("\n--- Retrieved context ---")
    print(result["context"] or "(nothing retrieved)")
    print("\n--- Answer ---")
    print(result["answer"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
