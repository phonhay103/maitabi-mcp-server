---
name: maitabi-bus-extractor
description: Skill for searching, filtering, and extracting mountain bus tour, alpine trekking, and general tour data from Maitabi (まいたび - 毎日新聞旅行 / 毎日あるぺん号 - bus.maitabi.jp & www.maitabi.jp). Supports filter modeling, querying REST API/HTML endpoints via curl or MCP tools, parsing listing and detail pages, monthly calendar schedules, and standardized JSON output formatting.
---

# Maitabi Tour & Bus Extractor

This skill equips the Agent to act as a powerful curl/API extractor and connector for both mountain bus tours (**毎日あるぺん号** - `bus.maitabi.jp`) and general travel/alpine trekking tours (**毎日新聞旅行** - `www.maitabi.jp`).

---

## 1. 3-Layer Architecture

The extractor operates on a 3-layer pattern to separate parameter handling, network requests, and data parsing:

1. **`build_query(filters)`**:
   Converts user-selected filters (JSON/Object format) into exact URL Query String parameters corresponding to Maitabi ID codes and travel types.
2. **`fetch_list(query)`**:
   Uses `curl` or HTTP clients to issue GET requests to `api.bus.maitabi.jp` REST endpoints or `www.maitabi.jp/api/v1` REST endpoints.
3. **`parse_list(payload)`**:
   Extracts and normalizes tour listings (`course_no`/`courseNo`, `course_cd`/`courseCd`, `title`/`courseName`, `date`/`saikouDate`, `duration`, `price`, `status`, `detail_url`) along with pagination metadata from JSON responses or HTML pages.

---

## 2. Domains & Supported Travel Categories

Maitabi covers two main domains and 5 travel category types (`travel_type` / `travelType`):

### Domain A: Mountain Bus Tours (毎日あるぺん号 - `bus.maitabi.jp` & `api.bus.maitabi.jp`)
Focuses on direct mountain access buses and mountain lodge packages (`travel_type = 3`).

### Domain B: General Travel & Trekking Tours (毎日新聞旅行 - `www.maitabi.jp`)
Focuses on guided mountain trekking, hiking, and travel packages across 5 categories:
- `travel_type = 1`: **国内登山・トレッキング (Domestic Mountain Climbing & Trekking)**
- `travel_type = 2`: **国内旅行・ハイキング (Domestic Travel & Hiking)**
- `travel_type = 3`: **毎日あるぺん号 (Mountain Bus Tours)**
- `travel_type = 4`: **海外登山・トレッキング (Overseas Mountain Climbing & Trekking)**
- `travel_type = 5`: **海外旅行 (Overseas Travel)**

---

## 3. Filter Schema & Modeling

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

#### Mountain Bus Filter Parameters:
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

---

## 4. Key Actions & Endpoints

### Action 1: `list_filters(departure, month)` / `list_district_groups(departure, month)`
Retrieve all available filter dropdown options, departure places, mountain lodge options, area groups, and tour counts.
- **API Endpoints**:
  - `GET https://api.bus.maitabi.jp/tour_course?departure={departure}&month={month}`
  - `GET https://api.bus.maitabi.jp/district_group?departure={departure}&month={month}`

### Action 2: `search_tours(filters)`
Search mountain bus tours on `api.bus.maitabi.jp`.
- **cURL Example**:
  ```bash
  curl -L -s 'https://api.bus.maitabi.jp/tour_search?departure=1&month=8&area=18&page=1'
  ```

### Action 3: `get_tour_detail(course_no)`
Extract full itinerary, schedule, and pricing for a specific mountain bus tour.
- **cURL Example**:
  ```bash
  curl -L -s 'https://api.bus.maitabi.jp/tour_detail?course_no=14241'
  ```

### Action 4: `search_general_tours(travel_type, keyword, year_month, day, page)`
Search general Mainichi Travel tours on `www.maitabi.jp`.
- **cURL Example**:
  ```bash
  curl -L -s 'https://www.maitabi.jp/api/v1/category_search?travelType=1&keyword=%E7%AB%8B%E5%B1%B1&startDateYearMonthMin=2026-08&page=1'
  ```

### Action 5: `get_general_tour_detail(course_no)`
Extract complete details, points, meal conditions, guide info, and booking links for general tours.
- **cURL Example**:
  ```bash
  curl -L -s 'https://api.bus.maitabi.jp/tour_detail?course_no=1723'

### Action 6: `get_tour_calendar(year, month, travel_type)`
Retrieve monthly departure calendar matrix showing active tours per day.
- **cURL Example**:
  ```bash
  curl -L -s 'https://www.maitabi.jp/api/v1/calendar/2026/8?travelType=1'
  ```

---

## 5. Standard Output Formatting

All tour extraction operations return uniform JSON responses containing query parameters, results array with direct `detail_url` links, and pagination metadata.

For full ID mappings, refer to [Filter Mapping Reference Guide](references/filter-mapping.md).
