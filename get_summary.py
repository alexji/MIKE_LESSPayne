import numpy as np
import os, sys, glob
from astropy.table import Table
if __name__=="__main__":
    alldata = []
    fnames = np.sort(glob.glob("outputs/*.npz"))
    for fn in fnames:
        dirname = os.path.dirname(fn)
        basename = os.path.basename(fn)
        s = basename.split("_")
        star = s[0]
        print(star)
        tmp = np.load(fn)
        params = tmp["popt_print"]
        Teff, logg, MH, aFe = params[0:4]
        vt = 1.0
        vbroad, rv = params[-2:]
        chi2 = tmp["chi_square"]
        snr = np.median(np.nanmedian(tmp["spectrum"]/tmp["spectrum_err"], axis=1))
        norder = tmp["spectrum"].shape[0]
        alldata.append([star, Teff, logg, vt, MH, aFe, vbroad, rv, chi2, snr, norder])
    alldata = Table(rows=alldata, names=["star", "Teff", "logg", "vt", "MH", "aFe", "vbroad", "rvobs", "chi2", "snr", "norder"])
    alldata["Teff"].format = ".0f"
    for col in ["logg", "vt", "MH", "aFe", "chi2"]: alldata[col].format = ".2f"
    for col in ["vbroad","rvobs","snr"]: alldata[col].format = ".1f"

    #alldata.sort("star")
    alldata.write("summary.org", format="ascii.fixed_width", overwrite=True)
