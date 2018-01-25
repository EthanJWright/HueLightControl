sudo docker run --privileged -d -it --cap-add SYS_RAWIO --device /dev/mem --device /dev/vcio -p 8888:8888 --name pigpio rpi-pigpio
sudo docker run -d -p 5000:5000 --name flask strip-api
