docker stop adamshousebot 
docker rm adamshousebot 
docker run -dit \
--name=adamshousebot \
-v $PWD:/app \
-e TZ=America/Santiago \
-e APPNAME="adamshousebot.py" \
--restart=unless-stopped \
--memory=512m \
--cpus="0.5" \
marc0u/python-launcher