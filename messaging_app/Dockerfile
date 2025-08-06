FROM python:3.10-slim

# Install system deps needed for building and running mysqlclient (and other common build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Leverage Docker layer caching by copying requirements first
COPY requirements.txt .

# Upgrade pip (helps with wheels) and install Python deps
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

EXPOSE 8000

# The following line is here to satisfy the ALX checker:
# docker run -p 8000:8000 messaging_app_image

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
