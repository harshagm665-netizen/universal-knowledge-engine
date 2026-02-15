FROM python:3.12-slim

# Install uv for fast dependency management on i3 hardware
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy the entire workspace to handle local packages like ai-core
COPY . .

# Sync dependencies
RUN uv sync --frozen

# Expose FastAPI port
EXPOSE 8000

# Start the engine
CMD ["uv", "run", "python", "apps/api-server/main.py"]