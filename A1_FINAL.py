"""
Template input file for HX_solver.py
""" 

from Airfoil_profile_FINAL import test_run

# set model parameters
"""
Set parameters that define model conditions (optional)
mdata.Pinf     - (defualt = 0 Pa)        sets P-infinity used in calculations
mdata.rho      - (default = 1.225 kg/s)  sets density used for calculations
mdata.Uinf     - (default = np.nan m/s)      sets U-infinity used in calculations. 
                        If NaN this will be calculated automatically. 
"""
mdata.name = 'Vortex + Uniform Flow adjacent to a wall'
mdata.dimensions = 2

# Define the Building Blocks 
"""
The following is a short summary of the supported components. See the User-Guide 
for more detailed instructions and detailed definition.

A = UniformFlow(Vx,Vy,label='UFlow1')
--> creates an uniform with velocity magnitude and direction defined by the 
        x and y components Vx and Vy

B = Vortex(Cx,Cy,K=K,label='Vortex1')
--> creates a irrotational vortex located at (Cx, Cy) with a strength 
        K = Gamma / (2 * pi). A positive Gamma results in a vortex rotating in 
        the anticlockwise direction.

B = Vortex(Cx,Cy,Gamma=Gamma,label='Vortex1')
--> creates an irrotational vortex located at (Cx, Cy) with a strength Gamma. A 
        positive K results in a vortex rotating in the anticlockwise direction.

C = Source(Cx,Cy,m,label='Source1')
--> creates a source/sink located at (Cx,Cy). m is the mass flow rate (per unit 
        depth) coming out of the source. Use +ve m for source and -ve m for sinks

D = Doublet(Cx,Cy,R,Uinf,label='Doublet1')
--> creates a doublet (co-located source and sink) located at (Cx, Cy). R sets 
        the radius of the enclosing streamline that is generated. When used in 
        conjunction with a uniform flow to show the flow around a cylinder, set 
        Ux and Uy to match the x and y components of the uniform flow.

E = User_Defined(Cx,Cy,n,label='user1')
--> Secret. Try it out and see if you can work out what it is.  

"""

# Uniform Flows  
A1 = UniformFlow(30.,0.)



Gamma, X_v, Y_v, X_c, Y_c, Gamma2, X2_v, Y2_v, X2_c, Y2_c = test_run()

N =len(X_v) 
X = []
X.append(A1)
for i in range(N):
    X.append(Vortex(X_v[i],Y_v[i],Gamma = Gamma[i]))
 
   
X2 = []
for i in range(N):
    X2.append(Vortex(X2_v[i],Y2_v[i],Gamma = Gamma2[i]))



# Define how the solution will be visualised. 
"""
By use the following settings to adjust the visaulisation.
---- Define plotting Window -----
visual.xmin     - (default = -1.) sets x_min for plots
visual.xmax     - (default =  1.) sets x_max for plots
visual.ymin     - (default = -1.) sets y_min for plots
visual.ymax     - (default =  1.) sets y_max for plots
visual.Nx       - (default = 50) number of points used for discretisation 
                                in x-direction
visual.Ny       - (default = 50) number of points used for discretisation 
                                in x-direction
visual.subplot  - (default = 0)  0 - all individual graphs; 1 - subplots in 
                                single figure 

---- Define what is plotted ----
plot.psi(levels=20) - plots 'real' streamlines, contours of psi. Use levels to 
                        set number of contours.
plot.psi_magU(min=[], max=[], levels=20) - create contour plot of velocity 
                        magnitude with overlaid stream functions. Use min and 
                        max to specify range and levels sets numbers of contours.
plot.vectors()  - plots nice looking streamlines. Note these are not 
                        euqipotentials of psi.
plot.vectors_magU(min=[], max=[], levels=20) - create contour plot of velocity 
                        magnitude with overlaid velocity vectors. Use min and 
                        max to specify range and levels sets numbers of contours.
plot.magU(min=[], max=[], levels=20) - create contour plot of velocity magnitude. 
                        Use min and max to specify range and levels sets numbers 
                        of contours.
plot.U(min=[], max=[], levels=20) - create contour plot of U velocity. Use min 
                        and max to specify range and levels sets numbers of contours.
plot.V(min=[], max=[], levels=20) - create contour plot of V velocity. Use min 
                        and max to specify range and levels sets numbers of contours.
plot.P(P_inf=0., rho=1.225, min=[], max=[], levels=20) - create contour plot of 
                        pressure, using P_inf and rho to perform the calculation. 
                        P = P_inf - 1/2 * rho * magU**2. Use min and max to 
                        specify range and levels sets numbers of contours.
plot.Cp(U_inf=1., rho=1.225, min=[], max=[]) - create contorus of pressure 
                        coefficient Cp, using U_inf and rho to perform the 
                        calculation.
                        Cp = P / ( 1/2 * rho * U_inf**2 )
"""

visual.xmin=-1.
visual.xmax =2.
visual.Nx = 200
visual.Ny = 200
visual.subplot = 0

plot.psi(levels = 50)
plot.vectors_magU(min=0., max=1500.)
plot.P(min=-1500, max=1500)


# Define what is printed to screen
"""
---- Define what is displayed ----
screen.variables(['Psi','magU','U','V','P','Cp'])  - provide list of parameters that 
                        will be evaluated. (default ['Psi','P', 'magU'])
screen.locations([ [x0,y0], [x1,y1], [x2,y2], ...] ) - provide list of points 
                        where to evaluate data
screen.Lineval([x0,y0], [x1,y1], N=5)     - evaluates conditions at N equally 
                        spaced points between (x0,y0) and (x1,y1)
"""

screen.variables(['Psi', 'U', 'V', 'P']) 
screen.Lineval([-2.0,0.0], [2.0,0.0], N=19) 

loc_top = []
loc_bottom = []
for i in range(len(X_c)):
    if i == 0:
        loc_top.append([X_c[i],Y_c[i]])        
        loc_bottom.append([X_c[i],Y_c[i]])        
    elif i % 2 == 0:
        loc_bottom.append([X_c[i],Y_c[i]])
    else:
        loc_top.append([X_c[i],Y_c[i]])    

screen.locations(loc_top)
screen.locations(loc_bottom)

