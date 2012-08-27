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

# <pep8-80 compliant>

bl_info = {
    "name": "SpringRTS Feature Placement Importer",
    "author": "Samuel Nicholas",
    "version": (0,1),
    "blender": (2, 6, 3),
    "location": "File > Import-Export",
    "description": "Import feature locations from set.lua text file"
                   "",
    "warning": "",
    "wiki_url": ""
                "",
    "tracker_url": "",
    "category": "SpringRTS"}

import re
import bpy

def read_some_data(context, filepath, x,z):
    print("running read_some_data...")
    f = open(filepath, 'r', encoding='utf-8')

    # would normally load the data here
    count = 0
    
    for line in f:
        k = re.split("\W+", line)
        if k[1] == "name":
            print("Object Name:\tfeature")
            print("Mesh Name:\t" + k[2] )
            print("Location:\t" + k[4] +"," + k[6] )
            print("rotation:\t" + k[8]  + "\n")
            
            if k[2] in bpy.data.meshes:
                print("mesh exists\n")
                mesh = bpy.data.meshes[k[2]]
            else:
                mesh = bpy.data.meshes.new(name=k[2])
            
            object = bpy.data.objects.new(name="feature", object_data = mesh)
            object.location.x = int(k[4])/512 - x/2
            object.location.y = int(k[6])/-512 + z/2
            object.rotation_euler.z = int(k[8]) / 65535.0 * 6.283184
            scene = bpy.context.scene
            scene.objects.link(object)
            count += 1

    print(count ," feature locations loaded")

    f.close()

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportSomeData(Operator, ImportHelper):
    """Load feature positions from SpringRTS map"""
    bl_idname = "import_springrts.map_features"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import SpringRTS Feature Placement"

    # ImportHelper mixin class uses this
    filename_ext = ".lua"

    filter_glob = StringProperty(
            default="*.*",
            options={'HIDDEN'},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    size_x = bpy.props.IntProperty(
            name="Map Width(x)",
            description="The Width of the map in SpringRTS map units",
            min=2, max=64,
            soft_min=4, soft_max=32,
            step=2,
            default=8,
            )

    size_z = bpy.props.IntProperty(
            name="Map Length(z)",
            description="The Length of the map in SpringRTS map units",
            min=2, max=64,
            soft_min=4, soft_max=32,
            step=2,
            default=8,
            )

    def execute(self, context):
        return read_some_data(context, self.filepath, self.size_x, self.size_z)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportSomeData.bl_idname, text="SpringRTS Map Features")


def register():
    bpy.utils.register_class(ImportSomeData)
    bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportSomeData)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
