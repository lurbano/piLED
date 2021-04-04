import pexpect
import sys

child = pexpect.spawn('sudo python3 runLEDs.py', encoding='utf-8')
child.expect("Ready")
child.sendline('{"info": "green"}')
child.logfile = sys.stdout
print('done')
