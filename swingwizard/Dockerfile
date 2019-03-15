FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/swingwizard

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt --upgrade

RUN pip install gunicorn

COPY app app/
COPY migrations migrations/
COPY swingwizard.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP swingwizard.py

RUN python swingwizard.py

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]

CMD ["python", "swingwizard.py", "runserver"]
