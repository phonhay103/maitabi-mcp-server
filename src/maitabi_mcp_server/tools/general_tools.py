"""MCP tools for general Mainichi Travel tours and calendar schedule."""

from typing import Annotated, Optional
from pydantic import Field

from maitabi_mcp_server.models import (
    GetGeneralTourDetailInput,
    GetTourCalendarInput,
    SearchGeneralToursInput,
    TravelType,
)
from maitabi_mcp_server.services.general_service import (
    get_general_tour_detail_service,
    get_tour_calendar_service,
    search_general_tours_service,
)


def register_general_tools(mcp) -> None:
    """Register general tour and calendar tools with FastMCP instance."""

    @mcp.tool()
    async def search_general_tours(
        travel_type: Annotated[
            TravelType,
            Field(
                description="Category ID: 1=Domestic Mountain (default), 2=Domestic Travel, 3=Mountain Bus, 4=Overseas Mountain, 5=Overseas Travel"
            ),
        ] = TravelType.DOMESTIC_MOUNTAIN,
        keyword: Annotated[
            Optional[str],
            Field(
                min_length=1,
                max_length=100,
                description="Search keyword in Japanese (e.g., '富士山', '京都')",
            ),
        ] = None,
        year_month: Annotated[
            Optional[str],
            Field(
                pattern=r"^\d{4}-(?:0[1-9]|1[0-2])$",
                description="Departure year-month string in 'YYYY-MM' format (e.g., '2026-08')",
            ),
        ] = None,
        day: Annotated[
            Optional[int],
            Field(ge=1, le=31, description="Departure day of month (1-31)"),
        ] = None,
        page: Annotated[int, Field(ge=1, description="Page number (1-based)")] = 1,
    ) -> str:
        """Search general travel tours and mountain climbing packages on www.maitabi.jp.

        Returns a JSON string containing matching tours, total count, pagination, and course numbers.
        """
        input_data = SearchGeneralToursInput(
            travel_type=travel_type,
            keyword=keyword,
            year_month=year_month,
            day=day,
            page=page,
        )
        return await search_general_tours_service(input_data)

    @mcp.tool()
    async def get_general_tour_detail(
        course_no: Annotated[
            int,
            Field(
                gt=0,
                description="Tour course number on www.maitabi.jp (e.g., 1723, 24865)",
            ),
        ],
    ) -> str:
        """Fetch complete details, itinerary, pricing, and booking information for a general tour on www.maitabi.jp.

        Returns a JSON string containing tour itinerary, meal conditions, price matrix, lodging, and booking links.
        """
        return await get_general_tour_detail_service(
            GetGeneralTourDetailInput(course_no=course_no)
        )

    @mcp.tool()
    async def get_tour_calendar(
        year: Annotated[
            int, Field(ge=2000, le=2100, description="Year (e.g., 2026)")
        ],
        month: Annotated[int, Field(ge=1, le=12, description="Month (1-12)")],
        travel_type: Annotated[
            Optional[TravelType],
            Field(
                description="Optional category ID filter: 1=Domestic Mountain, 2=Domestic Travel, 3=Mountain Bus, 4=Overseas Mountain, 5=Overseas Travel"
            ),
        ] = None,
    ) -> str:
        """Fetch monthly departure calendar and tour schedule matrix on www.maitabi.jp for a given year and month.

        Returns a JSON string with daily departure schedule matrix, tour availability, and calendar dates.
        """
        return await get_tour_calendar_service(
            GetTourCalendarInput(year=year, month=month, travel_type=travel_type)
        )
