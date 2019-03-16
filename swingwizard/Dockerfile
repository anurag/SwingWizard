FROM rottenberg/ffmpeg

RUN apt-get update && apt-get install -y \
    git python3 python3-dev python3-pip gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt --upgrade

COPY app app/
COPY migrations migrations/
COPY app.db app.db
COPY config.py config.py
COPY swingwizard.py swingwizard.py
COPY swingwizard.py config.py boot.sh ./

EXPOSE 5000

CMD ["python3", "swingwizard.py", "serve"]
