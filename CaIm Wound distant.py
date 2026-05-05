# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 19:11:52 2026

@author: Angel.BAUDON
"""
import pandas as pd, numpy as np, matplotlib.pyplot as plt, glob, os
from scipy.signal import savgol_filter

folder = r"C:\Users\Angel.BAUDON\Desktop\To analyse\2026_GCaMP_Wound Distant BAPTA"
if not os.path.exists(rf'{folder}\analysis'): os.makedirs(rf'{folder}\analysis')

file = glob.glob(f'{folder}\*.xlsx')[0]
file_name = file.split('\\')[-1]
wound, sampling_Hz, rec_len = 40, .2, 120
data, Amps, Max_indx = [], [], []
xl = pd.ExcelFile(file)

for s, sheet_name in enumerate(xl.sheet_names):
    raw = pd.read_excel(file, sheet_name=sheet_name, header=None).to_numpy()
    F = raw[:,1] - raw[:,0]

    baseline = np.nanmean(F[:wound])
    dff0 = (F[:rec_len]-baseline)/baseline
        
    fltr = savgol_filter(dff0, 5, 2)
    while len(fltr) < rec_len: fltr = np.append(fltr, np.nan)

    amp = max(fltr[wound:])
    max_index = np.where(fltr[wound:] == amp)[0][0] + wound
    
    plt.figure(), plt.plot(fltr), plt.axvline(wound)

    data.append(np.asarray(fltr)), Amps.append(amp), Max_indx.append(max_index)

x_ax = np.linspace(0, rec_len/sampling_Hz, rec_len)
ar = np.asarray(data)

plt.figure()
for rec in range(ar.shape[0]):
    plt.subplot(int(ar.shape[0]/2+1), 2, rec+1)
    plt.plot(x_ax, ar[rec,:]), plt.xlabel('Time(s)'), plt.ylabel('dF/F0')
    plt.axvline(wound/sampling_Hz)
plt.savefig(rf'{folder}/analysis/{file_name[:-5]}.pdf')

      
writer = pd.ExcelWriter(rf'{folder}/analysis/{file_name[:-5]} analysis.xlsx')
pd.DataFrame(Amps).to_excel(writer, sheet_name = 'Amp')
pd.DataFrame(Max_indx).to_excel(writer, sheet_name = 'Index')
writer.save()  
