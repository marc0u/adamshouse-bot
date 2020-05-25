FROM python:3-alpine as base

RUN apk add --update \
    tzdata

FROM python:3-alpine

COPY --from=base /usr/share/zoneinfo /usr/share/zoneinfo
ENV TZ=America/Santiago
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD [ "python3", "/app/bot_AdamsHouse.py" ]