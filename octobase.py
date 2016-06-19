#!/usr/bin/env python

from EZCAD3 import *

class Layer_Frame(Part):

    def __init__(self, up, name):
	""" *Layer_Frame*: """

	# Verify argument types:
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str)

	# Initialize the superclass:
	Part.__init__(self, up, name)

	tube_width = L(inch=0.75)
	tube_height = L(inch=1.50)
	tube_thickness = L(inch="1/8")
	tube = {
	  "width": tube_width,
	  "height": tube_height,
          "thickness": tube_thickness
	}
	material = Material("aluminum", "")

	degrees0 = Angle()
	degrees45 = Angle(deg=45.0)
	degrees90 = Angle(deg=90.0)
	degrees135 = Angle(deg=135.0)
	degrees180 = Angle(deg=180.0)
	outer_radius = L(inch=9.0)
	lidar_radius = L(inch=2.5)
	green = Color("green")
	red = Color("red")
	magenta = Color("magenta")
	cyan = Color("cyan")
	gold = Color("gold")
	silver = Color("silver")
	blue = Color("blue")
	z = L()

	self.face_tube_e_  = \
	  Face_Tube(self, "face_tube_e",  material, green, tube, outer_radius,  degrees0,   z)
	self.face_tube_ne_ = \
	  Face_Tube(self, "face_tube_ne", material, red,   tube, outer_radius,  degrees45,  z)
	self.face_tube_n_  =  \
	  Face_Tube(self, "face_tube_n",  material, green, tube, outer_radius,  degrees90,  z)
	self.face_tube_nw_ = \
	  Face_Tube(self, "face_tube_nw", material, red,   tube, outer_radius,  degrees135, z)
	self.face_tube_w_  = \
	  Face_Tube(self, "face_tube_w",  material, green, tube, outer_radius,  degrees180, z)
	self.face_tube_sw_ = \
	  Face_Tube(self, "face_tube_sw", material, red,   tube, outer_radius, -degrees135, z)
	self.face_tube_s_ =  \
	  Face_Tube(self, "face_tube_s",  material, green, tube, outer_radius, -degrees90,  z)
	self.face_tube_se_ = \
	  Face_Tube(self, "face_tube_se", material, red,   tube, outer_radius, -degrees45,  z)

	self.long_inner_tube_e_ = Inner_Tube(self, "long_inner_tube_e", material, magenta,
	  tube, lidar_radius, "long",  degrees0,   z)
	self.long_inner_tube_n_ = Inner_Tube(self, "long_inner_tube_n", material, cyan,
	  tube, lidar_radius, "long",  degrees90,  z)
	self.long_inner_tube_w_ = Inner_Tube(self, "long_inner_tube_w", material, magenta,
	  tube, lidar_radius, "long",  degrees180, z)
	self.long_inner_tube_s_ = Inner_Tube(self, "long_inner_tube_s", material, cyan,
	  tube, lidar_radius, "long", -degrees90,  z)

	self.short_inner_tube_e_ = Inner_Tube(self, "short_inner_tube_e", material, gold,
	  tube, lidar_radius, "short",  degrees0,   z)
	self.short_inner_tube_n_ = Inner_Tube(self, "short_inner_tube_n", material, silver,
	  tube, lidar_radius, "short",  degrees90,  z)
	self.short_inner_tube_w_ = Inner_Tube(self, "short_inner_tube_w", material, gold,
	  tube, lidar_radius, "short",  degrees180, z)
	self.short_inner_tube_s_ = Inner_Tube(self, "short_inner_tube_s", material, silver,
	  tube, lidar_radius, "short", -degrees90,  z)

	self.center_inner_tube_n_ = Inner_Tube(self, "center_inner_tube_n", material, blue,
	  tube, lidar_radius, "center",  degrees90,   z)
	self.center_inner_tube_s_ = Inner_Tube(self, "center_inner_tube_s", material, blue,
	  tube, lidar_radius, "center", -degrees90,   z)

    def construct(self):
	""" *Layer_Frame*: """

	pass


