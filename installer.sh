echo "Removing previous version..."
docker stop adamshousebot
docker container rm adamshousebot 
echo "Creating new container..."
docker run -dit --name=adamshousebot -v $PWD:/app -e TZ=America/Santiago -e APPNAME=adamshousebot.py --restart=unless-stopped --memory=512m --cpus="0.5" marc0u/python-launcher
echo "Done!"