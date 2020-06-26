
##
# @mainpage
# @section description Description
# This module contains methods to import svg file exports from a collection of Gerber files and automatically turns the imports into a 3D model of the PCB in Blender.\n
# For putting it together and only testing so far, the PCB was designed using EasyEDA online circuit editing software. The exported Gerber files were opened in gerbv Gerber Viewer software, from which the SVG files were exported. The components of the model will be named identical to the SVG files.
# @section Author
# Developed By: Christopher S. Francis 25 June 2020 to ...



import bpy


##
# The directory where the SVG files are located \(this needs to be automated somehow\)
directory = "C:/Users/Chris/Documents/AB_Controller/Documentation/Model"

##
# The list of SVG files to import \(this should probably be handled from an __init__.py file\)
files = ["board_outline.svg", "bottom_solder.svg", "bottom_layer.svg", "top_layer.svg", "top_solder.svg", "drill_holes.svg", "silk_screen.svg"]



##
# Brings in the SVG file, applies the x and y orientation, converts the curves to meshes, scales it to 1 meter in blender equals 1 millimeter in the real world, and places the objects into a collection ... \(still to come: extrusions, height placement, materials, cut the holes, and join a copy into a completed version\)\n
# Uses Blender 2.8.2 or higher API
# @param dir -the directory where the files are located
# @param file -the list of SVG files representing the Gerber Files / PCB
def import_svg(dir, file):
    bpy.ops.import_curve.svg(filepath=(dir + "/" + file))


    context = bpy.context
    scene = context.scene

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

    


   







for f in files:
    import_svg(directory, f)




""" WORKED

bpy.ops.import_curve.svg(filepath="C:/Users/Chris/Documents/AB_Controller/Documentation/Model/bottom_layer.svg")


context = bpy.context
scene = context.scene

col = bpy.data.collections.get("bottom_layer.svg")
if col:
    for obj in col.objects:    
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        obj.to_mesh(preserve_all_data_layers=True)
        

bpy.ops.object.join()
layer = bpy.context.selected_objects[0]
layer.name = "bottom_layer"
layer.scale = (1000, 1000, 1000)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)



bpy.ops.object.move_to_collection(collection_index = 0, is_new = True, new_collection_name="layers")

col = bpy.data.collections.get("bottom_layer.svg")
if col:
    bpy.data.collections.remove(col)
    
"""