class Inner_Tube(Part):

    def __init__(self, up, name, material, color, tube, lidar_radius, kind, bearing, z):
	""" *Inner_Tube*: """

	# Verify argument types:
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str)
	assert isinstance(material, Material)
	assert isinstance(color, Color)
	assert isinstance(tube, dict) and len(tube) == 3
	assert "height" in tube and isinstance(tube["height"], L)
	assert "width" in tube and isinstance(tube["width"], L)
	assert "thickness" in tube and isinstance(tube["thickness"], L)
	assert isinstance(lidar_radius, L)
	assert isinstance(kind, str)
	assert isinstance(bearing, Angle)
	assert isinstance(z, L)
	
	# Initialize the superclass:
	Part.__init__(self, up, name)

	# Load up *self*:
	self.bearing_a = bearing
	self.color_c = color
	self.kind_o = kind
	self.lidar_radius_l = lidar_radius
	self.material_m = material
	self.tube_o = tube
	self.z_l = z

    def construct(self):
	""" *Inner_Tube*: """

	# Use *inner_tube* instead of *self*:
	inner_tube = self

	# Grab some values from *self*:
	color = self.color_c
	bearing = self.bearing_a
	kind = self.kind_o
	lidar_radius = self.lidar_radius_l
	material = self.material_m
	tube = self.tube_o
	z = self.z_l

	# Grab some values out of *tube*:
	tube_width = tube["width"]
	tube_height = tube["height"]
	tube_thickness = tube["thickness"]

	face_tube_e = inner_tube.up.face_tube_e_
	inner_chord_radius = face_tube_e.inner_chord_radius_l

	# The *inner_radius*, *outer_radius*, and *offset* are determined by whether
	# *kind* is "long", "short", or "center":
	if kind == "long":
	    # Provide the values for the long inner tube:
	    inner_radius = -lidar_radius + tube_width/2
	    outer_radius = inner_chord_radius
	    offset = lidar_radius
	elif kind == "short":
	    # Provide the values for the short inner tube:
	    inner_radius = lidar_radius + tube_width/2
	    outer_radius = inner_chord_radius
	    offset = -lidar_radius
	elif kind == "center":
	    # Provide the values for the short inner tube:
	    inner_radius = lidar_radius + tube_width/2
	    outer_radius = inner_chord_radius
	    offset = L()
	else:
	    assert False, "kind is '{0}' valid".format(kind)

	# Some constants:
	zero = L()
	degrees0 = Angle(deg=0)
	degrees90 = Angle(deg=90)

	# Compute the *start* and *end* points:
	start_x = inner_radius.cosine(bearing)
	start_y = inner_radius.sine(bearing)
	end_x =   outer_radius.cosine(bearing)
	end_y =   outer_radius.sine(bearing)
	
	# Offset everything by *offset*:
	offset_bearing = (bearing + degrees90).normalize()
	start_x += offset.cosine(offset_bearing)
	start_y += offset.sine(offset_bearing)
	end_x +=   offset.cosine(offset_bearing)
	end_y +=   offset.sine(offset_bearing)

	# Compute the *start* and *end_points*:
	start = P(start_x, start_y, z)
	end =   P(end_x,   end_y,   z)

	inner_tube.rectangular_tube_extrude(inner_tube._name, material, color,
	   tube_width, tube_height, tube_thickness, start, zero, end, zero, degrees0)

