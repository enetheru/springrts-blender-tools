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
    "name": "SpringRTS Feature UI",
    "author": "Samuel Nicholas",
    "version": (0,1),
    "blender": (2, 6, 3),
    "location": "properties > Scene",
    "description": "Modify properties associated with features"
                   "",
    "warning": "",
    "wiki_url": ""
                "",
    "tracker_url": "",
    "category": "SpringRTS"}


import bpy


class SpringRTSFeaturePanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "SpringRTS Feature Properties"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        sc = context.scene

        row = layout.row()
        row.operator('export_springrts.feature', "export")

        row = layout.row()
        row.prop_search(sc, 'root', context.scene, 'objects')

        layout.label(text=" Attributes:")
        row = layout.row()
        row.prop(sc, 'description')
        
        row = layout.row()
        row.prop(sc, 'mass')
        row = layout.row()
        row.prop(sc, 'damage')
        row = layout.row()
        row.prop(sc, 'crushResistance')
        row = layout.row()
        row.prop(sc, 'metal')
        row.prop(sc, 'energy')
        row = layout.row()
        row.prop(sc, 'reclaimTime')

        layout.label(text=" Options:")
        row = layout.row()
        row.prop(sc, 'flammable')
        row.prop(sc, 'indestructable')
        row = layout.row()
        row.prop(sc, 'reclaimable')
        row.prop(sc, 'autoReclaimable')
        row = layout.row()
        row.prop(sc, 'resurrectable')
        row = layout.row()
        row.prop(sc, 'noSelect')
        row.prop(sc, 'blocking')

        layout.label(text=" Engine Stuff:")
        row = layout.row()
        row.prop(sc, 'featureDead')
        row = layout.row()
        row.prop(sc, 'smokeTime')

        row = layout.row()
        row.prop(sc, 'upright')
        row.prop(sc, 'nodrawundergrey')
        row = layout.row()
        row.prop(sc, 'geothermal')

        layout.label(text=" Pathfinding:")
        row = layout.row(align=True)
        row.prop(sc, 'footprintX')
        row.prop(sc, 'footprintZ')

        layout.label(text=" Collision Volume:")
        row = layout.row()
        row.prop(sc, 'collisionVolumeType')
        row = layout.row()
        row.prop(sc, 'collisionVolumeScales')
        row = layout.row()
        row.prop(sc, 'collisionVolumeOffsets')
        row = layout.row()
        row.prop(sc, 'collisionVolumeTest')

def register():

#Internal
    bpy.types.Scene.root = bpy.props.StringProperty()

#General
    bpy.types.Scene.description = bpy.props.StringProperty(name="Description")

    bpy.types.Scene.damage = bpy.props.FloatProperty(
        name="Damage",
        description = "How much damage this feature can take before"
            "being destroyed.",
        min = 0.0,
        default = 0,
        precision = 3)

    bpy.types.Scene.featureDead = bpy.props.StringProperty(
        name = "Death Feature",
        description = "The featureName of the feature to spawn when this"
            "feature is destroyed.")

    bpy.types.Scene.indestructable = bpy.props.BoolProperty(
        name="Indestructable",
        description = "Can the feature take damage?")

    bpy.types.Scene.flammable = bpy.props.BoolProperty(
        name = "Flammable",
        description = "Can the feature be set on fire?")

    bpy.types.Scene.noSelect = bpy.props.BoolProperty(
        name = "No Select",
        description = "If true the cursor won't change to `reclaim` when"
            "hovering the feature.")

    bpy.types.Scene.mass = bpy.props.FloatProperty(
        name = "Mass",
        description = "The mass of the feature.",
        default = 1.0,
        min = 1.0,
        precision = 3)

    bpy.types.Scene.crushResistance = bpy.props.FloatProperty(
        name = "Crush Resistance",
        description = "How resistant is the feature to being crushed.",
        min = 0.0,
        precision = 3)

