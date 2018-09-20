#!/usr/bin/python
"""
Spyder Editor

This is a temporary script file.
"""



import os
import sys
import math
import matplotlib.pyplot as plt

def plot_convergence():
    
    forces_file = "postProcessing/airfoil/0/forces.dat"
    
    if not os.path.isfile(forces_file):
    	print "Forces file not found at "+forces_file
    	print "Be sure that the case has been run and you have the right directory!"
    	print "Exiting."
    	sys.exit()
    
    def line2dict(line):
    	tokens_unprocessed = line.split()
    	tokens = [x.replace(")","").replace("(","") for x in tokens_unprocessed]
    	floats = [float(x) for x in tokens]
    	data_dict = {}
    	data_dict['time'] = floats[0]
    	force_dict = {}
    	force_dict['pressure'] = floats[1:4]
    	force_dict['viscous'] = floats[4:7]
    	force_dict['porous'] = floats[7:10]
    	moment_dict = {}
    	moment_dict['pressure'] = floats[10:13]
    	moment_dict['viscous'] = floats[13:16]
    	moment_dict['porous'] = floats[16:19]
    	data_dict['force'] = force_dict
    	data_dict['moment'] = moment_dict
    	return data_dict
    
    time = []
    drag = []
    lift = []
    moment = []
    with open(forces_file,"r") as datafile:
    	for line in datafile:
    		if line[0] == "#":
    			continue
    		data_dict = line2dict(line)
    		time += [data_dict['time']]
    		drag += [data_dict['force']['pressure'][0] + data_dict['force']['viscous'][0]]
    		lift += [data_dict['force']['pressure'][1] + data_dict['force']['viscous'][1]]
    		moment += [data_dict['moment']['pressure'][2] + data_dict['moment']['viscous'][2]]
    datafile.close()
    

    plt.plot(time, lift, 'r-', label="Lift")
    plt.plot(time, drag, 'b-', label="Drag")
    
    plt.xlabel("Time (s)")
    plt.ylabel("Force (N)")

    
    plt.title("Convergence Plot - Forces over Time")
    plt.legend()
    plt.savefig("Convergence_forces.png", dpi = 480)
    plt.show()
    
plot_convergence()  
    
#outputfile = open('forces.txt','w')
#for i in range(0,len(time)):
#	outputfile.write(str(time[i])+' '+str(lift[i])+' '+str(drag[i])+' '+str(moment[i])+'\n')
#outputfile.close()