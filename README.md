# Stacking-Fault-Energy

This allows to evaluate the stacking fault energy of a potential for a fcc system, along the (111) plane. Or course this can be re-adapted for other applications. This requires python, atomsk and lammps.
/!\ works only for eam type potential for now !



How to use it :
0. Make sure python, lammps and atomsk (https://atomsk.univ-lille.fr/) is installed
1. Find the potential you want to evaluate (ex : https://www.ctcms.nist.gov/potentials/)
2. Paste the potential file with the 3 other files in the "scripts" folder. Name the potential file XX.eam.alloy, with XX = the material you want to evaluate. For example, Ni.eam.alloy, Cu.eam.alloy...)
3. Launch the python script. I recommand to launch it with Spyder, to have access to the variable explorer
4. The script gives the lowest energy value among all calculated, this is normally the stacking fault energy. Check the "energy_diff" variable to find which calculation it is, and check with Ovito if this configuration corresponds to a stacking fault. (ex : if the scirpt gives 17.76 mJ/m², open the "energy_diff" variable, check its position (ex : 16), and check with Ovito if the "RESULTS_16" is a stacking fault configuration)
Else, take the lowest energy corresponding to a stacking fault configuration.
