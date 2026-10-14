FROM python:3.13-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY extracao ./extracao
CMD ["python", "-m", "extracao.sincronizar", "--intervalo-segundos", "21600"]
