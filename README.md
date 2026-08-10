# Maitabi MCP Server (Python)

An MCP (Model Context Protocol) server written in Python using FastMCP for searching and extracting mountain bus tour, alpine trekking, and general tour information from **Maitabi (まいたび - 毎日新聞旅行 / 毎日あるぺん号)** (`www.maitabi.jp`, `bus.maitabi.jp`, & `api.bus.maitabi.jp`).

Docker Hub Repository: [phonhay103/maitabi-mcp-server](https://hub.docker.com/r/phonhay103/maitabi-mcp-server)

## Tools Provided

### Mountain Bus Tours (毎日あるぺん号 - `bus.maitabi.jp`)
- `list_filters`: Fetch available filter options, departure areas, tour styles, mountain lodges, and tour counts for mountain bus tours.
- `list_district_groups`: Fetch area/district groups and tour counts for mountain bus tours.
- `search_tours`: Search mountain bus tours with full filter support (departure, month, day, area, style, return date, bus seat, lodges, keyword, course code).
- `get_tour_detail`: Fetch complete bus tour details, schedules, comments, and pricing by `course_no`.

### General Travel & Trekking Tours (毎日新聞旅行 - `www.maitabi.jp`)
- `search_general_tours`: Search general Mainichi Travel tours across categories (`travel_type`: 1=Domestic Mountain Climbing/Trekking, 2=Domestic Travel/Hiking, 3=Mountain Bus, 4=Overseas Mountain Climbing/Trekking, 5=Overseas Travel) with keyword, date, and pagination filters.
- `get_general_tour_detail`: Fetch complete tour details, itinerary, meal condition, guide info, points of interest, and booking links for general tours by `courseNo`.
- `get_tour_calendar`: Fetch monthly departure schedule calendar and tour matrix on `www.maitabi.jp` for a given year and month.

## Development & Usage via Makefile

```bash
make help          # Show available Makefile targets
make install       # Install dependencies using uv
make dev           # Run the MCP server locally over stdio
make dev-http      # Run the MCP server locally over Streamable HTTP (Port 8000)
make test          # Run test suite
make docker-build  # Build 2-stage Docker image (Python 3.14)
make docker-push   # Build & push Docker image to Docker Hub (phonhay103/maitabi-mcp-server)
make build         # Build Python package wheel & sdist
make publish       # Show instructions to trigger PyPI publish via CI tag
```

## Running via Docker Image (Docker Hub)

```bash
docker pull phonhay103/maitabi-mcp-server:latest
docker run -i --rm phonhay103/maitabi-mcp-server:latest
```

## Running via `uvx` (Zero-setup)

### From PyPI (once published):
```bash
uvx maitabi-mcp-server
```

### From Git repository directly:
```bash
uvx --from git+https://github.com/phonhay103/maitabi-mcp-server.git maitabi-mcp-server
```

## Configuration for MCP Clients

### Claude Desktop / Pi / Cursor Configuration

Add the following to your MCP client settings (e.g. `claude_desktop_config.json`):

#### Using `uvx` (PyPI / Zero Setup):
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

#### Using Docker (Public Image):
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

#### Using `uv` locally:
```json
{
  "mcpServers": {
    "maitabi": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/maitabi-mcp-server",
        "maitabi-mcp-server"
      ]
    }
  }
}
```
