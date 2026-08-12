"""Service functions for Maitabi mountain bus tours (bus.maitabi.jp & api.bus.maitabi.jp)."""

from datetime import datetime
import json
import asyncio

import httpx

from maitabi_mcp_server.config import API_BASE, WEB_BASE
from maitabi_mcp_server.models import (
    GetBusTourDetailInput,
    ListDistrictGroupsInput,
    ListFiltersInput,
    SearchBusToursInput,
)
from maitabi_mcp_server.services.http_client import get_http_client
from maitabi_mcp_server.services.utils import parse_days


async def _make_api_request(url: str, params: dict = None) -> dict:
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

    data = await _make_api_request(f"{API_BASE}/tour_course", params=params)
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

    data = await _make_api_request(f"{API_BASE}/district_group", params=params)
    return json.dumps(data, ensure_ascii=False, indent=2)


async def search_tours_service(input: SearchBusToursInput) -> str:
    """Search mountain bus tours with filters."""
    params = {"departure": str(input.departure), "page": str(input.page)}
    if input.month is not None:
        params["month"] = str(input.month)
    # Parse day input into a list of ints if possible
    parsed_days = parse_days(input.day)

    # If day is a list, we need to gather multiple requests concurrently
    if parsed_days and len(parsed_days) > 1:
        semaphore = asyncio.Semaphore(5)
        
        async def fetch_for_day(d: int):
            d_params = dict(params)
            d_params["day"] = str(d)
            async with semaphore:
                return await _make_api_request(f"{API_BASE}/tour_search", params=d_params)
                
        results = await asyncio.gather(*(fetch_for_day(d) for d in parsed_days))
        
        # Merge tours from all responses
        all_tours = []
        data = {"tour": []}
        for res in results:
            if "tour" in res and isinstance(res["tour"], list):
                all_tours.extend(res["tour"])
        data["tour"] = all_tours
    else:
        if parsed_days and len(parsed_days) == 1:
            params["day"] = str(parsed_days[0])
        data = await _make_api_request(f"{API_BASE}/tour_search", params=params)
    # Enrich and filter result items
    if "tour" in data and isinstance(data["tour"], list):
        filtered_tours = []
        for item in data["tour"]:
            # Apply min_price & max_price filters
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
                status = item.get("status", "")
                if status in ["満席", "受付終了", ""]:
                    continue

            # Extract year/month without regex
            date_str = item.get("date", "")
            y, m = datetime.now().year, input.month or datetime.now().month
            if "年" in date_str and "月" in date_str:
                parts = date_str.split("年")
                if len(parts) == 2:
                    y_str = parts[0]
                    m_str = parts[1].split("月")[0]
                    if y_str.isdigit() and m_str.isdigit():
                        y, m = int(y_str), int(m_str)
                        
            item["detail_url"] = (
                f"{WEB_BASE}/detail.html?course_no={item.get('course_no')}&year={y}&month={m}"
            )
            filtered_tours.append(item)
            
        data["tour"] = filtered_tours
    return json.dumps(data, ensure_ascii=False, indent=2)


async def get_tour_detail_service(input: GetBusTourDetailInput) -> str:
    """Fetch full details for a mountain bus tour."""
    if isinstance(input.course_no, list):
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
