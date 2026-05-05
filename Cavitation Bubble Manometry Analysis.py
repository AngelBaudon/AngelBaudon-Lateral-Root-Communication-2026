# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:11:05 2026

@author: Angel.BAUDON
"""
import pandas as pd, numpy as np, matplotlib.pyplot as plt, glob, os, scipy.stats as stat
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

folder = r"C:\Users\Angel.BAUDON\Desktop\CBM"
if not os.path.exists(rf'{folder}\analysis'): os.makedirs(rf'{folder}\analysis')

files = glob.glob(f'{folder}\*.xlsx')
t_min, t_max = -600, 600
common_t = np.linspace(t_min, t_max, 1200)

plt.figure()
for file in files:
    
    file_name = file.split('\\')[-1]
    print(f'\n\n {file_name} \n\n')
    
    xl = pd.ExcelFile(file)
    
    interpolated_curves = []
    for s, sheet_name in enumerate(xl.sheet_names):
        print(sheet_name)
        raw = pd.read_excel(file, sheet_name=sheet_name, header=None).to_numpy()
        diam, rad, time, wound_indx = raw[:,1], raw[:,2], raw[:,6], raw[0,3]
        
        time = time - time[0]
        wound_t = time[wound_indx]
        t_aligned = time - wound_t
    
    
        f = interp1d(t_aligned, diam, kind="linear", bounds_error=False, fill_value=np.nan)
    
        y_interp = f(common_t)
        interpolated_curves.append(y_interp)
    
    aligned_curves = np.array(interpolated_curves, dtype=float)
    
    
    mean, sem = np.nanmean(aligned_curves, axis=0), stat.sem(aligned_curves, axis=0, nan_policy='omit')
    
    for y in aligned_curves: plt.plot(common_t, y, alpha=0.3)
    
    plt.plot(common_t, mean, linewidth=2, label="PSTH")
    plt.fill_between(common_t, mean - sem, mean + sem, alpha=0.2)
    
plt.axvline(0, label="Wound"), plt.xlabel("Time relative to event (s)")
plt.ylabel("Signal"), plt.title("PSTH (aligned & interpolated)"), plt.legend()
plt.savefig(rf'{folder}/analysis/{file_name[:-5]}.pdf')