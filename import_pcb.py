bl_info = {
    "name": "Generate PCB Model",
    "author": "Christopher S. Francis",
    "version": (1, 0),
    "blender": (2, 80, 3),
    "location": "",
    "description": "Imports layers from a Gerber file package in SVG form and generates a model of the given PCB to allow for 3D inspection before ordering",
    "warning": "",
    "wiki_url": "",
    "category": "Add PCB Object",
}


##
# @mainpage
# @section description Description
# This module contains methods to import svg file exports from a collection of Gerber files and automatically turns the imports into a 3D model of the PCB in Blender.\n
# For putting it together and only testing so far, the PCB was designed using EasyEDA online circuit editing software. The exported Gerber files were opened in gerbv Gerber Viewer software, from which the SVG files were exported. The components of the model will be named identical to the SVG files.
# @section Example
# Here are some pictures of example files generated by this plug-in. The first couple are of the resultant board models, one as produced and one with a couple layers turned off. The second set shows the generated board models used with components downloaded from GrabCad.com or modeled myself.\n
# <IMG src="../images/screenshot1.png">
# <IMG src="../images/screenshot2.png">\n
# <IMG src="../images/screenshot3.png">
# <IMG src="../images/screenshot4.png">\n
#\n\n
# Here is a sample output of create_pcb_view.py.\n
# @htmlonly
# <iframe src="../images/pcb.html" width="700" height="300">
# </iframe>
# @endhtmlonly
# @section Author
# Developed By: Christopher S. Francis 25 June 2020 to ...


import bpy
import math
from mathutils import Vector
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty


##
# The ImportPCB class is actually just the file dialog box which has to be an object in the current API when this was written (bpy 2.8.3)\n
class ImportPCB(Operator, ImportHelper):
    bl_idname = "pcb.import_svg"
    bl_label = "Import PCB Folder"
    
    filename_ext = "."
    use_filter_folder = True
    
    def execute(self, context):
        try:
            filenames = []
            directory = self.properties.filepath
            cut = directory.rindex("\\")
            directory = directory[0:cut]        
            with open(directory + "\\filenames.txt", mode="r") as file:
                for line in file:
                   filenames.append(line[0:-1])
                          
            for file in filenames:
                import_svg(directory, file)
            
            bpy.ops.object.select_all(action="SELECT")
            for layer in bpy.context.selected_objects:
                if layer.name != "board_outline":
                    removeExtraVerts(layer)
                    removeOutline(layer)
                else:
                    removeExtraVerts(layer)

            extrudeLayers()
            
            for layer in bpy.data.objects:
                if layer.name == "board_outline":
                    create_material(layer, "board", (0.062, 0.296, 0.020, 0.99), 0.234, 0.235, 0.202) 
                elif layer.name == "bottom_solder":
                    create_material(layer, "metal", (0.391, 0.521, 0.627, 1.0), 0.849, 0.279, 0.245)
                elif layer.name == "bottom_layer":
                    create_material(layer, "metal", (0.391, 0.521, 0.627, 1.0), 0.849, 0.279, 0.245)
                elif layer.name == "top_layer":
                    create_material(layer, "metal", (0.391, 0.521, 0.627, 1.0), 0.849, 0.279, 0.245)
                elif layer.name == "top_solder":
                    create_material(layer, "metal", (0.391, 0.521, 0.627, 1.0), 0.849, 0.279, 0.245)
                elif layer.name == "silk_screen":
                    create_material(layer, "silk_screen", (0.513, 0.627, 0.552, 1.0), 0.234, 0.500, 0.202)
            
            solidify("bottom_layer", 0.254)
            solidify("top_layer", 0.254)
            
            drill_layer("board_outline")
            drill_layer("bottom_solder")
            drill_layer("bottom_layer")
            drill_layer("top_layer")
            drill_layer("top_solder")
            drill_layer("silk_screen")
            
            harden()
        except:
            bpy.ops.pcb.import_error("INVOKE_DEFAULT")

        return {"FINISHED"}






##
# Dialog box to handle error messages
class ErrorDialog(Operator):
    bl_idname = "pcb.import_error"
    bl_label = "Import PCB Error"

    text = StringProperty(name="An Error Occurred", default="Please Try Again")
    
    def execute(self, context):
        return {"FINISHED"}    
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)






    
##
# Adds this class to the list the bpy module knows about, necessary to run it\n
# in later versions register it to whichever menu or panel it will be called from
def register():
    bpy.utils.register_class(ImportPCB)
    bpy.utils.register_class(ErrorDialog)







##
# Removes this class from the list the bpy module knows about 
def unregister():
    bpy.utils.unregister_class(ImportPCB)
    bpy.utils.unregister_class(ErrorDialog)
    





