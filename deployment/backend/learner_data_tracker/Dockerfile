FROM python:3.10-slim
WORKDIR /app
COPY deployment/backend/learner_data_tracker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY deployment/backend/learner_data_tracker/ .
CMD ["python", "app.py"]