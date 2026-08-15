# Maitabi MCP Server

## Tagline
Search and explore Japanese alpine bus tours, mountain lodges, and trekking packages from Maitabi (毎日あるぺん号 & 毎日新聞旅行).

## Description
Maitabi MCP Server provides AI agents with real-time access to Japan's premier alpine transportation and mountain tour network, **Maitabi (まいたび - 毎日新聞旅行 / 毎日あるぺん号)**. Operating across `bus.maitabi.jp` and `www.maitabi.jp`, it allows LLM-powered assistants to search mountain bus departures, filter alpine lodge packages, inspect guided trekking itineraries, compare pricing, and examine departure calendars across the Northern, Central, and Southern Japanese Alps (including Kamikochi, Tateyama Murodo, Hakuba, Yatsugatake, and Mt. Fuji).

The server supports multi-parameter cascading filters (departure cities including Tokyo, Osaka, Kyoto, and Nagoya; departure months and date ranges; tour styles; standard/premium seat types; specific mountain lodges like Enzanso and Nishiho Sanso; price range and seat availability). It delivers clean, structured JSON data designed for itinerary planning, travel agent workflows, and mountain trip orchestration.

## Category
Travel & Lifestyle

## Pricing
Free (Open Source under Apache-2.0 License)

## Use Cases
Japan Alpine Trip Planning, Mountain Bus Departure Search, Mountain Lodge Package Discovery, Guided Trekking Itinerary Exploration, Multi-filter Tour Comparison, Departure Calendar Matrix Tracking, Outdoor & Hiking Concierge

## Features
- **Mountain Bus & Lodge Packages (`bus.maitabi.jp`)**: Direct access to Mainichi Alpen bus tours with seat types (Standard, Premium, Double seat) and mountain lodge stays.
- **General Trekking & Guided Tours (`www.maitabi.jp`)**: Full search across 5 travel categories (Domestic Mountain Climbing, Domestic Travel, Mountain Bus, Overseas Mountain, Overseas Travel).
- **Cascading Filter Discovery**: Fetch dynamic filter dropdowns, area groups, and live tour counts (`list_filters`, `list_district_groups`).
- **Comprehensive Tour Details**: Detailed itineraries, pricing breakdowns, pickup/drop-off points, meal plans, guide details, and direct booking links (`get_tour_detail`, `get_general_tour_detail`).
- **Departure Matrix Calendar**: Monthly calendar schedule extraction showing departures and availability for any year/month (`get_tour_calendar`).
- **Zero API Key Requirement**: Connects directly to public endpoints without requiring paid API tokens or complex credentials.
- **Multiple Transports Supported**: Works seamlessly over standard input/output (`stdio`), Server-Sent Events (`sse`), and Streamable HTTP (`streamable-http`).

## Setup Requirements
- **No API Key Required**: The server queries public Maitabi endpoints directly.
- **Runtime Prerequisites**:
  - Python 3.12+ (when running via `uvx` / `uv`) OR
  - Docker (when running via container)
- **Package**: Published as `maitabi-mcp-server` on PyPI and Docker Hub (`phonhay103/maitabi-mcp-server:latest`).

## Tools Provided

| Tool Name | Scope | Description |
| :--- | :--- | :--- |
| `list_filters` | Mountain Bus | Fetch cascading filter options, departure areas, tour styles, mountain lodges, and tour counts. |
| `list_district_groups` | Mountain Bus | Fetch mountain area/district groups and tour counts based on active filters. |
| `search_tours` | Mountain Bus | Search mountain bus tours with full filter support (departure point, date, area, style, seat type, lodge, price range, seat availability). |
| `get_tour_detail` | Mountain Bus | Fetch complete tour schedule, pricing matrix, and bus stop details by `course_no`. |
| `search_general_tours` | General Travel | Search general tours and alpine trekking packages on `www.maitabi.jp` by travel type, keyword, date, price, and subcategory filters. |
| `get_general_tour_detail` | General Travel | Fetch complete itinerary, meal condition, guide info, points of interest, and booking links by `course_no`. |
| `get_tour_calendar` | Calendar | Fetch monthly departure calendar matrix and tour counts for a given year and month. |

## Quick Start & Client Configuration

### 1. Claude Desktop
Add to `claude_desktop_config.json` (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

#### Via `uvx` (Recommended):
```json
{
  "mcpServers": {
    "maitabi": {
      "command": "uvx",
      "args": ["maitabi-mcp-server"]
    }
  }
}
```

#### Via Docker:
```json
{
  "mcpServers": {
    "maitabi": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "phonhay103/maitabi-mcp-server:latest"
      ]
    }
  }
}
```

### 2. Cursor (`.cursor/mcp.json` or Global `~/.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "maitabi": {
      "command": "uvx",
      "args": ["maitabi-mcp-server"]
    }
  }
}
```

### 3. VS Code / Cline / Roo Code (`mcp_settings.json`)
```json
{
  "servers": {
    "maitabi": {
      "type": "stdio",
      "command": "uvx",
      "args": ["maitabi-mcp-server"]
    }
  }
}
```

### 4. Agent Skills Integration (`npx skills`)
Install and use as an agent skill directly:
```bash
npx skills add phonhay103/maitabi-mcp-server
```

## Repository & Links
- **GitHub Repository**: [https://github.com/phonhay103/maitabi-mcp-server](https://github.com/phonhay103/maitabi-mcp-server)
- **Docker Hub**: [https://hub.docker.com/r/phonhay103/maitabi-mcp-server](https://hub.docker.com/r/phonhay103/maitabi-mcp-server)
- **License**: Apache-2.0
