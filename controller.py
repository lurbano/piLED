import subprocess

p = subprocess.Popen("sudo", "python3", "runLEDs.py", stdin=PIPE, stdout=PIPE, bufsize=1)

q = input("?>")

if q == "green":
    print("g\n", file=p.stdin)
    #p.stdin.flush()
