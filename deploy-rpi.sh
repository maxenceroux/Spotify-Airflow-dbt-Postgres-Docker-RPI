#!bin/sh

docker pull maxenceroux/airflow
docker pull maxenceroux/spotify_web
echo "yes"
cd /home/pi/project/test_prod
docker-compose up -d
