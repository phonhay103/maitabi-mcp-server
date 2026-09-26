# Maitabi Core ↔ MCP ↔ CLI ↔ Skills Sync Guide

**Purpose**: Core logic lives once in `models.py` + `services/`. MCP (`tools/` + `server.py`) and CLI (`cli/` + `cli_main.py`) are thin wrappers — never duplicate business logic. Three skills stay independent.

**Default distribution is MCP.** CLI (`maitabi`) is optional but ships in the same package/image. `dependencies` in `pyproject.toml` stay full (mcp, fastmcp, httpx, pydantic) so PyPI (`pip install maitabi-mcp-server` / `uvx maitabi-mcp-server`) and Docker Hub keep working unchanged.

---

## Architecture (All Layers Match)

```
Core:    models.py (Inputs/Enums) + services/bus_service.py + services/general_service.py
         + services/http_client.py + services/utils.py
Wrapper: tools/bus_tools.py + tools/general_tools.py + server.py   (MCP)
Wrapper: cli/parser.py + cli/commands.py + cli_main.py             (CLI)
Skill:   skills/maitabi-bus-extractor/ (raw curl/HTTP, standalone)
Skill:   skills/maitabi-cli/           (terminal `maitabi ...` only)
Skill:   skills/maitabi-mcp/           (MCP client tools only)
```

Rules:
- Fix/query/parse logic once in `services/`; MCP + CLI only map args → `*Input` → `*_service`.
- `cli/*` must NEVER import `fastmcp`/`mcp`/`server`/`tools` (keeps CLI importable without MCP deps).
- `__init__.py` stays empty (no heavy imports at package import time).

---

## Must-Match Tables

### Domains / Travel Types
| Domain | travel_type | MCP Enum | CLI Flag | Extractor Param |
|--------|-------------|----------|----------|-----------------|
| Mountain Bus | 3 | `TravelType.MOUNTAIN_BUS` | `--travel-type 3` | `travelType=3` |
| Domestic Mountain | 1 | `TravelType.DOMESTIC_MOUNTAIN` | `--travel-type 1` | `travelType=1` |
| Domestic Travel | 2 | `TravelType.DOMESTIC_TRAVEL` | `--travel-type 2` | `travelType=2` |
| Overseas Mountain | 4 | `TravelType.OVERSEAS_MOUNTAIN` | `--travel-type 4` | `travelType=4` |
| Overseas Travel | 5 | `TravelType.OVERSEAS_TRAVEL` | `--travel-type 5` | `travelType=5` |

### Mountain Bus Filters
| Param | MCP Field | CLI Flag | Extractor Param | Enum/Type |
|-------|-----------|----------|-----------------|-----------|
| Departure | `departure` | `--departure` | `departure` | `DeparturePoint` (1/2/3) |
| Month | `month` | `--month` | `month` | int 1-12 (required) |
| Day | `day` | `--day` | `day` | int/list/str 1-31 |
| Area | `area` | `--area` | `area` | int (see filter-mapping.md) |
| Style | `style` | `--style` | `style` | `TourStyle` (1-7) |
| Return Day | `return_day` | `--return-day` | `return_day` | `ReturnDayOption` (1-5) |
| Bus Seat | `bus_sheet` | `--bus-sheet` | `bus_sheet` | `BusSeatType` (1-6) |
| Lodges | `stay1/2/3` | `--stay1/2/3` | `stay1/2/3` | int |
| Course Code | `course_cd` | `--course-cd` | `course_cd` | str |
| Keyword | `keyword` | `--keyword` | `keyword` | str |
| Min/Max Price | `min_price`/`max_price` | `--min-price`/`--max-price` | (post-filter) | int JPY |
| Require Seats | `require_available_seats` | `--require-available-seats` | (post-filter) | bool |

### Actions / Tools / Commands / Endpoints
| Action | MCP Tool | CLI Subcommand | Service | Endpoint |
|--------|----------|----------------|---------|----------|
| `list_filters` | `list_filters` | `list-filters` | `list_filters_service` | `GET /tour_course` |
| `list_district_groups` | `list_district_groups` | `list-district-groups` | `list_district_groups_service` | `GET /district_group` |
| `search_tours` | `search_tours` | `search-tours` | `search_tours_service` | `GET /tour_search` |
| `get_tour_detail` | `get_tour_detail` | `get-tour-detail` | `get_tour_detail_service` | `GET /tour_detail` |
| `search_general_tours` | `search_general_tours` | `search-general-tours` | `search_general_tours_service` | `GET /category_search` |
| `get_general_tour_detail` | `get_general_tour_detail` | `get-general-tour-detail` | `get_general_tour_detail_service` | `GET /tour_detail` |
| `get_tour_calendar` | `get_tour_calendar` | `get-tour-calendar` | `get_tour_calendar_service` | `GET /calendar/{year}/{month}` |

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
- [ ] `services/*.py` endpoints/logic updated (fix once — both wrappers benefit)
- [ ] `tools/*.py` MCP wrappers updated
- [ ] `cli/parser.py` + `cli/commands.py` CLI wrappers updated
- [ ] `maitabi-bus-extractor/SKILL.md` cURL examples updated (standalone, no MCP/CLI refs)
- [ ] `maitabi-cli/SKILL.md` command examples updated (no curl/MCP refs)
- [ ] `maitabi-mcp/SKILL.md` tool docs updated (no curl/CLI refs)
- [ ] `filter-mapping.md` ID mappings updated (single source in `maitabi-bus-extractor/references/`)
- [ ] Tests pass: `uv run pytest tests/ -v` + `make cli-help`
- [ ] CLI output matches MCP output matches cURL response shape

---

## File Map

| Component | Path |
|-----------|------|
| Models | `src/maitabi_mcp_server/models.py` |
| Bus Service | `src/maitabi_mcp_server/services/bus_service.py` |
| General Service | `src/maitabi_mcp_server/services/general_service.py` |
| Bus Tools (MCP) | `src/maitabi_mcp_server/tools/bus_tools.py` |
| General Tools (MCP) | `src/maitabi_mcp_server/tools/general_tools.py` |
| CLI Parser | `src/maitabi_mcp_server/cli/parser.py` |
| CLI Commands | `src/maitabi_mcp_server/cli/commands.py` |
| CLI Entrypoint | `src/maitabi_mcp_server/cli_main.py` |
| Extractor Skill | `skills/maitabi-bus-extractor/SKILL.md` |
| CLI Skill | `skills/maitabi-cli/SKILL.md` |
| MCP Skill | `skills/maitabi-mcp/SKILL.md` |
| Filter Refs | `skills/maitabi-bus-extractor/references/filter-mapping.md` |

---

## Workflow

1. Branch → 2. Edit core (`services/`/`models.py`) → 3. Update MCP + CLI wrappers together → 4. Update affected skills → 5. Test all three interfaces → 6. PR → 7. Merge → 8. Tag release (`v*` triggers PyPI + Docker Hub) → 9. `npx skills add -g <repo>`
