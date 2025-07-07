FROM python:3.12-slim
WORKDIR /app
RUN mkdir -p /app/tmp_uploads
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev
COPY . .
CMD ["python", "-m", "src.main"]