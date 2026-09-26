---
name: maitabi-mcp
description: Use the Maitabi MCP server tools (list_filters, search_tours, get_tour_detail, search_general_tours, get_general_tour_detail, get_tour_calendar) from an MCP client to search mountain bus and general tours. Use when the user works inside Claude Desktop, Cursor, VSCode/Cline, or Pi — no terminal CLI or raw HTTP needed.
---

# Maitabi MCP Skill

Connect the `maitabi-mcp-server` to your MCP client. The server wraps the same core as the `maitabi` CLI, so results match CLI outputs.

## 1. Install / configure client

### Via `uvx` (recommended)

Claude Desktop / Cursor / Pi (`claude_desktop_config.json`, top-level `mcpServers`):

```json
{
  "mcpServers": {
    "maitabi": { "command": "uvx", "args": ["maitabi-mcp-server"] }
  }
}
```

VSCode / Cline / Roo Code (`mcp_settings.json`, top-level `servers`, needs `"type": "stdio"`):

```json
{
  "servers": {
    "maitabi": { "command": "uvx", "args": ["maitabi-mcp-server"], "type": "stdio" }
  },
  "inputs": []
}
```

### Via Docker

```json
{
  "mcpServers": {
    "maitabi": { "command": "docker", "args": ["run", "-i", "--rm", "phonhay103/maitabi-mcp-server:latest"] }
  }
}
```

### Local checkout

```json
{
  "mcpServers": {
    "maitabi": { "command": "uv", "args": ["run", "--directory", "/path/to/maitabi-mcp-server", "maitabi-mcp-server"] }
  }
}
```

HTTP/SSE transports: run `maitabi-mcp-server --transport streamable-http --host 0.0.0.0 --port 8000` (or `sse`) and point the client at the URL. Env overrides: `MCP_TRANSPORT`, `HOST`, `PORT`, `MCP_PATH`.

## 2. Tools (7)

### Mountain bus (`bus.maitabi.jp`)

- **`list_filters`** — filter dropdown options, lodges, tour counts. Cascading: counts update with other filters. Args: `departure` (1=Tokyo, 2=Osaka/Kyoto, 3=Nagoya), `month` 1-12, `day`, `area`, `style` 1-7, `return_day` 1-5, `bus_sheet` 1-6, `stay1/2/3`, `course_cd`, `keyword`.
- **`list_district_groups`** — area/district groups + counts. Same args as `list_filters`.
- **`search_tours`** — search bus tours + lodge packages. Same filters plus `day` as int/list/range string (e.g. `'14-16, 20'`), `page`, `min_price`/`max_price` (JPY), `require_available_seats` (drops 満席/受付終了).
- **`get_tour_detail`** — full itinerary/schedule/pricing by `course_no` (int or list for batch).

### General tours (`www.maitabi.jp`)

- **`search_general_tours`** — categories `travel_type`: 1=Domestic Mountain, 2=Domestic Travel, 3=Mountain Bus, 4=Overseas Mountain, 5=Overseas Travel. Args: `keyword`, `year_month` (`YYYY-MM`), `day`, `page`, `min_price`/`max_price`, `require_available_seats`, `list_order` (`startDateAsc`, `saikouStatus`, `yoyakuStatus`, `priceAsc`, `priceDesc`), `category_nos1-5` (lists).
- **`get_general_tour_detail`** — itinerary/meals/guide/booking by `course_no` (int or list).
- **`get_tour_calendar`** — monthly departure matrix for `year`/`month`, optional `travel_type`.

## 3. Typical flows

1. Discover: `list_filters` (departure+month) → pick `area`/`style` IDs.
2. Search: `search_tours` (bus) or `search_general_tours` (trekking) with `require_available_seats=true` when user wants bookable tours.
3. Detail: `get_tour_detail` / `get_general_tour_detail` with `course_no` from results.
4. Calendar: `get_tour_calendar` for month overview before narrowing days.

## 4. Output

Tools return JSON strings with `detail_url` links included:

```json
{
  "count": 23,
  "page": "1",
  "tour": [{ "course_no": 14241, "course_cd": "S104C21", "date": "2026年09月12日(土)", "title": "...", "price": "15,500円", "status": "受付中", "detail_url": "https://bus.maitabi.jp/detail.html?course_no=14241&year=2026&month=9" }],
  "param": { "departure": "1", "page": "1", "month": "9" }
}
```

## 5. Filter ID reference

See `../maitabi-bus-extractor/references/filter-mapping.md` for departure/area/style/return-day/seat/lodge ID tables.

## 6. Troubleshooting

- No tools listed → check client config key (`mcpServers` vs `servers`+`type: stdio`) and restart client.
- Empty results → widen filters; `month` is required by backend (defaults to current month).
- `{"error": ...}` payload → upstream/network issue, retry before changing filters.
