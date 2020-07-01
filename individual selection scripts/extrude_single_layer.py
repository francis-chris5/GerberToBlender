

import bpy
import bmesh
import math
from mathutils import Vector





##
# Removes the overlapping vertices on all layers
def removeExtraVerts(layer):
    bpy.context.view_layer.objects.active = layer
    bpy.ops.object.editmode_toggle()
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
    bpy.ops.mesh.select_linked()
    bpy.ops.mesh.delete(type="VERT")
    bpy.ops.object.editmode_toggle()
    





##
# extrudes all components and sets the vertical position of each layer
def extrude_layer(layer):
    if layer.name.startswith("board_outline"):
        removeExtraVerts(layer)
    else:
        removeExtraVerts(layer)
        removeOutline(layer)
        
    if layer.name.startswith("board_outline"):
        bpy.context.view_layer.objects.active = layer
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0, 0, 2.4))})
        bpy.ops.object.editmode_toggle()
    elif layer.name.startswith("bottom_solder"):
        bpy.context.view_layer.objects.active = layer
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.editmode_toggle()
        layer.location.z = -0.01
    elif layer.name.startswith("bottom_layer"):
        bpy.context.view_layer.objects.active = layer
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0, 0, 0.8))})
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.editmode_toggle()
        layer.location.z = 0.2
    elif layer.name.startswith("top_layer"):
        bpy.context.view_layer.objects.active = layer
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0, 0, 0.8))})
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.editmode_toggle()
        layer.location.z = 1.4
    elif layer.name.startswith("top_solder"):
        bpy.context.view_layer.objects.active = layer
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.editmode_toggle()
        layer.location.z = 2.41
    elif layer.name.startswith("silk_screen"):
        bpy.context.view_layer.objects.active = layer
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0.2, 0.2, 0))})
        bpy.ops.object.editmode_toggle()
        layer.location.z = 2.41
    elif layer.name.startswith("drill_holes"):
        bpy.context.view_layer.objects.active = layer
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0, 0, 2.8))})
        bpy.ops.object.editmode_toggle()
        layer.location.z = -0.2



layer = bpy.context.selected_objects[0]
extrude_layer(layer)


