import argparse
from ledPixels import *

nPix = 20
ledPin = board.D18


leds = ledPixels(nPix, ledPin)

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
    q = input()
    if q == "q":
        print("Quitting.")
        break
    elif q == "g":
        ledPix.pixels[5] = (0,100,0)
