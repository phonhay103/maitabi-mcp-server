"""MCP tools for Maitabi mountain bus tours."""

from typing import Annotated, Optional
from pydantic import Field

from maitabi_mcp_server.models import (
    GetBusTourDetailInput,
    ListDistrictGroupsInput,
    ListFiltersInput,
    SearchBusToursInput,
)
from maitabi_mcp_server.services.bus_service import (
    get_tour_detail_service,
    list_district_groups_service,
    list_filters_service,
    search_tours_service,
)


def register_bus_tools(mcp) -> None:
    """Register mountain bus tour tools with FastMCP instance."""

    @mcp.tool()
    async def list_filters(
        departure: Annotated[int, Field(description="Point of departure: 1=Tokyo, 2=Osaka/Kyoto, 3=Nagoya")] = 1,
        month: Annotated[Optional[int], Field(description="Departure month (1-12). Defaults to current month if omitted.")] = None,
    ) -> str:
        """Fetch available filter dropdown options, departure areas, tour styles, mountain lodges, and tour counts for Maitabi bus tours."""
        return await list_filters_service(ListFiltersInput(departure=departure, month=month))

    @mcp.tool()
    async def list_district_groups(
        departure: Annotated[int, Field(description="Point of departure: 1=Tokyo, 2=Osaka/Kyoto, 3=Nagoya")] = 1,
        month: Annotated[Optional[int], Field(description="Departure month (1-12). Defaults to current month if omitted.")] = None,
    ) -> str:
        """Fetch area/district groups and tour counts for mountain bus tours on Maitabi."""
        return await list_district_groups_service(ListDistrictGroupsInput(departure=departure, month=month))

    @mcp.tool()
    async def search_tours(
        departure: Annotated[int, Field(description="Point of departure: 1=Tokyo, 2=Osaka/Kyoto, 3=Nagoya")] = 1,
        month: Annotated[Optional[int], Field(description="Departure month (1-12)")] = None,
        day: Annotated[Optional[int], Field(description="Departure day (1-31)")] = None,
        area: Annotated[Optional[int], Field(description="Area/direction ID (e.g. 18=Tateyama Murodo, 10=Kamikochi)")] = None,
        style: Annotated[Optional[int], Field(description="Tour style ID (e.g. 6=Night trip/round-trip)")] = None,
        return_day: Annotated[Optional[int], Field(description="Return date option ID (1=1 day after, 2=2 days after)")] = None,
        bus_sheet: Annotated[Optional[int], Field(description="Bus seat type ID (1=Standard, 2=Premium)")] = None,
        stay1: Annotated[Optional[int], Field(description="Mountain lodge ID for night 1")] = None,
        stay2: Annotated[Optional[int], Field(description="Mountain lodge ID for night 2")] = None,
        stay3: Annotated[Optional[int], Field(description="Mountain lodge ID for night 3")] = None,
        course_cd: Annotated[Optional[str], Field(description="Course code (e.g. 'S104C21')")] = None,
        keyword: Annotated[Optional[str], Field(description="Search keyword in Japanese (e.g. '立山')")] = None,
        page: Annotated[int, Field(description="Page number")] = 1,
    ) -> str:
        """Search mountain bus tours on Maitabi (bus.maitabi.jp) with filters."""
        input_data = SearchBusToursInput(
            departure=departure,
            month=month,
            day=day,
            area=area,
            style=style,
            return_day=return_day,
            bus_sheet=bus_sheet,
            stay1=stay1,
            stay2=stay2,
            stay3=stay3,
            course_cd=course_cd,
            keyword=keyword,
            page=page,
        )
        return await search_tours_service(input_data)

    @mcp.tool()
    async def get_tour_detail(
        course_no: Annotated[int, Field(description="Internal course number (e.g. 14241 or 8518)")],
    ) -> str:
        """Fetch full details for a specific Maitabi mountain bus tour by course_no."""
        return await get_tour_detail_service(GetBusTourDetailInput(course_no=course_no))
