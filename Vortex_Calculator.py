# -*- coding: utf-8 -*-
"""
Spyder Editor: Santiago Vera 10/08/2018

This is a temporary script file.
"""
import math as m
import numpy as np
import scipy as sp

def u_vel(r,y_A,y_0):
    """Recieves r= distance from source to point, y_A= coordinate of constraint, y_0 = coordinate of vortex
    Returns the constant of u_A0 = constant_A0 * m_0, m_0 = strength of vortex
    """
    k_A0 = (y_A - y_0)/(2*m.pi*r) 

    return k_A0
    
def v_vel(r,x_A,x_0):
    """Recieves r= distance from vortex to point, y_A= coordinate of constraint, y_0 = coordinate of vortex
    Returns the constant of u_A0 = constant_A0 * m_0, m_0 = strength of vortex
    """
    h_A0 = -1*(x_A - x_0)/(2*m.pi*r) 
    
    return h_A0  

def vector_vel(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """Recieves coordinates x_A,y_A of the constraints and a pair of vectors with the coordinates x,y of each vortex
    Returns a vector Vn of the linear combination of the vector U and vector V as Vn=-U*sin(alpha)+V*cos(alpha) where alpha is the gradient at the constraint point
    """
    V_A =[]

    for i in range(len(x_vortex)):
        
        r = (x_A-x_vortex[i])**2 + (y_A-y_vortex[i])**2
        
        V_A.append( -1 * u_vel(r,y_A,y_vortex[i]) * m.sin(alpha) + v_vel(r,x_A,x_vortex[i]) * m.cos(alpha) )
        
#    V_A.append(0)
        
    return V_A

def uinf_v(uinf, alpha_v):
    """Recieves flow velocity uinf and vector of alpha gradients of each constrain point 
    Returns a vector of flow velocity component for different alphas to set up matrix A*x=b
    """
    U_inf=[]
    for i in range(len(alpha_v)):
        U_inf.append(uinf*m.sin(alpha_v[i]))
#    U_inf.append(0)
#    print(U_inf)
    return U_inf

def matrix_vel(x_vortex, y_vortex, x_point, y_point, uinf, alpha_v):
    """Builds a matrix of velocities of size NxN given a vector of coordinates of the vortex, coordinates of constraint point, velocity of fluid uinf
    and vector of alpha gradients of each constraint point. 
    Returns the matrix of velocities as a list of lists V_N
    """
    V_N =[]
    
    for i in range(len(x_vortex)):
        V_N.append(vector_vel(x_point[i], y_point[i], x_vortex, y_vortex , uinf, alpha_v[i]))
    
#    kutta_v=[1]
#    for i in range(2,len(V_N[0])):
#        kutta_v.append(0)
#    kutta_v.append(1)
#    V_N.append(kutta_v)
    

    return V_N

def strength_vortex(x_vortex, y_vortex, x_point, y_point, uinf, alpha_v):
    """Calculates the vortex strength for each vortex applied on the airfoil given the coordinates of all the vortex positions, constraint points and 
    alpha gradients for each point, and the flow velocity uinf
    """
#    v =[]
#    A = matrix_vel(x_vortex, y_vortex, x_point, y_point, uinf, alpha_v)
#    B = uinf_v(uinf, alpha_v)
#    LU = sp.linalg.lu_factor(A)
#    x = sp.linalg.lu_solve(LU,B)
    inv_matrix = np.linalg.inv(matrix_vel(x_vortex, y_vortex, x_point, y_point, uinf, alpha_v))
    vortex_s = np.linalg.solve( matrix_vel(x_vortex, y_vortex, x_point, y_point, uinf, alpha_v), uinf_v(uinf, alpha_v))

    
#    for i in range(len(vortex_s)):
#        v.append(vortex_s[i])
    return vortex_s
    

#test=strength_vortex([0, 0.13477, 0.501174, 0.855503, 1.0, 0.851604, 0.498826, 0.153123],[0, 0.076589, 0.091737, 0.036484, 0, -0.002197, -0.01396, -0.0028733],[0.032437, 0.305921, 0.693744, 0.946424, 0.944583, 0.688933, 0.311395, 0.043684],[0.038325, 0.09784, 0.06768, 0.014531, -0.000659, -0.006542, -0.022012, -0.023825], 30.0, [0.1837815 \
#,0.0470395, -0.146872, -0.273212, -0.2722915, -0.1444665, 0.0443025, 0.1781555])
#print(test) 


#x_vortex = [0.0, 0.49999999999999994, 1.0, 0.49999999999999994]
#y_vortex = [0.0, 0.091750390889460465, -1.6653345369377347e-17, -0.0139726131116827]
#
#x_point = [0.25, 0.75, 0.24999999999999997, 0.74999999999999989]
#y_point = [0.045875195444730232, 0.045875195444730232, -0.0069863065558413507, -0.0069863065558413403]
#
#alpha_v = [0.18350078177892096, -0.18350078177892096, 0.027945226223365403, -0.027945226223365434]
#
#uinf= 30.0
#
#test = strength_vortex(x_vortex, y_vortex, x_point, y_point, uinf, alpha_v)
#print(test)
        
        
        
    

    