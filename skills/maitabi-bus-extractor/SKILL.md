---
name: maitabi-bus-extractor
description: Skill for searching, filtering, and extracting mountain bus tour, alpine trekking, and general tour data from Maitabi (まいたび - 毎日新聞旅行 / 毎日あるぺん号 - bus.maitabi.jp & www.maitabi.jp). Supports filter modeling, REST API/HTML endpoints querying, parsing listing and detail pages, monthly calendar schedules, and standardized JSON output formatting.
---

# Maitabi Bus Extractor Skill

## 1. Overview

This skill equips the Agent to act as a powerful curl/API extractor and connector for both mountain bus tours (**毎日あるぺん号** - `bus.maitabi.jp`) and general travel/alpine trekking tours (**毎日新聞旅行** - `www.maitabi.jp`). All operations work through direct HTTP requests without requiring MCP code.

## 2. 3-Layer Architecture

The extractor operates on a 3-layer pattern to separate parameter handling, network requests, and data parsing:

### Layer 1: `build_query(filters)`
- Converts user-selected filters (JSON/Object format) into exact URL Query String parameters corresponding to Maitabi ID codes and travel types
- Maps human-readable filter names to internal query parameter IDs
- Handles default values and validation of parameter ranges

### Layer 2: `fetch_list(query)`
- Issues GET requests to Maitabi endpoints using `curl` or HTTP clients
- Supports two base domains:
  - `api.bus.maitabi.jp` REST endpoints for mountain bus tours
  - `www.maitabi.jp/api/v1` REST endpoints for general travel tours
- Parameters are constructed from Layer 1's query string

### Layer 3: `parse_list(payload)`
- Extracts and normalizes tour listings from JSON responses or HTML pages
- Maps raw API fields to standardized output format:
  - `course_no`/`courseNo` - Internal course number
  - `course_cd`/`courseCd` - Course code string (e.g., `S104C21`)
  - `title`/`courseName` - Tour title
  - `date`/`saikouDate` - Departure date
  - `duration` - Tour duration
  - `price` - Price in JPY
  - `status` - Availability status
  - `detail_url` - Link to tour detail page
- Includes pagination metadata

## 3. Domains & Supported Travel Categories

Maitabi covers two main domains with 5 travel category types (`travel_type` / `travelType`):

### Domain A: Mountain Bus Tours (毎日あるぺん号 - `bus.maitabi.jp` & `api.bus.maitabi.jp`)
- Focuses on direct mountain access buses and mountain lodge packages
- `travel_type = 3`

### Domain B: General Travel & Trekking Tours (毎日新聞旅行 - `www.maitabi.jp`)
Focuses on guided mountain trekking, hiking, and travel packages across 5 categories:
- `travel_type = 1`: **国内登山・トレッキング (Domestic Mountain Climbing & Trekking)**
- `travel_type = 2`: **国内旅行・ハイキング (Domestic Travel & Hiking)**
- `travel_type = 3`: **毎日あるぺん号 (Mountain Bus Tours)** (cross-domain)
- `travel_type = 4`: **海外登山・トレッキング (Overseas Mountain Climbing & Trekking)**
- `travel_type = 5`: **海外旅行 (Overseas Travel)**

## 4. Filter Schema & Modeling

### Mountain Bus Tours Filter Schema (`bus.maitabi.jp`)

```json
{
  "departure": "1",
  "month": "8",
  "day": "10",
  "area": "0",
  "style": "6",
  "page": "1",
  "return_day": "1",
  "bus_sheet": "1",
  "stay1": null,
  "stay2": null,
  "stay3": null,
  "course_cd": null,
  "keyword": null,
  "travel_type": "3"
}
```

#### Filter Parameters:

