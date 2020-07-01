import bpy


##
# Generates a starting material \(base-color, mettalic, specular_intensity, and roughness\) for each of the layers of the PCB and applies said material\n
# @param object -the object to which the material will be applied
# @param name -string of a unique name for the material
# @param rgba -a tuple of floats representing the red-green-blue-alpha value for the base coloring
# @param metallic -a float for the percentage of metallic texture
# @param specular -a float for the percentage of specular-intensity \(reflected light\)
# @param roughness -a float for the percentage of roughness in the texture \(surface divisions for specular intensity\)
def create_material(layer, name="material_name", rgba=(0.0, 0.0, 0.0, 1.0), metallic=0.5, specular=0.5, roughness=0.5):
       # make sure computer thinks the mouse is in the right location, avoid ...poll() errors.
    for area in bpy.context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"

    bpy.context.view_layer.objects.active = layer
    material = bpy.data.materials.new(name)
    material.diffuse_color = rgba
    material.metallic = metallic
    material.specular_intensity = specular
    material.roughness = roughness
    layer.data.materials.append(material)
                    
    for area in bpy.context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "SOLID"




# run for a single selected oject
layer = bpy.context.selected_objects[0]
if layer.name.startswith("board_outline"):
    create_material(layer, "board", (0.062, 0.296, 0.020, 0.99), 0.234, 0.235, 0.202) 
elif layer.name.startswith("bottom_solder") or layer.name.startswith("bottom_layer") or layer.name.startswith("top_layer"):
    create_material(layer, "metal", (0.391, 0.521, 0.627, 1.0), 0.849, 0.279, 0.245)
elif layer.name.startswith("silk_screen"):
    create_material(layer, "silk_screen", (0.513, 0.627, 0.552, 1.0), 0.234, 0.500, 0.202)
            
            