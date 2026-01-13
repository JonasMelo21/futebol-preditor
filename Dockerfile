FROM python:3.11-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy project definition
COPY pyproject.toml .
# Copy requirements if exists, for backward compat
COPY requirements.txt .

# Install dependencies
RUN uv pip install --system -r requirements.txt || uv sync --frozen --no-cache

# Copy project code
COPY . .

EXPOSE 8501

# Adjust path to app.py based on workspace structure
# The frontend code is in frontend/app.py
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
