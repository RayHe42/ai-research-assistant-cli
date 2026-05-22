"""CLI entry point for AI Research Assistant."""

import argparse
import sys

from research_assistant.ai_client import get_client
from research_assistant.file_loader import load_file
from research_assistant.output_writer import save_output
from research_assistant.prompts import build_qa_prompt, build_summarize_prompt, build_tasks_prompt


def _load_file_or_exit(filepath: str) -> str:
    """Load a file or exit with an error message.

    Args:
        filepath: Path to the file to read.

    Returns:
        The file content as a string.
    """
    try:
        return load_file(filepath)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _print_and_save(result: str, args: argparse.Namespace, command: str) -> None:
    """Print result and optionally save to file.

    Args:
        result: The AI output to print/save.
        args: The parsed arguments (may have --save flag).
        command: The command name (summarize, ask, tasks).
    """
    print(result)

    if hasattr(args, "save") and args.save:
        try:
            filepath = save_output(result, command, args.file)
            print(f"\nOutput saved to: {filepath}", file=sys.stderr)
        except OSError as e:
            print(f"Error: Failed to save output: {e}", file=sys.stderr)


def cmd_summarize(args: argparse.Namespace) -> None:
    """Handle the summarize command."""
    content = _load_file_or_exit(args.file)
    prompt = build_summarize_prompt(content)
    client = get_client()
    result = client.summarize(prompt)
    _print_and_save(result, args, "summarize")


def cmd_ask(args: argparse.Namespace) -> None:
    """Handle the ask command."""
    content = _load_file_or_exit(args.file)
    prompt = build_qa_prompt(content, args.question)
    client = get_client()
    result = client.ask(prompt)
    _print_and_save(result, args, "ask")


def cmd_tasks(args: argparse.Namespace) -> None:
    """Handle the tasks command."""
    content = _load_file_or_exit(args.file)
    prompt = build_tasks_prompt(content)
    client = get_client()
    result = client.generate_tasks(prompt)
    _print_and_save(result, args, "tasks")


def cmd_history(args: argparse.Namespace) -> None:
    """Handle the history command."""
    print("No history yet.")


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="research",
        description="AI Research Assistant CLI - helps with research and study workflows",
    )

    subparsers = parser.add_subparsers(dest="command")

    # summarize command
    summarize_parser = subparsers.add_parser(
        "summarize", help="Summarize a text file"
    )
    summarize_parser.add_argument("file", help="Path to the .txt or .md file")
    summarize_parser.add_argument(
        "--save", action="store_true", help="Save output to file"
    )

    # ask command
    ask_parser = subparsers.add_parser(
        "ask", help="Ask a question about a text file"
    )
    ask_parser.add_argument("file", help="Path to the .txt or .md file")
    ask_parser.add_argument("question", help="The question to ask")
    ask_parser.add_argument(
        "--save", action="store_true", help="Save output to file"
    )

    # tasks command
    tasks_parser = subparsers.add_parser(
        "tasks", help="Generate follow-up study tasks from a text file"
    )
    tasks_parser.add_argument("file", help="Path to the .txt or .md file")
    tasks_parser.add_argument(
        "--save", action="store_true", help="Save output to file"
    )

    # history command
    subparsers.add_parser("history", help="Show research assistant history")

    args = parser.parse_args()

    if args.command == "summarize":
        cmd_summarize(args)
    elif args.command == "ask":
        cmd_ask(args)
    elif args.command == "tasks":
        cmd_tasks(args)
    elif args.command == "history":
        cmd_history(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
