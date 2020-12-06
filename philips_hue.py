from phue import Bridge

def initialize_bridge(ipadress="192.168.1.63"):
    return Bridge(ipadress)

def turn_lights(bridge, mode, light=2):
    # mode is a bool
    bridge.set_light(light, "on", mode)