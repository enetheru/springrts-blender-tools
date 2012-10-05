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

import bpy,mathutils

def recurse_radius(node, distance=0.0):
    
#   if vertex distance is larger than distance
    midpos = mathutils.Vector((
        bpy.context.scene.midpos[0],
        bpy.context.scene.midpos[2] * -1,
        bpy.context.scene.midpos[1]))
    offset = mathutils.Vector((
        node.matrix_world[0][3],
        node.matrix_world[1][3],
        node.matrix_world[2][3]))
    offset = offset - midpos

    for i in node.data.vertices:
        myvector = i.co + offset
        if myvector.length > distance:
            distance = myvector.length
    for j in node.children:
        distance = recurse_radius(j, distance)
    return distance

#def recurse_height(node,offset=mathutils.Vector((0.0,0.0,0.0)), height=0.0):
#    
#   if vertex distance is larger than distance
#    for i in node.data.vertices:
#        myheight = i.co.z + offset.z
#        if myheight > height:
#            height = myheight
#   distance = vertex distance
#    for j in node.children:
#        offset = j.location
#        height = recurse_height(j, offset, height)
#    return height

def recurse_midpos(
    node,
    bounds=[mathutils.Vector((0.0,0.0,0.0)), mathutils.Vector((0.0,0.0,0.0))],
    first=True):

    offset = mathutils.Vector(
        (node.matrix_world[0][3],
        node.matrix_world[1][3],
        node.matrix_world[2][3]))

    for i in node.data.vertices:
        if first == True:
            print("first vertex")
            bounds[0] = i.co + offset
            bounds[1] = i.co + offset
            first = False
        bounds[0].x = min(bounds[0].x, i.co.x + offset.x)
        bounds[0].y = min(bounds[0].y, i.co.y + offset.y)
        bounds[0].z = min(bounds[0].z, i.co.z + offset.z)
        bounds[1].x = max(bounds[1].x, i.co.x + offset.x)
        bounds[1].y = max(bounds[1].y, i.co.y + offset.y)
        bounds[1].z = max(bounds[1].z, i.co.z + offset.z)

    for j in node.children:
        bounds = recurse_midpos(j, bounds, first)
    return bounds

def calculate_radius(self, context):
    print("Calculate radius")
    root = context.scene.objects[context.scene.root]
    mp = context.scene.midpos
    origin = mathutils.Vector((mp[0],mp[1],mp[2]))
    context.scene.radius = recurse_radius(root) / 2.0
    return {'FINISHED'}

#def calculate_height(self, context):
#    print("Calculate height")
#    root = context.scene.objects[context.scene.root]
#    mp = context.scene.midpos
#    origin = mathutils.Vector((mp[0],mp[1],mp[2]))
#    context.scene.height = recurse_height(root,root.location - origin)
#    return {'FINISHED'}

def calculate_midpos(self, context):
    root = context.scene.objects[context.scene.root]
    bounds = recurse_midpos(root)
    centre = (bounds[0] + bounds[1]) * 0.5
    context.scene.midpos[0] = centre.x
    context.scene.midpos[1] = centre.z
    context.scene.midpos[2] = centre.y * -1
    return {'FINISHED'}

def update_footprint(self, context):
    create_SME_objects(self, context)

    object = bpy.data.objects["SME_footprint"]

    if context.scene.footprint:
        object.hide=False
    else:
        object.hide=True

    object.scale.x = context.scene.footprintX * 8
    object.scale.y = context.scene.footprintZ * 8
    object.location.x = object.scale.x * -1.0
    object.location.y = object.scale.y
    return {'FINISHED'}

def update_collision_volume(self, context):
    create_SME_objects(self, context)
    object = bpy.data.objects["SME_collisionvolume"]

    #Change mesh type
    if object.data.name != context.scene.collisionVolumeType:
        object.data = bpy.data.meshes[context.scene.collisionVolumeType] 

    #Visability
    if context.scene.collisionVolume:
        object.hide=False
    else:
        object.hide=True

    if context.scene.collisionEditMode == 'grab':
        #Create Drivers
        fcurve = context.scene.driver_add('collisionVolumeScales')
        fcurve[0].driver.expression = "bpy.data.objects['SME_collisionvolume'].scale.x"
        fcurve[1].driver.expression = "bpy.data.objects['SME_collisionvolume'].scale.z"
        fcurve[2].driver.expression = "bpy.data.objects['SME_collisionvolume'].scale.y"
        fcurve = context.scene.driver_add('collisionVolumeOffsets')
        fcurve[0].driver.expression = "bpy.data.objects['SME_collisionvolume'].location.x - bpy.context.scene.midpos[0]"
        fcurve[1].driver.expression = "bpy.data.objects['SME_collisionvolume'].location.z - bpy.context.scene.midpos[1]"
        fcurve[2].driver.expression = "(bpy.data.objects['SME_collisionvolume'].location.y * -1) - bpy.context.scene.midpos[2]"
        #Change attributes
        object.hide_select=False
        for lock in object.lock_location:
            lock=False
        for lock in object.lock_scale:
            lock=False
    else:
        context.scene.driver_remove('collisionVolumeScales')
        context.scene.driver_remove('collisionVolumeOffsets')
#                context.scene.collisionVolumeOffsets[0] -= context.scene.midpos[0]
        object.select=False
        object.hide_select=True
        for lock in object.lock_location:
            lock=True
        for lock in object.lock_scale:
            lock=True
        object.scale.x = context.scene.collisionVolumeScales[0]
        object.scale.y = context.scene.collisionVolumeScales[2]
        object.scale.z = context.scene.collisionVolumeScales[1]
        object.location.x = context.scene.collisionVolumeOffsets[0] + context.scene.midpos[0]
        object.location.y = (context.scene.collisionVolumeOffsets[2] + context.scene.midpos[2]) * -1
        object.location.z = context.scene.collisionVolumeOffsets[1] + context.scene.midpos[1]

    return None

