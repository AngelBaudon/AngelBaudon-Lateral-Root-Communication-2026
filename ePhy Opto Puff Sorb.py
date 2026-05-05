# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:31:54 2026

@author: Angel.BAUDON
"""
import pyabf, matplotlib.pyplot as plt, numpy as np, glob, pandas as pd, os, scipy.stats as stat
from pyabf.filter import gaussian


folder = r"C:\Users\Angel.BAUDON\Desktop\New folder"
index_puff = 10

for sub_folder in glob.glob(rf'{folder}\*/'):
    subfo = sub_folder.split('\\')[-2]
    print('\n'*2, ':'*30, '\n', subfo, '\n', ':'*30, '\n'*2)
    if not os.path.exists(rf'{sub_folder}\analysis'): os.makedirs(rf'{sub_folder}\analysis')
    
    puff_folders = [x for x in glob.glob(rf'{sub_folder}\*/') if x[-9:-1] != 'analysis']
    for p, puff_folder in enumerate(puff_folders):
        
        cells = glob.glob(rf'{puff_folder}\*.abf')
    
        Raw_Vm, Data, Amp, Indexes = [], [], [], []
        for cell in cells:
            cell_id = cell.split('\\')[-1]
            # print('\n'*2, '='*30, '\n', cell_id, '\n', '='*30, '\n'*2)
    
            abf = pyabf.ABF(cell)
            gaussian(abf, 10)
            raw = abf.sweepY
            
            fltr, sampling = raw[20000:220000:100], 10
            while len(fltr) < 2000: fltr = np.append(fltr, np.nan)
            time = np.linspace(0, len(fltr)/sampling, len(fltr))
            
            #Find peak
            baseline = np.nanmean(fltr[:index_puff*sampling])
            data, start = fltr - baseline, int(index_puff*sampling)
            amp = np.nanmax(data[start:])
            max_index = np.where(data[start:] == amp)[0][0]+start
            wash = np.nanmin(data[max_index:])
            
            Raw_Vm.append([baseline, *[x+baseline for x in (amp, wash)]])
            Data.append(data), Amp.append(amp)
            Indexes.append(max_index/sampling)
    
        print(Amp)
        writer = pd.ExcelWriter(f'{sub_folder}/analysis/{subfo} puff {p}.xlsx')
        for x, y in zip((Raw_Vm, Amp, Indexes), ('Raw Vm', 'Amp', 'Indexes')):
            df = pd.DataFrame(x)
            df.rename(index=pd.Series([x.split('\\')[-1] for x in cells])).to_excel(writer, sheet_name=y)
        writer.save()
        
            
        plt.figure(), plt.title(subfo)
        mean, sem = np.nanmean(Data, axis=0), stat.sem(Data, nan_policy='omit', axis=0)
        plt.plot(time, mean), plt.fill_between(time, mean-sem, mean+sem, alpha=.5, zorder=1)
        plt.legend(), plt.savefig(rf'{sub_folder}\analysis\Mean trace puff {p}.pdf')
        plt.close()
    


