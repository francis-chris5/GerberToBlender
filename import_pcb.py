
import bpy
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
        filenames = []
        directory = self.properties.filepath
        cut = directory.rindex("\\")
        directory = directory[0:cut]        
        with open(directory + "\\filenames.txt", mode="r") as file:
            for line in file:
               filenames.append(line[0:-1])
               
         
        for file in filenames:
            import_svg(directory, file)
            
        return {"FINISHED"}


    
    
def register():
    bpy.utils.register_class(ImportPCB)
    
    
def unregister():
    bpy.utils.unregister_class(ImportPCB)
    
    

if __name__ == "__main__":
    register()
    bpy.ops.pcb.import_svg("INVOKE_DEFAULT")
    






##
# Brings in the SVG file, applies the x and y orientation, converts the curves to meshes, scales it to 1 meter in blender equals 1 millimeter in the real world, and places the objects into a collection ... \(still to come: extrusions, height placement, cut the holes, and join a copy into a completed version\)\n
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
