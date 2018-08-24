-- surface.lua
--
--            
--          (h)-----(g)----------------------(p)-----(o)
--          |        |                        |       |
--          |        |                        |       |      
--          |   B1   |     Airfoil NACA       |   B3  |
--          |        |                        |       |
--         (c)-----(leading edge)  (trailing edge)---(k)
--          |        |                        |       |
--          |        |                        |       |
--          |    B0  |                        |   B2  |
--          |        |                        |       |
--          (a)-----(b)----------------------(i)-----(j)
--        
--
-- Authors:  ,Santiago Vera, , ,  Team LL
-- Date: 21/08/2018

--################################################################################
--FUNCTIONS
-------------------------------
--Returns length of a table 
function len(table_s)
 local counter = 0
 for index in pairs(table_s) do
  counter = counter +1
 end
 return counter
end
-------------------------------

--################################################################################

--[[
-- Global settings go first
axisymmetric = false
turbulence_model = "S-A" -- other option is: "k-epsilon"
--]]



-- Blocks corners
-- Block B0
c = Vector3:new{x=-0.3, y=0}
a = Vector3:new{x=-0.3, y=-0.17}; b = Vector3:new{x=0.0, y=-0.17}

-- Block B1
h = Vector3:new{x=-0.3, y=0.17}; g = Vector3:new{x=0.0, y=0.17}

----------------------------------------------------------------

-- Block B2
k = Vector3:new{x=1.3, y=0}
i = Vector3:new{x=1.0, y=-0.17}; j = Vector3:new{x=1.3, y=-0.17}


-- Block B3
p = Vector3:new{x=1.0, y=0.17}; o = Vector3:new{x=1.3, y=0.17}

--NACA4412-------------------------------------------------------------------------------
--x point of camber--------------------------------------------------------------

naca_pi_points = {} --list of 100 points from 0 to pi
beta=0

for ib= 0, 99 do
 naca_pi_points[ib] = beta
 beta = beta + math.pi/100
end 

naca_xc_point = {} -- list of 100 points of the camber x coordinates
x = 0

for ib=0, 99 do
 x = (1-math.cos(naca_pi_points[ib]))/2
 naca_xc_point[ib]=x
end

---------------------------------------------------------------------------------
M = 4/100
P = 4/10
XX = 12/100

yc = {}
grad_yc = {}
angle_theta = {}

for ib=0, 99 do
 if naca_xc_point[ib]<P then
  yc[ib]=(M/math.pow(P,2))*(2*P*naca_xc_point[ib]-math.pow(naca_xc_point[ib],2))
  grad_yc[ib]= (2*M/math.pow(P,2))*(P-naca_xc_point[ib])
 elseif naca_xc_point[ib]>=P then
  yc[ib]=(M/math.pow ((1-P),2))*(1-2*P+2*P*naca_xc_point[ib]-math.pow (naca_xc_point[ib],2))
  grad_yc[ib]= (2*M/math.pow((1-P),2))*(P-naca_xc_point[ib])
 else
  error("invalid operation")
 end
 angle_theta[ib] = math.atan(grad_yc[ib])
end

--Thickness----------------------------------------------------------------------
yt = {}

a0=0.2969
a1=-0.126
a2=-0.3516
a3=0.2843
a4=-0.1036

for ib=0, 99 do
 yt[ib]= (XX/0.2)*(a0*math.pow(naca_xc_point[ib],0.5) + a1*naca_xc_point[ib] + a2*math.pow(naca_xc_point[ib],2) + 			a3*math.pow(naca_xc_point[ib],3) + a4*math.pow(naca_xc_point[ib],4))
end 

--Top airfoil--------------------------------------------------------------------
naca_xu = {}
naca_yu = {}

for ib=0, 99 do
 naca_xu[ib] = naca_xc_point[ib] - yt[ib]* math.sin(angle_theta[ib])
 naca_yu[ib] = yc[ib] + yt[ib]* math.cos(angle_theta[ib])
end

--Bottom airfoil-----------------------------------------------------------------
naca_xl = {}
naca_yl = {}

