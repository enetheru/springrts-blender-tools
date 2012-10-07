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
    "name": "SpringRTS Feature Tools",
    "author": "Samuel Nicholas",
    "blender": (2, 6, 3),
    "location": "File > Import-Export, properties->scene",
    "description": "Import-Export , feature properties ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "SpringRTS"}

if "bpy" in locals():
    import imp
    if "springrts_feature_bits" in locals():
        imp.reload(stringrts_feature_bits)
    if "springrts_feature_import" in locals():
        imp.reload(stringrts_feature_import)
    if "springrts_feature_export" in locals():
        imp.reload(stringrts_feature_export)


import bpy, os, re

from bpy_extras.io_utils import ExportHelper,ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from . import springrts_feature_bits, springrts_feature_import, springrts_feature_export

class SpringRTSFeatureCalculateRadius(Operator):
    """Calculate radius of feature"""
    bl_idname = "springrts_feature.calculate_radius"
    bl_label = "Calculate SpringRTS Feature Radius"

    def execute(self, context):
        springrts_feature_bits.calculate_radius(self, context)
        return {'FINISHED'}

#class SpringRTSFeatureCalculateHeight(Operator):
#    """Calculate height of feature"""
#    bl_idname = "springrts_feature.calculate_height"
#    bl_label = "Calculate SpringRTS Feature Height"
#
#    def execute(self, context):
#        from . import springrts_feature_bits
#        springrts_feature_bits.calculate_height(self, context)
#        return {'FINISHED'}

class SpringRTSFeatureCalculateMidpos(Operator):
    """Calculate midpos of feature"""
    bl_idname = "springrts_feature.calculate_midpos"
    bl_label = "Calculate SpringRTS Feature Midpos"

    def execute(self, context):
        springrts_feature_bits.calculate_midpos(self, context)
        return {'FINISHED'}

class ImportSpringRTSFeature(Operator, ImportHelper):
    """Load a SpringRTS feature"""
    bl_idname = "import_springrts.feature"
    bl_label = "Import SpringRTS Feature"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".lua"
    filter_glob = StringProperty(
            default="*.lua",
            options={'HIDDEN'},
            )

    def execute(self, context):
        print("== Import SpringRTS feature ==")
        return {'FINISHED'}

class ExportSpringRTSFeature(Operator, ExportHelper):
    """Save a SpringRTS Feature"""
    bl_idname = "export_springrts.feature"
    bl_label = 'Export SpringRTS Feature'

    filename_ext = ""
    filter_glob = StringProperty(
            default="*.*",
            options={'HIDDEN'},
            )

    def execute(self, context):
        print("== Export SpringRTS feature ==")
        return springrts_feature_export.export(context, self.filepath)

