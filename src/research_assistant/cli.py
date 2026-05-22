"""CLI entry point for AI Research Assistant."""

import argparse
import sys

from research_assistant.ai_client import get_client
from research_assistant.exceptions import ResearchAssistantError
from research_assistant.file_loader import load_file
from research_assistant.logger import setup_logger
from research_assistant.output_writer import save_output
from research_assistant.prompts import build_qa_prompt, build_summarize_prompt, build_tasks_prompt


def cmd_summarize(args: argparse.Namespace) -> None:
    """Handle the summarize command."""
    content = load_file(args.file)
    prompt = build_summarize_prompt(content)
    client = get_client()
    result = client.summarize(prompt)
    print(result)

    if hasattr(args, "save") and args.save:
        filepath = save_output(result, "summarize", args.file)
        print(f"\nOutput saved to: {filepath}", file=sys.stderr)


def cmd_ask(args: argparse.Namespace) -> None:
    """Handle the ask command."""
    content = load_file(args.file)
    prompt = build_qa_prompt(content, args.question)
    client = get_client()
    result = client.ask(prompt)
    print(result)

    if hasattr(args, "save") and args.save:
        filepath = save_output(result, "ask", args.file)
        print(f"\nOutput saved to: {filepath}", file=sys.stderr)


def cmd_tasks(args: argparse.Namespace) -> None:
    """Handle the tasks command."""
    content = load_file(args.file)
    prompt = build_tasks_prompt(content)
    client = get_client()
    result = client.generate_tasks(prompt)
    print(result)

    if hasattr(args, "save") and args.save:
        filepath = save_output(result, "tasks", args.file)
        print(f"\nOutput saved to: {filepath}", file=sys.stderr)


def cmd_history(args: argparse.Namespace) -> None:
    """Handle the history command."""
    print("No history yet.")


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="research",
        description="AI Research Assistant CLI - helps with research and study workflows",
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose debug output",
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
    logger = setup_logger(verbose=args.verbose)

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "summarize":
            cmd_summarize(args)
        elif args.command == "ask":
            cmd_ask(args)
        elif args.command == "tasks":
            cmd_tasks(args)
        elif args.command == "history":
            cmd_history(args)
    except ResearchAssistantError as e:
        logger.error("Error: %s", e)
        sys.exit(1)
    except Exception as e:
        if args.verbose:
            logger.error("Unexpected error: %s", e, exc_info=True)
        else:
            logger.error("Error: An unexpected error occurred. Use --verbose for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
