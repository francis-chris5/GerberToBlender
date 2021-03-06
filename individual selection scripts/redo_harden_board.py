import bpy



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




##
# Turns on all objects which are part of the PCB, this excludes the drill_holes tool object
def revealAll():
    for layer in bpy.data.objects:
        layer.select_set(False)
        if layer.name == "drill_holes":
            layer.hide_set(True)
        else:
            layer.hide_set(False)



harden()


