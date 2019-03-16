FROM python:3.7

RUN apt-get update && apt-get install -y ffmpeg git python3-dev gcc \
    pkg-config libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev \
    libswscale-dev libavresample-dev libavfilter-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt --upgrade

COPY app app/
COPY migrations migrations/
COPY app.db app.db
COPY config.py config.py
COPY swingwizard.py swingwizard.py
COPY swingwizard.py config.py boot.sh ./

EXPOSE 5000

CMD ["python", "swingwizard.py", "serve"]
