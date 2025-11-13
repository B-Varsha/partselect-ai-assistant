#FROM python:3.10-slim
#
#WORKDIR /app
#
## Install build tools
#RUN apt-get update && apt-get install -y \
#    build-essential \
#    && rm -rf /var/lib/apt/lists/*
#
## Install Python deps
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#
## Copy backend code
#COPY . .
#
#EXPOSE 8001
#
## Enable hot reload for development mode
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

FROM python:3.10-slim

WORKDIR /app

# (optional but safe) Install build tools for some Python libs
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Render requires port 10000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

