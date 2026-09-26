"""Argparse definition for the `maitabi` CLI.

Thin wrapper: every subcommand maps 1-1 to an MCP tool / core service.
No network or parsing logic lives here — see `commands.py` and `services/`.
Must NOT import fastmcp/mcp/server/tools so the CLI stays importable
without MCP dependencies installed.
"""

import argparse


def _add_bus_filter_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--departure", type=int, choices=[1, 2, 3], default=1,
                   help="Departure point: 1=Tokyo, 2=Osaka/Kyoto, 3=Nagoya (default: 1)")
    p.add_argument("--month", type=int, choices=range(1, 13), default=None, metavar="1-12",
                   help="Departure month (1-12)")
    p.add_argument("--day", type=str, default=None, metavar="DAY",
                   help="Departure day: single int, comma list, or range (e.g. '14-16, 20')")
    p.add_argument("--area", type=int, default=None,
                   help="Area/direction ID (e.g. 18=Tateyama Murodo, 10=Kamikochi, 0=All)")
    p.add_argument("--style", type=int, choices=range(1, 8), default=None, metavar="1-7",
                   help="Tour style: 1=Round-trip bus, 2=Outbound, 3=Inbound, 4=Round-trip+lodge, 5=Outbound+lodge, 6=Night bus, 7=Taxi")
    p.add_argument("--return-day", dest="return_day", type=int, choices=range(1, 6),
                   default=None, metavar="1-5",
                   help="Return date option relative to departure: 1=next day ... 5=5 days after")
    p.add_argument("--bus-sheet", dest="bus_sheet", type=int, choices=range(1, 7),
                   default=None, metavar="1-6",
                   help="Bus seat type: 1=Standard, 2=Premium, 3=Outbound Premium/Inbound Standard, 4=Outbound Standard/Inbound Premium, 5=Double, 6=Taxi")
    p.add_argument("--stay1", type=int, default=None, help="Mountain lodge ID for night 1")
    p.add_argument("--stay2", type=int, default=None, help="Mountain lodge ID for night 2")
    p.add_argument("--stay3", type=int, default=None, help="Mountain lodge ID for night 3")
    p.add_argument("--course-cd", dest="course_cd", type=str, default=None,
                   help="Course code string (e.g. S104C21)")
    p.add_argument("--keyword", type=str, default=None,
                   help="Search keyword in Japanese (e.g. 立山)")


def _add_output_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--pretty", action="store_true",
                   help="Pretty-print JSON with indent=2")
    p.add_argument("--output", type=str, default=None, metavar="FILE",
                   help="Write JSON output to FILE instead of stdout")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maitabi",
        description="Maitabi CLI — search mountain bus & general tours (same core as MCP server)",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    # 1. list-filters
    p = sub.add_parser("list-filters", help="Fetch bus tour filter options and tour counts")
    _add_bus_filter_args(p)
    _add_output_args(p)

    # 2. list-district-groups
    p = sub.add_parser("list-district-groups", help="Fetch area/district groups and tour counts")
    _add_bus_filter_args(p)
    _add_output_args(p)

    # 3. search-tours
    p = sub.add_parser("search-tours", help="Search mountain bus tours with filters")
    _add_bus_filter_args(p)
    p.add_argument("--page", type=int, default=1, help="Page number (1-based, default: 1)")
    p.add_argument("--min-price", dest="min_price", type=int, default=None,
                   help="Minimum price in JPY")
    p.add_argument("--max-price", dest="max_price", type=int, default=None,
                   help="Maximum price in JPY")
    p.add_argument("--require-available-seats", dest="require_available_seats",
                   action="store_true",
                   help="Filter out full/closed tours (満席, 受付終了)")
    _add_output_args(p)

    # 4. get-tour-detail
    p = sub.add_parser("get-tour-detail", help="Fetch bus tour detail by course_no")
    p.add_argument("--course-no", dest="course_no", type=str, required=True, metavar="NO",
                   help="Course number(s), comma-separated for batch (e.g. '14241' or '14241,8518')")
    _add_output_args(p)

    # 5. search-general-tours
    p = sub.add_parser("search-general-tours", help="Search general tours on www.maitabi.jp")
    p.add_argument("--travel-type", dest="travel_type", type=int, choices=range(1, 6),
                   default=1, help="Category: 1=Domestic Mountain, 2=Domestic Travel, 3=Mountain Bus, 4=Overseas Mountain, 5=Overseas Travel (default: 1)")
    p.add_argument("--keyword", type=str, default=None, help="Search keyword in Japanese")
    p.add_argument("--year-month", dest="year_month", type=str, default=None, metavar="YYYY-MM",
                   help="Departure year-month (e.g. 2026-08)")
    p.add_argument("--day", type=str, default=None, metavar="DAY",
                   help="Departure day: single int, comma list, or range (e.g. '14-16, 20')")
    p.add_argument("--page", type=int, default=1, help="Page number (1-based, default: 1)")
    p.add_argument("--min-price", dest="min_price", type=int, default=None, help="Minimum price in JPY")
    p.add_argument("--max-price", dest="max_price", type=int, default=None, help="Maximum price in JPY")
    p.add_argument("--require-available-seats", dest="require_available_seats",
                   action="store_true", help="Filter out full/closed tours")
    p.add_argument("--list-order", dest="list_order", type=str, default=None,
                   help="Sort: startDateAsc, saikouStatus, yoyakuStatus, priceAsc, priceDesc")
    for i in range(1, 6):
        p.add_argument(f"--category-nos{i}", dest=f"category_nos{i}", type=str, default=None,
                       metavar="IDS", help=f"Subcategory Nos group {i}, comma-separated (e.g. '36,259')")
    _add_output_args(p)

    # 6. get-general-tour-detail
    p = sub.add_parser("get-general-tour-detail", help="Fetch general tour detail by courseNo")
    p.add_argument("--course-no", dest="course_no", type=str, required=True, metavar="NO",
                   help="Course number(s), comma-separated for batch (e.g. '1723' or '1723,24865')")
    _add_output_args(p)

    # 7. get-tour-calendar
    p = sub.add_parser("get-tour-calendar", help="Fetch monthly departure calendar matrix")
    p.add_argument("--year", type=int, required=True, help="Year (e.g. 2026)")
    p.add_argument("--month", type=int, choices=range(1, 13), required=True, help="Month (1-12)")
    p.add_argument("--travel-type", dest="travel_type", type=int, choices=range(1, 6),
                   default=None, help="Optional category filter 1-5")
    _add_output_args(p)

    return parser
