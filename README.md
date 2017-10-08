# Threw this together to allow for full control of hue lights from terminal
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
