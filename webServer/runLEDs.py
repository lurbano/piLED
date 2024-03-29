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

# Startup Color
ledPix.light(0, (0,100,0))

while True:
	q = input("Ready:")

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
			print("made Green")

		if msg["what"] == "blue":
			ledPix.setColor((0,0,50))
			print("made Green")

		if msg["what"] == "led":
			if msg["todo"] == "setColor":
				ledPix.cancelTask()
				col = msg["color"]
				ledPix.setColor(col)

			if msg["todo"] == "setBrightness":
				ledPix.cancelTask()
				bright = msg["brightness"]
				ledPix.setBrightness(bright)
				#ledPix.setColor((10,0,0))
				m = {
					"info": "setBrightness",
					"brightness": ledPix.brightness
				}
				print(json.dumps(m)+"\n")

			if msg["todo"] == 'clear':
				ledPix.cancelTask()
				ledPix.clear()
				m = {
					"info": "Cleared"
				}
				print(json.dumps(m)+"\n")
