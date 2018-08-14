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
    
    #hact = 15 + h # Height from bottom of box to reference
    #hact = hact/100
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
    print(X)
    Yc = [] # Camber vertical coords
    #Yt = []
    Yc2 = []    
    
    Upper = []
    Lower = []
    
    Upper2 = []
    Lower2 = []    
    
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
        #Yt.append(yt)
        
        if x < p:
            yc = hact + (m/p**2) * (2*p*x - x**2)
            Yc.append(yc)
            Yc2.append(yc*-1)
            #g = (2*m/p**2) * (p-x)
            #G.append(g)
            
        else:
            yc = hact + (m/(1-p)**2) * (1 - 2*p + 2*p*x - x**2)
            Yc.append(yc)
            Yc2.append(yc*-1)
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
        
        Upper2.append(up*-1)
        Lower2.append(low*-1)
#    print(Upper)
#    print(Lower)    
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
        
    
    for x in X[1:-1]: #change back to X[0:-1]
        
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
        
        Xcons_u2.append(xu) # Upper X constraint points coords
        Ycons_u2.append(yu*-1) # Upper Y constraint points coords
        Grad_u2.append(grad_u*-1)        
        
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
        
        Xcons_l2.append(xl) # Upper X constraint points coords
        Ycons_l2.append(yl*-1) # Upper Y constraint points coords
        Grad_l2.append(grad_l*-1)
    
    Grad_u.insert(0,1.5708)
    
    Lower = Lower[1:-1]
    Lower2 = Lower2[1:-1]
    
    Xcons_u = Xcons_u[0:-1]
    Xcons_u.append( X[-1] )

    Xcons_u.insert(0,0.0)   #delete
    
    Xcons_u2 = Xcons_u2[0:-1]
    Xcons_u2.append( X[-1] )    
    
    Ycons_u = Ycons_u[0:-1]

    Ycons_u.append( Yc[-1] )
    
    Ycons_u.insert(0,0.4) #delete      
    
    Ycons_u2 = Ycons_u2[0:-1]
    Ycons_u2.append( Yc2[-1] )
    
    #Doublet coordinates
    du_x = X[-2]
    du_y = (Upper[-2] + Lower[-1]) / 2
    du_y2 = (Upper2[-2] + Lower2[-1]) / 2
    
#==============================================================================
#     
#==============================================================================
   
#    plt.figure(figsize=(16,10), dpi=400) # Print figure in larger size
#    plt.plot(X,[0]*len(X),'--')    
#    plt.plot(X,Yc, 'b') # Plot of camber line
#    plt.plot(X[0:-1], Upper[0:-1], 'ro')
#    plt.plot(X[1:-1], Lower, 'ro')
#    #plt.plot(Xu, Yu, 'ro')
#    #plt.plot(Xl, Yl, 'ro')
#    plt.plot( Xcons_u ,Ycons_u,'g')
#    plt.plot( Xcons_l[0:-1] ,Ycons_l[0:-1],'y')
#    plt.xlim(-0.1,1.1)  
   
   
#    #Lower wing plotting:
#    plt.plot(X,Yc2)  
#    plt.plot(X[0:-1], Upper2[0:-1], 'ro')
#    plt.plot(X[1:-1], Lower2, 'ro')
#    plt.plot( Xcons_u2 ,Ycons_u2,'g')
#    plt.plot( Xcons_l2[0:-1] ,Ycons_l2[0:-1],'y')
#    #plt.show()
#    
#    #Doublet points
#    plt.plot(du_x,du_y,'bo')
#    plt.plot(du_x,du_y2,'bo')
#    plt.show()
#==============================================================================
#     print(len(X[0:-1]))
#     print(len(X[1:-1]))
#     print(len(Xcons_u))
#     print(len(Xcons_l[0:-1]))
#==============================================================================
# =============================================================================
#     plt.plot(Xcons_u,Grad_u)
#     plt.plot(Xcons_l,Grad_l)
#     plt.show()
# =============================================================================
    a= (X[1:-2],Upper[1:-2])
    b= (X[1:-2],Lower[0:-1])
    c= (Xcons_u[0:-1],Ycons_u[0:-1])
    d= (Xcons_l[0:-1],Ycons_l[0:-1])
    e= (Xcons_u,Grad_u)
    f= (Xcons_l[0:-1],Grad_l[0:-2])
    vortex1= (X[-2],Upper[-2])
    vortex2= (X[-2],Lower[-1])
#    a2=
#    b2=
#    c2=
#    d2=
#    e2=
#    f2=
#    dx=
#    dy=

    return a,b,c,d,e,f,vortex1,vortex2 ,(X[0:-1],Upper2[0:-1]), (X[1:-1],Lower2), (Xcons_u2,Ycons_u2), (Xcons_l2[0:-1],Ycons_l2[0:-1]), (Xcons_u2,Grad_u2), (Xcons_l2[0:-1],Grad_l2[0:-1]),du_x,du_y

def test_run():
    
    a, b, c, d, e, f, vortex1, vortex2, a2, b2, c2, d2, e2, f2, dx, dy = NACA(4412,52)
    #4412
    x_v1,y_v1 = a

    x_v2,y_v2 = b
    x_c1,y_c1 = c
    x_c2,y_c2 = d
    xc1,gra1 = e
    xc2,gra2 = f
    
    x_vortex = x_v1+x_v2
#    print(x_vortex)
#    print(len(x_vortex))
    
    y_vortex = y_v1+y_v2
#    print(y_vortex)
#    print(len(y_vortex))
    
    x_point = x_c1 + x_c2
#    print(x_point)
#    print(len(x_point))
    
    y_point= y_c1 + y_c2
#    print(y_point)
#    print(len(y_point))
#    
#    print(vortex1)
#    print(vortex2)

    
    uinf= 30.0
    
    alpha_v = gra1 +gra2
#    print(alpha_v)
#    print(len(alpha_v))
    
    x2_v1,y2_v1 = a2
    x2_v2,y2_v2 = b2
    x2_c1,y2_c1 = c2
    x2_c2,y2_c2 = d2
    x2c1,gra21 = e2
    x2c2,gra22 = f2
    
    x2_vortex = x2_v1+x2_v2
    y2_vortex = y2_v1+y2_v2
    x2_point = x2_c1 + x2_c2
    y2_point= y2_c1 + y2_c2
    alpha_v2 = gra21 +gra22
    
    
    return strength_vortex(x_vortex, y_vortex, x_point, y_point, uinf, alpha_v, vortex1, vortex2), x_vortex, y_vortex, x_point, y_point#, strength_vortex(x2_vortex, y2_vortex, x2_point, y2_point, uinf, alpha_v2), x2_vortex, y2_vortex, x2_point, y2_point,dx,dy

#a,b,c,d,e,a2,b2,c2,d2,e2,dx,dy=test_run()
#a,b,c,d,e = test_run()
#print('vortex=  ',a)
#print('# de vortex = ',len(a))
#print(c)
#print(d)
#print(e)
#print(a)





