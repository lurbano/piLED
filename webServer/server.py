#! /usr/bin/python3

# From: https://www.hackster.io/dataplicity/control-raspberry-pi-gpios-with-websockets-af3d0c

import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.gen
import RPi.GPIO as GPIO
import time
import subprocess
import json
import sys
import argparse
import asyncio
import pexpect
import board
#from numpy import arange, mean
import numpy as np

#from ledController import *
#from ledPixels import *
#from oledU import *
from basic import *

# Broadcaster (to all attached sockets)
from wsBroadcasterU import *
wsCast = wsBroadcasterU()
# Broadcaster (END)

# LEDs (1/2)
try:
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
	#ledPix = ledPixels(nPix, ledPin)
	ledProg = pexpect.spawn(f'sudo python3 runLEDs.py -n {nPix}', encoding='utf-8')
except:
	ledProg = None

if not ledProg:
	print("Problem: ledProg = ", ledProg)
# LEDs (END)


#Tornado Folder Paths
settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static")
	)

#pyPath = '/home/pi/rpi-led-strip/pyLED/'

#Tonado server port
PORT = 8040

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		print ("[HTTP](MainHandler) User Connected.")
		self.render("index.html")


class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print ('[WS] Connection was opened.')
		self.write_message('{"who": "server", "info": "on"}')
		#self.oled = oledU(128,32)

		# Broadcaster (add new socket to list)
		wsCast.append(self)
		# Broadcaster (END)

		# LEDs (confirm if led's are active)
		if ledProg:
			self.write_message({"info": "LEDsActive", "active": "show", "nPix": nPix})
			print("LED's Active")
		else:
			self.write_message({"info": "LEDsActive", "active": "hide"})
			print("LED's Inactive")
		# LEDs (END)


	async def on_message(self, message):
		print ('[WS] Incoming on_message:', message)
		try:
			msg = json.loads(message)
			if msg["what"] == "server":
				if msg["opts"] == "off":
					sys.exit("Stopping server")

			if msg["what"] == "hello":
				r = 'Say what?'
				self.write_message({"info": "hello", "reply":r})

			if msg["what"] == "timer":
				m = float(msg["minutes"])
				s = float(msg["seconds"])
				task = asyncio.create_task(basicTimer(self, m, s))

			if msg["what"] == "reboot":
				subprocess.Popen('sleep 5 ; sudo reboot', shell=True)
				main_loop.stop()

			# LED STRIP (2/3)

			# if msg["what"] == "nPix":
			# 	print("Resetting nPix")
			# 	global ledPix
			# 	ledPix.cancelTask()
			# 	n = int(msg["n"])
			# 	ledPix = ledPixels(n, ledPin)
			# 	ledPix.initCodeColor()
			#
			# if msg["what"] == "clearButton":
			# 	print("Clearing LEDs ")
			# 	ledPix.cancelTask()
			# 	ledPix.clear()
			# 	self.write_message({"info":"cleared"})
			#
			# if msg["what"] == "rainbowButton":
			# 	print("rainbow LEDs ")
			# 	ledPix.cancelTask()
			# 	n = int(msg["ct"])
			# 	s = float(msg["speed"])
			# 	task = asyncio.create_task(ledPix.aRainbow(n, s))
			# 	ledPix.task = task
			#
			# if msg["what"] == "rainbowForever":
			# 	print("rainbow LEDs (forever) infinite loop")
			# 	ledPix.cancelTask()
			# 	s = float(msg["speed"])
			# 	task = asyncio.create_task(ledPix.aRainbowForever(s))
			# 	ledPix.task = task

			if msg["what"] == "led":
				if msg["todo"] == "setColor":
					# ledPix.cancelTask()
					# col = msg["color"]
					# ledPix.setColor(col)
					ledProg.expect("Ready")
					ledProg.sendline(json.dumps(msg))
					
					# reset the brightness bar to 100 since brightness is overwritten by the change in color
					m = {
						"info": "resetBrightness",
						"brightness": 100
					}
					wsCast.write(m)

					# let all other connections know about the new color
					m = {
						"info": "resetColor",
						"color": msg["color"];
					}
					wsCast.write(m)


				if msg["todo"] == "setBrightness":
					# bright = msg["brightness"]
					# ledPix.setBrightness(bright)
					ledProg.expect("Ready")
					ledProg.sendline(json.dumps(msg))

				if msg["todo"] == "clear":
					ledProg.expect("Ready")
					ledProg.sendline(json.dumps(msg))

			# if msg["what"] == "interruptButton":
			# 	ledPix.cancelTask()
			#
			# if msg["what"] == "blueButton":
			# 	print("blue LEDs ")
			# 	ledPix.cancelTask()
			# 	ledPix.blue()

			# LED STRIP (END)


		except Exception as e:
			print(e)
			print("Exception: Error with data recieved by server")
			print(message)


	def on_close(self):
		print ('[WS] Connection was closed.')


application = tornado.web.Application([
  (r'/', MainHandler),
  (r'/ws', WSHandler),
  ], **settings)


if __name__ == "__main__":
	try:
		http_server = tornado.httpserver.HTTPServer(application)
		http_server.listen(PORT)
		print("hello")
		main_loop = tornado.ioloop.IOLoop.instance()

		print ("Tornado Server started")

		# get ip address
		cmd = "hostname -I | cut -d\' \' -f1"
		IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
		print('IP: '+ IP +":" + str(PORT))
		#oled.write('IP: '+ IP, 3)
		cmd = 'iwgetid | sed \'s/.*://\' | sed \'s/"//g\''
		wifi = subprocess.check_output(cmd, shell=True).decode("utf-8")
		#oled.write(wifi, 2)
		print(wifi)

		main_loop.start()




	except:
		print ("Exception triggered - Tornado Server stopped.")

#End of Program
