import threading
from time import sleep

i=0

def threadToRun():
    global i
    while True:
        i += 1
        print(i)
        sleep(1)
    
t=threading.Thread(target=threadToRun)
t.daemon = True
t.start()

sleep(3)
assert 1 == 0