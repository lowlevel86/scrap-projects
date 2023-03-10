#!BPY

"""
Name: 'Quick Vertex Color Editor'
Blender: 249
Group: 'Mesh'
Tip: 'Quickly editor vertex colors in edit mode.'
"""

__bpydoc__ = """\
Quickly editor vertex colors in edit mode.

Note: Make sure 'Draw type' is set to Textured.

You can use the 'tab' key in the 3D View to go in and out of Edit Mode.

A new material may need to be created for a duplicated object if a separate alpha or emit value is needed.

"""


from Blender import *
from random import *
import math
import bpy


emit_value = 0.0
alpha_value = 1.0
vCol_value = (0.4, 0.4, 0.8)
vari_value = 0.0

exit_HDL = 1
emitSlider_HDL = 2
alphaSlider_HDL = 3
colorPick_HDL = 4
variSlider_HDL = 5


def updateVCol(evt, val):
	global vCol_value
	global vari_value
	
	Window.WaitCursor(1)
	vCol_value = val

	# Get the active object
	sce = bpy.data.scenes.active
	ob = sce.objects.active

	# checking object
	if not ob or ob.type != 'Mesh':
		return 

	if not Window.EditMode():
		Draw.PupMenu("   Must be in 'Edit Mode'.   ")
		return

	me = ob.getData(mesh=1)

	if (me.materials == []) or (me.materials == [None]):
		if (ob.getMaterials(-1) == []):
			ob.setMaterials([Material.New('Material')])
			ob.colbits = 1
		mat = ob.getMaterials(-1)[0]
	else:
		mat = me.materials[0]
	
	Window.EditMode(0)

	mat.mode |= Material.Modes.VCOL_PAINT
	me.vertexColors = 1

	for f in me.faces:
		if len(f.v) == 3:
			randVal = (random() - 0.5) * vari_value
			rCol = vCol_value[0] + randVal
			gCol = vCol_value[1] + randVal
			bCol = vCol_value[2] + randVal
			if rCol > 1.0: rCol = 1.0
			if gCol > 1.0: gCol = 1.0
			if bCol > 1.0: bCol = 1.0
			if rCol < 0.0: rCol = 0.0
			if gCol < 0.0: gCol = 0.0
			if bCol < 0.0: bCol = 0.0
			for i in range(0, 3):
				if f.verts[i].sel:
					f.col[i].r = int(round(rCol * 255))
					f.col[i].g = int(round(gCol * 255))
					f.col[i].b = int(round(bCol * 255))
		if len(f.v) == 4:
			randVal = (random() - 0.5) * vari_value
			rCol = vCol_value[0] + randVal
			gCol = vCol_value[1] + randVal
			bCol = vCol_value[2] + randVal
			if rCol > 1.0: rCol = 1.0
			if gCol > 1.0: gCol = 1.0
			if bCol > 1.0: bCol = 1.0
			if rCol < 0.0: rCol = 0.0
			if gCol < 0.0: gCol = 0.0
			if bCol < 0.0: bCol = 0.0
			for i in range(0, 4):
				if f.verts[i].sel:
					f.col[i].r = int(round(rCol * 255))
					f.col[i].g = int(round(gCol * 255))
					f.col[i].b = int(round(bCol * 255))
	
	Window.EditMode(1)
	Window.WaitCursor(0)


def updateObjEmitVal(evt, val):
	global emit_value

	Window.WaitCursor(1)
	emit_value = val

	# Get the active object
	sce = bpy.data.scenes.active
	ob = sce.objects.active

	# checking object
	if not ob or ob.type != 'Mesh':
		return 

	me = ob.getData(mesh=1)

	if (me.materials == []) or (me.materials == [None]):
		if (ob.getMaterials(-1) == []):
			ob.setMaterials([Material.New('Material')])
			ob.colbits = 1
		mat = ob.getMaterials(-1)[0]
	else:
		mat = me.materials[0]
	
	# saves the editmode state and go's out of editmode
	editmode_state = Window.EditMode()
	if editmode_state: Window.EditMode(0)

	mat.setEmit(emit_value)

	# restore editmode if it was enabled
	if editmode_state: Window.EditMode(1)

	Window.WaitCursor(0)


