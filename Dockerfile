FROM python:3.13-slim-bullseye

WORKDIR /marketplace

COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "src.main"]