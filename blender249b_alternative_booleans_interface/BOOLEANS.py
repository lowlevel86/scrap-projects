#!BPY

"""
Name: 'Boolean Operators'
Blender: 249
Group: 'Mesh'
Tip: 'Alternative boolean operators.'
"""

__bpydoc__ = """\
These are mesh boolean alternatives to the builtin boolean operators.
"""

from Blender import *
import BPyAddMesh
import math
import bpy
import ctypes
import array
import os
import sys


def booleanOp(in_coords, in_tris, in_labels, boolOp):

    # get the python scripts directory
    py_path = bpy.config.userScriptsDir

    if py_path == "":
        py_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), '.blender/scripts')

    # Load the shared library
    lib = ctypes.CDLL(os.path.join(py_path, 'mesh_booleans.so'))

    # Define the function signatures
    lib.boolean_ops.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    lib.boolean_ops.restype = None

    lib.free_memory.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    lib.free_memory.restype = None


    # Convert the input Python list to a ctypes array
    pt_array = array.array('d', in_coords)
    pt_array_addr = pt_array.buffer_info()[0]  # Get the address
    ctypes_pt_array = ctypes.cast(pt_array_addr, ctypes.POINTER(ctypes.c_double))
    ptSz = len(pt_array)
    
    tri_array = array.array('i', in_tris)
    tri_array_addr = tri_array.buffer_info()[0]  # Get the address
    ctypes_tri_array = ctypes.cast(tri_array_addr, ctypes.POINTER(ctypes.c_int))
    triSz = len(tri_array)
    
    label_array = array.array('i', in_labels)
    label_array_addr = label_array.buffer_info()[0]  # Get the address
    ctypes_label_array = ctypes.cast(label_array_addr, ctypes.POINTER(ctypes.c_int))
    labelSz = len(label_array)
    
    # Prepare output variables
    out_coords = ctypes.POINTER(ctypes.c_double)()
    out_coordsSz = ctypes.c_int()
    
    out_tris = ctypes.POINTER(ctypes.c_int)()
    out_trisSz = ctypes.c_int()
    
    out_labels = ctypes.POINTER(ctypes.c_int)()
    out_labelsSz = ctypes.c_int()

    # Call the C++ function
    lib.boolean_ops(ctypes_pt_array, ptSz, ctypes_tri_array, triSz, ctypes_label_array, labelSz, ctypes.byref(out_coords), ctypes.byref(out_coordsSz), ctypes.byref(out_tris), ctypes.byref(out_trisSz), ctypes.byref(out_labels), ctypes.byref(out_labelsSz), boolOp)
    
    # Convert the output to a Python list
    coord_list = [out_coords[i] for i in range(out_coordsSz.value)]
    tri_list = [out_tris[i] for i in range(out_trisSz.value)]
    label_list = [out_labels[i] for i in range(out_labelsSz.value)]

    # Free the allocated memory in C++
    lib.free_memory(out_coords, out_tris, out_labels)

    return coord_list, tri_list, label_list



def meshCheck(in_coords, in_tris):

    # get the python scripts directory
    py_path = bpy.config.userScriptsDir

    if py_path == "":
        py_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), '.blender/scripts')

    # Load the shared library
    lib = ctypes.CDLL(os.path.join(py_path, 'mesh_booleans_inputcheck.so'))

    # Define the function signatures
    lib.mesh_check.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib.mesh_check.restype = None

    # Convert the input Python list to a ctypes array
    pt_array = array.array('d', in_coords)
    pt_array_addr = pt_array.buffer_info()[0]  # Get the address
    ctypes_pt_array = ctypes.cast(pt_array_addr, ctypes.POINTER(ctypes.c_double))
    ptSz = len(pt_array)
    
    tri_array = array.array('i', in_tris)
    tri_array_addr = tri_array.buffer_info()[0]  # Get the address
    ctypes_tri_array = ctypes.cast(tri_array_addr, ctypes.POINTER(ctypes.c_int))
    triSz = len(tri_array)
    
    # prepare output variable
    checkVal = ctypes.c_int()

    # Call the C++ function
    lib.mesh_check(ctypes_pt_array, ptSz, ctypes_tri_array, triSz, ctypes.byref(checkVal))
    
    return int(checkVal.value)



