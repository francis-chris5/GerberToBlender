import bpy


##
# Duplicates all component layers in the pcb and joins them into a single object. It then moves this object out of the layers collection and into the primary collection.
def harden():
    context = bpy.context
    scene = context.scene

    layer = bpy.data.objects["bottom_layer"]



    for area in context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"



    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.duplicate_move()
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")
    board = context.selected_objects[0]
    board.name = "PCB"
    bpy.data.collections["Collection"].objects.link(board)
    bpy.ops.transform.translate(value=(100, 0, 0))
    bpy.ops.collection.objects_remove_active(collection="layers")



harden()





