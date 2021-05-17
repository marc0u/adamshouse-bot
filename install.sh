#!/bin/bash
APPNAME="adamshousebot"
echo "Removing previous version..."
docker stop $APPNAME
docker rm $APPNAME 
echo "Creating new container..."
docker run -dit \
--name=$APPNAME \
-v $PWD:/app \
-e TZ=America/Santiago \
-e APPNAME="${APPNAME}.py" \
--restart=unless-stopped \
--memory=512m \
--cpus="0.5" \
marc0u/python-launcher
echo "Done!"