##
# Turns visibility off for all objects           
def hideAll():
    for layer in bpy.data.objects:
        layer.select_set(False)
        layer.hide_set(True) 





##
# Turns on all objects which are part of the PCB, this excludes the drill_holes tool object
def revealAll():
    for layer in bpy.data.objects:
        layer.select_set(False)
        if layer.name == "drill_holes":
            layer.hide_set(True)
        else:
            layer.hide_set(False)





##
# Brings in the SVG file, applies the x and y orientation, converts the curves to meshes, scales it to 1 meter in blender equals 1 millimeter in the real world, and places the objects into a collection ... \(still to come: extrusions, height placement, cut the holes, and join a copy into a completed version\)\n
# Uses Blender 2.8.2 or higher API
# @param dir -the directory where the files are located
# @param file -the list of SVG files representing the Gerber Files / PCB
def import_svg(dir, file):
    bpy.ops.import_curve.svg(filepath=(dir + "/" + file))

    col = bpy.data.collections.get(file)
    if col:
        for obj in col.objects:    
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            obj.to_mesh(preserve_all_data_layers=True)
               
    bpy.ops.object.join()
    layer = bpy.context.selected_objects[0]
    layer.name = file[0:-4]
    layer.scale = (2814.5, 2814.5, 2814.5)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.convert(target="MESH") 

    if "layers" not in bpy.data.collections:
        bpy.ops.object.move_to_collection(collection_index = 0, is_new = True, new_collection_name="layers")
    else:
        bpy.data.collections["layers"].objects.link(layer)

    col = bpy.data.collections.get(file)
    if col:
        bpy.data.collections.remove(col)
    col = bpy.data.collections.get("layers")
    if col:
        for obj in col.objects:
            obj.select_set(False)
			


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
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":Vector((0.2, 0.2, 0))})
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










##
# Generates a starting material \(base-color, mettalic, specular_intensity, and roughness\) for each of the layers of the PCB and applies said material\n
# @param object -the object to which the material will be applied
# @param name -string of a unique name for the material
# @param rgba -a tuple of floats representing the red-green-blue-alpha value for the base coloring
# @param metallic -a float for the percentage of metallic texture
# @param specular -a float for the percentage of specular-intensity \(reflected light\)
# @param roughness -a float for the percentage of roughness in the texture \(surface divisions for specular intensity\)
def create_material(layer, name="material_name", rgba=(0.0, 0.0, 0.0, 1.0), metallic=0.5, specular=0.5, roughness=0.5):
       # make sure computer thinks the mouse is in the right location, avoid ...poll() errors.
    for area in bpy.context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"

    bpy.context.view_layer.objects.active = layer
    material = bpy.data.materials.new(name)
    material.diffuse_color = rgba
    material.metallic = metallic
    material.specular_intensity = specular
    material.roughness = roughness
    layer.data.materials.append(material)
                    
    for area in bpy.context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "SOLID"










##
# Applies a thickness to the 2d \(extruded along z by this point\) curves representing the traces for the top and bottom layer in the PCB
# @param layer -string name of the layer of the board to apply modifier to
# @param thickness -the width of the trace in the design
def solidify(layer_name, thickness):
    for area in bpy.context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "SOLID"

    layer = bpy.data.objects[layer_name]
    modifier = layer.modifiers.new(name="Solidify", type="SOLIDIFY")
    modifier.thickness = thickness
    bpy.context.view_layer.objects.active = layer
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Solidify")









##
# creates a drill hole through an individual layer of the pcb
# @param layer_name -the layer to drill the holes in
def drill_layer(layer_name):
    for area in bpy.context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "SOLID"
    
    layer = bpy.data.objects[layer_name]
    modifier = layer.modifiers.new(name="Boolean", type="BOOLEAN")
    modifier.object = bpy.data.objects["drill_holes"]
    bpy.context.view_layer.objects.active = layer
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")









##
# Duplicates all component layers in the pcb and joins them into a single object. It then moves this object out of the layers collection and into the primary collection. The single board is placed at the origin with a geometry-centralized local origin and the layered board is moved off to the side
def harden():
    revealAll()

    for area in bpy.context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "SOLID"

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.duplicate_move()
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")
    board = bpy.context.selected_objects[0]
    board.name = "PCB"
    bpy.data.collections["Collection"].objects.link(board)
    board.location = (0, 0, 0)
    bpy.ops.collection.objects_remove_active(collection="layers")
    for layer in bpy.data.objects:
        if layer.name != "PCB":
            layer.location.x += 100






# run the script
if __name__ == "__main__":
    register()
    bpy.ops.pcb.import_svg("INVOKE_DEFAULT")
    