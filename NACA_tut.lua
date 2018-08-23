-- NACAstart.lua
-- Simple job-specification for a NACA aerofoil mesh
-- IJ, 20-Aug-2017

job_title = "NACA aerofoil example"
print(job_title)

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
---------------------------------------------------------------------------------------------------------
--Lines

b2b1 = Bezier:new{points={B2, B2z1, B1}}
b2b3 = Bezier:new{points={B2, B2z3, B3}}
--b1b0 = Bezier:new{points={B1, B1z0, B0}}
b1b0 = Line:new{p0=B1 , p1=B0}
--b3b4 = Bezier:new{points={B3, B3z4, B4}}
b3b4 = Line:new{p0=B3 , p1=B4}

b3b4 = Line:new{p0=B3 , p1=B4}
b3b4 = Line:new{p0=B3 , p1=B4}

--[[b2_mid1 = Line:new{p0=B2 , p1=B2z1}
mid1_B1 = Line:new{p0=B2z1 , p1=B1}

b2_mid3 = Line:new{p0=B2 , p1=B2z3}
mid3_B3 = Line:new{p0=B2z3 , p1=B3}--]]




-- ############################################################
-- ############################################################
-- Add code to write you grid to a .vtk file

dofile("draw-NACA.lua")
