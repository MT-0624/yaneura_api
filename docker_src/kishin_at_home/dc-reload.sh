
if [ $# == 0 ]; then
  docker-compose down
  docker-compose build --no-cache
  docker-compose up -d
  sleep 20s
  docker ps
else
  docker-compose stop $1
  docker-compose build --no-cache $1
  docker-compose up -d $1
  docker ps
fi
