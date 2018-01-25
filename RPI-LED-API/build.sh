cp ../iot.properties Flask-API/
sudo docker build -t pigpio:latest Pigpio/
sudo docker build -t strip-api:latest Flask-API/
rm Flask-API/iot.properties
