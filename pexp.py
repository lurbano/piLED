import pexpect

child = pexpect.spawn('sudo python3 runLEDs.py')
child.expect("Ready")
child.sendline('{"info": "green"}')
print('done')
