"""MCP tools for general Mainichi Travel tours and calendar schedule."""

from typing import Annotated, Optional
from pydantic import Field

from maitabi_mcp_server.models import (
    GetGeneralTourDetailInput,
    GetTourCalendarInput,
    SearchGeneralToursInput,
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
        travel_type: Annotated[int, Field(description="Category ID: 1=Domestic Mountain Climbing/Trekking, 2=Domestic Travel/Hiking, 3=Mountain Bus, 4=Overseas Mountain Climbing/Trekking, 5=Overseas Travel")] = 1,
        keyword: Annotated[Optional[str], Field(description="Search keyword in Japanese (e.g. '富士山', '京都')")] = None,
        year_month: Annotated[Optional[str], Field(description="Departure year-month string (e.g. '2026-08')")] = None,
        day: Annotated[Optional[int], Field(description="Departure day (1-31)")] = None,
        page: Annotated[int, Field(description="Page number")] = 1,
    ) -> str:
        """Search Mainichi Travel general tours (www.maitabi.jp) across mountain climbing, hiking, and travel categories."""
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
        course_no: Annotated[int, Field(description="Tour course number on www.maitabi.jp (e.g. 1723, 24865)")],
    ) -> str:
        """Fetch complete details, itinerary, meal condition, and pricing for a general Mainichi Travel tour on www.maitabi.jp by courseNo."""
        return await get_general_tour_detail_service(GetGeneralTourDetailInput(course_no=course_no))

    @mcp.tool()
    async def get_tour_calendar(
        year: Annotated[int, Field(description="Year (e.g. 2026)")],
        month: Annotated[int, Field(description="Month (1-12)")],
        travel_type: Annotated[Optional[int], Field(description="Optional category ID filter (1=Domestic Mountain, 2=Domestic Travel, 3=Mountain Bus, 4=Overseas Mountain, 5=Overseas Travel)")] = None,
    ) -> str:
        """Fetch monthly departure calendar and tour schedule matrix on www.maitabi.jp for a given year and month."""
        return await get_tour_calendar_service(GetTourCalendarInput(year=year, month=month, travel_type=travel_type))
