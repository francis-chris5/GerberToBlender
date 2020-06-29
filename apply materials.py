import bpy



##
# Generates a starting material \(base-color, mettalic, specular_intensity, and roughness\) for each of the layers of the PCB and applies said material\n
# Final version of project will probably have this overloaded to accept rgba values for the base colorings and tint of the metal, for now it's:\n
# green circuit board\n
# metallic trace layers and outside solder masks\n
# off-white silk-screen\n
def apply_materials():
    context = bpy.context
    scene = context.scene

	# make sure computer thinks the mouse is in the right location, avoid ...poll() errors.
    for area in context.screen.areas: 
        if area.type == "VIEW_3D":
            for space in area.spaces: 
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"

	
	# turn visibility off on everything
    for layer in bpy.data.objects:
        layer.select_set(False)
        layer.hide_set(True)
        

	# loop through all objects and apply the material
    for layer in bpy.data.objects:
        if layer.name == "board_outline":
            layer.hide_set(False)
            layer.select_set(True)
            object = bpy.context.selected_objects[0]
            data = object.data
            material = bpy.data.materials.new("board")
            material.diffuse_color = (0.062, 0.296, 0.020, 0.99)
            data.materials.append(material)
            object.active_material.metallic = 0.234
            object.active_material.roughness = 0.20
            layer.select_set(False)
            layer.hide_set(True)
			
			
        elif layer.name == "bottom_solder":
            layer.hide_set(False)
            layer.select_set(True)
            object = bpy.context.selected_objects[0]
            data = object.data
            material = bpy.data.materials.new("metal")
            material.diffuse_color = (0.391, 0.521, 0.627, 1.0)
            data.materials.append(material)
            object.active_material.metallic = 0.849
            object.active_material.specular_intensity = 0.279
            object.active_material.roughness = 0.245
            layer.select_set(False)
            layer.hide_set(True)
			
			
        elif layer.name == "bottom_layer":
            layer.hide_set(False)
            layer.select_set(True)
            object = bpy.context.selected_objects[0]
            data = object.data
            material = bpy.data.materials.new("metal")
            material.diffuse_color = (0.391, 0.521, 0.627, 1.0)
            data.materials.append(material)
            object.active_material.metallic = 0.849
            object.active_material.specular_intensity = 0.279
            object.active_material.roughness = 0.245
            layer.select_set(False)
            layer.hide_set(True)
			
			
        elif layer.name == "top_layer":
            layer.hide_set(False)
            layer.select_set(True)
            object = bpy.context.selected_objects[0]
            data = object.data
            material = bpy.data.materials.new("metal")
            material.diffuse_color = (0.391, 0.521, 0.627, 1.0)
            data.materials.append(material)
            object.active_material.metallic = 0.849
            object.active_material.specular_intensity = 0.279
            object.active_material.roughness = 0.245
            layer.select_set(False)
            layer.hide_set(True)
			
			
        elif layer.name == "top_solder":
            layer.hide_set(False)
            layer.select_set(True)
            object = bpy.context.selected_objects[0]
            data = object.data
            material = bpy.data.materials.new("metal")
            material.diffuse_color = (0.391, 0.521, 0.627, 1.0)
            data.materials.append(material)
            object.active_material.metallic = 0.849
            object.active_material.specular_intensity = 0.279
            object.active_material.roughness = 0.245
            layer.select_set(False)
            layer.hide_set(True)
			
			
        elif layer.name == "silk_screen":
            layer.hide_set(False)
            layer.select_set(True)
            object = bpy.context.selected_objects[0]
            data = object.data
            material = bpy.data.materials.new("silk_screen")
            material.diffuse_color = (0.513, 0.627, 0.552, 1.0)
            data.materials.append(material)
            object.active_material.metallic = 0.234
            object.active_material.roughness = 0.20
            layer.select_set(False)
            layer.hide_set(True)
        
        
		# turn all visibilites except drill back on
    for layer in bpy.data.objects:
        layer.select_set(False)
        if layer.name == "drill_holes":
            layer.hide_set(True)
        else:
            layer.hide_set(False)
            








# call the function
apply_materials()
            
            
            