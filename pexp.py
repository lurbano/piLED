import pexpect
import sys
import time

child = pexpect.spawn('sudo python3 runLEDs.py', encoding='utf-8')

# child.logfile = sys.stdout
# print('done')

for i in range(10):
    child.expect("Ready")
    child.sendline('{"what": "green"}')
    time.sleep(1)
    child.expect("Ready")
    child.sendline('{"what": "blue"}')
    time.sleep(1)
