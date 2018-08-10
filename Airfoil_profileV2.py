# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from math import *
import numpy as np
import matplotlib.pyplot as plt
from Vortex_Calculator import strength_vortex

def NACA(code,N):
    
    """
        Receives the NACA for digit code as input and number of points N.
        Returns the contour point coordinates.
    """
    
    # Show an error message if inputs are not in the correct format
    if not (int(code) and int(N)):
        raise ValueError("Invalid function input!")
    
    # Obtain individual airfoil parameters from the input information
    code = str(code)
    M = float(code[0]) # Max camber of m%
    P = float(code[1]) # Located 0.p chords from leading edge
    XX = float(code[2:]) # With a max thickness of xx% of the chord
    
    # Transform to percentage values
    m = M/100
    p = P/10
    xx = XX/100
    
    B = np.linspace(0.,np.pi,N)
    X = []
    
    for b in B:
        
        x = (1-np.cos(b))/2
        X.append(x)
    
    Yc = [] # Camber vertical coords
    Yt = []
    Upper = []
    Lower = []
    
    a0 = 0.2969
    a1 = -0.126
    a2 = -0.3516
    a3 = 0.2843
    #a4 = -0.1015
    a4 = -0.1036 # For closed trailing edge
    
# =============================================================================
#     G = []
#     Xu = []
#     Xl = []
#     Yu = []
#     Yl = []
# =============================================================================
    
    for x in X:
        
        yt = (xx/0.2) * (a0*x**0.5 + a1*x + a2*x**2 + a3*x**3 +a4*x**4)
        Yt.append(yt)
        
        if x < p:
            yc = (m/p**2) * (2*p*x - x**2)
            Yc.append(yc)
            #g = (2*m/p**2) * (p-x)
            #G.append(g)
            
        else:
            yc = (m/(1-p)**2) * (1 - 2*p + 2*p*x - x**2)
            Yc.append(yc)
            #g = ( 2*m/(1-p)**2 ) * (p-x)
            #G.append(g)
        #####################
# =============================================================================
#         alpha = np.arctan(g)
#         
#         xu = x - yt*np.sin(alpha)
#         xl = x + yt*np.sin(alpha)
#         
#         yu = yc + yt*np.cos(alpha)
#         yl = yc - yt*np.cos(alpha)
#         
#         Xu.append(xu)
#         Xl.append(xl)
#         Yu.append(yu)
#         Yl.append(yl)
# =============================================================================
        
        #########################
        up = yc + yt # Upper wing profile vertical coord
        low = yc - yt # Lower wing profile vertical coord
        
        Upper.append(up) # Upper profile coordinates
        Lower.append(low) # Lower profile coordinates
        
        
    Xcons_u = [] # Constraint points X coordinates
    Ycons_u = [] # Constraint points Y coordinates
    
    Xcons_l = [] # Constraint points X coordinates
    Ycons_l = [] # Constraint points Y coordinates
    
    Grad_u = [] # Upper constraint point gradients
    Grad_l = [] # Lower constraint point gradients
    
    for x in X[0:-1]:
        
        pos = X.index(x)
        x2 = X[ pos + 1 ]
        dx = x2 - x
        
        #Upper branch##########################################################
        yu2 = Upper[ pos + 1 ]
        yu1 = Upper[ pos ]
        
        dyu = yu2 - yu1
        theta_u = np.arctan(dyu/dx)
        grad_u = np.tan(theta_u)
        ru = ( dx**2 + dyu**2 )**0.5
        
        yu = (ru/2) * np.sin(theta_u)
        xu = (ru/2) * np.cos(theta_u)
         
        xu = xu + x
        yu = yu + yu1
        
        Xcons_u.append(xu) # Upper X constraint points coords
        Ycons_u.append(yu) # Upper Y constraint points coords
        Grad_u.append(grad_u) # Upper constraint points gradients
        
        #Lower branch##########################################################
        yl1 = Lower[ pos + 1 ]
        yl2 = Lower[ pos ]
        
        dyl = yl2 - yl1
        theta_l = np.arctan(dyl/dx)
        grad_l = np.tan(theta_l)
        rl = ( dx**2 + dyl**2 )**0.5
        
        yl = (rl/2) * np.sin(theta_l)
        xl = (rl/2) * np.cos(theta_l)
         
        xl = xl + x
        yl = yl + yl1
        
        Xcons_l.append(xl) # Upper X constraint points coords
        Ycons_l.append(yl) # Upper Y constraint points coords
        Grad_l.append(grad_l) # Lower constraint points gradients        
    
    Lower=Lower[1:-1]
    
#    plt.plot(X,Yc) # Plot of camber line
#    plt.plot(X, Upper, 'ro')
#    plt.plot(X[1:-1], Lower, 'ro')
#    #plt.plot(Xu, Yu, 'ro')
#    #plt.plot(Xl, Yl, 'ro')
#    plt.plot(Xcons_u,Ycons_u,'g')
#    plt.plot(Xcons_l,Ycons_l,'y')
#    plt.ylim(-0.1,0.12)
#    plt.show()
#    
#    plt.plot(Xcons_u,Grad_u)
#    plt.plot(Xcons_l,Grad_l)
#    plt.show()

    return (X,Upper), (X[1:-1],Lower), (Xcons_u,Ycons_u), (Xcons_l,Ycons_l), (Xcons_u,Grad_u), (Xcons_l,Grad_l)

def test_run():
    
    a, b, c, d, e, f = NACA(4412, 51)
    
    x_v1,y_v1 = a
    x_v2,y_v2 = b
    x_c1,y_c1 = c
    x_c2,y_c2 = d
    xc1,gra1 = e
    xc2,gra2 = f
    
    x_vortex = x_v1+x_v2
    y_vortex = y_v1+y_v2
    x_point = x_c1 + x_c2
    y_point= y_c1+y_c2
    uinf= 30.0
    alpha_v = gra1 +gra2
#    print(alpha_v)
    
    
    return strength_vortex(x_vortex, y_vortex, x_point, y_point, uinf, alpha_v), x_vortex, y_vortex, x_point, y_point

a,b,c,d,e=test_run()
