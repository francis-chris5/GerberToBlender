import bpy



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
# Turns visibility off for all objects           
def hideAll():
    for layer in bpy.data.objects:
        layer.select_set(False)
        layer.hide_set(True) 



##
# Applies a thickness to the 2d \(only extruded along z by this point\) curves representing the traces for the top and bottom layer in the PCB
def solidify():
    context = bpy.context
    scene = context.scene

    layer = bpy.data.objects["bottom_layer"]



    for area in context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "SOLID"


    hideAll()


    bottom = bpy.data.objects["bottom_layer"]
    modifier = bottom.modifiers.new(name="Solidify", type="SOLIDIFY")
    modifier.thickness = 0.254
    context.view_layer.objects.active = bottom
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Solidify")
    bottom.select_set(False)



    top = bpy.data.objects["top_layer"]
    modifier = top.modifiers.new(name="Solidify", type="SOLIDIFY")
    modifier.thickness = 0.254
    context.view_layer.objects.active = top
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Solidify")
    top.select_set(False)


        
    revealAll()
    
    
    
solidify()
   

       