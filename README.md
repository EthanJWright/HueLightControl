# This repo is the code for my IoT subnet running on Raspberry Pi's.

### Quick Information

To start any of the containers on a Raspberry Pi:
```
#Install Docker
curl -sSL https://get.docker.com | sh
#login 
sudo docker login

#Add correct RPi IP's to iot.properties for project
vim IoT-Home/iot.properties

#CD to correct directory
cd IoT-Home/<Project to be built>/

#Deploy Docker Containers
./build.sh
./run.sh
```

### RPI-Controller-API runs one Docker container hosting a Flask Restful API
The API forks off the processes to either be handled with Cloud-to-Cloud
integration or hits other Raspberry Pi's running in the home.


### RPI-LED-API sits on one Pi that has GPIO wired to an RGB strip
This API sits on the subnet and adjusts the RGB strip in my house for a fully
controlled Hue - esque experience. 
Two docker containers run on the Pi, one running the PIGPIO C bindings, the
other to set up the Flask API on the subnet.

### React-Native-App contains the source code for the app to hit the API
I threw this together so that I can add controllers as I add functionality to
the IoT functionality. Pretty poorly written, just a quick and dirty solution.

### Documents for reference:

#### React Native Stuff:
  - [For help building an APK for Android.](https://docs.expo.io/versions/latest/guides/building-standalone-apps.html)
  - [Tutorial to React Native](https://facebook.github.io/react-native/docs/tutorial.html)

#### RGB LED Controls via GPIO:
  - [Hardware for RGB Controls](https://dordnung.de/raspberrypi-ledstrip/)
  - [Pigpio Library](http://abyz.me.uk/rpi/pigpio/)
  - [Github found for Docker Pigpio](https://github.com/lachatak/rpi-pigpio)

