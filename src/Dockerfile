FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev
RUN pip install uv
RUN uv pip install --no-cache-dir -r requirements.txt --system

COPY . .

CMD ["python", "main.py"]