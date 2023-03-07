FROM python:3.10.9-slim
MAINTAINER Mikael Allison <mikellallison@hotmail.com>
WORKDIR /app

COPY . .
# FFMpeg is required for post-processing i.e. converting
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
