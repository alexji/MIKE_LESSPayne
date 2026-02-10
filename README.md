# MIKE LESSPayne Analysis

Automated stellar abundance analysis of Magellan/MIKE spectra using [LESSPayne](https://github.com/alexji/LESSPayne).

## Prerequisites

- Python 3 with numpy, astropy, matplotlib, pandas, pyyaml
- [LESSPayne](https://github.com/alexji/LESSPayne) installed
- Reduced MIKE spectra as multi-order FITS files (`*blue_multi.fits` and `*red_multi.fits` pairs), placed in `reduced_data/`
- A MOOG-format equivalent width linelist (provided as `master_merged_eqw_short.moog`, or specify your own in the config)
- You'll want to `chmod +x run_lesspayne_all.sh` and same for `copy_reduced_data.sh`

## Directory Structure

```
.
├── reduced_data/          # Input: reduced MIKE spectra (*blue_multi.fits, *red_multi.fits)
├── cfgs/                  # Generated YAML config files (one per star)
├── outputs/               # LESSPayne output files (.npz, .smh, abundance tables)
├── figs/                  # Summary figures
├── copy_reduced_data.sh            # Step 0: copy data
├── create_cfgs_directory_mike.py   # Step 1: generate config files
├── make_all_cfgs.py                # Step 2: build the run list
├── run_lesspayne_all.sh            # Step 3: run LESSPayne
├── get_summary.py                  # Step 4: extract stellar parameter summary
├── make_summary_figs.py            # Step 5: make summary plots
├── quick_abund.ipynb               # Step 6: interactive abundance analysis
└── master_merged_eqw_short.moog    # Reference linelist
```

## Step-by-Step Guide

### Step 0: Copy reduced data

Edit the file so it has a path to the data directory you are reducing in

```bash
./copy_reduced_data.sh
```

### Step 1: Create configuration files

Generate one YAML config file per star from the reduced data directory:

```bash
python create_cfgs_directory_mike.py reduced_data cfgs
```

- First argument: path to directory containing the reduced FITS files
- Second argument: directory to write config files into
- Note: you need both the blue and red files for the same thing or else it will crash

Each config file specifies the input spectra, output paths, Payne fitting parameters, normalization settings, EQW fitting options, and more. Review `create_cfgs_directory_mike.py` to adjust default parameters (e.g., wavelength range, initial stellar parameters, mask regions, linelist paths).

**Important:** You will need to update the hardcoded paths in `create_cfgs_directory_mike.py` to match your system:
- `NN_file`: path to the LESSPayne neural network model file
- `template_spectrum_fname`: path to the template spectrum for auto-velocity
- `eqw_linelist_fname`: path to the EQW linelist, default is the one bundled here

### Step 2: Build the run list

Generate `all_cfgs.txt`, the list of config files to process:

```bash
python make_all_cfgs.py
```

This script:
- Scans `cfgs/` for all YAML config files
- Skips any config with "bad" in the filename
- Skips stars that already have output files in `outputs/` (for resuming interrupted runs)
- Writes the remaining config paths to `all_cfgs.txt`

Re-run this script to update the list if you want to process only unfinished stars.

### Step 3: Run LESSPayne

Run the full LESSPayne pipeline on all stars in the run list (Note: this requires being in the LESSPayne environment):

```bash
./run_lesspayne_all.sh
```

This calls `LESSPayne/cli/run.py` with flags `-12348` on each config file, which runs these steps in order:
1. Payne spectral fitting (Teff, logg, [M/H], [alpha/Fe])
2. Continuum normalization, create .smh file
3. Equivalent width fitting
4. Stellar parameters and measure abundances
8. Summary output

Steps 5, 6, and 7 are for syntheses and uncertainty analysis, but these can take some time so I don't use them in the autorun.

**Note:** Update the path to `LESSPayne/cli/run.py` in `run_lesspayne_all.sh` to match your installation. You can also run individual stars:

```bash
python /path/to/LESSPayne/LESSPayne/cli/run.py -12348 cfgs/cfg_STARNAME.yaml
```

### Step 4: Extract stellar parameter summary

After all stars are processed, generate a summary table:

```bash
python get_summary.py
```

This reads the `*_paynefit.npz` files from `outputs/` and writes `summary.org`, a table containing Teff, logg, [M/H], [alpha/Fe], vbroad, radial velocity, chi-squared, and SNR for each star.

### Step 5: Make summary figures

Generate summary plots for each star (Note: this requires being in the LESSPayne environment):

```bash
python make_summary_figs.py
```

This loads each `.smh` session file and creates three figures per star in `figs/`:
- `STAR_summary1.png`: regular spectrum summary plot
- `STAR_summary2.png`: neutron-capture spectrum summary plot
- `STAR_snr.png`: signal-to-noise plot

### Step 6: Interactive abundance analysis

Open `quick_abund.ipynb` in Jupyter for interactive abundance analysis. This notebook:
- Reads the abundance output tables (`outputs/*abunds.txt`)
- Compiles a combined abundance table across all stars
- Plots [X/Fe] vs [Fe/H] for various elements (Na, Mg, Al, Ca, Ti, Sr, Ba, etc.)

## Customization

### Marking bad stars

To exclude a star from processing, either:
- Rename its config file to include "bad" (e.g., `cfg_bad_STARNAME.yaml`)
- Or manually remove its entry from `all_cfgs.txt`

### Adjusting analysis parameters

Edit the `default_kws` dictionary in `create_cfgs_directory_mike.py`, or modify individual YAML config files directly.

### Re-running specific steps

The `-12348` flags in `run_lesspayne_all.sh` control which steps to run. Use subsets to re-run specific stages (e.g., `-3` for just EQW fitting, `-8` for just the summary). 
