"""Entrypoint for the `maitabi` CLI (optional wrapper; default distribution is MCP)."""

from maitabi_mcp_server.cli.commands import COMMAND_HANDLERS
from maitabi_mcp_server.cli.parser import build_parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return
    handler = COMMAND_HANDLERS.get(args.command)
    if handler is None:  # pragma: no cover - argparse restricts choices
        parser.error(f"unknown command: {args.command}")
    handler(args)


if __name__ == "__main__":
    main()
