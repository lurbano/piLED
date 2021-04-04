from sensor_T import *


sensor = sensor_T()

while True:
    r = input()
    if r == 'n':
        print("exiting")
        break
    else:
        T = sensor.read()
        print(T)
