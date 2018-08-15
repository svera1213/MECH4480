# -*- coding: utf-8 -*-
"""
Spyder Editor: Santiago Vera 15/08/2018

This is a temporary script file.
"""
import math as m
import numpy as np
import scipy as sp

#==============================================================================
# 
#==============================================================================

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
    
#==============================================================================
# 
#==============================================================================

def vector_vel(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """Recieves coordinates x_A,y_A of the constraints and a pair of vectors with the coordinates x,y of each vortex
    Returns a vector Vn of the linear combination of the vector U and vector V as Vn=-U*sin(alpha)+V*cos(alpha) where alpha is the gradient at the constraint point
    """
    V_A =[]

    for i in range(len(x_vortex)):
        
        r = (x_A-x_vortex[i])**2 + (y_A-y_vortex[i])**2
        
        V_A.append( (-1 * u_vel(r,y_A,y_vortex[i]) * m.sin(alpha)) + (v_vel(r,x_A,x_vortex[i]) * m.cos(alpha)) )
        
#    V_A.append(0)
        
    return V_A
    
def vector_vel_t(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """Recieves coordinates x_A,y_A of the constraints and a pair of vectors with the coordinates x,y of each vortex
    Returns a vector Vn of the linear combination of the vector U and vector V as Vn=-U*sin(alpha)+V*cos(alpha) where alpha is the gradient at the constraint point
    """
    V_A =[]

    for i in range(len(x_vortex)):
        
        r = (x_A-x_vortex[i])**2 + (y_A-y_vortex[i])**2
        
        V_A.append( (u_vel(r,y_A,y_vortex[i]) * m.cos(alpha)) - (v_vel(r,x_A,x_vortex[i]) * m.sin(alpha)) )
        
#    V_A.append(0)
        
    return V_A
    
#==============================================================================
# 
#==============================================================================
    
def vector_vel_low(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """Recieves coordinates x_A,y_A of the constraints and a pair of vectors with the coordinates x,y of each vortex
    Returns a vector Vn of the linear combination of the vector U and vector V as Vn=-U*sin(alpha)+V*cos(alpha) where alpha is the gradient at the constraint point
    """
    V_A =[]

    for i in range(len(x_vortex)):
        
        r = (x_A-x_vortex[i])**2 + (y_A-y_vortex[i])**2
        
        V_A.append( ( u_vel(r,y_A,y_vortex[i]) * m.sin(alpha)) - (v_vel(r,x_A,x_vortex[i]) * m.cos(alpha)) )
        
#    V_A.append(0)
        
    return V_A

def vector_vel_low_t(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """Recieves coordinates x_A,y_A of the constraints and a pair of vectors with the coordinates x,y of each vortex
    Returns a vector Vn of the linear combination of the vector U and vector V as Vn=-U*sin(alpha)+V*cos(alpha) where alpha is the gradient at the constraint point
    """
    V_A =[]

    for i in range(len(x_vortex)):
        
        r = (x_A-x_vortex[i])**2 + (y_A-y_vortex[i])**2
        
        V_A.append( ( -1 * u_vel(r,y_A,y_vortex[i]) * m.cos(alpha)) - (v_vel(r,x_A,x_vortex[i]) * m.sin(alpha)) )
        
#    V_A.append(0)
        
    return V_A
    
#==============================================================================
# 
#==============================================================================
    
def vector_vel_T(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """
    """
    V_t =[]
    
    for i in range(len(x_vortex)):
        
        r = (x_A - x_vortex[i])**2 + (y_A - y_vortex[i])**2
        
        V_t.append( u_vel(r, y_A, y_vortex[i]) * m.cos(alpha) + v_vel(r, x_A, x_vortex[i]) * m.sin(alpha) )
        
    return V_t
    
#==============================================================================
# 
#==============================================================================

def uinf_v(uinf, alpha_up, alpha_low):
    """Recieves flow velocity uinf and vector of alpha gradients of each constrain point 
    Returns a vector of flow velocity component for different alphas to set up matrix A*x=b
    """
    U_inf=[]
    
    N_up = len(alpha_up)
    N_low = len(alpha_low)
    
    for i in range(N_up - 1):
        U_inf.append(uinf*m.sin(alpha_up[i]))
        
    U_inf.append(-1*uinf*m.cos(alpha_up[N_up - 1]))
    
    for i in range(N_low - 1):
        U_inf.append(-1*uinf*m.sin(alpha_low[i])) 
        
    U_inf.append(uinf*m.cos(alpha_low[N_low - 1]))     
    
    U_inf.append(-uinf*m.cos(0))
#    U_inf.append(0)
#    print(U_inf)
    return U_inf

#==============================================================================
# 
#==============================================================================

def matrix_vel(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_low, uinf, alpha_up, alpha_low):
    """Builds a matrix of velocities of size NxN given a vector of coordinates of the vortex, coordinates of constraint point, velocity of fluid uinf
    and vector of alpha gradients of each constraint point. 
    Returns the matrix of velocities as a list of lists V_N
    """
    V_N =[]
#    zeros = [0]*(len(x_vortex)-2)
    
    N_up = len(x_point_up)
    N_low = len(x_point_low)   
    
    
    for i in range(N_up - 1):
        V_N.append(vector_vel(x_point_up[i], y_point_up[i], x_vortex, y_vortex , uinf, alpha_up[i]))
    
    V_N.append(vector_vel_t(x_point_up[N_up - 1], y_point_up[N_up - 1], x_vortex, y_vortex , uinf, alpha_up[N_up - 1]))
    
    for i in range(N_low - 1):
        V_N.append(vector_vel_low(x_point_low[i], y_point_low[i], x_vortex, y_vortex , uinf, alpha_low[i]))
    
    V_N.append(vector_vel_low_t(x_point_low[N_low - 1], y_point_low[N_low - 1], x_vortex, y_vortex , uinf, alpha_low[N_low - 1]))
    

    
    V_N.append(vector_vel_T(1.0 , 0.4, x_vortex, y_vortex , uinf, 0.0))
    

    return V_N
    
def matrix_vel_low(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_low, uinf, alpha_up, alpha_low):
    """Builds a matrix of velocities of size NxN given a vector of coordinates of the vortex, coordinates of constraint point, velocity of fluid uinf
    and vector of alpha gradients of each constraint point. 
    Returns the matrix of velocities as a list of lists V_N
    """
    V_N =[]

    
    N_up = len(x_point_up)
    N_low = len(x_point_low)   
    
    
    for i in range(N_up - 1):
        V_N.append(vector_vel(x_point_up[i], y_point_up[i], x_vortex, y_vortex , uinf, alpha_up[i]))
    
    V_N.append(vector_vel_t(x_point_up[N_up - 1], y_point_up[N_up - 1], x_vortex, y_vortex , uinf, alpha_up[N_up - 1]))
    
    for i in range(N_low - 1):
        V_N.append(vector_vel_low(x_point_low[i], y_point_low[i], x_vortex, y_vortex , uinf, alpha_low[i]))
    
    V_N.append(vector_vel_low_t(x_point_low[N_low - 1], y_point_low[N_low - 1], x_vortex, y_vortex , uinf, alpha_low[N_low - 1]))
    

    
    V_N.append(vector_vel_T(1.0 , -0.4, x_vortex, y_vortex , uinf, 0.0))
    

    return V_N
    
#==============================================================================
# 
#==============================================================================

def strength_vortex(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_los, uinf, alpha_up, alpha_low, vortex_end, vortex_start):
    """Calculates the vortex strength for each vortex applied on the airfoil given the coordinates of all the vortex positions, constraint points and 
    alpha gradients for each point, and the flow velocity uinf
    """
  
    inv_matrix = np.linalg.inv(matrix_vel(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_los, uinf, alpha_up, alpha_low))
    vortex_s = np.linalg.solve( matrix_vel(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_los, uinf, alpha_up, alpha_low), uinf_v(uinf, alpha_up, alpha_low))

    

    return vortex_s
    

def strength_vortex_low(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_los, uinf, alpha_up, alpha_low, vortex_end, vortex_start):
    """Calculates the vortex strength for each vortex applied on the airfoil given the coordinates of all the vortex positions, constraint points and 
    alpha gradients for each point, and the flow velocity uinf
    """


    
    
    inv_matrix = np.linalg.inv(matrix_vel_low(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_los, uinf, alpha_up, alpha_low))
    vortex_s = np.linalg.solve( matrix_vel_low(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_los, uinf, alpha_up, alpha_low), uinf_v(uinf, alpha_up, alpha_low))

    

    return vortex_s
        
        
    

    