exit_HDL = 1
INTERSECTION_HDL = 2
UNION_HDL = 3
SUBTRACTION_HDL = 4
XOR_HDL = 5
check_mesh_HDL = 6


# handle input events
def event(evt, val):

	# exit when user presses Q
	if evt == Draw.QKEY:
		Draw.Exit()


# rotate point using degrees
def degRot(horiP, vertP, degrees):

	hUc = math.cos(degrees * (math.pi * 2.0 / 360.0))
	vUc = math.sin(degrees * (math.pi * 2.0 / 360.0))

	hLine1 = hUc
	vLine1 = vUc
	hLine2 = -vUc
	vLine2 = hUc

	h = vertP * hLine2 + horiP * vLine2
	v = horiP * vLine1 + vertP * hLine1
	horiP = h
	vertP = v

	return (horiP, vertP)


def applyTrans(mesh, x, y, z):

	# apply scale
	x *= mesh.size[0]
	y *= mesh.size[1]
	z *= mesh.size[2]

	# apply rotation
	y, z = degRot(y, z, mesh.rot[0] / (math.pi * 2.0 / 360.0)) # x rot
	x, z = degRot(x, z, -mesh.rot[1] / (math.pi * 2.0 / 360.0)) # y rot
	x, y = degRot(x, y, mesh.rot[2] / (math.pi * 2.0 / 360.0)) # z rot

	# apply object location
	x += mesh.loc[0]
	y += mesh.loc[1]
	z += mesh.loc[2]
	
	return x, y, z


def getFmtMeshData(mesh, coords, tris, labels, triCnt):

	if triCnt == 0:
		label = 0
	else:
		label = 1

	iTri=triCnt
	for f in mesh.getData().faces:
		if len(f.v) == 4:
		
			x1, y1, z1 = applyTrans(mesh, f.v[0].co[0], f.v[0].co[1], f.v[0].co[2])
			x2, y2, z2 = applyTrans(mesh, f.v[1].co[0], f.v[1].co[1], f.v[1].co[2])
			x3, y3, z3 = applyTrans(mesh, f.v[2].co[0], f.v[2].co[1], f.v[2].co[2])
			x4, y4, z4 = applyTrans(mesh, f.v[3].co[0], f.v[3].co[1], f.v[3].co[2])
			
			coords.append(x1)
			coords.append(y1)
			coords.append(z1)
			tris.append(iTri)
			iTri+=1
			coords.append(x2)
			coords.append(y2)
			coords.append(z2)
			tris.append(iTri)
			iTri+=1
			coords.append(x3)
			coords.append(y3)
			coords.append(z3)
			tris.append(iTri)
			iTri+=1
			labels.append(label)
			
			coords.append(x1)
			coords.append(y1)
			coords.append(z1)
			tris.append(iTri)
			iTri+=1
			coords.append(x3)
			coords.append(y3)
			coords.append(z3)
			tris.append(iTri)
			iTri+=1
			coords.append(x4)
			coords.append(y4)
			coords.append(z4)
			tris.append(iTri)
			iTri+=1
			labels.append(label)
			
		if len(f.v) == 3:
			for v in f.v:
				x, y, z = applyTrans(mesh, v.co[0], v.co[1], v.co[2])
				coords.append(x)
				coords.append(y)
				coords.append(z)
				tris.append(iTri)
				iTri+=1
			labels.append(label)
			
	triCnt=iTri
	return coords, tris, labels, triCnt


