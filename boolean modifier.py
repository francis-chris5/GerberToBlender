import bpy

context = bpy.context
scene = context.scene

layer = bpy.data.objects["bottom_layer"]


def revealAll():
    for layer in bpy.data.objects:
        layer.select_set(False)
        if layer.name == "drill_holes":
            layer.hide_set(True)
        else:
            layer.hide_set(False)
            
     
            
def hideAll():
    for layer in bpy.data.objects:
        layer.select_set(False)
        layer.hide_set(True) 



for area in context.screen.areas: 
    if area.type == "VIEW_3D":
        for space in area.spaces: 
            if space.type == "VIEW_3D":
                space.shading.type = "SOLID"



hideAll()

board = bpy.data.objects["board_outline"]
modifier = board.modifiers.new(name="Boolean", type="BOOLEAN")
modifier.object = bpy.data.objects["drill_holes"]
board.select_set(True)
bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
board.select_set(False)

bSolder = bpy.data.objects["bottom_solder"]
modifier = bSolder.modifiers.new(name="Boolean", type="BOOLEAN")
modifier.object = bpy.data.objects["drill_holes"]
bSolder.select_set(True)
bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
bSolder.select_set(False)


bottom = bpy.data.objects["bottom_layer"]
modifier = bottom.modifiers.new(name="Boolean", type="BOOLEAN")
modifier.object = bpy.data.objects["drill_holes"]
bottom.select_set(True)
bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
bottom.select_set(False)


top = bpy.data.objects["top_layer"]
modifier = top.modifiers.new(name="Boolean", type="BOOLEAN")
modifier.object = bpy.data.objects["drill_holes"]
top.select_set(True)
bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
top.select_set(False)

tSolder = bpy.data.objects["top_solder"]
modifier = tSolder.modifiers.new(name="Boolean", type="BOOLEAN")
modifier.object = bpy.data.objects["drill_holes"]
tSolder.select_set(True)
bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
tSolder.select_set(False)


silk = bpy.data.objects["silk_screen"]
modifier = silk.modifiers.new(name="Boolean", type="BOOLEAN")
modifier.object = bpy.data.objects["drill_holes"]
silk.select_set(True)
bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
silk.select_set(False)


    
revealAll()
   

       