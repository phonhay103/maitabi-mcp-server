"""Service functions for general Mainichi Travel tours & calendar (www.maitabi.jp)."""

import json
import re

import httpx

from maitabi_mcp_server.config import API_BASE, MAIN_BASE
from maitabi_mcp_server.models import (
    GetGeneralTourDetailInput,
    GetTourCalendarInput,
    SearchGeneralToursInput,
)
from maitabi_mcp_server.services.http_client import get_http_client


async def _make_api_request(url: str, params: list | dict | None = None) -> dict:
    """Helper to make GET requests to Maitabi API with error handling."""
    client = get_http_client()
    try:
        res = await client.get(url, params=params)
        res.raise_for_status()
        return res.json()
    except httpx.HTTPStatusError as e:
        return {
            "error": f"Upstream service returned error: {e.response.status_code}",
            "detail": str(e),
        }
    except httpx.RequestError as e:
        return {"error": "Failed to connect to Maitabi server", "detail": str(e)}


async def search_general_tours_service(input: SearchGeneralToursInput) -> str:
    """Search Mainichi Travel general tours."""
    params = [
        ("travelType", str(input.travel_type.value)),
        ("page", str(input.page))
    ]
    if input.keyword:
        params.append(("keyword", input.keyword))
    if input.year_month:
        params.append(("startDateYearMonthMin", input.year_month))
    if input.day is not None:
        params.append(("startDateDayMin", str(input.day)))
    if input.list_order:
        params.append(("listOrder", input.list_order))

    # Category arrays
    if input.category_nos1:
        for val in input.category_nos1:
            params.append(("categoryNos1[]", str(val)))
    if input.category_nos2:
        for val in input.category_nos2:
            params.append(("categoryNos2[]", str(val)))
    if input.category_nos3:
        for val in input.category_nos3:
            params.append(("categoryNos3[]", str(val)))
    if input.category_nos4:
        for val in input.category_nos4:
            params.append(("categoryNos4[]", str(val)))
    if input.category_nos5:
        for val in input.category_nos5:
            params.append(("categoryNos5[]", str(val)))

    data = await _make_api_request(f"{MAIN_BASE}/api/v1/category_search", params=params)

    # Enrich items with detail_url
    if "data" in data and isinstance(data["data"], list):
        for item in data["data"]:
            c_no = item.get("courseNo")
            if c_no:
                item["detail_url"] = f"{MAIN_BASE}/detail.php?courseNo={c_no}"

    return json.dumps(data, ensure_ascii=False, indent=2)


async def get_general_tour_detail_service(input: GetGeneralTourDetailInput) -> str:
    """Fetch complete details for a general tour using API_BASE."""
    data = await _make_api_request(
        f"{API_BASE}/tour_detail", params={"course_no": str(input.course_no)}
    )
    return json.dumps(data, ensure_ascii=False, indent=2)


async def get_tour_calendar_service(input: GetTourCalendarInput) -> str:
    """Fetch monthly departure calendar and tour schedule matrix."""
    url = f"{MAIN_BASE}/api/v1/calendar/{input.year}/{input.month}"
    params = {}
    if input.travel_type is not None:
        params["travelType"] = str(input.travel_type.value)

    data = await _make_api_request(url, params=params)
    return json.dumps(data, ensure_ascii=False, indent=2)
