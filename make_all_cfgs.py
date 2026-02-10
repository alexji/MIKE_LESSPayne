import os, sys, glob
import numpy as np

all_cfgs = np.sort(glob.glob("cfgs/*"))
with open("all_cfgs.txt","w") as fp:
    def write(x): fp.write(x+"\n")
    for cfgfile in all_cfgs:
        star = os.path.basename(cfgfile).split("_")[1].split(".")[0]
        if "bad" in star: continue
        if os.path.exists(f"outputs/{star}_paynefit.npz"):
            print("Skipping",star)
        else:
            print("Writing",star)
            write(cfgfile)

