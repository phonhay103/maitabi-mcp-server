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
from maitabi_mcp_server.services.utils import parse_days


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
    parsed_days = parse_days(input.day)
    
    if parsed_days and len(parsed_days) > 1:
        # If it's a list, the underlying general tour API doesn't seem to support array day properly.
        # But we can try multiple parallel requests like bus tours.
        import asyncio
        semaphore = asyncio.Semaphore(5)
        
        async def fetch_for_day(d: int):
            d_params = list(params)
            d_params.append(("startDateDayMin", str(d)))
            async with semaphore:
                return await _make_api_request(f"{MAIN_BASE}/api/v1/category_search", params=d_params)
                
        results = await asyncio.gather(*(fetch_for_day(d) for d in parsed_days))
        
        all_tours = []
        data = {"data": []}
        for res in results:
            if "data" in res and isinstance(res["data"], list):
                all_tours.extend(res["data"])
        data["data"] = all_tours
    else:
        if parsed_days and len(parsed_days) == 1:
            params.append(("startDateDayMin", str(parsed_days[0])))
        data = await _make_api_request(f"{MAIN_BASE}/api/v1/category_search", params=params)
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

    # Enrich items with detail_url
    if "data" in data and isinstance(data["data"], list):
        filtered_tours = []
        for item in data["data"]:
            if c_no := item.get("courseNo"):
                item["detail_url"] = f"{MAIN_BASE}/detail.php?courseNo={c_no}"
            if input.min_price is not None or input.max_price is not None:
                price_str = str(item.get("price", "0"))
                cleaned = price_str.replace(",", "").replace("円", "").replace("～", "").strip()
                if cleaned.isdigit():
                    price_val = int(cleaned)
                    if input.min_price is not None and price_val < input.min_price:
                        continue
                    if input.max_price is not None and price_val > input.max_price:
                        continue
                        
            # Apply availability filter
            if input.require_available_seats:
                status = item.get("saikouStatus", "")
                if status in ["満席", "受付終了", "キャンセル待ち", "催行中止", ""]:
                    continue
                    
            filtered_tours.append(item)
            
        data["data"] = filtered_tours
    return json.dumps(data, ensure_ascii=False, indent=2)


async def get_general_tour_detail_service(input: GetGeneralTourDetailInput) -> str:
    """Fetch complete details for a general tour using API_BASE."""
    if isinstance(input.course_no, list):
        import asyncio
        semaphore = asyncio.Semaphore(5)
        
        async def fetch_one(c_no: int):
            async with semaphore:
                return await _make_api_request(
                    f"{API_BASE}/tour_detail", params={"course_no": str(c_no)}
                )
                
        results = await asyncio.gather(*(fetch_one(c) for c in input.course_no))
        return json.dumps({"tours": results}, ensure_ascii=False, indent=2)
    else:
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
