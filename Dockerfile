FROM python:3-alpine
# Install base packages
RUN apk update
RUN apk upgrade
RUN apk add ca-certificates && update-ca-certificates
# Change TimeZone
RUN apk add --update tzdata
ENV TZ=America/Santiago
# Clean APK cache
RUN rm -rf /var/cache/apk/*
# Run App
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD [ "python3", "/app/bot_AdamsHouse.py" ]