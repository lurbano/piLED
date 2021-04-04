import subprocess

p = subprocess.Popen(["sudo", "python3", "runLEDs.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

q = input("?>")

if q == "green":
    print("g\n", file=p.stdin)
    #p.stdin.flush()
