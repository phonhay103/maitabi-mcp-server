---
name: maitabi-bus-extractor
description: Extract mountain bus tour, alpine trekking, and general tour data from Maitabi (bus.maitabi.jp & www.maitabi.jp) using only raw HTTP requests (curl or any HTTP client). No MCP server, no CLI, no Python package required. Supports filter modeling, REST endpoint querying, and standardized JSON output.
---

# Maitabi Bus Extractor Skill

## 1. Overview

This skill works with **plain HTTP only**. You build URL query strings, issue `GET` requests with `curl` (or any HTTP client in any language), and parse the JSON responses. Nothing to install — no MCP client, no `maitabi` CLI, no Python package.

> Need a different interface? The `maitabi-cli` skill covers the `maitabi` terminal command and the `maitabi-mcp` skill covers MCP client tools. This skill is standalone and does not depend on either.

## 2. 3-Layer Architecture

### Layer 1: `build_query(filters)`
- Convert user filters into exact URL query parameters (see §4).
- `month` (1-12) is required by the backend — always include it to avoid HTTP 500.

### Layer 2: `fetch_list(query)`
- `GET` the endpoints in §5 with `curl -L -s` (follow redirects).
- Two base hosts:
  - `https://api.bus.maitabi.jp` — mountain bus tours (毎日あるぺん号).
  - `https://www.maitabi.jp/api/v1` — general travel/trekking tours (毎日新聞旅行).

### Layer 3: `parse_list(payload)`
- Responses are JSON. Normalize each item to:
  - `course_no`/`courseNo`, `course_cd`/`courseCd`, `title`/`courseName`, `date`/`saikouDate`, `price`, `status`/`saikouStatus`, plus pagination (`count`, `page`, `param`/`data`).
- Append `detail_url` yourself:
  - Bus: `https://bus.maitabi.jp/detail.html?course_no={course_no}&year={YYYY}&month={M}` (derive YYYY/MM from the `date` field, e.g. `2026年09月12日(土)` → year=2026, month=9).
  - General: `https://www.maitabi.jp/detail.php?courseNo={courseNo}`.
- Post-filter client-side when needed: price range (strip `,`/`円`/`～` then compare ints), availability (drop `満席`, `受付終了`, `キャンセル待ち`, `催行中止`, empty).

## 3. Domains & Travel Categories

| Domain | Host | `travel_type` |
|--------|------|---------------|
| Mountain Bus (毎日あるぺん号) | `api.bus.maitabi.jp` / `bus.maitabi.jp` | 3 |
| Domestic Mountain (国内登山・トレッキング) | `www.maitabi.jp` | 1 |
| Domestic Travel (国内旅行・ハイキング) | `www.maitabi.jp` | 2 |
| Overseas Mountain (海外登山・トレッキング) | `www.maitabi.jp` | 4 |
| Overseas Travel (海外旅行) | `www.maitabi.jp` | 5 |

## 4. Filter Schema

### Mountain bus query params (`api.bus.maitabi.jp`)

```
departure={1|2|3}&month={1..12}&day={1..31}&area={id}&style={1..7}&return_day={1..5}&bus_sheet={1..6}&stay1={id}&stay2={id}&stay3={id}&course_cd={code}&keyword={text}&page={N}
```

| Param | Meaning / values |
| :--- | :--- |
| `departure` | `1`=東京 Tokyo, `2`=大阪・京都 Osaka/Kyoto, `3`=名古屋 Nagoya |
| `month` | `1`-`12` — **required** |
| `day` | `1`-`31` (one request per day; fan out for ranges) |
| `area` | Area ID (`0`=All, `18`=立山（室堂）, `10`=上高地, …) |
| `style` | `1`=Round-trip bus, `2`=Outbound, `3`=Inbound, `4`=Round-trip+lodge, `5`=Outbound+lodge, `6`=Night bus (夜行日帰り/往復夜行), `7`=Taxi |
| `return_day` | `1`=1 day after … `5`=5 days after |
| `bus_sheet` | `1`=Standard, `2`=Premium, `3`=Outbound Premium/Inbound Standard, `4`=Outbound Standard/Inbound Premium, `5`=Double, `6`=Taxi |
| `stay1/2/3` | Mountain lodge IDs |
| `course_cd` | Course code (e.g. `S104C21`) |
| `keyword` | Japanese keyword (e.g. `立山`, URL-encode it) |
| `page` | Page number (1-based) |

### General tour query params (`www.maitabi.jp/api/v1/category_search`)

```
travelType={1..5}&keyword={text}&startDateYearMonthMin={YYYY-MM}&startDateDayMin={D}&page={N}&listOrder={order}&categoryNos1[]={id}&...&categoryNos5[]={id}
```

`listOrder`: `startDateAsc`, `saikouStatus`, `yoyakuStatus`, `priceAsc`, `priceDesc`. `categoryNos1-5`: repeatable subcategory IDs (style/duration, difficulty, departure region, themes, guides).

## 5. Endpoints & cURL

### `GET /tour_course` — bus filter options + counts

```bash
curl -L -s 'https://api.bus.maitabi.jp/tour_course?departure=1&month=8'
curl -L -s 'https://api.bus.maitabi.jp/tour_course?departure=1&month=8&day=10&area=18'
```

### `GET /district_group` — area groups + counts

```bash
curl -L -s 'https://api.bus.maitabi.jp/district_group?departure=1&month=8'
```

### `GET /tour_search` — search bus tours

```bash
curl -L -s 'https://api.bus.maitabi.jp/tour_search?departure=1&month=8&area=18&page=1'
curl -L -s 'https://api.bus.maitabi.jp/tour_search?departure=1&month=8&style=6&return_day=1&page=1'
```

### `GET /tour_detail` — bus/general tour detail

```bash
curl -L -s 'https://api.bus.maitabi.jp/tour_detail?course_no=14241'
```

### `GET /api/v1/category_search` — search general tours

```bash
curl -L -s 'https://www.maitabi.jp/api/v1/category_search?travelType=1&keyword=%E7%AB%8B%E5%B1%B1&startDateYearMonthMin=2026-08&page=1'
```

### `GET /api/v1/calendar/{year}/{month}` — monthly matrix

```bash
curl -L -s 'https://www.maitabi.jp/api/v1/calendar/2026/8?travelType=1'
```

## 6. Standard output

Normalize every extraction to:

```json
{
  "count": 23,
  "page": "1",
  "tour": [{ "travel_type": 3, "course_cd": "S104C21", "course_no": 14241, "date": "2026年09月12日(土)", "title": "...", "tour_day": "1日", "price": "15,500円", "status": "受付中", "phone_reserve": 0, "detail_url": "https://bus.maitabi.jp/detail.html?course_no=14241&year=2026&month=9" }],
  "param": { "departure": "1", "page": "1", "month": "9", "day": "12" }
}
```

## 7. Reference

Full ID tables (departure/area/style/return-day/seat/lodges): [filter-mapping.md](references/filter-mapping.md).
