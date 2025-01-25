#!BPY

"""
Name: 'Quick Py'
Blender: 249b
Group: 'Misc'
Tooltip: 'Execute any python script with a click of a button.'
"""

__bpydoc__ = """\
Execute any python script with a click of a button.

1. Create a folder called "quickPy" next to your *.blend file.

2. Add blender python scripts to the "quickPy" folder.

3. Run this script found in "Misc".
"""

from Blender import *
from random import *
import math
import bpy
import os

btn_text = ["Exit"]
btn_HDL = list(range(0, 32))
script_path = [""]

# handle input events
def event(evt, val):

	# exit when user presses Q
	if evt == Draw.QKEY:
		Draw.Exit()

# handle button events
def button_event(evt):
	global script_path
	
	for i in range(1, len(script_path)+1):
	    if evt == btn_HDL[i]:
	        Run(script_path[i])
	
	if evt == btn_HDL[0]:
		Draw.Exit()
	

# draw to screen
def gui():
	global btn_HDL
	global btn_text
	
	BGL.glClearColor(0.72,0.7,0.7,1)
	BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
	BGL.glColor3f(0.25,0.25,0.25)
	x = 10
	y = 5
	
	for i in range(0, len(btn_text)):
	    Draw.Button(btn_text[i], btn_HDL[i], x, y+30*i, 10*len(btn_text[i]), 25, "") #btn_hint[i])
    

# get the current scene
scene = Scene.GetCurrent()

# Get the scripts filepath
file_path = Get('filename')
directory = os.path.dirname(file_path)
py_path = os.path.join(directory, 'quickPy')

if not os.path.exists(py_path):
    Draw.PupMenu("'quickPy' folder does not exist.")
else:
    result = Draw.PupMenu("User Script Directory will be modifed?%t|OK|Cancel")
    
    if result == 1:
        bpy.config.userScriptsDir = py_path

        py_path = bpy.config.userScriptsDir

        py_scripts = [f for f in os.listdir(py_path) if f.endswith('.py')]

        if len(py_scripts) < 32:
            for i in range(0, len(py_scripts)):
                btn_text.append(py_scripts[i])
                script_path.append(os.path.join(py_path, py_scripts[i]))

        # registering callbacks
        Draw.Register(gui, event, button_event)