class SpringRTSFeatureAttributes(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "SpringRTS Feature Attributes"
    bl_idname = "SCENE_PT_SME_featureAttributes"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        sfp = context.scene.sfp

        layout.label(text=" Attributes:")
        row = layout.row()
        row.prop(sfp, 'description')        
        row = layout.row()
        row.prop(sfp, 'mass')
        row = layout.row()
        row.prop(sfp, 'damage')
        row = layout.row()
        row.prop(sfp, 'crushResistance')
        row = layout.row()
        row.prop(sfp, 'metal')
        row.prop(sfp, 'energy')
        row = layout.row()
        row.prop(sfp, 'reclaimTime')

class SpringRTSFeatureCollisionVolume(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "SpringRTS Feature Collision Volume"
    bl_idname = "SCENE_PT_SME_collisionvolume"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        sfp = context.scene.sfp

        row = layout.row()
        row.prop(sfp, 'collisionVolume')
        row.prop(sfp, 'collisionVolumeType')
        row = layout.row()
        row.prop(sfp, 'collisionEditMode')
        row = layout.row()
        row.active = sfp.collisionEditMode != 'grab'
        row.prop(sfp, 'collisionVolumeScales')
        row = layout.row()
        row.active = sfp.collisionEditMode != 'grab'
        row.prop(sfp, 'collisionVolumeOffsets')

class SpringRTSFeatureOptions(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "SpringRTS Feature Options"
    bl_idname = "SCENE_PT_SME_featureOptions"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        sfp = context.scene.sfp

        layout.label(text=" Options:")
        row = layout.row()
        row.prop(sfp, 'flammable')
        row.prop(sfp, 'indestructable')
        row = layout.row()
        row.prop(sfp, 'reclaimable')
        row.prop(sfp, 'autoReclaimable')
        row = layout.row()
        row.prop(sfp, 'resurrectable')
        row = layout.row()
        row.prop(sfp, 'noSelect')
        row.prop(sfp, 'blocking')


class SpringRTSFeatureMesh(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "SpringRTS Feature Mesh"
    bl_idname = "SCENE_PT_SME_featuremesh"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        split = layout.split()
        sfp = context.scene.sfp

        row = layout.row()
        row.prop_search(sfp, 'rootObject', context.scene, 'objects')
        row = layout.row()
        row.prop_search(sfp, 'tex1', bpy.data, 'images')
        row = layout.row()
        row.prop_search(sfp, 'tex2', bpy.data, 'images')
        row = layout.row()
        row.prop(sfp, 'occlusionVolume', "Show Occlusion Volume")
        row = layout.row()
        row.prop(sfp, 'occlusionEditMode')
        row = layout.row()
        row.active = sfp.occlusionEditMode != 'grab'
        row.prop(sfp, 'radius')
        row.operator('springrts_feature.calculate_radius', "Recalc")
        row = layout.row()
        row.active = sfp.occlusionEditMode != 'grab'
        row.prop(sfp, 'midpos', "")
        row.operator('springrts_feature.calculate_midpos', "Recalc")


class SpringRTSFeatureEngine(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "SpringRTS Feature Engine"
    bl_idname = "SCENE_PT_SME_featureengine"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        sfp = context.scene.sfp

        layout.label(text=" Engine Stuff:")
        row = layout.row()
        row.prop(sfp, 'featureDead')
        row = layout.row()
        row.prop(sfp, 'smokeTime')

        row = layout.row()
        row.prop(sfp, 'upright')
        row.prop(sfp, 'floating')
        row = layout.row()
        row.prop(sfp, 'geothermal')

        layout.label(text=" Pathfinding:")
        row = layout.row()
        row.prop(sfp, 'footprint')
        row = layout.row(align=True)
        row.prop(sfp, 'footprintX')
        row.prop(sfp, 'footprintZ')

class SpringRTSFeatureImages(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "SpringRTS Feature Images"
    bl_idname = "SCENE_PT_SME_featureimages"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        sfp = context.scene.sfp

        layout.label(text=" Source Images:")
        row = layout.row()
        row.prop_search(sfp, 'texRGBA', bpy.data, 'images')
        row = layout.row()
        row.prop_search(sfp, 'texTeam', bpy.data, 'images')
        row = layout.row()
        row.prop_search(sfp, 'texAmbient', bpy.data, 'images')
        row = layout.row()
        row.prop_search(sfp, 'texSpecular', bpy.data, 'images')

class SpringRTSFeaturePropertyGroup(bpy.types.PropertyGroup):
    # Source Images 
    texRGBA = bpy.props.StringProperty(
        name = "Diffuse+Alpha",
        description = "RGBA diffuse + Alpha")

    texTeam = bpy.props.StringProperty(
        name = "Team Mask",
        description = "Team Colour Mask")

    texAmbient = bpy.props.StringProperty(
        name = "Ambient",
        description = "Ambient Multiplier")

    texSpecular = bpy.props.StringProperty(
        name = "Specular",
        description = "Specular Addition")

    # Occlusion Volume
    occlusionVolume = bpy.props.BoolProperty(
        name = "Show",
        description = "Turn on visual for occlusion Volume.",
        default = False,
        update = springrts_feature_bits.update_occlusion_volume)

    occlusionEditMode = bpy.props.EnumProperty(
        name = "Edit Mode",
        items = (('manual',"Manual","Enter Values Manually"),
            ('grab',"Grab","Transform the occlusion volume in 3d view"),),
        description = "Occlusion Volume Edit Mode",
        update = springrts_feature_bits.update_occlusion_volume)

    # 3D object Properties
    rootObject = bpy.props.StringProperty(
        name="Root Object",
        update = springrts_feature_bits.root_object_check)

    tex1 = bpy.props.StringProperty(name = "tex1",
        description = "RGB diffuse and team overlay")

    tex2 = bpy.props.StringProperty(name = "tex2",
        description = "ambient, specular, unused and alpha")

    radius = bpy.props.FloatProperty(
        name="Radius",
        description = "",
        min = 0.01,
        default = 1,
        precision = 3,
        update = springrts_feature_bits.update_occlusion_volume)

    midpos = bpy.props.FloatVectorProperty(
        name="Mid Point",
        description = "",
        update = springrts_feature_bits.update_occlusion_volume)

    # General
    description = bpy.props.StringProperty(name="Description")

    damage = bpy.props.FloatProperty(
        name="Damage",
        description = "How much damage this feature can take before"
            "being destroyed.",
        min = 0.0,
        default = 0,
        precision = 3)

    featureDead = bpy.props.StringProperty(
        name = "Death Feature",
        description = "The featureName of the feature to spawn when this"
            "feature is destroyed.")

    indestructable = bpy.props.BoolProperty(
        name="Indestructable",
        description = "Can the feature take damage?")

    flammable = bpy.props.BoolProperty(
        name = "Flammable",
        description = "Can the feature be set on fire?")

    noSelect = bpy.props.BoolProperty(
        name = "No Select",
        description = "If true the cursor won't change to `reclaim` when"
            "hovering the feature.")

    mass = bpy.props.FloatProperty(
        name = "Mass",
        description = "The mass of the feature.",
        default = 1.0,
        min = 1.0,
        precision = 3)

    crushResistance = bpy.props.FloatProperty(
        name = "Crush Resistance",
        description = "How resistant is the feature to being crushed.",
        min = 0.0,
        precision = 3)

    # Visual
    smokeTime = bpy.props.IntProperty(
        name = "Smoke Time",
        description = "How many frames a corpse feature should emit smoke"
            "for after unit death.",
        default = 300,
        min = 0)

    # Reclaim & Resource
    reclaimable = bpy.props.BoolProperty(
        name = "Reclaimable",
        description = "Can be reclaimed by a construction unit?",
        default = True)

    autoReclaimable = bpy.props.BoolProperty(
        name = "Auto Reclaim",
        description = "Can be be reclaimed by a construction"
            "unit executing a patrol or area-reclaim command?",
        default = True)

    reclaimTime = bpy.props.FloatProperty(
        name = "Reclaim Time",
        description = "The time taken to reclaim this feature.")

    metal = bpy.props.FloatProperty(
        name = "Metal",
        description = "Amount of metal this feature gives when reclaimed.",
        default = 0.0,
        min = 0.0)

    energy = bpy.props.FloatProperty(
        name = "Energy",
        description = "Amount of energy this feature gives when reclaimed.",
        default = 0.0,
        min = 0.0)

    resurrectable = bpy.props.EnumProperty(
        name = "Resurrectable",
        items = (('first',"First Corpse","Only if feature is in first level decay"),
            ('no',"No", "feature is not able to be resurrected"),
            ('yes', "Yes", "Unit is always able to be resurrected")),
        description = "Can this feature be resurrected?")

    geothermal = bpy.props.BoolProperty(
        name = "Geothermal Vent",
        description = "Does this feature act as a geothermal vent?")

    # Placement
    footprint = bpy.props.BoolProperty(
        name = "Show Footprint",
        description = "Turn on visual for footprint.",
        default = False,
        update = springrts_feature_bits.update_footprint)

    footprintX = bpy.props.IntProperty(
        name = "Footprint X",
        description = "How wide the feature is, for pathfinding and blocking.",
        default = 1,
        min = 1,
        update = springrts_feature_bits.update_footprint)

    footprintZ = bpy.props.IntProperty(
        name = "Footprint Z",
        description = "How wide the feature is, for pathfinding and blocking.",
        default = 1,
        min = 1,
        update = springrts_feature_bits.update_footprint)

    blocking = bpy.props.BoolProperty(
        name = "Blocking",
        description = "Does this feature block unit movement and is ignored"
            "by weapon aiming",
        default = True)

    upright = bpy.props.BoolProperty(
        name = "Upright",
        description = "Tilt with the slope of the terrain or stay upright?")

    floating = bpy.props.BoolProperty(
        name = "Float",
        description = "Float on top of water or sit on the seabed?")

    # Collision Volumes
    collisionVolume = bpy.props.BoolProperty(
        name = "Show",
        description = "Turn on visual for Collision Volume.",
        default = False,
        update = springrts_feature_bits.update_collision_volume)

    collisionEditMode = bpy.props.EnumProperty(
        name = "Edit Mode",
        items = (('manual',"Manual","Enter Values Manually"),
            ('grab',"Grab","Transform the volume in 3d view"),),
        description = "Collision Volume Edit Mode",
        update = springrts_feature_bits.update_collision_volume)

    collisionVolumeType = bpy.props.EnumProperty(
        name = "Type",
        items = (('SME_box',"Box","Simple Box"),
            ('SME_ellipsoid',"Ellipsoid","Spherical like object"),
            ('SME_cylX',"Cylinder X","X Axis Aligned Cylinder"),
            ('SME_cylY',"Cylinder Y","Y Axis Aligned Cylinder"),
            ('SME_cylZ',"Cylinder Z","Z Axis Aligned Cylinder")),
        description = "The Shape of the collision volume",
        update = springrts_feature_bits.update_collision_volume)

    collisionVolumeScales = bpy.props.FloatVectorProperty(
        name = "Scale",
        description = "The lengths of the collision volume in each axis",
        default = (1.0,1.0,1.0),
        min = 0.01,
        update = springrts_feature_bits.update_collision_volume)

    collisionVolumeOffsets = bpy.props.FloatVectorProperty(
        name = "Offset",
        description = "The offset from the unit centre to the hit volume"
            "centre in each axis",
        update = springrts_feature_bits.update_collision_volume)

def menu_func_import(self, context):
    self.layout.operator(ImportSpringRTSFeature.bl_idname, text="SpringRTS Feature")


def menu_func_export(self, context):
    self.layout.operator(ExportSpringRTSFeature.bl_idname, text="SpringRTS Feature")


def register():
#    bpy.utils.register_module(__name__)

    # Register and use feature property group
    bpy.utils.register_class(SpringRTSFeaturePropertyGroup)
    bpy.types.Scene.sfp = bpy.props.PointerProperty(
        type=SpringRTSFeaturePropertyGroup)

    # Register export operator
    bpy.utils.register_class(ExportSpringRTSFeature)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

    # Register import operator
    bpy.utils.register_class(ImportSpringRTSFeature)
    bpy.types.INFO_MT_file_import.append(menu_func_import)

    # Register other operators
    bpy.utils.register_class(SpringRTSFeatureCalculateRadius)
    bpy.utils.register_class(SpringRTSFeatureCalculateMidpos)

    # Register Scene Menu Panels
    bpy.utils.register_class(SpringRTSFeatureAttributes)
    bpy.utils.register_class(SpringRTSFeatureOptions)
    bpy.utils.register_class(SpringRTSFeatureEngine)
    bpy.utils.register_class(SpringRTSFeatureMesh)
    bpy.utils.register_class(SpringRTSFeatureCollisionVolume)
    bpy.utils.register_class(SpringRTSFeatureImages)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

    bpy.utils.unregister_class(ExportSpringRTSFeature)
    bpy.utils.unregister_class(ImportSpringRTSFeature)

    bpy.utils.unregister_class(SpringRTSFeatureAttributes)
    bpy.utils.unregister_class(SpringRTSFeatureOptions)
    bpy.utils.unregister_class(SpringRTSFeatureEngine)
    bpy.utils.unregister_class(SpringRTSFeatureMesh)
    bpy.utils.unregister_class(SpringRTSFeatureCollisionVolume)
    bpy.utils.unregister_class(SpringRTSFeatureImages)

if __name__ == "__main__":
    register()
