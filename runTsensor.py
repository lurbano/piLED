from sensor_T import *


sensor = sensor_T()

while True:
    r = raw_input()
    if r == 'n':
        print "exiting"
        break
    else:
        T = sensor.read()
        print(T)
