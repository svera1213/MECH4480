# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 03:47:32 2018

@author: s4384905
"""

import os
import sys 
import math
import numpy as np
import matplotlib.pyplot as plt

from plot_forces_func import plot_forces



def update_U(Ux,Uy,Uz):
    """This fuction updates the flow velocity in the U file 
    """
    inputfilename = "0/U"
    outfilename = "0/U"
    
    
    lines =[]

    
    with open(inputfilename, 'r') as infile:
        for line in infile:
            
            if "\tvelocity_x" in line: 
                line = "\tvelocity_x {0};\n".format(Ux)

            if "\tvelocity_y" in line: 
                line = "\tvelocity_y {0};\n".format(Uy)
                
            lines.append(line)
    infile.close()
    
    with open(outfilename,'w') as outfile:
        for line in lines:
            outfile.write(line)
    outfile.close()

def update_controlDict(Uinf, Lift_dir, Drag_dir):
    inputfilename = "system/controlDict"
    outfilename = "system/controlDict"
    
    
    lines =[]
    
    with open(inputfilename, 'r') as infile:
        for line in infile:            
            if "\tmagUInf" in line: 
                line = "\tmagUInf {0};\n".format(Uinf)
            
            if "\tliftDir" in line:
                LDx = Lift_dir[0]
                LDy = Lift_dir[1]
                line = "\tliftDir ({0} {1} {2});\n".format(LDx,LDy,0.0)
            
            if "\tdragDir" in line:
                DDx = Drag_dir[0]
                DDy = Drag_dir[1]
                line = "\tdragDir ({0} {1} {2});\n".format(DDx,DDy,0.0)
            lines.append(line)
    infile.close()
    
    with open(outfilename,'w') as outfile:
        for line in lines:
            outfile.write(line)
    outfile.close()   

 
def extract_cl():
    os.system('rm -rf 0_temp 1* 2* 3* 4* 5* 6* 7* 8* 9* postProcessing')
    os.system('foamMesh --job=Assignment2_new')
    os.system('simpleFoam > log')   
    #os.system('paraFoam') 
    
    forcesCoeff_file = "postProcessing/forces/0/forceCoeffs.dat"
    
    coeff_file = open(forcesCoeff_file, 'r')
    linelist = coeff_file.readlines()
    coeff_file.close()
    
    line_unprocessed =  linelist[-1].split()
    
    c_d = float(line_unprocessed[2])
    c_l = float(line_unprocessed[3])
    
    Fd , Fl = plot_forces()
    
    return c_d,c_l,Fd,Fl

###############################################################################


lift_force =[[3.6602,	3.3602,2.9602,2.7602],\
            [4.6602,4.2102,3.8352,3.5602],\
            [5.3602,5.0102,4.5602,4.1102],\
            [5.7852,5.2602,5.2602,4.5102],\
            [9.5102,8.6102,7.9102,7.5102]] 
            
drag_force = [3.6602,	3.3602,2.9602,	2.7602]


###############################################################################
AoA = [0,1,2,5,10]

Lift_dir = [[0,1,0],\
    [-math.sin(math.radians(1)), math.cos(math.radians(1)), 0],\
    [-math.sin(math.radians(2)), math.cos(math.radians(2)), 0],\
    [-math.sin(math.radians(5)), math.cos(math.radians(5)), 0],\
    [-math.sin(math.radians(10)), math.cos(math.radians(10)), 0]]
    
Drag_dir = [[1,0,0],\
    [math.cos(math.radians(1)), math.sin(math.radians(1)), 0],\
    [math.cos(math.radians(2)), math.sin(math.radians(2)), 0],\
    [math.cos(math.radians(5)), math.sin(math.radians(5)), 0],\
    [math.cos(math.radians(10)), math.sin(math.radians(10)), 0]]
    
Uinf = np.linspace(26.0, 30.00, num=5) #CHANGE LIMITS FOR DESIRED FLOW VELOCITY INTERVAL
#Ux = 35.0
#Uy = 0.0
#Uz = 0.0
##Uz = 0.0
#
#Uinf = Ux
#update_U(Ux,Uy,Uz)
#update_controlDict(Uinf)
#cd, cl = extract_cl()
#print(cl)

CL = [] #CL LISTS WILL BE STORED HERE
CD = [] #CL LISTS WILL BE STORED HERE

FL = []
FD = []



for j in range(len(Lift_dir)):
    CL_list = [] 
    CD_list = [] 

    FL_list = []
    FD_list = []
    
    counter =0
    
    for i in Uinf: # LOOP WILL UPDATE U FILE, controlDict FILE, AND RUN foamMesh-simpleFoam FOR EACH VELOCITY
        
        Ux = i*math.cos(math.radians(AoA[counter]))
        Uy = i*math.sin(math.radians(AoA[counter]))
        
        update_U(Ux,Uy,0.0)
        
        update_controlDict(i, Lift_dir[j], Drag_dir[j])
        
        cd, cl, Fd, Fl = extract_cl()
        
        CL_list.append(cl)
        CD_list.append(cd)
        
        FL_list.append(Fl)
        FD_list.append(Fd)
        counter+=1
    
    CL.append(CL_list)
    CD.append(CD_list)
    FL.append(FL_list)
    FD.append(FD_list)

print("********SIMULATION SUCCESSFULLY COMPLETED********")

c=0
for i in CL:
    plt.plot(Uinf, i, '-', label="AoA %s deg" %AoA[c])
    c+=1

plt.grid()
lgd = plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=5)  
plt.xlabel("Flow velocity (m/s)")
plt.ylabel("CL")

plt.savefig("CL-Vel.png", dpi = 500 , bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()


plt.figure()
c=0
for i in CD:
    plt.plot(Uinf, i, '-', label="AoA %s deg" %AoA[c])
    c+=1

plt.grid()
lgd = plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=5) 
plt.xlabel("Flow velocity (m/s)")
plt.ylabel("CD")

plt.savefig("CD-Vel.png", dpi = 500 , bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()


plt.figure()
c=0
for i in FD:
    plt.plot(Uinf, i, '-', label="AoA %s deg" %AoA[c])
    c+=1

plt.grid()
lgd =  plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=5) 
plt.xlabel("Flow velocity (m/s)")
plt.ylabel("FD")

plt.savefig("FD-Vel.png", dpi = 500 , bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()


plt.figure()
c=0
for i in FL:
    plt.plot(Uinf, i, '-', label="AoA %s deg" %AoA[c])
    c+=1

plt.grid()
lgd =   plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=5) 
plt.xlabel("Flow velocity (m/s)")
plt.ylabel("FL")

plt.savefig("FL-Vel.png", dpi = 500 , bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()


