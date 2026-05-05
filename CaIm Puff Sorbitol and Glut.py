# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 13:07:47 2026

@author: Angel.BAUDON
"""
import pandas as pd, numpy as np, matplotlib.pyplot as plt, glob, scipy.stats as stat, os
from scipy.signal import savgol_filter, find_peaks


folder = r"C:\Angel.BAUDON\Exp\Data\0_Root XXM IAA project\IAA Puff\Root GECO Imaging IAA puff"
if not os.path.exists(rf'{folder}\analysis'): os.makedirs(rf'{folder}\analysis')

file = glob.glob(f'{folder}\*.xlsx')[2]
file_name = file.split('\\')[-1]
sampling_Hz, rec_len, indx_puff = .2, 120, 200
data, Amps = [], []
xl = pd.ExcelFile(file)

plt.figure()
for s, sheet_name in enumerate(xl.sheet_names):
    
    raw = pd.read_excel(file, sheet_name=sheet_name).to_numpy()
    _, n_rec = raw.shape
    
    F = raw[:,1] - raw[:,0]
    baseline = np.nanmean(F[:indx_puff])
    dff0 = (F[:rec_len]-baseline)/baseline
    fltr = savgol_filter(dff0, 5, 2)
    while len(fltr) < rec_len: fltr = np.append(fltr, np.nan)

    
    plt.subplot(len(xl.sheet_names), 1, s+1)
    plt.plot(dff0), plt.plot(fltr), plt.axvline(indx_puff*sampling_Hz)
    amp = np.nanmax(fltr)
    
    data.append(np.asarray(fltr)), Amps.append(amp)


plt.savefig(rf'{folder}/analysis/{file_name[:-5]} individual traces.pdf')


x_ax = np.linspace(0, rec_len/sampling_Hz, rec_len)

plt.figure()
d = np.asarray(data)
m, s = np.nanmean(d, axis=0), stat.sem(d, axis=0, nan_policy='omit')
# m, s = savgol_filter(m, 3, 1), savgol_filter(s, 3, 1)
plt.plot(x_ax, m), plt.fill_between(x_ax, m-s, m+s, alpha=0.5), plt.axvline(indx_puff)
plt.xlabel('Time(s)'), plt.ylabel('dF/F0'), plt.legend()
plt.savefig(rf'{folder}/analysis/{file_name[:-5]}.pdf')


plt.figure()
for trace in d: plt.plot(x_ax, trace)
plt.axvline(indx_puff), plt.xlabel('Time(s)'), plt.ylabel('dF/F0'), plt.legend()
plt.savefig(rf'{folder}/analysis/{file_name[:-5]} all traces.pdf')
      
writer = pd.ExcelWriter(rf'{folder}/analysis/{file_name[:-5]} analysis.xlsx')
pd.DataFrame(d).to_excel(writer, sheet_name = 'dFF0')
pd.DataFrame(Amps).to_excel(writer, sheet_name = 'Amp')
writer.save()  

    