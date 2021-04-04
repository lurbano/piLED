

import argparse
import json
from ledPixels import *


# default values
nPix = 20
ledPin = board.D18

# get number of pixels from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nPix", help = "Number of pixels")
args = parser.parse_args()

if args.nPix:
	try:
		nPix = int(args.nPix)
	except:
		print("using default (20) pixels: -nPix 20")


#Initialize neopixels
ledPix = ledPixels(nPix, ledPin)

while True:
    q = input("Ready")
    print(q)
    try:
        msg = json.loads(q)
    except:
        msg = None
        print('{"info", "Input Not JSON"}')
        if q == "q":
            print("Quitting.")
            break
        elif q == "g":
            print("green")
            ledPix.pixels[5] = (0,100,0)
            ledPix.pixels.show()

    if msg:
        if msg["what"] == "green":
            ledPix.setColor((0,100,0))
