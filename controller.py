import subprocess

p = subprocess.Popen(["sudo", "python3", "runLEDs.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,  universal_newlines=True)

q = input("?>")

if q == "green":
    p.stdin.write("g")
    #print(b'g', file=p.stdin)
    #p.stdin.flush()
