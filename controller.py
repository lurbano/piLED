import subprocess
import time

p = subprocess.Popen(["sudo", "python3", "runLEDs.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,  universal_newlines=True)

time.sleep(1)
p.stdin.write("g\n")
time.sleep(5)
print("done")

# q = input("?>")
#
# if q == "green":
#     p.stdin.write("g")
#     #print(b'g', file=p.stdin)
#     #p.stdin.flush()