def updateObjAlphaVal(evt, val):
	global alpha_value

	Window.WaitCursor(1)
	alpha_value = val

	# Get the active object
	sce = bpy.data.scenes.active
	ob = sce.objects.active

	# checking object
	if not ob or ob.type != 'Mesh':
		return 

	me = ob.getData(mesh=1)

	if (me.materials == []) or (me.materials == [None]):
		if (ob.getMaterials(-1) == []):
			ob.setMaterials([Material.New('Material')])
			ob.colbits = 1
		mat = ob.getMaterials(-1)[0]
	else:
		mat = me.materials[0]
	
	# saves the editmode state and go's out of editmode
	editmode_state = Window.EditMode()
	if editmode_state: Window.EditMode(0)

	mat.mode |= Material.Modes.ZTRANSP
	mat.setAlpha(alpha_value)

	# restore editmode if it was enabled
	if editmode_state: Window.EditMode(1)

	Window.WaitCursor(0)

def updateVari(evt, val):
    global vari_value
    
    vari_value = val


# handle input events
def event(evt, val):
	global emit_value
	global alpha_value

	# exit when user presses Q
	if evt == Draw.QKEY:
		Draw.Exit()

	# Get the active object
	sce = bpy.data.scenes.active
	ob = sce.objects.active

	# checking object
	if not ob or ob.type != 'Mesh':
		return 

	me = ob.getData(mesh=1)

	if (me.materials == []) or (me.materials == [None]):
		if (ob.getMaterials(-1) == []):
			return
		mat = ob.getMaterials(-1)[0]
	else:
		mat = me.materials[0]
	
	if (emit_value != mat.emit):
		emit_value = mat.getEmit()
		Draw.Redraw(1)
	
	if (alpha_value != mat.getAlpha()):
		alpha_value = mat.getAlpha()
		Draw.Redraw(1)

# handle button events
def button_event(evt):

	if evt == emitSlider_HDL:
		Window.RedrawAll()
	
	if evt == alphaSlider_HDL:
		Window.RedrawAll()
	
	if evt == colorPick_HDL:
		Window.RedrawAll()
	
	if evt == variSlider_HDL:
		Window.RedrawAll()
	
	if evt == exit_HDL:
		Draw.Exit()
	

# draw to screen
def gui():
	global colorPick_HDL
	
	BGL.glClearColor(0.72,0.7,0.7,1)
	BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
	BGL.glColor3f(0.25,0.25,0.25)
	
	x = 10
	y = 5
	Draw.Button("Exit", exit_HDL, x, y, 155, 25, "End this python script.")

	y += 30
	Draw.Slider("Emit ", emitSlider_HDL, x, y, 155, 25, emit_value, 0.0, 1.0, 0, "", updateObjEmitVal)
	
	y += 30
	Draw.Slider("Alpha ", alphaSlider_HDL, x, y, 155, 25, alpha_value, 0.0, 1.0, 0, "", updateObjAlphaVal)

	y += 30
	BGL.glRasterPos2i(x, y)
	Draw.Text("Material Controls")
	
	y += 20
	Draw.ColorPicker(colorPick_HDL, x, y, 155, 25, vCol_value, "", updateVCol)
	
	y += 30
	BGL.glRasterPos2i(x, y)
	Draw.Text("Choose Vertex Color")
	
	y += 15
	Draw.Slider("Vari ", variSlider_HDL, x, y, 155, 25, vari_value, 0.0, 1.0, 0, "", updateVari)
	

	y = 90
	BGL.glRasterPos2i(180, y)
	Draw.Text("QUICK VERTEX COLOR EDITOR")
	y -= 15
	BGL.glRasterPos2i(180, y)
	Draw.Text("Note: Make sure 'Draw type' is set to Textured.")
	y -= 15
	BGL.glRasterPos2i(180, y)
	Draw.Text("You can use the 'tab' key in the 3D View to go in and out of Edit Mode.")


# registering callbacks
Draw.Register(gui, event, button_event)

