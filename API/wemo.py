from ouimeaux.environment import Environment

def on_switch(switch):
    print "switch found", switch.name

def on_motion(motion):
    print "Motion found", motion.name

env = Environment(on_switch, on_motion)

env.start()