for ib=0, 99 do
 naca_xl[ib] = naca_xc_point[ib] + yt[ib]* math.sin(angle_theta[ib])
 naca_yl[ib] = yc[ib] - yt[ib]* math.cos(angle_theta[ib])
end

---------------------------------------------------------------------------------
--NACA vertices

--Top----------------------------------------------------------------------------

top_s = {}
top_edge = {}

--Top Airfoil divided in two parts
top_front ={}
top_back = {}
----------------------------------
--print("ib	","X     	","Y	      ","point")
for ib= 0, 99 do

 if naca_xu[ib] < 0.3 and naca_xu[ib] >= 0 then 
  --top_front[ib]= Vector3:new{x=naca_xu[ib], y=naca_yu[ib]}
  table.insert(top_front,Vector3:new{x=naca_xu[ib], y=naca_yu[ib]})
  --print(ib,naca_xu[ib],naca_yu[ib],"front = ", top_front[ib])
 elseif naca_xu[ib] >= 0.3 then
  --top_back[ib]= Vector3:new{x=naca_xu[ib], y=naca_yu[ib]}
  table.insert(top_back,Vector3:new{x=naca_xu[ib], y=naca_yu[ib]})
  --print(ib,naca_xu[ib],naca_yu[ib],"back = ", top_back[ib])
 end

-- top_s[ib] = Vector3:new{x=naca_xu[ib], y=naca_yu[ib]}
-- top_edge[ib] = Vector3:new{x=naca_xu[ib], y=0.17}
end




table.insert(top_front,top_back[1])



--Bottom----------------------------------------------------------------------------
bottom_s = {}
bottom_edge = {}

--Bottom Airfoil divided in two parts
bottom_front ={}
bottom_back ={}
b_f={}
-------------------------------------

bottom_s[0]=top_s[0]

table.insert(b_f,top_front[1])

for ib= 1, 98 do

 if naca_xl[ib] < 0.3 then 
  --b_f[ib]= Vector3:new{x=naca_xl[ib], y=naca_yl[ib]}
  table.insert(b_f,Vector3:new{x=naca_xl[ib], y=naca_yl[ib]})
 elseif naca_xl[ib] >= 0.3 then
  --bottom_back[ib]= Vector3:new{x=naca_xl[ib], y=naca_yl[ib]}
  table.insert(bottom_back,Vector3:new{x=naca_xl[ib], y=naca_yl[ib]})
 end

 bottom_s[ib] = Vector3:new{x=naca_xl[ib], y=naca_yl[ib]}
 bottom_edge[ib] = Vector3:new{x=naca_xl[ib], y=-0.17}
end

bottom_s[99]=top_s[99]

table.insert(b_f,bottom_back[0])

table.insert(bottom_back,top_back[len(top_back)])



--------------------------------------------------------------------------------
--Reverse b_f table in bottom_front
N= len(b_f)
for ib=0, N do 
 --bottom_front[ib] = b_f[N-ib]
  table.insert(bottom_front,b_f[N-ib])
end

---------------------------------------------------------------------------------
--NACA lines

--Top

--top_surface = Spline:new{points=top_s}

--Top Front----------------------------------
top_front_line = Spline:new{points=top_front}

--Top Back 
top_back_line = Spline:new{points=top_back}
---------------------------------------------

--Bottom

--bottom_surface = Spline:new{points=bottom_s}

--Bottom Front--------------------------------------
bottom_front_line = Spline:new{points=bottom_front}

--Bottom Back
bottom_back_line = Spline:new{points=bottom_back}
----------------------------------------------------

