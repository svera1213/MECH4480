# -*- coding: utf-8 -*-
"""
Spyder Editor: Santiago Vera 15/08/2018

This is a temporary script file.
"""
import math as m
import numpy as np
import scipy as sp

#==============================================================================
# Velocity contribution constants
#==============================================================================

def u_vel(r,y_A,y_0):
    """Recieves r= distance from vortex to point, y_A= y coordinate of constraint, y_0 = y coordinate of vortex
    Returns the constant of k_A0 = constant_A0 * m_0, m_0 = strength of vortex for constraint A and vortex 0. It changes for each constraint and vortex in the airfoil
    """
    k_A0 = (y_A - y_0)/(2*m.pi*r) 

    return k_A0
    
def v_vel(r,x_A,x_0):
    """Recieves r= distance from vortex to point, x_A= x coordinate of constraint, x_0 = x coordinate of vortex
    Returns the constant of h_A0 = constant_A0 * m_0, m_0 = strength of vortex for constraint A and vortex 0. It changes for each constraint and 
    vortex in the airfoil
    """
    h_A0 = -1*(x_A - x_0)/(2*m.pi*r) 
    
    return h_A0  
    
#==============================================================================
# Airfoil Upper surface total velocity vectors (Normal velocity and Tangential velocity)
#==============================================================================

