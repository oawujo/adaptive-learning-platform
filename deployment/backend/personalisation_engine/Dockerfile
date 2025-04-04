FROM python:3.10-slim
WORKDIR /app
COPY deployment/backend/personalisation_engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY deployment/backend/personalisation_engine/ .
CMD ["python", "app.py"]