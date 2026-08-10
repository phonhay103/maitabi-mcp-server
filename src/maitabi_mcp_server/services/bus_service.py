"""Service functions for Maitabi mountain bus tours (bus.maitabi.jp & api.bus.maitabi.jp)."""

from datetime import datetime
import json
import re

import httpx

from maitabi_mcp_server.config import API_BASE, WEB_BASE
from maitabi_mcp_server.models import (
    GetBusTourDetailInput,
    ListDistrictGroupsInput,
    ListFiltersInput,
    SearchBusToursInput,
)


async def list_filters_service(input: ListFiltersInput) -> str:
    """Fetch available filter options for mountain bus tours."""
    target_month = input.month if input.month is not None else datetime.now().month
    params = {"departure": str(input.departure.value), "month": str(target_month)}
    if input.day is not None:
        params["day"] = str(input.day)
    if input.area is not None:
        params["area"] = str(input.area)
    if input.style is not None:
        params["style"] = str(input.style)
    if input.return_day is not None:
        params["return_day"] = str(input.return_day)
    if input.bus_sheet is not None:
        params["bus_sheet"] = str(input.bus_sheet)
    if input.stay1 is not None:
        params["stay1"] = str(input.stay1)
    if input.stay2 is not None:
        params["stay2"] = str(input.stay2)
    if input.stay3 is not None:
        params["stay3"] = str(input.stay3)
    if input.course_cd:
        params["course_cd"] = input.course_cd
    if input.keyword:
        params["keyword"] = input.keyword

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{API_BASE}/tour_course", params=params)
        res.raise_for_status()
        data = res.json()
        return json.dumps(data, ensure_ascii=False, indent=2)


async def list_district_groups_service(input: ListDistrictGroupsInput) -> str:
    """Fetch district groups and tour counts for mountain bus tours."""
    target_month = input.month if input.month is not None else datetime.now().month
    params = {"departure": str(input.departure.value), "month": str(target_month)}
    if input.day is not None:
        params["day"] = str(input.day)
    if input.area is not None:
        params["area"] = str(input.area)
    if input.style is not None:
        params["style"] = str(input.style)
    if input.return_day is not None:
        params["return_day"] = str(input.return_day)
    if input.bus_sheet is not None:
        params["bus_sheet"] = str(input.bus_sheet)
    if input.stay1 is not None:
        params["stay1"] = str(input.stay1)
    if input.stay2 is not None:
        params["stay2"] = str(input.stay2)
    if input.stay3 is not None:
        params["stay3"] = str(input.stay3)
    if input.course_cd:
        params["course_cd"] = input.course_cd
    if input.keyword:
        params["keyword"] = input.keyword

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{API_BASE}/district_group", params=params)
        res.raise_for_status()
        data = res.json()
        return json.dumps(data, ensure_ascii=False, indent=2)


async def search_tours_service(input: SearchBusToursInput) -> str:
    """Search mountain bus tours with filters."""
    params = {"departure": str(input.departure), "page": str(input.page)}
    if input.month is not None:
        params["month"] = str(input.month)
    if input.day is not None:
        params["day"] = str(input.day)
    if input.area is not None:
        params["area"] = str(input.area)
    if input.style is not None:
        params["style"] = str(input.style)
    if input.return_day is not None:
        params["return_day"] = str(input.return_day)
    if input.bus_sheet is not None:
        params["bus_sheet"] = str(input.bus_sheet)
    if input.stay1 is not None:
        params["stay1"] = str(input.stay1)
    if input.stay2 is not None:
        params["stay2"] = str(input.stay2)
    if input.stay3 is not None:
        params["stay3"] = str(input.stay3)
    if input.course_cd:
        params["course_cd"] = input.course_cd
        params["travel_type"] = "3"
    if input.keyword:
        params["keyword"] = input.keyword
        params["travel_type"] = "3"

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{API_BASE}/tour_search", params=params)
        res.raise_for_status()
        data = res.json()

        # Enrich result items with dynamic detail_url
        if "tour" in data and isinstance(data["tour"], list):
            for item in data["tour"]:
                date_str = item.get("date", "")
                match = re.search(r"(\d{4})年(\d{2})月", date_str)
                if match:
                    y, m = match.group(1), int(match.group(2))
                else:
                    y, m = datetime.now().year, input.month or datetime.now().month
                item["detail_url"] = (
                    f"{WEB_BASE}/detail.html?course_no={item.get('course_no')}&year={y}&month={m}"
                )

        return json.dumps(data, ensure_ascii=False, indent=2)


async def get_tour_detail_service(input: GetBusTourDetailInput) -> str:
    """Fetch full details for a mountain bus tour."""
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{API_BASE}/tour_detail", params={"course_no": str(input.course_no)})
        res.raise_for_status()
        data = res.json()
        return json.dumps(data, ensure_ascii=False, indent=2)
