FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install dependencies
COPY regulatory-monitor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and shared module
COPY regulatory-monitor/app ./app
COPY shared ./shared

# Optional: add /app and /app/shared to PYTHONPATH
ENV PYTHONPATH=/app:/app/shared

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
