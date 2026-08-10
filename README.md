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

---

## 1. MCP Server Usage

### Running the Server

#### Option A: Zero-setup via `uvx`
```bash
# From PyPI (once published)
uvx maitabi-mcp-server

# Directly from Git repository
uvx --from git+https://github.com/phonhay103/maitabi-mcp-server.git maitabi-mcp-server
```

#### Option B: Via Docker Image
```bash
docker pull phonhay103/maitabi-mcp-server:latest
docker run -i --rm phonhay103/maitabi-mcp-server:latest
```

### Configuration for MCP Clients

Add the following to your MCP client settings depending on your client platform:

#### 1. For Claude Desktop / Cursor / Pi (`claude_desktop_config.json`)
Uses the `"mcpServers"` top-level key format:

##### Via `uvx` (Recommended):
```json
{
  "mcpServers": {
    "maitabi-pypi": {
      "command": "uvx",
      "args": ["maitabi-mcp-server"]
    }
  }
}
```

##### Via Docker:
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

#### 2. For VSCode / Cursor Extensions (e.g. Cline, Roo Code, etc.)
Uses the `"servers"` top-level key and requires the `"type": "stdio"` field (typically in `clines_mcp_settings.json` or `mcp_settings.json`):

```json
{
    "servers": {
        "maitabi": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "phonhay103/maitabi-mcp-server:latest"
            ],
            "type": "stdio"
        },
        "maitabi-pypi": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "maitabi-mcp-server"
            ]
        }
    },
    "inputs": []
}
```

### Agent Skills ([vercel-labs/skills](https://github.com/vercel-labs/skills))

Install and use Agent Skills from this repository via `npx skills`:

```bash
# Install to current project
npx skills add phonhay103/maitabi-mcp-server

# Install globally
npx skills add phonhay103/maitabi-mcp-server -g

# List skills / Use without installing
npx skills add phonhay103/maitabi-mcp-server --list
npx skills use phonhay103/maitabi-mcp-server
```

**Available Skills:**
- **`maitabi-bus-extractor`** (`skills/maitabi-bus-extractor/SKILL.md`): Search and extract Maitabi mountain bus (`bus.maitabi.jp`) and general trekking tours (`www.maitabi.jp`).

---

## 2. Development

### Makefile Commands

```bash
make help          # Show available Makefile targets
make install       # Install dependencies using uv
make dev           # Run the MCP server locally over stdio
make dev-http      # Run the MCP server locally over Streamable HTTP (Port 8000)
make test          # Run test suite
make docker-build  # Build 2-stage Docker image (Python 3.14)
make build         # Build Python package wheel & sdist
```

### Local Development Client Configuration

To test a local checkout with an MCP client:

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
