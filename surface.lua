-- surface.lua
--
--            
--          (h)-----(g)----------------------(p)-----(o)
--          |    b2  |           b4           |   b7  |
--          |        |                        |       |      
--          (e)-----(f)----------------------(m)-----(n)
--          |    b1  |      Airfoil NACA      |       |
--          |        |       Here             |   b6  |
--          (d)-----(c)----------------------(l)-----(k)
--          |    b0  |          b3            |       |
--          |        |                        |  b5   |
--          (a)-----(b)----------------------(i)-----(j)
--        
--
-- Authors:  ,Santiago Vera, , ,  Team LL
-- Date: 21/08/2018


-- Global settings go first
axisymmetric = false
turbulence_model = "S-A" -- other option is: "k-epsilon"


-- Blocks corners
-- Block B0
d = Vector3:new{x=-0.3, y=-0.07}; c = Vector3:new{x=0.0, y=-0.07}
a = Vector3:new{x=-0.3, y=-0.17}; b = Vector3:new{x=0.0, y=-0.17}

-- Block B1
e = Vector3:new{x=-0.3, y=0.07}; f = Vector3:new{x=0.0, y=0.07}

-- Block B2
h = Vector3:new{x=-0.3, y=0.17}; g = Vector3:new{x=0.0, y=0.17}

----------------------------------------------------------------

-- Block B5
l = Vector3:new{x=1.0, y=-0.07}; k = Vector3:new{x=1.3, y=-0.07}
i = Vector3:new{x=1.0, y=-0.17}; j = Vector3:new{x=1.3, y=-0.17}

-- Block B6
m = Vector3:new{x=1.0, y=0.07}; n = Vector3:new{x=1.3, y=0.07}

-- Block B7
p = Vector3:new{x=1.0, y=0.17}; o = Vector3:new{x=1.3, y=0.17}

--NACA4412-------------------------------------------------------------------------------
--x point of camber--------------------------------------------------------------

naca_pi_points = {}
beta=0

for ib= 0, 99 do
 naca_pi_points[ib] = beta
 beta = beta + math.pi/100
end 

naca_xc_point = {}
x = 0

for ib=0, 99 do
 x = (1-math.cos(naca_pi_points[ib]))/2
 naca_xc_point[ib]=x
end

---------------------------------------------------------------------------------
M = 4/100
P = 40/10
XX = 12/100

yc = {}
grad_yc = {}
angle_theta = {}

for ib=0, 99 do
 if naca_xc_point[ib]<P then
  yc[ib]=(M/math.pow(P,2))*(2*P*naca_xc_point[ib]-math.pow(naca_xc_point[ib],2))
  grad_yc[ib]= (2*M/math.pow(P,2))*(P-naca_xc_point[ib])
 elseif naca_xc_point[ib]>=P then
  yc[ib]=(M/math.pow ((1-P),2))*(1-2*P+2*P*naca_x_point[ib]-math.pow (naca_x_point[ib],2))
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

--Top
top_s = {}
top_egde = {}

for ib= 0, 99 do
 top_s[ib] = Vector3:new{x=naca_xu[ib], y=naca_yu[ib]}
end

--Bottom
bottom_s = {}

for ib= 1, 98 do
 bottom_s[ib] = Vector3:new{x=naca_xl[ib], y=naca_yl[ib]}
end

---------------------------------------------------------------------------------
--NACA lines

--Top
top_line = {}

for ib= 0, 98 do
 top_line[ib] = Line:new{p0=top_s[ib], p1=top_s[ib+1]}
end

--Bottom
bottom_line = {}

bottom_line[0]= Line:new{p0=top_s[0], p1=bottom_s[1]}

for ib= 1, 97 do
 bottom_line[ib] = Line:new{p0=bottom_s[ib], p1=bottom_s[ib+1]}
end

bottom_line[98]= Line:new{p0=bottom_s[98], p1=top_s[99]}

---------------------------------------------------------------------------------




--[[
--(M/math.pow((1-P),2))*(1-2*P+2*P*naca_x_point[ib]-math.pow(naca_x_point[ib],2))
---------------------------------------------------------------------------------
--Block lines
--horizontal lines
ab = Line:new{p0=a, p1=b}
dc = Line:new{p0=d, p1=c}
ef = Line:new{p0=e, p1=f}
hg = Line:new{p0=h, p1=g}

bi = Line:new{p0=b, p1=i}
cl = Line:new{p0=c, p1=l}
fm = Line:new{p0=f, p1=m}
gp = Line:new{p0=g, p1=p}

ij = Line:new{p0=i, p1=j}
lk = Line:new{p0=l, p1=k}
mn = Line:new{p0=m, p1=n}
po = Line:new{p0=p, p1=o}

--vertical lines
ad = Line:new{p0=a, p1=d}; bc = Line:new{p0=b, p1=c}
de = Line:new{p0=d, p1=e}; cf = Line:new{p0=c, p1=f}
eh = Line:new{p0=e, p1=h}; fg = Line:new{p0=f, p1=g}

il = Line:new{p0=i, p1=l}; jk = Line:new{p0=j, p1=k}
lm = Line:new{p0=l, p1=m}; kn = Line:new{p0=k, p1=n}
mp = Line:new{p0=m, p1=p}; no = Line:new{p0=n, p1=o}

--patches
b0 = CoonsPatch:new{north=dc ,south=ab ,west=ad ,east=bc}
b1 = CoonsPatch:new{north=ef ,south=dc ,west=de ,east=cf}
b2 = CoonsPatch:new{north=hg ,south=ef ,west=eh ,east=fg}

b3 = CoonsPatch:new{north=cl ,south=bi ,west=bc ,east=il}
b4 = CoonsPatch:new{north=gp ,south=fm ,west=fg ,east=mp}

b5 = CoonsPatch:new{north=lk ,south=ij ,west=il ,east=jk}
b6 = CoonsPatch:new{north=mn ,south=lk ,west=lm ,east=kn}
b7 = CoonsPatch:new{north=po ,south=mn ,west=mp ,east=no}

--grids
grid={}

grid[0] = StructuredGrid:new{psurface=b0, niv=4+1, njv=5+1}
grid[1] = StructuredGrid:new{psurface=b1, niv=4+1, njv=5+1}
grid[2] = StructuredGrid:new{psurface=b2, niv=4+1, njv=5+1}
grid[3] = StructuredGrid:new{psurface=b3, niv=4+1, njv=5+1}
grid[4] = StructuredGrid:new{psurface=b4, niv=4+1, njv=5+1}
grid[5] = StructuredGrid:new{psurface=b5, niv=4+1, njv=5+1}
grid[6] = StructuredGrid:new{psurface=b6, niv=4+1, njv=5+1}
grid[7] = StructuredGrid:new{psurface=b7, niv=4+1, njv=5+1}


for ib= 0, 7 do
	fileName = string.format("airfoil-NACA4412-blk-%d.vtk",ib)
	grid[ib]:write_to_vtk_file(fileName)
end
--]]


--defined blocks
--[[
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
