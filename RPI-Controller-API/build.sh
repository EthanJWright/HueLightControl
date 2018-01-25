cp ../iot.properties Flask-API/
sudo docker build -t flask-api:latest Flask-API
rm Flask-API/iot.properties

