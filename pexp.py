import pexpect

child = pexpect.spawn('sudo python3 runLEDs.py')
child.expect("Ready")
child.sendline('{"info": "green"}', encoding='utf-8')
child.logfile = sys.stdout
print('done')