def vector_vel(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """Recieves coordinates x_A,y_A of the constraints and a pair of vectors with the coordinates x,y of each vortex
    Returns a normal velocity vector Vn of the linear combination of the vector U and vector V as Vn=-U*sin(alpha)+V*cos(alpha) where alpha is the angle 
    from the horizontal at the constraint point
    """
    V_A =[]

    for i in range(len(x_vortex)):
        
        r = (x_A-x_vortex[i])**2 + (y_A-y_vortex[i])**2
        
        V_A.append( (-1 * u_vel(r,y_A,y_vortex[i]) * m.sin(alpha)) + (v_vel(r,x_A,x_vortex[i]) * m.cos(alpha)) )
        

        
    return V_A
    
def vector_vel_t(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """Recieves coordinates x_A,y_A of the constraints and a pair of vectors with the coordinates x,y of each vortex
    Returns a tangential velocity vector Vt of the linear combination of the vector U and vector V as Vt=U*cos(alpha)-V*sin(alpha) where alpha is the angle 
    from the horizontal at the constraint point
    """
    V_A =[]

    for i in range(len(x_vortex)):
        
        r = (x_A-x_vortex[i])**2 + (y_A-y_vortex[i])**2
        
        V_A.append( (u_vel(r,y_A,y_vortex[i]) * m.cos(alpha)) - (v_vel(r,x_A,x_vortex[i]) * m.sin(alpha)) )
        

        
    return V_A
    
#==============================================================================
# Airfoil Lower surface total velocity vectors (Normal velocity and Tangential velocity)
#==============================================================================
    
def vector_vel_low(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """Recieves coordinates x_A,y_A of the constraints and a pair of vectors with the coordinates x,y of each vortex
    Returns a normal velocity vector Vn of the linear combination of the vector U and vector V as Vn=-U*sin(alpha)+V*cos(alpha) where alpha is the angle 
    from the horizontal at the constraint point
    """
    V_A =[]

    for i in range(len(x_vortex)):
        
        r = (x_A-x_vortex[i])**2 + (y_A-y_vortex[i])**2
        
        V_A.append( ( u_vel(r,y_A,y_vortex[i]) * m.sin(alpha)) - (v_vel(r,x_A,x_vortex[i]) * m.cos(alpha)) )
        

        
    return V_A

def vector_vel_low_t(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """Recieves coordinates x_A,y_A of the constraints and a pair of vectors with the coordinates x,y of each vortex
    Returns a tangential velocity vector Vt of the linear combination of the vector U and vector V as Vt=-U*cos(alpha)-V*sin(alpha) where alpha is the angle 
    from the horizontal at the constraint point
    """
    V_A =[]

    for i in range(len(x_vortex)):
        
        r = (x_A-x_vortex[i])**2 + (y_A-y_vortex[i])**2
        
        V_A.append( ( -1 * u_vel(r,y_A,y_vortex[i]) * m.cos(alpha)) - (v_vel(r,x_A,x_vortex[i]) * m.sin(alpha)) )
        

        
    return V_A
    
#==============================================================================
# Near trailing edge tangential velocity constraint Vt=0
#==============================================================================
    
def vector_vel_T(x_A,y_A,x_vortex,y_vortex,uinf,alpha):
    """Recieves coordinates x_A,y_A of the near trailing edge constraints and a pair of vectors with the coordinates x,y of each vortex
    Returns a tangential velocity vector Vt of the linear combination of the vector U and vector V as Vt=U*cos(alpha)-V*sin(alpha) where alpha is the angle 
    from the horizontal at the constraint point
    """
    V_t =[]
    
    for i in range(len(x_vortex)):
        
        r = (x_A - x_vortex[i])**2 + (y_A - y_vortex[i])**2
        
        V_t.append( u_vel(r, y_A, y_vortex[i]) * m.cos(alpha) + v_vel(r, x_A, x_vortex[i]) * m.sin(alpha) )
        
    return V_t
    
#==============================================================================
# Uniform flow contribution vector for Upper and Lower surface
#==============================================================================

def uinf_v(uinf, alpha_up, alpha_low):
    """Recieves uniform flow velocity uinf and vector of alpha angles of each constrain point 
    Returns a vector of flow velocity component for different alphas to set up matrix A*x=b
    """
    U_inf=[]
    

    N_up = len(alpha_up)
    N_low = len(alpha_low)
    
    #Calculate b vector for upper surface except constraint near trailing edge
    for i in range(N_up - 1):
        U_inf.append(uinf*m.sin(alpha_up[i]))
    
    #Calculate b for upper surface constraint near trailing edge 
    U_inf.append(-1*uinf*m.cos(alpha_up[N_up - 1]))
    
    #Calculate b vector for lower surface except constraint near trailing edge
    for i in range(N_low - 1):
        U_inf.append(-1*uinf*m.sin(alpha_low[i])) 
    
    #Calculate b for lower surface constraint near trailing edge   
    U_inf.append(uinf*m.cos(alpha_low[N_low - 1]))     
    
    #Calculate b for constraint at trailing edge 
    U_inf.append(-uinf*m.cos(0))

    return U_inf

#==============================================================================
# Velocity vector matrix Upper airfoil
#==============================================================================

def matrix_vel(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_low, uinf, alpha_up, alpha_low):
    """Builds a matrix of velocity contributions of size NxN given a vector of coordinates of the vortex, coordinates of constraint point, velocity of fluid uinf
    and vector of alpha gradients of each constraint point. 
    Returns the matrix of velocities as a list of lists V_N
    """
    V_N =[]

    
    N_up = len(x_point_up)
    N_low = len(x_point_low)   
    
    #Calculate vectors of the upper surface
    for i in range(N_up - 1):
        V_N.append(vector_vel(x_point_up[i], y_point_up[i], x_vortex, y_vortex , uinf, alpha_up[i]))
    
    #Calculate vector for the constraint on the upper surface near the trailing edge
    V_N.append(vector_vel_t(x_point_up[N_up - 1], y_point_up[N_up - 1], x_vortex, y_vortex , uinf, alpha_up[N_up - 1]))
    
    
    #Calculate vectors of the lower surface
    for i in range(N_low - 1):
        V_N.append(vector_vel_low(x_point_low[i], y_point_low[i], x_vortex, y_vortex , uinf, alpha_low[i]))
    
    #Calculate vector for the constraint on the lower surface near the trailing edge
    V_N.append(vector_vel_low_t(x_point_low[N_low - 1], y_point_low[N_low - 1], x_vortex, y_vortex , uinf, alpha_low[N_low - 1]))
    

    #Calculate vector for the constraint at the trailing edge
    V_N.append(vector_vel_T(1.0 , 0.4, x_vortex, y_vortex , uinf, 0.0))
    

    return V_N
    
#==============================================================================
# Velocity vector matrix Lower airfoil - Ground effect
#==============================================================================
    
def matrix_vel_low(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_low, uinf, alpha_up, alpha_low):
    """Builds a matrix of velocities of size NxN given a vector of coordinates of the vortex, coordinates of constraint point, velocity of fluid uinf
    and vector of alpha gradients of each constraint point. 
    Returns the matrix of velocities as a list of lists V_N
    """
    V_N =[]

    
    N_up = len(x_point_up)
    N_low = len(x_point_low)   
    
    #Calculate vectors of the lower surface
    for i in range(N_up - 1):
        V_N.append(vector_vel(x_point_up[i], y_point_up[i], x_vortex, y_vortex , uinf, alpha_up[i]))
    
    #Calculate vector for the constraint on the lower surface near the trailing edge
    V_N.append(vector_vel_t(x_point_up[N_up - 1], y_point_up[N_up - 1], x_vortex, y_vortex , uinf, alpha_up[N_up - 1]))
    
    
    #Calculate vectors of the upper surface
    for i in range(N_low - 1):
        V_N.append(vector_vel_low(x_point_low[i], y_point_low[i], x_vortex, y_vortex , uinf, alpha_low[i]))
    
    #Calculate vector for the constraint on the upper surface near the trailing edge
    V_N.append(vector_vel_low_t(x_point_low[N_low - 1], y_point_low[N_low - 1], x_vortex, y_vortex , uinf, alpha_low[N_low - 1]))
    

    #Calculate vector for the constraint at the trailing edge
    V_N.append(vector_vel_T(1.0 , -0.4, x_vortex, y_vortex , uinf, 0.0))
    

    return V_N
    
#==============================================================================
# Vortex strenght calculator Upper wing
#==============================================================================

def strength_vortex(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_los, uinf, alpha_up, alpha_low, vortex_end, vortex_start):
    """Calculates the vortex strength for each vortex applied on the airfoil given the coordinates of all the vortex positions, constraint points and 
    alpha gradients for each point, and the flow velocity uinf
    Solve A*x=b matrix 
    """
  
    vortex_s = np.linalg.solve( matrix_vel(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_los, uinf, alpha_up, alpha_low), uinf_v(uinf, alpha_up, alpha_low))

    

    return vortex_s
    

#==============================================================================
# Vortex strenght calculator Lower wing- Ground effect
#==============================================================================
def strength_vortex_low(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_los, uinf, alpha_up, alpha_low, vortex_end, vortex_start):
    """Calculates the vortex strength for each vortex applied on the airfoil given the coordinates of all the vortex positions, constraint points and 
    alpha gradients for each point, and the flow velocity uinf
    Solve A*x=b matrix 
    """
    
    vortex_s = np.linalg.solve( matrix_vel_low(x_vortex, y_vortex, x_point_up, y_point_up, x_point_low, y_point_los, uinf, alpha_up, alpha_low), uinf_v(uinf, alpha_up, alpha_low))

    

    return vortex_s
        
        
    

    