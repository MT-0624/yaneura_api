docker-compose down
docker-compose build --no-cache
docker-compose up -d
sleep 30s
docker ps