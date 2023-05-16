
import os
import time


for k in [12, 24, 48, 72,  96, 120, 144, 180, 240, 288]:
    if (24*60)/k != int(24*60/k):
        y = int((24*60)/k)
        k = (24*60)/y
        if int(k) != k: continue
    print("-"*80)
    print(f"Schedule every {(24*60)/k} minutes: K = {k}")
    os.system(f"make -e K={k}")
    time.sleep(1)
    os.system(f"make -e K={k} run")
    time.sleep(1)
    

