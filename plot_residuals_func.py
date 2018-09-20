# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 17:01:42 2018

@author: s4384905
"""
import os
import sys 
import math
import numpy as np
import matplotlib.pyplot as plt


def plot_residuals():
    inputfilename = "postProcessing/residuals/0/residuals.dat"
    
    time = []
    p = []
    Ux = []
    Uy = []
    
    resi_file = open(inputfilename, 'r')
    list_resi = resi_file.readlines()
    resi_file.close()
    
    list_unprocessed = []
    
    for i in list_resi:
        list_unprocessed.append(i.split())

    list_unprocessed.pop(0)
    list_unprocessed.pop(0)
    

    for i in range(len(list_unprocessed)):
        time.append(float(list_unprocessed[i][0]))
        p.append(float(list_unprocessed[i][1]))
        Ux.append(float(list_unprocessed[i][2]))
        Uy.append(float(list_unprocessed[i][3]))
        
    plt.plot(time, p, label='p')
    plt.plot(time, Ux, label='Ux')
    plt.plot(time, Uy, label='Uy')
    plt.legend(loc='lower left')
    
    plt.xlabel("Time (s)")
    plt.ylabel("Residuals ")
    plt.yscale('log')

    plt.title("Convergence Plot - Residuals over Time")
    plt.savefig("Convergence_residuals.png", dpi = 480)
    plt.show()

plot_residuals()   