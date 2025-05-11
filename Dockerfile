FROM python:3.11.9-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3.11", "app/app.py"]
