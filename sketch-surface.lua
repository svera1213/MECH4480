-- sketch-surface.lua
-- Called by the user input script to make a sketch of the geometric elements.
-- Santiago
sk = Sketch:new{renderer="svg", projection="xyortho"}
sk:set{canvas={0.0,0.0,150.0,60.0}, viewport={-0.5,-0.5,1.5,0.5}}
sk:start{file_name="surface.svg"}

-- surfaces
sk:set{line_width=0.5, fill_colour="green"}

--[[
for ib= 0, 98 do
   sk:render{path=top_line[ib]}
   sk:render{path=bottom_line[ib]}
   sk:render{path=bottom_edge_line[ib]}
   sk:render{path=top_edge_line[ib]}
end

for ib=0, 99 do
   sk:render{path=top_vertical[ib]}
   sk:render{path=bottom_vertical[ib]}
end
--]]

sk:render{path=top_front_line}
sk:render{path=top_back_line}
sk:render{path=bottom_front_line}
sk:render{path=bottom_back_line}


--[[
sk:render{path=top_surface}
sk:render{path=bottom_surface}
sk:render{path=top_edge_line}
sk:render{path=bottom_edge_line}
sk:render{path=top_vertical_left}
sk:render{path=top_vertical_right}
sk:render{path=bottom_vertical_left}
sk:render{path=bottom_vertical_right}

sk:render{path=ab}
sk:render{path=c_0}
sk:render{path=hg}
sk:render{path=ij}
sk:render{path=trail_k}
sk:render{path=po}

sk:render{path=ac}
sk:render{path=b_0}
sk:render{path=ch}
sk:render{path=leading_g}
sk:render{path=i_trailing}
sk:render{path=jk}
sk:render{path=trailing_p}
sk:render{path=ko}


sk:render{surf=b0}
sk:render{surf=b1}
sk:render{surf=b2}
sk:render{surf=b3}
sk:render{surf=b4}
sk:render{surf=b5}
--]]

--sk:render{surf=surf_tfi}
--sk:render{surf=surf_ao}

-- draw some lines across the surface to show how
-- the interpolation varies
--sk:set{line_width=0.2}

function draw_constant_r(surf, r)
   local n = 10
   local ds = 1.0/n
   for i=1, n do
      local p0 = surf(r,ds*(i-1))
      local p1 = surf(r,ds*i)
      sk:line{p0=p0, p1=p1}
   end
end

function draw_constant_s(surf, s)
   local n = 10
   local dr = 1.0/n
   for i=1, n do
      local p0 = surf(dr*(i-1),s)
      local p1 = surf(dr*i,s)
      sk:line{p0=p0, p1=p1}
   end
end

function plot_lines_on_surface(surf)
   for _,v in ipairs({0.25, 0.5, 0.75}) do
      draw_constant_r(surf, v)
      draw_constant_s(surf, v)
   end
end



--for ib= 0, 5 do
--   plot_lines_on_surface(grid[ib])
--end
--[[
plot_lines_on_surface(b0)
plot_lines_on_surface(b1)
plot_lines_on_surface(b2)
plot_lines_on_surface(b3)
plot_lines_on_surface(b4)
plot_lines_on_surface(b5)
--]]

--plot_lines_on_surface(surf_ao)

-- labelled points of interest

--sk:dotlabel{point=a, label="a"}
--sk:dotlabel{point=b, label="b"}
--sk:dotlabel{point=c, label="c"}
--sk:dotlabel{point=d, label="d"}
--sk:dotlabel{point=p00, label="p00"}
--sk:dotlabel{point=p10, label="p10"}
--sk:dotlabel{point=p11, label="p11"}
--sk:dotlabel{point=p01, label="p01"}

-- axes
sk:set{line_width=0.3} -- for drawing rules
sk:rule{direction="x", vmin=-0.4, vmax=1.4, vtic=0.2,
       anchor_point=Vector3:new{x=0,y=0},
       tic_mark_size=0.02, number_format="%.1f",
       text_offset=0.06, font_size=10}
sk:text{point=Vector3:new{x=1.4,y=-0.1}, text="x", font_size=12}
sk:rule{direction="y", vmin=-0.3, vmax=0.3, vtic=0.2,
       anchor_point=Vector3:new{x=0,y=0},
       tic_mark_size=0.02, number_format="%.1f",
       text_offset=0.025, font_size=10}
sk:text{point=Vector3:new{x=-0.1,y=0.4}, text="y", font_size=12}

sk:finish{}
