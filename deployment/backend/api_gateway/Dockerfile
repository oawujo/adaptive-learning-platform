FROM python:3.10-slim
WORKDIR /app
COPY deployment/backend/api_gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY deployment/backend/api_gateway/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]