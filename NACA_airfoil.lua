-- NACAstart.lua
-- Simple job-specification for a NACA aerofoil mesh
-- IJ, 20-Aug-2017

--job_title = "NACA aerofoil example"
--print(job_title)

--*********************ADD ASSIGNMENT AIRFOIL HERE************************


--************************************************************************

-- define points along NACA profile
C = 1.0   -- set chord length
t = 12    -- set thickness as a percentage of chord length. E.g. 12 = 12% thickness

-- top edge coordinates
A2 = Vector3:new{x=0.0 * C, y=0.0 *t}
t01 = Vector3:new{x=0.005 * C, y=0.0010 *t}
t02 = Vector3:new{x=0.018 * C, y=0.0019 *t}
t03 = Vector3:new{x=0.04 * C, y=0.0027 *t}
t04 = Vector3:new{x=0.06 * C, y=0.0032 *t}
t05 = Vector3:new{x=0.09 * C, y=0.0038 *t}
t06 = Vector3:new{x=0.12 * C, y=0.0042 *t}
t07 = Vector3:new{x=0.16 * C, y=0.0045 *t}
t08 = Vector3:new{x=0.20 * C, y=0.0048 *t}
t09 = Vector3:new{x=0.25 * C, y=0.0050 *t}
A1 = Vector3:new{x=0.30 * C, y=0.0050 *t}
t11 = Vector3:new{x=0.40 * C, y=0.0048 *t}
t12 = Vector3:new{x=0.50 * C, y=0.0044 *t}
t13 = Vector3:new{x=0.60 * C, y=0.0038 *t}
t14 = Vector3:new{x=0.70 * C, y=0.0030 *t}
t15 = Vector3:new{x=0.80 * C, y=0.0021 *t}
t16 = Vector3:new{x=0.90 * C, y=0.0011 *t}
A0 = Vector3:new{x=1.00 * C, y=0.0 *t}

-- bottom edge coordinates
-- A2 = Vector3:new{x=0.0 * C, y=0.0 *t}
b01 = Vector3:new{x=0.005 * C, y=-0.0010 *t}
b02 = Vector3:new{x=0.018 * C, y=-0.0019 *t}
b03 = Vector3:new{x=0.04 * C, y=-0.0027 *t}
b04 = Vector3:new{x=0.06 * C, y=-0.0032 *t}
b05 = Vector3:new{x=0.09 * C, y=-0.0038 *t}
b06 = Vector3:new{x=0.12 * C, y=-0.0042 *t}
b07 = Vector3:new{x=0.16 * C, y=-0.0045 *t}
b08 = Vector3:new{x=0.20 * C, y=-0.0048 *t}
b09 = Vector3:new{x=0.25 * C, y=-0.0050 *t}
A3 = Vector3:new{x=0.30 * C, y=-0.0050 *t}
b11 = Vector3:new{x=0.40 * C, y=-0.0048 *t}
b12 = Vector3:new{x=0.50 * C, y=-0.0044 *t}
b13 = Vector3:new{x=0.60 * C, y=-0.0038 *t}
b14 = Vector3:new{x=0.70 * C, y=-0.0030 *t}
b15 = Vector3:new{x=0.80 * C, y=-0.0021 *t}
b16 = Vector3:new{x=0.90 * C, y=-0.0011 *t}
A4 = Vector3:new{x=1.00 * C, y=-0.0 *t}

-- Create lines that form aerofoil profile
a1a0 = Spline:new{points={A1,t11,t12,t13,t14,t15,t16,A0}}
a2a1 = Spline:new{points={A2,t01,t02,t03,t04,t05,t06,t07,t08,t09,A1}}
a3a2 = Spline:new{points={A3,b09,b08,b07,b06,b05,b04,b03,b02,b01,A2}}
a4a3 = Spline:new{points={A4,b16,b15,b14,b13,b12,b11,A3}}

-- The following code can be use to show just the aerofoil. 
-- I.e. it generates a block inside the aerofoil. Uncomment this if you want to show just the aerofoil. Use at your own peril.
-- a3a4 = ReversedPath:new{underlying path=a4a3}
-- a2a3 = ReversedPath:new{underlying path=a3a2}
-- internal_surface = CoonsPatch:new{south=a2a3, north=a1a0, west=a2a1, east=a3a4}:
-- grid_aerofoil = StructuredGrdi:new{psurface=internal_surface, niv=20, njv=21}
-- grid_aerofoil.write_to_vtk_file("aerofoil_internal.vtk")


-- ############################################################
-- ############################################################
-- Start adding your code to build the external mesh here....

--Vertices
BL = 0.1
B0 = Vector3:new{x = A0.x, y = A0.y+BL}
B4 = Vector3:new{x = A4.x, y = A4.y-BL}

B2 = Vector3:new{x = A2.x - BL, y = A2.y}