#Visual
    bpy.types.Scene.smokeTime = bpy.props.IntProperty(
        name = "Smoke Time",
        description = "How many frames a corpse feature should emit smoke"
            "for after unit death.",
        default = 300,
        min = 0)

#Reclaim & Resource
    bpy.types.Scene.reclaimable = bpy.props.BoolProperty(
        name = "Reclaimable",
        description = "Can be reclaimed by a construction unit?",
        default = True)

    bpy.types.Scene.autoReclaimable = bpy.props.BoolProperty(
        name = "Auto Reclaim",
        description = "Can be be reclaimed by a construction"
            "unit executing a patrol or area-reclaim command?",
        default = True)

    bpy.types.Scene.reclaimTime = bpy.props.FloatProperty(
        name = "Reclaim Time",
        description = "The time taken to reclaim this feature.")

    bpy.types.Scene.metal = bpy.props.FloatProperty(
        name = "Metal",
        description = "Amount of metal this feature gives when reclaimed.",
        default = 0.0,
        min = 0.0)

    bpy.types.Scene.energy = bpy.props.FloatProperty(
        name = "Energy",
        description = "Amount of energy this feature gives when reclaimed.",
        default = 0.0,
        min = 0.0)

    bpy.types.Scene.resurrectable = bpy.props.EnumProperty(
        name = "Resurrectable",
        items = (('first',"First Corpse","Only if feature is in first level decay"),
            ('no',"No", "feature is not able to be resurrected"),
            ('yes', "Yes", "Unit is always able to be resurrected")),
        description = "Can this feature be resurrected?")

    bpy.types.Scene.geothermal = bpy.props.BoolProperty(
        name = "Geothermal Vent",
        description = "Does this feature act as a geothermal vent?")

#Placement
    bpy.types.Scene.footprintX = bpy.props.IntProperty(
        name = "Footprint X",
        description = "How wide the feature is, for pathfinding and blocking.",
        default = 1,
        min = 1)

    bpy.types.Scene.footprintZ = bpy.props.IntProperty(
        name = "Footprint Z",
        description = "How wide the feature is, for pathfinding and blocking.",
        default = 1,
        min = 1)

    bpy.types.Scene.blocking = bpy.props.BoolProperty(
        name = "Blocking",
        description = "Does this feature block unit movement and is ignored"
            "by weapon aiming",
        default = True)

    bpy.types.Scene.upright = bpy.props.BoolProperty(
        name = "Upright",
        description = "Tilt with the slope of the terrain or stay upright?")

    bpy.types.Scene.nodrawundergrey = bpy.props.BoolProperty(
        name = "Float",
        description = "Float on top of water or sit on the seabed?")

#Collision Volumes
    bpy.types.Scene.collisionVolumeType = bpy.props.EnumProperty(
        name = "Collision Volume",
        items = (('box',"Box","Simple Box"),
            ('ellipsoid',"Ellipsoid","Spherical like object"),
            ('cylX',"Cylinder X","X Axis Aligned Cylinder"),
            ('cylY',"Cylinder Y","Y Axis Aligned Cylinder"),
            ('cylZ',"Cylinder Z","Z Axis Aligned Cylinder")),
        description = "The Shape of the collision volume")

    bpy.types.Scene.collisionVolumeScales = bpy.props.FloatVectorProperty(
        name = "Scale",
        description = "The lengths of the collision volume in each axis")

    bpy.types.Scene.collisionVolumeOffsets = bpy.props.FloatVectorProperty(
        name = "Offset",
        description = "The offset from the unit centre to the hit volume"
            "centre in each axis")

    bpy.types.Scene.collisionVolumeTest = bpy.props.EnumProperty(
        name = "Colission Test",
        items = (('discrete', "Discrete", "description"),
            ('continuous',"Continuous", "beware increse performance cost")),
        description = "")


    bpy.utils.register_class(SpringRTSFeaturePanel)

def unregister():
    bpy.utils.unregister_class(SpringRTSFeaturePanel)


if __name__ == "__main__":
    register()
