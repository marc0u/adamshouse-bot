PY_APPNAME="adamshousebot"
echo "Removing previous version..."
docker stop $PY_APPNAME
docker container rm $PY_APPNAME 
echo "Creating new container..."
docker run -dit \
--name=$PY_APPNAME \
-v $PWD:/app \
-e TZ=America/Santiago \
-e APPNAME="${PY_APPNAME}.py" \
--restart=unless-stopped \
--memory=512m \
--cpus="0.5" \
marc0u/python-launcher
echo "Done!"