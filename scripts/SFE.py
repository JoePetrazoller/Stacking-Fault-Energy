# -*- coding: utf-8 -*-
"""
Created on Tue May  9 11:49:58 2023

@author: petrazol2
"""


#TAILLE DE BOITE, POT NAME, LOG

 # allfiles = os.listdir(os.getcwd())
import os
import subprocess
import glob
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np



def findline(file_path, word):

    with open(file_path, 'r') as fp:
        # read all lines in a list
        lines = fp.readlines()
        count = 0
        for line in lines:
            count = count+1
            if line.find(word) != -1:
                if line[0:5] == 'print':
                    line = lines[count]
                    return(line)
                else:
                    return(line)


def findword(file_path, word, first, last):
    line = findline(file_path, word)
    try:
        start = line.index(first) + len(first)
        end = line.index(last, start)
        value = line[start:end]
        return value
    except ValueError:
                return ""




WORKDIR = glob.glob(os. getcwd())[0]
allfiles = os.listdir(os.getcwd())
POT=''

for i in range(0,len(allfiles)):
    if allfiles[i][-10:]=='.eam.alloy':
        POT=str(allfiles[i])
        print('Potential identified : '+POT)



if glob.glob(WORKDIR+'\\0.log_SFE.txt'):
    Mat=findword(WORKDIR+'\\0.log_SFE.txt','Material','Material studied : ','\n')
    a=float(findword(WORKDIR+'\\0.log_SFE.txt','Lattice','Lattice parameter : ', '(A)'))
else:
    Mat=input('Name ? : \n')
    a=float(input('Lattice parameter ? : \n'))




if glob.glob(WORKDIR+'\\log_step1.lammps'):
    pass
else:
    subprocess.call('atomsk --create fcc '+str(a)+' '+Mat+' orient [-110] [111] [11-2] -duplicate 8 8 8 '+Mat+'_cell_before.xsf lammps', shell=True, stdout=subprocess.DEVNULL)
    os.remove(glob.glob(WORKDIR+'\\'+Mat+'_cell_before.xsf')[0])
    subprocess.call('lmp -in SFE_step1.lmp -v POT '+POT+' -v Mat '+Mat, shell=True, stdout=subprocess.DEVNULL)
    os.rename(WORKDIR+'\\log.lammps', WORKDIR+'\\log_step1.lammps')

with open('RESULTS', 'r') as fp:
    lines = fp.readlines()
    
fill=0
count=0
here=0

for i in range(0,len(lines)):
    count=count+1
    if lines[i]=='ITEM: TIMESTEP\n':
        if float(lines[i+1])>fill:
            fill=float(lines[i+1])
            here=count
            
        
line_copy=here+8

with open(Mat+'_cell_before.lmp','r') as fp:
    lines_cell = fp.readlines()


# lines_cell[6]='      0.000000000000      '+str(float(lines[6].split()[1]))+'  ylo yhi\n'




with open(Mat+'_cell.lmp', 'w') as fp:
    for i in range(0,15):
        fp.write(lines_cell[i])
    for i in range(0,len(lines[line_copy:])):
        fp.write(lines[i+line_copy])
        












Energies = []
Energies_incr = 0





x=[1,1,0]
y=[1,1,1]
z=[1,1,2]
maxshift_1=(a*(x[0]**2+x[1]**2+x[2]**2)**(0.5))/2
maxshift_2=(a*(z[0]**2+z[1]**2+z[2]**2)**(0.5))/2


c=0

if glob.glob(WORKDIR+'\\log_ref.lammps'):
    pass
else:
    subprocess.call('cmd /c lmp -in SFE.lmp -v boundary s -v POT '+POT+' -v Mat '+Mat+' -v c '+str(c)+' -v name '+Mat+'_cell', shell=True, stdout=subprocess.DEVNULL)
    os.rename(WORKDIR+'\\log.lammps', WORKDIR+'\\log_ref.lammps')


for x1 in (np.linspace(0,maxshift_1,10)):
    for y1 in (np.linspace(0,maxshift_2,10)):
        c=c+1
        if glob.glob(WORKDIR+'\\log'+str(c)+'.lammps'):
            pass
        else:
            subprocess.call('atomsk '+Mat+'_cell.lmp -shift above 0.5*box Y '+str(x1)+' 0.0 '+str(y1)+' -remove-doubles 0.05 SF'+str(c)+'.xsf lammps', shell=True, stdout=subprocess.DEVNULL)
            subprocess.call('cmd /c lmp -in SFE.lmp -v boundary s -v POT '+POT+' -v name SF'+str(c)+' -v c '+str(c)+' -v Mat '+Mat, shell=True, stdout=subprocess.DEVNULL)
            os.rename(WORKDIR+'\\log.lammps', WORKDIR+'\\log'+str(c)+'.lammps')
        
        




allfiles = os.listdir(os.getcwd())
for i in range(0,len(allfiles)):
    if allfiles[i][-4:]=='.xsf':
        os.remove(glob.glob(WORKDIR+'\\'+str(allfiles[i]))[0])
        
        


Energy_ref = float(findword('log_ref.lammps', 'RESULT:', 'of ', ' eV'))
nb_Atoms_ref = float(findword('log_ref.lammps','RESULT:', 'for ', ' atoms'))

Energies=[]
for i in range(0,len(allfiles)):
    if glob.glob(WORKDIR+'\\log'+str(i)+'.lammps'):
        Energies.append(float(findword('log'+str(i)+'.lammps', 'RESULT:', 'of ', ' eV')))



xdim=float(findword(Mat+'_cell.lmp','xlo','.000000000000      ','xlo'))
zdim=float(findword(Mat+'_cell.lmp','zlo','.000000000000      ','zlo'))
A=(xdim*zdim)*10**-20   #lx * lz


Energies_diff=[]
for i in range(0,len(Energies)):
    Energies_diff.append((Energies[i])-(Energy_ref))
    Energies_diff[i]=Energies_diff[i]*1.60217657*10**-16   #eV to mJ
    Energies_diff[i]=Energies_diff[i]/A


# Energies_diff.sort()
    
    

for i in range(0,len(Energies_diff)):
    if Energies_diff[i]<0.1 and Energies_diff[i]>-0.1:
        Energies_diff[i]=10000
        
print('=========================================================================')
print('Stacking fault energy = '+str(min(Energies_diff)) + ' mJ/m²')
print('=========================================================================')


if glob.glob(WORKDIR+'\\0.log_SFE.txt'):
    pass
else:
    with open('0.log_SFE.txt', 'w') as fp:
        fp.write('Stacking fault energy = '+str(min(Energies_diff)) + ' mJ/m²\n')
        fp.write('\n')
        fp.write('Potential used : '+POT+'\n')
        fp.write('Material studied : '+Mat+'\n')
        fp.write('Lattice parameter : '+str(a)+' (A)\n')
    
    print('Log file generated')