# -*- coding: utf-8 -*-
"""
Spyder Editor
V.15.08
This is a temporary script file.
"""

from math import *
import numpy as np
import matplotlib.pyplot as plt
from Vortex_Calculator_FINAL import strength_vortex
from Vortex_Calculator_FINAL import strength_vortex_low


def NACA(code,N):
    
    """
        Receives the NACA for digit code as input and number of points N.
        Returns the contour point coordinates.
    """
    # Height from ground
    hact = 0.4
    
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
    
    Yc = [] # Camber vertical coords upper wing
    Yc2 = [] # Camber vertical coords lower wing  
    
    #WING 
    a0 = 0.2969
    a1 = -0.126
    a2 = -0.3516
    a3 = 0.2843
    #a4 = -0.1015
    a4 = -0.1036 # For closed trailing edge
    
    #TOP WING:
    Xu = [] #Upper vortex x-points
    Xl = [] #Lower vortex x-points
    Yu = [] #Upper vortex y-points
    Yl = [] #Lower vortex y-points
    
    #BOTTOM WING:
    Xu2 = [] #Upper vortex x-points
    Xl2 = [] #Lower vortex x-points
    Yu2 = [] #Upper vortex y-points
    Yl2 = [] #Lower vortex y-points
    
    for x in X:
        
        yt = (xx/0.2) * (a0*x**0.5 + a1*x + a2*x**2 + a3*x**3 +a4*x**4) #Distance from chord
        
        if x < p:
            
            yc = hact + (m/p**2) * (2*p*x - x**2)
            g = (2*m/p**2) * (p-x)
            
            Yc.append(yc)
            Yc2.append(yc*-1)
            
        else:
            
            yc = hact + (m/(1-p)**2) * (1 - 2*p + 2*p*x - x**2)
            g = ( 2*m/(1-p)**2 ) * (p-x)
            
            Yc.append(yc)
            Yc2.append(yc*-1)

        alpha = np.arctan(g)
          
        xu = x - yt*np.sin(alpha)
        xl = x + yt*np.sin(alpha)
         
        yu = yc + yt*np.cos(alpha)
        yl = yc - yt*np.cos(alpha)
        
        Xu.append(xu)
        Xl.append(xl)
        Yu.append(yu)
        Yl.append(yl)
          
        Xu2.append(xu)
        Xl2.append(xl)
        Yu2.append(-1*yu)
        Yl2.append(-1*yl)
        
    Xu = Xu[1:-1]
    Yu = Yu[1:-1]
    Xl = Xl[1:-1]
    Yl = Yl[1:-1]
    
    Xu2 = Xu2[1:-1]
    Yu2 = Yu2[1:-1]
    Xl2 = Xl2[1:-1]
    Yl2 = Yl2[1:-1]    
            
    Xcons_u = [] # Constraint points X coordinates
    Ycons_u = [] # Constraint points Y coordinates
    Xcons_u2 = [] # Constraint points X coordinates
    Ycons_u2 = []   
    
    Xcons_l = [] # Constraint points X coordinates
    Ycons_l = [] # Constraint points Y coordinates
    Xcons_l2 = [] # Constraint points X coordinates
    Ycons_l2 = []    
    
    Grad_u = [] # Upper constraint point gradients
    Grad_l = [] # Lower constraint point gradients
    Grad_u2 = [] # Upper constraint point gradients
    Grad_l2 = []    
        
    
    for xu in Xu[0:-1]:
        
        pos = Xu.index(xu)
        
        yu = Yu[pos]
        yl = Yl[pos]
        
        xu2 = Xu[ pos + 1 ]
        xl2 = Xl[ pos + 1 ]
        
        xl = Xl[pos]
        
        dxu = xu2 - xu
        dxl = xl2 - xl
        
        yu2 = Yu[ pos + 1 ]
        yu1 = Yu[ pos ]
        
        yl2 = Yl[ pos + 1 ]
        yl1 = Yl[ pos ]        
        
        dyu = yu2 - yu1
        dyl = yl2 - yl1
        
        theta_u = np.arctan(dyu/dxu)
        theta_l = np.arctan(dyl/dxl)        
        
#        grad_u = np.tan(theta_u)
#        grad_l = np.tan(theta_l)
        grad_u = theta_u
        grad_l = theta_l
        
        ru = ( dxu**2 + dyu**2 )**0.5
        rl = ( dxl**2 + dyl**2 )**0.5
        
        xcu = (ru/2) * np.cos(theta_u)
        ycu = (ru/2) * np.sin(theta_u)
        
        xcl = (rl/2) * np.cos(theta_l)
        ycl = (rl/2) * np.sin(theta_l)
         
        xcu = xu + xcu
        ycu = yu + ycu
        
        xcl = xl + xcl
        ycl = yl + ycl
        
        Xcons_u.append(xcu) # Upper X constraint points coords
        Ycons_u.append(ycu) # Upper Y constraint points coords
        Grad_u.append(grad_u) # Upper constraint points gradients
        
        Xcons_l.append(xcl) # Upper X constraint points coords
        Ycons_l.append(ycl) # Upper Y constraint points coords
        Grad_l.append(grad_l)
        
        Xcons_u2.append(xcu) # Upper X constraint points coords
        Ycons_u2.append(ycu*-1) # Upper Y constraint points coords
        Grad_u2.append(grad_u*-1)
        
        Xcons_l2.append(xcl) # Upper X constraint points coords
        Ycons_l2.append(ycl*-1) # Upper Y constraint points coords
        Grad_l2.append(grad_l*-1)        
    
    pos = Xu.index( Xu[-1] )
    
    # TOP WING LAST TWO VORTICES 
    vu_x = Xcons_u[-2]
    vu_y = Ycons_u[-2]
    
    vl_x = Xcons_l[-2]
    vl_y = Ycons_l[-2]
    
    # BOTTOM WING LAST TWO VORTICES
    vu_x2 = vu_x
    vu_y2 = -1 * vu_y
    
    vl_x2 = vl_x
    vl_y2 = -1 * vl_y
    
    # Remove these vortices for their recpective lists
