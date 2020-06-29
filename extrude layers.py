

import bpy
import bmesh
import math
from mathutils import Vector




 ##
 # Turns visibility off for all objects           
def hideAll():
    for layer in bpy.data.objects:
        layer.select_set(False)
        layer.hide_set(True) 



def fullDisplay():
    for layer in bpy.data.objects:
        layer.hide_set(False)

##
# Removes the overlapping vertices on all layers
def removeExtraVerts(layer):
    #bpy.ops.object.select_all(action="SELECT")
    #obj = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = layer
    bpy.ops.object.editmode_toggle()

    # remove duplicate vertices
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.object.editmode_toggle()




##
# Finds the vertex closest to the origin \(that has to be in the board outline\) and removes all the vertices connected to it.
def removeOutline(layer):
    bpy.context.view_layer.objects.active = layer
    min = layer.data.vertices[0]
    minDistance = math.sqrt(min.co[0] **2 + min.co[1]**2)
    for vert in layer.data.vertices:
        vertDistance = math.sqrt(vert.co[0] **2 + vert.co[1]**2)
        if(vertDistance < minDistance):
            min = vert
            minDistance = vertDistance       
    min.select = True
    bpy.ops.object.editmode_toggle()
    #mesh = bmesh.from_edit_mesh(layer.data)
    bpy.ops.mesh.select_linked()
    bpy.ops.mesh.delete(type="VERT")
    bpy.ops.object.editmode_toggle()
    




def extrudeLayers():
    bpy.ops.object.select_all(action="DESELECT")
    for layer in bpy.data.objects:
        if layer.name == "board_outline":
            bpy.context.view_layer.objects.active = layer
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.edge_face_add()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0, 0, 2.4))})
            bpy.ops.object.editmode_toggle()
        elif layer.name == "bottom_solder":
            bpy.context.view_layer.objects.active = layer
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.editmode_toggle()
            layer.location.z = -0.01
        elif layer.name == "bottom_layer":
            bpy.context.view_layer.objects.active = layer
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0, 0, 0.8))})
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.editmode_toggle()
            layer.location.z = 0.2
        elif layer.name == "top_layer":
            bpy.context.view_layer.objects.active = layer
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0, 0, 0.8))})
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.editmode_toggle()
            layer.location.z = 1.4
        elif layer.name == "top_solder":
            bpy.context.view_layer.objects.active = layer
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.edge_face_add()
            bpy.ops.mesh.flip_normals()
            bpy.ops.object.editmode_toggle()
            layer.location.z = 2.41
        elif layer.name == "silk_screen":
            bpy.context.view_layer.objects.active = layer
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0.1, 0.1, 0))})
            bpy.ops.object.editmode_toggle()
            layer.location.z = 2.41
        elif layer.name == "drill_holes":
            bpy.context.view_layer.objects.active = layer
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.edge_face_add()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0, 0, 2.8))})
            bpy.ops.object.editmode_toggle()
            layer.location.z = -0.2





# run the methods
bpy.ops.object.select_all(action="SELECT")
for layer in bpy.context.selected_objects:
    if layer.name != "board_outline":
        removeExtraVerts(layer)
        removeOutline(layer)
    else:
        removeExtraVerts(layer)


extrudeLayers()