grad_A1 = 0.14845*math.pow(A1.x,-0.5)-0.126-0.7032*A1.x+0.8529*math.pow(A1.x,2)-0.4144*math.pow(A1.x,3)
grad_A3 = 0.14845*math.pow(A3.x,-0.5)-0.126-0.7032*A3.x+0.8529*math.pow(A3.x,2)-0.4144*math.pow(A3.x,3)

alpha_A1 = math.atan(grad_A1)
alpha_A3 = math.atan(grad_A3)

B1 = Vector3:new{x = A1.x-BL*math.sin(grad_A1), y = A1.y+BL*math.cos(grad_A1)}
B3 = Vector3:new{x = A3.x-BL*math.sin(grad_A3), y = A3.y-BL*math.cos(grad_A3)}
--------------------------------------------------------------------------------------------------------
dx=-(B2.x-B1.x)/2
dy=B1.y/2

B2z1 = Vector3:new{x = B1.x - dx - 0.15, y= B2.y + dy + 0.1}

B2z3 = Vector3:new{x = B3.x - dx - 0.15, y= B2.y - dy - 0.1}

dx1=(B1.x-B0.x)/2
dy1=0.01

B1z0 = Vector3:new{x = B1.x + dx, y= B1.y + dy}

B3z4 = Vector3:new{x = B3.x + dx, y= B3.y - dy}

--#######################################################################################################
--Lines

b2b1 = Bezier:new{points={B2, B2z1, B1}}
b3b2 = Bezier:new{points={B3, B2z3, B2}}
--b1b0 = Bezier:new{points={B1, B1z0, B0}}

--b3b4 = Bezier:new{points={B3, B3z4, B4}}





--Block B0
b1a1 = Line:new{p0=B1 , p1=A1} --north
b2a2 = Line:new{p0=B2 , p1=A2} --south
b2b1_new = ArcLengthParameterizedPath:new{underlying_path= b2b1} --west
a2a1_new = ArcLengthParameterizedPath:new{underlying_path= a2a1} --east

--Block B1*
b0a0 = Line:new{p0=B0 , p1=A0} --north
--b1a1 *already created in B0* --south
b1b0 = Line:new{p0=B1 , p1=B0} --west
a1a0_new = ArcLengthParameterizedPath:new{underlying_path= a1a0} --east

 --east

--Block B2
b3a3 = Line:new{p0=B3 , p1=A3} --north
b4a4 = Line:new{p0=B4 , p1=A4} --south
b4b3 = Line:new{p0=B4 , p1=B3} --west
a4a3_new = ArcLengthParameterizedPath:new{underlying_path= a4a3} --east

--Block B3
--b2a2 *already created in B0* --north
--b3a3 *already created in B2* --south
b3b2_new = ArcLengthParameterizedPath:new{underlying_path= b3b2} --west
a3a2_new = ArcLengthParameterizedPath:new{underlying_path= a3a2} --east




-- ############################################################


patch={}

patch[0]= CoonsPatch:new{north=b1a1 ,south=b2a2 ,west=b2b1_new ,east=a2a1_new}
patch[1]= CoonsPatch:new{north=b0a0 ,south=b1a1 ,west=b1b0 ,east=a1a0_new}
patch[2]= CoonsPatch:new{north=b3a3 ,south=b4a4 ,west=b4b3 ,east=a4a3_new}
patch[3]= CoonsPatch:new{north=b2a2 ,south=b3a3 ,west=b3b2_new ,east=a3a2_new}


rcfL = RobertsFunction:new{end0 = false, end1 = true, beta=1.02}


grid = {}
ny=10
grid[0] = StructuredGrid:new{psurface= patch[0], niv=10+1, njv=ny+1, cfList ={north=rcfL, south=rcfL}}
grid[1] = StructuredGrid:new{psurface= patch[1], niv=10+1, njv=ny+1, cfList ={noth=rcfL, south=rcfL}}
grid[2] = StructuredGrid:new{psurface= patch[2], niv=10+1, njv=ny+1, cfList ={north=rcfL, south=rcfL}}
grid[3] = StructuredGrid:new{psurface= patch[3], niv=10+1, njv=ny+1, cfList ={north=rcfL, south=rcfL}}


-- ############################################################
-- Add code to write you grid to a .vtk file
--grid[0]:write_to_vtk_file("tut_wk5_s0.vtk")
--grid[1]:write_to_vtk_file("tut_wk5_s1.vtk")
--grid[2]:write_to_vtk_file("tut_wk5_s2.vtk")

--####################################################################################################

blk = {}
	
blk[0] = FoamBlock:new{grid=grid[0], bndry_labels={west="i-00", east="w-01"}}

blk[1] = FoamBlock:new{grid=grid[1], bndry_labels={north="o-00",west="s-00", east="w-01"}}

blk[2] = FoamBlock:new{grid=grid[2], bndry_labels={west="s-00", south="o-00", east="w-01"}}

blk[3] = FoamBlock:new{grid=grid[3], bndry_labels={west="i-00", east="w-01"}}



--foamMesh --job=Nozzle_sim --verbosity=2

--dofile("sketch-NACA.lua")
