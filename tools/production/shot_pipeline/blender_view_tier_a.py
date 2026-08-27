"""Tier-A preview scene for Blender GUI.

Open in Blender > Scripting tab > Open > Run Script.
Then press F12 to render and view in Blender's render window.
"""

import bpy

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "TestCube"

bpy.ops.object.camera_add(location=(3, -3, 2.5))
cam = bpy.context.active_object
cam.name = "TestCamera"
cam.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type="POINT", location=(2, -2, 3))
light = bpy.context.active_object
light.name = "TestLight"
light.data.energy = 500

bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 360
