"""Service functions for general Mainichi Travel tours & calendar (www.maitabi.jp)."""

import json
import re

import httpx

from maitabi_mcp_server.config import MAIN_BASE
from maitabi_mcp_server.models import (
    GetGeneralTourDetailInput,
    GetTourCalendarInput,
    SearchGeneralToursInput,
)


async def search_general_tours_service(input: SearchGeneralToursInput) -> str:
    """Search Mainichi Travel general tours."""
    params = {"travelType": str(input.travel_type), "page": str(input.page)}
    if input.keyword:
        params["keyword"] = input.keyword
    if input.year_month:
        params["startDateYearMonthMin"] = input.year_month
    if input.day is not None:
        params["startDateDayMin"] = str(input.day)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(f"{MAIN_BASE}/api/v1/category_search", params=params)
        res.raise_for_status()
        data = res.json()

        # Enrich items with detail_url
        if "data" in data and isinstance(data["data"], list):
            for item in data["data"]:
                c_no = item.get("courseNo")
                if c_no:
                    item["detail_url"] = f"{MAIN_BASE}/detail.php?courseNo={c_no}"

        return json.dumps(data, ensure_ascii=False, indent=2)


async def get_general_tour_detail_service(input: GetGeneralTourDetailInput) -> str:
    """Fetch complete details for a general tour."""
    url = f"{MAIN_BASE}/detail.php?courseNo={input.course_no}"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(url)
        res.raise_for_status()
        match = re.search(r"const detailData = (\{.*?\});", res.text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                return json.dumps(data, ensure_ascii=False, indent=2)
            except Exception:
                pass
        return json.dumps({"error": "Failed to parse tour detail JSON from page", "url": url}, ensure_ascii=False)


async def get_tour_calendar_service(input: GetTourCalendarInput) -> str:
    """Fetch monthly departure calendar and tour schedule matrix."""
    url = f"{MAIN_BASE}/api/v1/calendar/{input.year}/{input.month}"
    params = {}
    if input.travel_type is not None:
        params["travelType"] = str(input.travel_type)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        return json.dumps(data, ensure_ascii=False, indent=2)
