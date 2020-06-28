import bpy



##
# Turns on visibility for all objects which are part of the PCB, this excludes the drill_holes tool
def revealAll():
    for layer in bpy.data.objects:
        layer.select_set(False)
        if layer.name == "drill_holes":
            layer.hide_set(True)
        else:
            layer.hide_set(False)
            
     

##
# Turns visibility off on all objects          
def hideAll():
    for layer in bpy.data.objects:
        layer.select_set(False)
        layer.hide_set(True) 





##
# Creates the connection holes through the layers in the PCB
def drill():
    context = bpy.context
    scene = context.scene

    layer = bpy.data.objects["bottom_layer"]


    for area in context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "SOLID"



    hideAll()

    board = bpy.data.objects["board_outline"]
    modifier = board.modifiers.new(name="Boolean", type="BOOLEAN")
    modifier.object = bpy.data.objects["drill_holes"]
    context.view_layer.objects.active = board
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
    board.select_set(False)

    bSolder = bpy.data.objects["bottom_solder"]
    modifier = bSolder.modifiers.new(name="Boolean", type="BOOLEAN")
    modifier.object = bpy.data.objects["drill_holes"]
    context.view_layer.objects.active = bSolder
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
    bSolder.select_set(False)


    bottom = bpy.data.objects["bottom_layer"]
    modifier = bottom.modifiers.new(name="Boolean", type="BOOLEAN")
    modifier.object = bpy.data.objects["drill_holes"]
    context.view_layer.objects.active = bottom
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
    bottom.select_set(False)


    top = bpy.data.objects["top_layer"]
    modifier = top.modifiers.new(name="Boolean", type="BOOLEAN")
    modifier.object = bpy.data.objects["drill_holes"]
    context.view_layer.objects.active = top
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
    top.select_set(False)

    tSolder = bpy.data.objects["top_solder"]
    modifier = tSolder.modifiers.new(name="Boolean", type="BOOLEAN")
    modifier.object = bpy.data.objects["drill_holes"]
    context.view_layer.objects.active = tSolder
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
    tSolder.select_set(False)


    silk = bpy.data.objects["silk_screen"]
    modifier = silk.modifiers.new(name="Boolean", type="BOOLEAN")
    modifier.object = bpy.data.objects["drill_holes"]
    context.view_layer.objects.active = silk
    bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
    silk.select_set(False)


        
    revealAll()
   




drill()

       