.PHONY: help install dev dev-http dev-sse test docker-build docker-run docker-run-http build clean

DOCKER_USER ?= phonhay103
IMAGE_NAME ?= maitabi-mcp-server
TAG ?= latest
HOST ?= 0.0.0.0
PORT ?= 8000

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	uv sync

dev: ## Run the MCP server locally using stdio transport
	uv run maitabi-mcp-server --transport stdio

dev-http: ## Run the MCP server locally using Streamable HTTP transport
	uv run maitabi-mcp-server --transport streamable-http --host $(HOST) --port $(PORT)

dev-sse: ## Run the MCP server locally using SSE transport
	uv run maitabi-mcp-server --transport sse --host $(HOST) --port $(PORT)

test: ## Run test suite
	uv run python -c "import asyncio; from maitabi_mcp_server.services.bus_service import list_filters_service; from maitabi_mcp_server.models import ListFiltersInput; asyncio.run(list_filters_service(ListFiltersInput())); print('Tests passed!')"

docker-build: ## Build the 2-stage Docker image (Python 3.14)
	docker build -t $(IMAGE_NAME):$(TAG) -t $(DOCKER_USER)/$(IMAGE_NAME):$(TAG) .

docker-run: ## Run the MCP server inside Docker container (stdio transport)
	docker run -i --rm $(IMAGE_NAME):$(TAG)

docker-run-http: ## Run the MCP server inside Docker container (Streamable HTTP transport)
	docker run -i --rm -p $(PORT):$(PORT) $(IMAGE_NAME):$(TAG) --transport streamable-http --port $(PORT)


build: ## Build Python package wheel & sdist for PyPI / uvx
	uv build

clean: ## Remove build artifacts and cache
	rm -rf .venv __pycache__ .pytest_cache *.egg-info src/*.egg-info dist
