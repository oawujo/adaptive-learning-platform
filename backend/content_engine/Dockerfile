
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install flask python-dotenv openai

EXPOSE 8003
CMD ["python", "app.py"]
