import bpy


##
# Applies a thickness to the 2d \(extruded along z by this point\) curves representing the traces for the top and bottom layer in the PCB, only run this for top_layer or bottom_layer
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




layer = bpy.context.selected_objects[0]
solidify(layer.name, 0.254)

       