#    Xu.pop(pos)
#    Yu.pop(pos)
#    
#    Xl.pop(pos)
#    Yl.pop(pos)
#    
#    Xu2.pop(pos)
#    Yu2.pop(pos)
#    
#    Xl2.pop(pos)
#    Yl2.pop(pos)
    
    
    Xcons_u.append(X[-1])    
    Ycons_u.append(hact)
    
    Xcons_u.insert(0,0.0)
    Ycons_u.insert(0,0.4)
    
    
    
    Xcons_u2.append(X[-1])    
    Ycons_u2.append(-1*hact)
    
    Xcons_u2.insert(0,0.0)
    Ycons_u2.insert(0,-0.4)
    
    
    
    #Grad_u.insert(0,1e16)
    Grad_u.append(1.5708)
    Grad_u.insert(0,0.0) #change back t 1.5708 angle at the LE
    
    #Grad_u2.insert(0,-1e16)
    Grad_u2.append(1.5708)
    Grad_u2.insert(0,0.0)
    
#    plt.figure(figsize=(16,12), dpi=400)
#    plt.xlim(-0.05,1.05)
    
#    plt.plot(X,Yc,'b')
#    plt.plot(Xu,Yu,"ro")
#    plt.plot(Xl,Yl,"ro")
#    
#    plt.plot(X,Yc2,'b')
#    plt.plot(Xu2,Yu2,"ro")
#    plt.plot(Xl2,Yl2,"ro")
#    
#    plt.plot(Xcons_u,Ycons_u,'y')
#    plt.plot(Xcons_l,Ycons_l,"g")
#    
#    plt.plot(Xcons_u2,Ycons_u2,'y')
#    plt.plot(Xcons_l2,Ycons_l2,"g")  
#    plt.show()   
    
#    plt.figure(figsize=(16,12), dpi=400)
#    plt.xlim(-0.05,1.05)
#    plt.plot(Xcons_u,Grad_u)    
#    plt.plot(Xcons_l,Grad_l)
#    plt.show()   
    
    
    return (Xu,Yu), (Xl,Yl), (Xcons_u[0:-1],Ycons_u[0:-1]), (Xcons_l,Ycons_l), (Xcons_u,Grad_u[0:-1]), (Xcons_l,Grad_l) \
    ,(vu_x,vu_y),(vl_x,vl_y),(Xu2,Yu2), (Xl2,Yl2), (Xcons_u2[0:-1],Ycons_u2[0:-1]) \
    ,(Xcons_l2,Ycons_l2), (Xcons_u2,Grad_u2[0:-1]), (Xcons_l2,Grad_l2)



def test_run():
    
    a, b, c, d, e, f, u, l ,a2, b2, c2, d2, e2, f2 = NACA("2412",52)#52
    #4412
    x_v1, y_v1 = a
    x_v2, y_v2 = b
    x_c1, y_c1 = c
    x_c2, y_c2 = d
    xc1, gra1 = e
    xc2, gra2 = f
    
    x_vortex = x_v1 + x_v2
#    print(x_vortex)
#    print(len(x_vortex))    
    
    y_vortex = y_v1 + y_v2
#    print(y_vortex)
#    print(len(y_vortex))    
    
    x_point = x_c1 + x_c2
#    print(x_point)
#    print(len(x_point))    
    
    y_point= y_c1 + y_c2
#    print(y_point)
#    print(len(y_point))    
    
    uinf= 30.0
    alpha_v = gra1 + gra2
#    print(alpha_v)
#    print(len(alpha_v)) 
#    
#    print(u)
#    print(l)
    
    
    x2_v1, y2_v1 = a2
    x2_v2, y2_v2 = b2
    x2_c1, y2_c1 = c2
    x2_c2, y2_c2 = d2
    x2c1, gra21 = e2
    x2c2, gra22 = f2
    
    x2_vortex = x2_v1 + x2_v2
#    print(x2_vortex)
#    print(len(x2_vortex))  
    y2_vortex = y2_v1 + y2_v2
#    print(y2_vortex)
#    print(len(y2_vortex)) 
    x2_point = x2_c1 + x2_c2
#    print(x2_point)
#    print(len(x2_point)) 
    y2_point= y2_c1 + y2_c2
    alpha_v2 = gra21 + gra22  
    
    
    return strength_vortex(x_vortex, y_vortex, x_c1, y_c1, x_c2, y_c2, uinf, gra1, gra2,u,l), x_vortex, y_vortex, x_point, y_point, \
    strength_vortex_low(x2_vortex, y2_vortex, x2_c1, y2_c1, x2_c2, y2_c2, uinf, gra21, gra22,u,l), x2_vortex, y2_vortex, x2_point, y2_point

#a,b,c,d,e,a1,b1,c1,d1,e1=test_run()
#print('gamma= ', a)
#print(len(a))
#print('gamma= ', a1)