| Filter Name | Query Param | Description / Sample Value |
| :--- | :--- | :--- |
| **Point of Departure (発着地)** | `departure` | `1`: 東京 (Tokyo), `2`: 大阪・京都 (Osaka/Kyoto), `3`: 名古屋 (Nagoya) |
| **Departure Month (出発月)** | `month` | `1` to `12` *(Required by backend API to avoid 500 error)* |
| **Departure Day (出発日)** | `day` | `1` to `31` |
| **Area / Direction (方面)** | `area` | Area ID (e.g., `0` = All, `18` = 立山（室堂）, `10` = 上高地) |
| **Tour Style (スタイル)** | `style` | `1`=Round-trip bus, `2`=Outbound bus, `3`=Inbound bus, `4`=Round-trip + lodge, `5`=Outbound + lodge, `6`=Night trip/round-trip overnight, `7`=Taxi plan |
| **Return Date (復路乗車日)** | `return_day` | `1`=1 day after, `2`=2 days after (1 night), `3`=3 days after, `4`=4 days after, `5`=5 days after |
| **Bus Seat Type (バスシート)** | `bus_sheet` | `1`=Standard, `2`=Premium, `3`=Outbound Premium / Inbound Standard, `4`=Outbound Standard / Inbound Premium, `5`=Double seat |
| **Mountain Lodge Night 1/2/3** | `stay1`, `stay2`, `stay3` | ID for mountain lodge accommodations |
| **Course Code (旅行番号)** | `course_cd` | Tour course code string (e.g., `S104C21`) |
| **Keyword (キーワード)** | `keyword` | Search string (e.g., `立山`, `槍ヶ岳`) |

### General Tours Filter Schema (`www.maitabi.jp`)

Parameters include `travelType`, `keyword`, `year_month`, `day`, and multiple `category_nos1-5` for subcategories covering style/duration, difficulty/shoes, departure region, themes/tours, and guides.

## 5. Key Actions & Endpoints

### Action 1: `list_filters(departure, month)` / `list_district_groups(departure, month)`
- **Purpose**: Retrieve all available filter dropdown options, departure places, mountain lodge options, area groups, and tour counts
- **API Endpoints**:
  - `GET https://api.bus.maitabi.jp/tour_course?departure={departure}&month={month}`
  - `GET https://api.bus.maitabi.jp/district_group?departure={departure}&month={month}`

### Action 2: `search_tours(filters)`
- **Purpose**: Search mountain bus tours on `api.bus.maitabi.jp`
- **cURL Example**:
  ```bash
  curl -L -s 'https://api.bus.maitabi.jp/tour_search?departure=1&month=8&area=18&page=1'
  ```

### Action 3: `get_tour_detail(course_no)`
- **Purpose**: Extract full itinerary, schedule, and pricing for a specific mountain bus tour
- **cURL Example**:
  ```bash
  curl -L -s 'https://api.bus.maitabi.jp/tour_detail?course_no=14241'
  ```

### Action 4: `search_general_tours(travel_type, keyword, year_month, day, page)`
- **Purpose**: Search general Mainichi Travel tours on `www.maitabi.jp`
- **cURL Example**:
  ```bash
  curl -L -s 'https://www.maitabi.jp/api/v1/category_search?travelType=1&keyword=%E7%AB%8B%E5%B1%B1&startDateYearMonthMin=2026-08&page=1'
  ```

### Action 5: `get_general_tour_detail(course_no)`
- **Purpose**: Extract complete details, points, meal conditions, guide info, and booking links for general tours
- **cURL Example**:
  ```bash
  curl -L -s 'https://api.bus.maitabi.jp/tour_detail?course_no=1723'
  ```

### Action 6: `get_tour_calendar(year, month, travel_type)`
- **Purpose**: Retrieve monthly departure calendar matrix showing active tours per day
- **cURL Example**:
  ```bash
  curl -L -s 'https://www.maitabi.jp/api/v1/calendar/2026/8?travelType=1'
  ```

## 6. Standard Output Formatting

All tour extraction operations return uniform JSON responses containing:
- Query parameters used for the search
- Results array with direct `detail_url` links
- Pagination metadata (total count, current page, per page)
- Standardized field mappings across both domains

## 7. Reference Guide

For full ID mappings and parameter details, refer to the [Filter Mapping Reference Guide](references/filter-mapping.md) which provides comprehensive mapping between UI Labels and internal ID query values used in Maitabi URLs.

## 8. Usage Without MCP

This skill can be used completely independently without any MCP code by:
1. Constructing query strings based on the filter schema
2. Making direct HTTP GET requests to the Maitabi endpoints
3. Parsing the JSON/HTML responses using the parsing logic described
4. Outputting results in the standardized JSON format

All operations use standard HTTP methods and can be performed with `curl`, `wget`, or any HTTP client library in any programming language.