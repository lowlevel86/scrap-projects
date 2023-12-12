#!BPY

"""
Name: '3D Mesh Data (.txt)...'
Blender: 249
Group: 'Export'
Tip: 'Export to mesh data.'
"""

import Blender
from Blender import Window
import math


# script main function
def ExportToC(file_name):
   file = open(file_name, "w")
   
   scene = Blender.Scene.GetCurrent()
   meshes = []
   for ob in scene.objects:
      obtype = ob.type
      if obtype == "Mesh":
         meshes.append(ob)
   
   #Sort meshes alphabetically
   meshNames = []
   sortedMeshNames = []
   for mesh in meshes:
      meshNames.append(mesh.getName())
      sortedMeshNames.append(mesh.getName())
   
   sortedMeshNames.sort()
   
   sortedMeshes = []
   for sortedMeshName in sortedMeshNames:
      sortedMeshes.append(meshes[meshNames.index(sortedMeshName)])
   meshes = sortedMeshes


   global meshCnt
   global meshPointDataCnt
   
   # change to object mode
   in_editmode = Window.EditMode()
   if in_editmode: Window.EditMode(0)


   contentName = Blender.sys.splitext(Blender.sys.basename(file_name))[0]
   
   
   # print the names of the objects
   i = 0
   obj_names = []
   file.write("obj_names %i\n" % (len(meshes)))
   for mesh in meshes:
      file.write("\"")
      n = ""
      for objNameChar in mesh.getName():
         if objNameChar != ".":
            file.write("%c" % (objNameChar))
            n += objNameChar
         else:
            file.write("%c" % ("_"))
            n += "_"
      obj_names.append(n)
      file.write("\",\n")
      i += 1
   file.write("\n\n")

   
   # print the transformation data to file
   iMesh = 0
   file.write("transformation data\n")
   file.write("x, y, z, size\n")
   file.write("x, y, z, rotation\n")
   file.write("x, y, z, location\n")
   for mesh in meshes:
      file.write("%s_TD 9\n" % (obj_names[iMesh]))
      file.write("%f, %f, %f,\n" % (mesh.size[0], mesh.size[1], mesh.size[2]))
      file.write("%f, %f, %f,\n" % (mesh.rot[0]*180.0/math.pi, mesh.rot[1]*180.0/math.pi, mesh.rot[2]*180.0/math.pi))
      file.write("%f, %f, %f,\n" % (mesh.loc[0], mesh.loc[1], mesh.loc[2]))
      file.write("\n")
      iMesh += 1
   file.write("\n")

   # count the number of quads
   quadCount = []
   for mesh in meshes:
      fCnt = 0
      for face in mesh.getData().faces:
         if len(face.v) == 4:
            fCnt += 1
      quadCount.append(fCnt)

   # count the number of trigon
   triCount = []
   for mesh in meshes:
      fCnt = 0
      for face in mesh.getData().faces:
         if len(face.v) == 3:
            fCnt += 1
      triCount.append(fCnt)

   # print quad vertices to file
   iMesh = 0
   for mesh in meshes:
      file.write("%s_quad %i\n" % (obj_names[iMesh], quadCount[iMesh] * 4 * 3))
      for f in mesh.getData().faces:
         if len(f.v) == 4:
            for v in f.v:
               file.write("%f, %f, %f,\n" % (v[0], v[1], v[2]))
      file.write("\n")
      iMesh += 1
   file.write("\n")

   # print triangle vertices to file
   iMesh = 0
   for mesh in meshes:
      file.write("%s_tri %i\n" % (obj_names[iMesh], triCount[iMesh] * 3 * 3))
      for f in mesh.getData().faces:
         if len(f.v) == 3:
            for v in f.v:
               file.write("%f, %f, %f,\n" % (v[0], v[1], v[2]))
      file.write("\n")
      iMesh += 1
   file.write("\n")
   
   
   # print quad color to file
   iMesh = 0
   for mesh in meshes:
      file.write("%s_quad_vcol %i\n" % (obj_names[iMesh], quadCount[iMesh] * 4 * 3))
      for f in mesh.getData().faces:
         if len(f.v) == 4:
            if f.col:
               for i in range(0, 4):
                  file.write("%i, %i, %i, " % (f.col[i].r, f.col[i].g, f.col[i].b))
            else:
               for i in range(0, 4):
                  file.write("%i, %i, %i, " % (255, 255, 255))
            file.write("\n")
      file.write("\n")
      iMesh += 1
   file.write("\n")
   
   # print triangle color to file
   iMesh = 0
   for mesh in meshes:
      file.write("%s_tri_vcol %i\n" % (obj_names[iMesh], triCount[iMesh] * 3 * 3))
      for f in mesh.getData().faces:
         if len(f.v) == 3:
            if f.col:
               for i in range(0, 3):
                  file.write("%i, %i, %i, " % (f.col[i].r, f.col[i].g, f.col[i].b))
            else:
               for i in range(0, 3):
                  file.write("%i, %i, %i, " % (255, 255, 255))
            file.write("\n")
      file.write("\n")
      iMesh += 1
   file.write("\n")
   

   file.close()

   
def FileSelectorCB(file_name):
   if not file_name.lower().endswith('.txt'):
      file_name += '.txt'
   ExportToC(file_name)

if __name__ == '__main__':
   Blender.Window.FileSelector(FileSelectorCB, "Export", Blender.sys.makename(ext='.txt'))