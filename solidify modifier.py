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


bottom = bpy.data.objects["bottom_layer"]
modifier = bottom.modifiers.new(name="Solidify", type="SOLIDIFY")
modifier.thickness = 0.254
bottom.select_set(True)
bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Solidify")
bottom.select_set(False)


top = bpy.data.objects["top_layer"]
modifier = top.modifiers.new(name="Solidify", type="SOLIDIFY")
modifier.thickness = 0.254
top.select_set(True)
bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Solidify")
top.select_set(False)


    
revealAll()
   

       