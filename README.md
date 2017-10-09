# Threw this together to allow for full control of hue lights from terminal

### choose.py must be modified so that hue_rgb(ip) is set to the ip of your hue bridge
on first connection, hue bridge center must be pressed to whitelist the IP of
your server.

Add to your bashrc:
```bash
alias hue=set_lights
set_lights(){
    ~/HueLightControl/choose.py $1
}
```

Now you can do things like:
```bash
hue on
hue off
hue blue
hue red
```

To edit the group that the script impacts, in choose.py change the hue.setGroup
value. 

Libraries to install:
```
pip install flask
pip install Flask-API
pip install phue
pip install colour
pip install simplejson
```
