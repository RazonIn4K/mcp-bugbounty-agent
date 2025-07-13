FROM python:3.11-slim

LABEL maintainer="hello@bugbounty-agent.com"
LABEL version="1.2.0"
LABEL description="MCP Bug Bounty Research Agent"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY examples/ ./examples/
COPY setup.py .

# Install the package
RUN pip install -e .

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port for web interface (future)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src.mcp_bugbounty_agent.agent; print('OK')" || exit 1

# Default command
ENTRYPOINT ["python", "-m", "mcp_bugbounty_agent.cli"]
CMD ["--help"]
