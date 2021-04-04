import pexpect
import sys
import time

ledProg = pexpect.spawn('sudo python3 runLEDs.py', encoding='utf-8')

# child.logfile = sys.stdout
# print('done')

for i in range(10):
    ledProg.expect("Ready")
    ledProg.sendline('{"what": "green"}')
    time.sleep(1)
    ledProg.expect("Ready")
    ledProg.sendline('{"what": "blue"}')
    time.sleep(1)
