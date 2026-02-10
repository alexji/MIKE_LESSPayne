from LESSPayne.smh import Session
import matplotlib.pyplot as plt
import numpy as np
import glob, os
fnames = glob.glob("on-the-fly-n1-outputs/*.smh") + glob.glob("outputs/*.smh")
fnames = np.sort(fnames)

OUTDIR = "figs/"


for fname in fnames:
    name = os.path.basename(fname)
    star = "_".join(name.split("_")[:-1])
    print(star)
    session = Session.load(fname)
    
    fig1 = session.make_summary_plot()
    fig2 = session.make_ncap_summary_plot()
    fig3 = session.make_snr_plot()
    fig1.savefig(f"{OUTDIR}/{star}_summary1.png")
    fig2.savefig(f"{OUTDIR}/{star}_summary2.png")
    fig3.savefig(f"{OUTDIR}/{star}_snr.png")
    plt.close(fig1)
    plt.close(fig2)
    plt.close(fig3)
    
