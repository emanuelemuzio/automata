FROM ollama/ollama:latest

WORKDIR /app

RUN apt update && apt install -y curl git python3 python3-pip libpq-dev

COPY . .