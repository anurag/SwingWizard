#!/usr/bin/env bash
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
flask translate compile
exec uvicorn -b :5000 --access-logfile - --error-logfile - swingwizard:app