--[[
---------------------------------------------------------------------------------
--Egde lines


top_edge_line = Line:new{p0=g, p1=p}
bottom_edge_line = Line:new{p0=b, p1=i}
---------------------------------------------------------------------------------
--Top Surface vertical lines



top_vertical_left = Line:new{p0=top_s[0], p1=g}
top_vertical_right = Line:new{p0=top_s[99], p1=p}
---------------------------------------------------------------------------------
--Bottom Surface vertical lines



bottom_vertical_left = Line:new{p0=b, p1=top_s[0]}
bottom_vertical_right = Line:new{p0=i, p1=top_s[99]}
---------------------------------------------------------------------------------
--Block lines
--horizontal lines
ab = Line:new{p0=a, p1=b}

c_0 = Line:new{p0=c, p1=top_s[0]}

hg = Line:new{p0=h, p1=g}

bi = Line:new{p0=b, p1=i}
gp = Line:new{p0=g, p1=p}

ij = Line:new{p0=i, p1=j}

trail_k = Line:new{p0=top_s[99], p1=k}

po = Line:new{p0=p, p1=o}

--vertical lines
ac = Line:new{p0=a, p1=c}
b_0 = Line:new{p0=b, p1=top_s[0]}

ch = Line:new{p0=c, p1=h}
leading_g = Line:new{p0=top_s[0], p1=g}

i_trailing = Line:new{p0=i, p1=top_s[99]}
jk = Line:new{p0=j, p1=k}

trailing_p = Line:new{p0=top_s[99], p1=p}
ko = Line:new{p0=k, p1=o}



--patches
b0 = CoonsPatch:new{north=c_0 ,south=ab ,west=ac ,east=b_0}
b1 = CoonsPatch:new{north=hg ,south=c_0 ,west=ch ,east=leading_g}

b2 = CoonsPatch:new{north=bottom_surface ,south=bi ,west=b_0 ,east=i_trailing}
b3 = CoonsPatch:new{north=gp ,south=top_surface ,west=leading_g ,east=trailing_p}

b4 = CoonsPatch:new{north=trail_k ,south=ij ,west=i_trailing ,east=jk}
b5 = CoonsPatch:new{north=po ,south=trail_k ,west=trailing_p ,east=ko}


rcfL = RobertsFunction:new{end0 = false, end1 = true, beta=1.02}

--grids
grid={}

grid[0] = StructuredGrid:new{psurface=b0, niv=10+1, njv=5+1, cfList ={west=rcfL, east=rcfL}}
grid[1] = StructuredGrid:new{psurface=b1, niv=10+1, njv=5+1, cfList ={west=rcfL, east=rcfL}}

grid[2] = StructuredGrid:new{psurface=b2, niv=10+1, njv=5+1, cfList ={west=rcfL, east=rcfL}}
grid[3] = StructuredGrid:new{psurface=b3, niv=10+1, njv=5+1, cfList ={west=rcfL, east=rcfL}}

grid[4] = StructuredGrid:new{psurface=b4, niv=10+1, njv=5+1, cfList ={west=rcfL, east=rcfL}}
grid[5] = StructuredGrid:new{psurface=b5, niv=10+1, njv=5+1, cfList ={west=rcfL, east=rcfL}}



for ib= 0, 5 do
	fileName = string.format("airfoil-NACA4412-blk-%d.vtk",ib)
	grid[ib]:write_to_vtk_file(fileName)
end
--]]


--[[
--defined blocks

blk = {}
	
blk[0] = FoamBlock:new{grid=grid[0], bndry_labels={west="w-01", south="w-01", east="w-01"}}

blk[1] = FoamBlock:new{grid=grid[1], bndry_labels={west="w-01", south="w-01", east="w-01"}}

blk[2] = FoamBlock:new{grid=grid[2], bndry_labels={west="w-01", south="w-01", east="w-01", north="w-00"}}

blk[3] = FoamBlock:new{grid=grid[3], bndry_labels={south="w-01", east="w-01", north="w-00"}}
blk[4] = FoamBlock:new{grid=grid[4], bndry_labels={south="w-01", east="w-01", north="w-00"}}
blk[5] = FoamBlock:new{grid=grid[5], bndry_labels={south="w-01", east="w-01"}}
blk[6] = FoamBlock:new{grid=grid[6], bndry_labels={south="w-01", east="w-01"}}
blk[7] = FoamBlock:new{grid=grid[7], bndry_labels={south="w-01", east="w-01", north="w-00"}}
--]]
--foamMesh --job=cavity-clipped --verbosity=2

dofile("sketch-surface.lua")
