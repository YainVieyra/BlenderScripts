# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Isometric cameras",
    "author": "Yain Rodrigo Vieyra Gatica",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "Camera Data context > Lens > Camera to Isometric view",
    "description": "Set Isometric view for all selected cameras",
    "category": "Camera",
}

"""
This addon allows to set isometric views for all selected cameras.
"""


import bpy
from math import pi, acos, floor, ceil
from mathutils import Vector

def Set_Isometric_Camera_Panel(self, context):
    layout = self.layout
    
    col = layout.column()
    col.operator("camera.set_isometric", icon="SCENE")
    
class CAMERA_OT_SET_ISOMETRIC(bpy.types.Operator):
    bl_idname = "camera.set_isometric"
    bl_label = "Camera to Isometric view"
    bl_description = "Set Isometric view for all selected cameras"
    
    def execute(self, context):
        def set_angle(current_rotation, angle=0):
            turn = pi * 2
            ratio = current_rotation / turn
            floor_ratio = floor(ratio)
            ceil_ratio = ceil(ratio)
            ratios = [floor_ratio, ceil_ratio]
            positive_differences = [abs(ratio - x) for x in ratios]
            min_diff_index = min(range(2), key=positive_differences.__getitem__)
            counter_angle = -turn + (angle if angle else turn)
            angle = angle if min_diff_index is 0 else counter_angle
            large_turning = ratios[min_diff_index] * turn
            return large_turning + angle

        for ob in context.selected_objects:
            if ob.type == "CAMERA":
                ob.data.type = "ORTHO"
                ob.data.ortho_scale = 10
                
                rot = ob.rotation_euler
                matrix = ob.matrix_world
                quadrant = matrix.to_quaternion() * Vector((0, 0, 1))
                octave = pi / 4
                x_tilt = (pi / 2) - acos((2/3) ** 0.5) # isometric factor as stablished
                                                       # by pythagorean theory
                rot.y = set_angle(rot.y)
                if quadrant.z >= 0:
                    rot.x = set_angle(rot.x, x_tilt)
                    if quadrant.x >= 0 and quadrant.y <= 0:
                        rot.z = set_angle(rot.z, octave)
                    elif quadrant.x >= 0 and quadrant.y >= 0:
                        rot.z = set_angle(rot.z, (octave * 3))
                    elif quadrant.x <= 0 and quadrant.y >= 0:
                        rot.z = set_angle(rot.z, (octave * 5))
                    elif quadrant.x <= 0 and quadrant.y <= 0:
                        rot.z = set_angle(rot.z, (octave * 7))
                elif quadrant.z <= 0:
                    rot.x = set_angle(rot.x, pi - x_tilt)
                    if quadrant.x >= 0 and quadrant.y <= 0:
                        rot.z = set_angle(rot.z, octave)
                    elif quadrant.x >= 0 and quadrant.y >= 0:
                        rot.z = set_angle(rot.z, (octave * 3))
                    elif quadrant.x <= 0 and quadrant.y >= 0:
                        rot.z = set_angle(rot.z, (octave * 5))
                    elif quadrant.x <= 0 and quadrant.y <= 0:
                        rot.z = set_angle(rot.z, (octave * 7))
        return {"FINISHED"}
        

def register():
    bpy.utils.register_module(__name__)
    bpy.types.DATA_PT_lens.append(Set_Isometric_Camera_Panel)
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.DATA_PT_lens.remove(Set_Isometric_Camera_Panel)
