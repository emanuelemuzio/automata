FROM python:3.11

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN curl -fsSL https://ollama.com/install.sh | sh

EXPOSE 8000

CMD ollama serve & ollama pull llama3.1 & fastapi run app/main.py --host 0.0.0.0 --port 8000