def update_occlusion_volume(self, context):
    create_SME_objects(self, context)
    object = bpy.data.objects["SME_occlusion"]

    #Visability
    if context.scene.occlusionVolume:
        object.hide=False
    else:
        object.hide=True

    if context.scene.occlusionEditMode == 'grab':
        #Create drivers so values are updates when model is modified.
        fcurve = context.scene.driver_add('radius')
        fcurve.driver.expression = "bpy.data.objects['SME_occlusion'].scale.x / 2.0"
        fcurve = context.scene.driver_add('midpos')
        fcurve[0].driver.expression = "bpy.data.objects['SME_occlusion'].location.x"
        fcurve[1].driver.expression = "bpy.data.objects['SME_occlusion'].location.z"
        fcurve[2].driver.expression = "bpy.data.objects['SME_occlusion'].location.y * -1"
        #change attributes
        object.hide_select = False
        for lock in object.lock_location:
            lock=False
        for lock in object.lock_scale:
            lock=False
    else:
        #Delete drivers
        context.scene.driver_remove('radius')
        context.scene.driver_remove('midpos')
        #Change Attributes
        object.select=False
        object.hide_select = True
        for lock in object.lock_location:
            lock=True
        for lock in object.lock_scale:
            lock=True
        # Change object transformations
        object.scale.x = object.scale.y = object.scale.z = context.scene.radius * 2
        object.location.x = context.scene.midpos[0]
        object.location.y = context.scene.midpos[2] * -1
        object.location.z = context.scene.midpos[1]
    return None

def create_SME_objects(self, context):
#Occlusion Mesh and objects
    if not "SME_occlusion" in bpy.data.meshes:
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=12,
            ring_count=12,
            enter_editmode=True)
        bpy.ops.transform.rotate(value=(1.5708,),axis=(1,0,0))
        bpy.ops.object.editmode_toggle()
        context.active_object.data.name="SME_occlusion"
        bpy.ops.object.delete()

    if not "SME_occlusion" in context.scene.objects:
        object = bpy.data.objects.new(
            name = "SME_occlusion",
            object_data = bpy.data.meshes["SME_occlusion"])
        context.scene.objects.link(object)
        object.show_name=True
        object.draw_type='WIRE'
        object.hide_render=True
        object.hide = True
        for lock in object.lock_rotation:
            lock=True

#Collision Mesh and objects
    if not "SME_box" in bpy.data.meshes:
        bpy.ops.mesh.primitive_cube_add(enter_editmode=True)
        bpy.ops.transform.resize(value=(0.5,0.5,0.5))
        bpy.ops.object.editmode_toggle()
        context.active_object.data.name="SME_box"
        bpy.ops.object.delete()
    if not "SME_ellipsoid" in bpy.data.meshes:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=12,enter_editmode=True)
        bpy.ops.transform.rotate(value=(1.5708,), axis=(1,0,0))
        bpy.ops.transform.resize(value=(0.5,0.5,0.5))
        bpy.ops.object.editmode_toggle()
        context.active_object.data.name="SME_ellipsoid"
        bpy.ops.object.delete()
    if not "SME_cylX" in bpy.data.meshes:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12,enter_editmode=True)
        bpy.ops.transform.rotate(value=(1.5708,), axis=(0,1,0))
        bpy.ops.transform.resize(value=(0.5,0.5,0.5))
        bpy.ops.object.editmode_toggle()
        context.active_object.data.name="SME_cylX"
        bpy.ops.object.delete()
    if not "SME_cylY" in bpy.data.meshes:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12,enter_editmode=True)
        bpy.ops.transform.resize(value=(0.5,0.5,0.5))
        bpy.ops.object.editmode_toggle()
        context.active_object.data.name="SME_cylY"
        bpy.ops.object.delete()
    if not "SME_cylZ" in bpy.data.meshes:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12,enter_editmode=True)
        bpy.ops.transform.rotate(value=(1.5708,), axis=(1,0,0))
        bpy.ops.transform.resize(value=(0.5,0.5,0.5))
        bpy.ops.object.editmode_toggle()
        context.active_object.data.name="SME_cylZ"
        bpy.ops.object.delete()


    if not "SME_collisionvolume" in context.scene.objects:
        object = bpy.data.objects.new(
            name = "SME_collisionvolume",
            object_data = bpy.data.meshes[context.scene.collisionVolumeType])
        context.scene.objects.link(object)
# parenting trick doesnt work for all use cases.        object.parent = context.scene.objects['SME_occlusion']
        object.show_name=True
        object.draw_type='WIRE'
        object.hide_render=True
        object.hide = True
        for lock in object.lock_rotation:
            lock=True

#footprint Mesh and objects
    if not "SME_footprint" in bpy.data.meshes:
        bpy.ops.mesh.primitive_plane_add()
        context.active_object.data.name="SME_footprint"
        bpy.ops.object.delete()

    if not "SME_footprint" in context.scene.objects:
        object = bpy.data.objects.new(
            name="SME_footprint",
            object_data = bpy.data.meshes["SME_footprint"])
        context.scene.objects.link(object)
        object.select=False
        object.hide_select=True
        object.show_name=True
        object.hide_render=True
        object.hide = True
        for lock in object.lock_rotation:
            lock=True
        for lock in object.lock_scale:
            lock=True
        for lock in object.lock_location:
            lock=True

    return {'FINISHED'}