class Face_Tube(Part):

    def __init__(self, up, name, material, color, tube, outer_radius, bearing, z):
	""" *Face_Tube*: Initialize *Base* object (i.e. *self*) with a parent of *up*. """

	# Verify argument types:
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str)
	assert isinstance(material, Material)
	assert isinstance(color, Color)
	assert isinstance(tube, dict) and len(tube) == 3
	assert "height" in tube and isinstance(tube["height"], L)
	assert "width" in tube and isinstance(tube["width"], L)
	assert "thickness" in tube and isinstance(tube["thickness"], L)
	assert isinstance(outer_radius, L)
	assert isinstance(bearing, Angle)
	assert isinstance(z, L)

	# Initialize the superclass:
	Part.__init__(self, up, name)

	# Load up *self*:
	self.bearing_a = bearing
	self.color_c = color
	self.material_m = material
	self.outer_radius_l = outer_radius
	self.tube_o = tube
	self.z_l = z

    def construct(self):
	""" *Face_Tube*: Construct the *Base* object (i.e. *self*). """

	# Set *debug* to *True* to trace:
	debug = False
	#debug = True
	if debug:
	    print("=>Face_Tube.construct(*)")

	# Use *face_tube* instead of *self*:
	face_tube = self

	# Grab some values from *face_tube*:
	bearing = face_tube.bearing_a
	color = face_tube.color_c
	material = face_tube.material_m
	outer_radius = face_tube.outer_radius_l
	tube = face_tube.tube_o
	z = face_tube.z_l

	# Extract values from *tube*:
	tube_width = tube["width"]
	tube_height = tube["height"]
	tube_thickness = tube["thickness"]

	# Some constants:
	zero = L()
	degrees0 = Angle()
	degrees22_5 = Angle(deg=22.50)
	degrees90 = Angle(deg=90.00)
	half_width = tube_width / 2
	degrees67_5 = Angle(deg=67.5)

	# The frame element looks as follows:
	#
	#    A-------B---------S   S---------E-------F
	#     \    | |                       | |----/
	#      \   +-|                       |-+   /
	#       \    |                       |    /
	#        C - | - - - - S   S - - - - | - G
	#         \  |                       |  /
	#          \ |                       | /
	#           \|                       |/
	#            D---------S   S---------H
	#
        # where both the angle <ADB and the angle <EHF are 22.5 degrees (= 360/16).
	# Obviously, the angle <DAB and the angle <HFE are 66.5 degrees (= 90 - 22.5).
	# The extrusion center-line goes along the line through points C and G.
	# The distance |BD| = |EH| = *tube_width*.  We need to compute the lengths
	# |AB| = |EF| and |AD| = |FH|.  This is done using the law of sines:
	#
	#       |AD|        |AB|        |BD|
	#     --------- = --------- = ---------                   (1)
	#     sin(<ABD)   sin(<ADB)   sin(<BAD)
	#
	#      |AD|      |AB|        |BD|
	#     ------ = --------- = ---------                      (2)
	#     sin(90)  sin(22.5)   sin(67.5)
	#
	#      |AD|      |AB|      tube_width
	#     ------ = --------- = ----------                     (3)
	#       1      sin(22.5)   sin(67.5)
	#
	#      |AD| =  tube_width / sin(67.5)                     (4)
	#
	#      |AB| =  sin(22.5) * tube_width/sin(67.5)           (5)
	ad = tube_width / degrees67_5.sine()
	ab = ad * degrees22_5.sine()

	# Compute the *inner*, *center* radius:
	face_tube.inner_radius_l = inner_radius = outer_radius - ad
	face_tube.center_radius_l = center_radius = outer_radius - ad/2

	# The *inner_chord_radius* is needed to figure out where to terminate the long inner tubes
	# the approprate face tubes:
	#
	#        A----B----C
	#         \   |   /
	#          \  |  /
	#           \ | /
	#            \|/
	#             D
	#
	# The *inner_chord_radius* is |BD| where |AD| = |CD| = *inner_radius*.  The angle
	# <ADB = <CDB = 22.5 degrees.  Since both triangles ABD and BCD are right triangles
	# the |BD| = |AC|*cosine(22.5) = *inner_radius* * cosine(22.5):
	face_tube.inner_chord_radius_l = inner_chord_radius = inner_radius.cosine(degrees22_5)

	# Now compute *angle1* = <ABD and *angle2* = <CDB:
	angle1 = bearing + degrees22_5
	angle2 = bearing - degrees22_5

	# Now we can compute (*start_x*, *start_y*, 0) and *start_extra*:
	start_x = center_radius.cosine(angle1)
	start_y = center_radius.sine(angle1)
	start = P(start_x, start_y, z)
	start_extra = ab / 2

	# Now we can compute (*end_x*, *end_y*, 0) and *end_extra*:
	end_x = center_radius.cosine(angle2)
	end_y = center_radius.sine(angle2)
	end = P(end_x, end_y, z)
	end_extra = ab / 2

	# Now we can extrude the tube:
	face_tube.rectangular_tube_extrude(face_tube._name, material, color,
	   tube_width, tube_height, tube_thickness, start, start_extra, end, end_extra, degrees0)
	
	# Compute the *trim_contour*:
	x1 = inner_radius.cosine(angle1)
	y1 = inner_radius.sine(angle1)
	x2 = inner_radius.cosine(angle2)
	y2 = inner_radius.sine(angle2)
	x3 = outer_radius.cosine(angle2)
	y3 = outer_radius.sine(angle2)
	x4 = outer_radius.cosine(angle1)
	y4 = outer_radius.sine(angle1)
	trim_contour = Contour("trim contour")
	trim_contour.bend_append("corner1", P(x1, y1, z), zero)
	trim_contour.bend_append("corner2", P(x2, y2, z), zero)
	trim_contour.bend_append("corner3", P(x3, y3, z), zero)
	trim_contour.bend_append("corner4", P(x4, y4, z), zero)
	face_tube.tool_prefer("Laser_007")
	face_tube.contour("trim contour", trim_contour,
	  P(x1, y1, z + tube_height/2), P(x1, y1, z - tube_height/2), L(inch=.007), "")

if __name__== "__main__":
    ezcad = EZCAD3(0)
    layer_frame = Layer_Frame(None, "frame_layer")
    layer_frame.process(ezcad)
