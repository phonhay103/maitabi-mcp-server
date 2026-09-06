# Maitabi MCP ↔ Skill Sync Guide

**Purpose**: Keep MCP server (`src/`) and standalone skill (`skills/maitabi-bus-extractor/`) in sync.

---

## Architecture (Both Layers Match)

```
Layer 1: build_query(filters)  →  URL query string
Layer 2: fetch_list(query)     →  HTTP GET to api.bus.maitabi.jp / www.maitabi.jp/api/v1
Layer 3: parse_list(payload)   →  Standardized JSON (course_no, course_cd, title, date, price, status, detail_url)
```

---

## Must-Match Tables

### Domains / Travel Types
| Domain | travel_type | MCP Enum | Skill Value |
|--------|-------------|----------|-------------|
| Mountain Bus | 3 | `TravelType.MOUNTAIN_BUS` | 3 |
| Domestic Mountain | 1 | `TravelType.DOMESTIC_MOUNTAIN` | 1 |
| Domestic Travel | 2 | `TravelType.DOMESTIC_TRAVEL` | 2 |
| Overseas Mountain | 4 | `TravelType.OVERSEAS_MOUNTAIN` | 4 |
| Overseas Travel | 5 | `TravelType.OVERSEAS_TRAVEL` | 5 |

### Mountain Bus Filters
| Param | MCP Field | Skill Param | Enum/Type |
|-------|-----------|-------------|-----------|
| Departure | `departure` | `departure` | `DeparturePoint` (1/2/3) |
| Month | `month` | `month` | int 1-12 (required) |
| Day | `day` | `day` | int/list/str 1-31 |
| Area | `area` | `area` | int (see filter-mapping.md) |
| Style | `style` | `style` | `TourStyle` (1-7) |
| Return Day | `return_day` | `return_day` | `ReturnDayOption` (1-5) |
| Bus Seat | `bus_sheet` | `bus_sheet` | `BusSeatType` (1-6) |
| Lodges | `stay1/2/3` | `stay1/2/3` | int |
| Course Code | `course_cd` | `course_cd` | str |
| Keyword | `keyword` | `keyword` | str |
| Min/Max Price | `min_price`/`max_price` | (post-filter) | int JPY |
| Require Seats | `require_available_seats` | (post-filter) | bool |

### Actions / Tools / Endpoints
| Action | MCP Tool | Service | Endpoint |
|--------|----------|---------|----------|
| `list_filters` | `list_filters` | `list_filters_service` | `GET /tour_course` |
| `list_district_groups` | `list_district_groups` | `list_district_groups_service` | `GET /district_group` |
| `search_tours` | `search_tours` | `search_tours_service` | `GET /tour_search` |
| `get_tour_detail` | `get_tour_detail` | `get_tour_detail_service` | `GET /tour_detail` |
| `search_general_tours` | `search_general_tours` | `search_general_tours_service` | `GET /category_search` |
| `get_general_tour_detail` | `get_general_tour_detail` | `get_general_tour_detail_service` | `GET /tour_detail` |
| `get_tour_calendar` | `get_tour_calendar` | `get_tour_calendar_service` | `GET /calendar/{year}/{month}` |

---

## Output Format (Identical)

```json
{
  "count": 23,
  "page": "1",
  "tour": [{ "travel_type": 3, "course_cd": "S104C21", "course_no": 14241, "date": "2026年09月12日(土)", "title": "...", "tour_day": "1日", "price": "15,500円", "status": "受付中", "phone_reserve": 0, "detail_url": "https://bus.maitabi.jp/detail.html?course_no=14241&year=2026&month=9" }],
  "param": { "departure": "1", "page": "1", "month": "9", "day": "12" }
}
```

---

## Sync Checklist (On Every Change)

- [ ] `models.py` enums/fields updated
- [ ] `services/*.py` endpoints/logic updated
- [ ] `tools/*.py` tool definitions updated
- [ ] `SKILL.md` filter schema, actions, cURL examples updated
- [ ] `filter-mapping.md` ID mappings updated
- [ ] Tests pass: `uv run pytest tests/ -v`
- [ ] cURL from SKILL.md matches MCP output

---

## File Map

| Component | Path |
|-----------|------|
| Models | `src/maitabi_mcp_server/models.py` |
| Bus Service | `src/maitabi_mcp_server/services/bus_service.py` |
| General Service | `src/maitabi_mcp_server/services/general_service.py` |
| Bus Tools | `src/maitabi_mcp_server/tools/bus_tools.py` |
| General Tools | `src/maitabi_mcp_server/tools/general_tools.py` |
| Skill Doc | `skills/maitabi-bus-extractor/SKILL.md` |
| Filter Refs | `skills/maitabi-bus-extractor/references/filter-mapping.md` |

---

## Workflow

1. Branch → 2. Edit MCP + Skill together → 3. Test both → 4. PR → 5. Merge → 6. Tag release → 7. `npx skills add -g <repo>`