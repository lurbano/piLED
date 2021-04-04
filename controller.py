import subprocess

p = subprocess.Popen("sudo", "python3", "runLEDs.py", stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)

q = input("?>")

if q == "green":
    print("g\n", file=p.stdin)
    #p.stdin.flush()