def boolOp(boolOpType, newMeshName):

	# change to object mode
	in_editmode = Window.EditMode()
	if in_editmode: Window.EditMode(0)

	scene = bpy.data.scenes.active
	
	if (len(scene.objects.selected) < 2):
		print("Two meshes are needed for boolean operations.")
		return
	
	if (scene.objects.active == scene.objects.selected[0]):
		meshA = scene.objects.selected[0]
		meshB = scene.objects.selected[1]
	else:
		meshA = scene.objects.selected[1]
		meshB = scene.objects.selected[0]
	
	coords = []
	tris = []
	labels = []
	triCnt = 0
	coords, tris, labels, triCnt = getFmtMeshData(meshA, coords, tris, labels, triCnt)
	coords, tris, labels, triCnt = getFmtMeshData(meshB, coords, tris, labels, triCnt)
	
	coord_list, tri_list, label_list = booleanOp(coords, tris, labels, boolOpType)
	
	verts = []
	for i in range(0, len(coord_list), 3):
		x = coord_list[i+0] - meshA.loc[0]
		y = coord_list[i+1] - meshA.loc[1]
		z = coord_list[i+2] - meshA.loc[2]
		verts.append([x, y, z])
	
	faces = []
	for i in range(0, len(tri_list), 3):
		faces.append([tri_list[i+0], tri_list[i+1], tri_list[i+2]])
	
	BPyAddMesh.add_mesh_simple(newMeshName, verts, [], faces)

def mCheck():

	# change to object mode
	in_editmode = Window.EditMode()
	if in_editmode: Window.EditMode(0)

	scene = bpy.data.scenes.active
	
	if (len(scene.objects.selected) < 1):
		print("Needs a mesh.")
		return
	
	mesh = scene.objects.active
	
	coords = []
	for v in mesh.getData().verts:
		x, y, z = applyTrans(mesh, v[0], v[1], v[2])
		coords.append(x)
		coords.append(y)
		coords.append(z)
	
	tris = []
	for f in mesh.getData().faces:
		if len(f.v) == 3:
			tris.append(f[0].index)
			tris.append(f[1].index)
			tris.append(f[2].index)
		if len(f.v) == 4:
			tris.append(f[0].index)
			tris.append(f[1].index)
			tris.append(f[2].index)
			tris.append(f[0].index)
			tris.append(f[2].index)
			tris.append(f[3].index)

	checkVal = meshCheck(coords, tris)

	meshCheckMsg = "Mesh Check:"
	if (not checkVal&1):
		meshCheckMsg += "|Failed the manifold test."

	if (not checkVal&2):
		meshCheckMsg += "|Failed the watertight test."

	if (not checkVal&4):
		meshCheckMsg += "|Failed the intersection test."

	if (checkVal == 7):
		meshCheckMsg += "|Good."
	
	Draw.PupMenu(meshCheckMsg)

# handle button events
def button_event(evt):

	INTERSECTION = 0
	UNION = 1
	SUBTRACTION = 2
	XOR = 3
	
	if evt == INTERSECTION_HDL:
		boolOp(INTERSECTION, "INTER")
	
	if evt == UNION_HDL:
		boolOp(UNION, "UNION")
	
	if evt == SUBTRACTION_HDL:
		boolOp(SUBTRACTION, "SUB")
	
	if evt == XOR_HDL:
		boolOp(XOR, "XOR")
	
	if evt == check_mesh_HDL:
		mCheck()
	
	if evt == exit_HDL:
		Draw.Exit()
	
	Window.RedrawAll() # update windows
	

# draw to screen
def gui():
	
	BGL.glClearColor(0.72,0.7,0.7,1)
	BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
	BGL.glColor3f(0.25,0.25,0.25)
	
	x = 10
	y = 5
	Draw.Button("XOR", XOR_HDL, x, y, 155, 25, "")
	
	y += 30
	Draw.Button("INTERSECTION", INTERSECTION_HDL, x, y, 155, 25, "")
	
	y += 30
	Draw.Button("SUBTRACTION", SUBTRACTION_HDL, x, y, 155, 25, "")
	
	y += 30
	Draw.Button("UNION", UNION_HDL, x, y, 155, 25, "")
	
	y += 30
	BGL.glRasterPos2i(x, y)
	Draw.Text("Boolean Operations:")

	x2 = 175
	y2 = 5
	Draw.Button("Exit", exit_HDL, x2, y2, 155, 25, "End this python script.")
	
	y2 += 30
	Draw.Button("Check Mesh", check_mesh_HDL, x2, y2, 155, 25, "")
	

# registering callbacks
Draw.Register(gui, event, button_event)

