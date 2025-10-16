FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
EXPOSE 8000
ENV TASKPILOT_SECRET_KEY="change-me"
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
