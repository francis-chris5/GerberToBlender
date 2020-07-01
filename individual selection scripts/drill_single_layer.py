import bpy



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




layer = bpy.context.selected_objects[0]
drill_layer(layer.name)
      