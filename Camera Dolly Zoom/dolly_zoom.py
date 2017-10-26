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
    "name": "Camera Dolly Zoom",
    "author": "Yain Rodrigo Vieyra Gatica",
    "version": (1, 0, 0),
    "blender": (2, 78, 0),
    "location": "Camera Data context > Lens > Dolly Zoom",
    "description": "Set Focal Length drivers to automate the Dolly Zoom when moving the Camera",
    "category": "Camera",
}

"""
This addon allows to set Focal Length drivers automatically to emulate the Dolly Zoom when moving the Camera.
"""

import bpy
from bpy.props import PointerProperty, StringProperty, FloatProperty

def get_driver_lens(data):
    if data.animation_data:
        anim = data.animation_data
        if len(anim.drivers) > 0:
            for d in anim.drivers:
                if d.data_path == "lens":
                    return d
    return None

def upd_lens_object(self, context):
    d = get_driver_lens(self)
    focal_length = None
    if d:
        expr = d.driver.expression
        if "*" in expr:
            word = expr.split("*")[0]
            if "focal_length" == word:
                focal_length = True
        self.driver_remove("lens")
    if focal_length:
        self.lens = self.driver_lens
    
    if self.lens_object:
        camera = context.object
        if type(self.lens_object) is str:
            objective = bpy.data.objects[self.lens_object]
            if camera == objective:
                self.lens_object = ""
                return
        else:
            objective = self.lens_object
            if camera == objective:
                self.lens_object = None
                return
        
        self.driver_lens = self.lens
        
        DRIVER = self.driver_add("lens")
        DRIVER.driver.expression = "distance"
        
        variable = DRIVER.driver.variables.new()
        variable.name = "focal_length"
        variable.type = "SINGLE_PROP"
        variable.targets[0].id_type = "CAMERA"
        variable.targets[0].id = self
        variable.targets[0].data_path = "driver_lens"
        
        variable = DRIVER.driver.variables.new()
        variable.name = "distance"
        variable.type = "LOC_DIFF"
        variable.targets[0].id = camera
        variable.targets[1].id = objective

        bpy.context.scene.update()

        distance = self.lens
        
        expression = "focal_length*(distance/{})".format(distance)
        DRIVER.driver.expression = expression
    else:
        self.property_unset("lens_object")
        self.property_unset("driver_lens")


def draw_warning(self, context):
    self.layout.label("When setting an object to focus, the current")
    self.layout.label("'Focal Length' driver will be overwritten")

class Lens_Driver_Warning(bpy.types.Operator):
    bl_idname = "camera.lens_driver_warning"
    bl_label = ""

    def execute(self, context):
        context.window_manager.popup_menu(draw_warning, title="Warning: 'Focal Length' driver is present", icon='ERROR')
        return {"FINISHED"}


def Dolly_Zoom_Panel(self, context):
    layout = self.layout
    data = context.object.data
    
    if data.type in "PERSP":
        d = get_driver_lens(data)
        focal_length = None
        if d:
            expr = d.driver.expression
            if "*" in expr:
                word = expr.split("*")[0]
                if "focal_length" == word:
                    focal_length = True
        
        col = layout.column(align=True)
        
        split = col.split(percentage=0.25)
        split.label("Dolly Zoom:")
        if d:
            row = split.row()
            row.alignment = "LEFT"
            row.operator("camera.lens_driver_warning", icon="INFO")
        
        split = col.split(align=True, percentage=0.35)
        col = split.column()
        col.label("Focus this Object:")
        
        col = split.column()
        col.prop_search(data, "lens_object", bpy.data, "objects", text="")
        if focal_length:
            col.prop(data, "driver_lens")
        

def register():
    bpy.utils.register_module(__name__)
    if bpy.app.version >= (2, 79, 0):
        bpy.types.Camera.lens_object = PointerProperty(type=bpy.types.Object, update=upd_lens_object)
    else:
        bpy.types.Camera.lens_object = StringProperty(default="", update=upd_lens_object)
    bpy.types.Camera.driver_lens = FloatProperty(name="Initial Focal Length", min=1,
                                                 description="Initial Lens value to tweak current Focal Length driver")
    bpy.types.DATA_PT_lens.append(Dolly_Zoom_Panel)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.DATA_PT_lens.remove(Dolly_Zoom_Panel)
    del bpy.types.Camera.lens_object
    del bpy.types.Camera.driver_lens
