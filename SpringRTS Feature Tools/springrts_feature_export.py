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

import bpy,os,re
    
def export(self, context):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp

    # get base directory
    dirname = os.path.dirname(self.filepath)
    sfp.name = os.path.basename(self.filepath)

    # check if root node exists
    if not sfp.rootObject in context.scene.objects:
        raise RuntimeError("ERROR: You need to make sure to set the root node")
        return {'FINISHED'}

    # prepare
    pre(self, context)
    # Write features definition
    write_featuredef(context, dirname)
    # Write mesh hierarchy
    write_meshdef(context, dirname)
    # write obj stuff
    write_obj(context, dirname)
    # Image
    copy_images(context, dirname)
    # cleanup
    post(self, context)

    return {'FINISHED'}

def pre(self, context):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp

    # get root object
    root = context.scene.objects[sfp.rootObject]
    #Prepare all objects in the hierarchy
    pre_recurse(self, context, root)

def pre_recurse(self, context, node):
    # if not mesh skip
    if node.type != 'MESH': return

    # Get spring feature properties
    sfp = bpy.context.scene.sfp

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # select the root node and make it active.
    node.select = True
    bpy.context.scene.objects.active = node

    # rename objects
    if node.name == sfp.rootObject: 
        sfp.rootObject = re.sub('\.','_',node.name).lower()
    node.name = re.sub('\.','_',node.name).lower()
    node.data.name = re.sub('\.','_',node.data.name).lower()

    # create UV maps
    if node.data.uv_textures.active == None:
        print("WARN: no UV coordinates specified for %s, Creating" % node.name)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.unwrap()
        bpy.ops.object.mode_set(toggle=True)

    # invert UV Maps
    if self.invertUV:
        for uvloop in node.data.uv_layers.active.data: uvloop.uv[1] = uvloop.uv[1] * -1 + 1
    
    #recurse through children
    for i in node.children: pre_recurse(self, context, i)

def write_featuredef(context, dirname):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp

    #creating directory
    os.makedirs(dirname+"/features",exist_ok=True)

    print("LOG: Writing Feature Definition")
    f = open(dirname + "/features/" + sfp.name + ".lua", 'w', encoding='utf-8')
    f.write("--// Feature Definition File\n")
    f.write("--// Generated by Enetheru's Blender Export Script\n\n")
    f.write("local objectname = \"%s\"\n" % sfp.name)
    f.write("local featureDef = {\n")

    # General
    f.write("\n--// General\n")

    try:
        f.write("\tdescription = \"%s\",\n" % sfp.description)
    except AttributeError:
        print("WARN: description not specified, skipping.")

    try:
        f.write("\tdamage = %.3f,\n" % sfp.damage)
    except AttributeError:
        print("WARN: damage not specified, skipping.")

    try:
        f.write("\tfeatureDead = \"%s\",\n" % sfp.featureDead)
    except AttributeError:
        print("WARN: featureDead not specified, skipping.")

    try:
        f.write("\tindestructable = %s,\n" % str(sfp.indestructable).lower())
    except AttributeError:
        print("WARN: indestructable not specified, skipping.")
    
    try:
        f.write("\tflammable = %s,\n" % str(sfp.flammable).lower())
    except AttributeError:
        print("WARN: flammable not specified, skipping.")

    try:
        f.write("\tnoSelect = %s,\n" % str(sfp.noSelect).lower())
    except AttributeError:
        print("WARN: noSelect not specified, skipping.")

    try:
        f.write("\tmass = %.3f,\n" % sfp.mass)
    except AttributeError:
        print("WARN: mass not specified, skipping.")

    try:
        f.write("\tcrushResistance = %.3f,\n" % sfp.crushResistance)
    except AttributeError:
        print("WARN: crushResistance not specified, skipping.")

    #Visual
    f.write("\n--// Visual\n")

    # Object needs to be the same as the name of the whole project
    f.write("\tobject = \"%s.obj\",\n" % sfp.name)

    try:
        f.write("\tsmokeTime = %i,\n" % sfp.smokeTime)
    except AttributeError:
        print("WARN: smokeTime not specified, skipping.")

    #Reclaim and Resource
    f.write("\n--// Reclaim & Resource\n")

    try:
        f.write("\treclaimable = %s,\n" % str(sfp.reclaimable).lower())
    except AttributeError:
        print("WARN: reclaimable not specified, skipping.")

    try:
        f.write("\tautoReclaimable = %s,\n" % str(sfp.noSelect).lower())
    except AttributeError:
        print("WARN: autoReclaim not specified, skipping.")

    try:
        f.write("\treclaimTime = %.3f,\n" % sfp.reclaimTime)
    except AttributeError:
        print("WARN: reclaimTime not specified, skipping.")

    try:
        f.write("\tmetal = %.3f,\n" % sfp.metal)
    except AttributeError:
        print("WARN: metal not specified, skipping.")

    try:
        f.write("\tenergy = %.3f,\n" % sfp.energy)
    except AttributeError:
        print("WARN: energy not specified, skipping.")

    try:
        f.write("\tresurrectable = ")
        if sfp.resurrectable == 'first':
            f.write("-1")
        elif sfp.resurrectable == 'no':
            f.write("0")
        else:
            f.write("1")
        f.write(",\n")
    except AttributeError:
        print("WARN: resurrectable not specified, skipping.")

    try:
        f.write("\tgeoThermal = %s,\n" % str(sfp.geoThermal).lower())
    except AttributeError:
        print("WARN: geoThermal not specified, skipping.")

    # Placement
    f.write("\n--// Placement\n",)

    try:
        f.write("\tfootprintX = %i,\n" % sfp.footprintX)
    except AttributeError:
        print("WARN: footprintX not specified, skipping.")

    try:
        f.write("\tfootprintZ = %i,\n" % sfp.footprintZ)
    except AttributeError:
        print("WARN: footprintY not specified, skipping.")

    try:
        f.write("\tblocking = %s,\n" % str(sfp.blocking).lower())
    except AttributeError:
        print("WARN: blocking not specified, skipping.")
        
    try:
        f.write("\tupright = %s,\n" % str(sfp.upright).lower())
    except AttributeError:
        print("WARN: upright not specified, skipping.")

    try:
        f.write("\tfloating = %s,\n" % str(sfp.floating).lower())
    except AttributeError:
        print("WARN: floating not specified, skipping.")

    # Collision VOlumes
    f.write("\n--// Collision Volumes\n",)

    try:
        if sfp.collisionVolumeType == "SME_box":
            ctype = "box"
        elif sfp.collisionVolumeType == "SME_ellipsoid":
            ctype = "ellipse"
        elif sfp.collisionVolumeType == "SME_cylX":
            ctype = "cylX"
        elif sfp.collisionVolumeType == "SME_cylY":
            ctype = "cylY"
        elif sfp.collisionVolumeType == "SME_cylZ":
            ctype = "cylZ"
    except AttributeError:
        print("WARN: collisionVolumeType not specified, skipping.")
    else:
        f.write("\tcollisionVolumeType = \"%s\",\n" % ctype)

    try:
        f.write("\tcollisionVolumeScales = {%.3f, %.3f, %.3f},\n" % (
            sfp.collisionVolumeScales[0],
            sfp.collisionVolumeScales[1],
            sfp.collisionVolumeScales[2]))
    except AttributeError:
        print("WARN: collisionVolumeScales not specified, skipping.")

    try:
        f.write("\tcollisionVolumeOffsets = {%.3f, %.3f, %.3f},\n" % (
            sfp.collisionVolumeOffsets[0],
            sfp.collisionVolumeOffsets[1],
            sfp.collisionVolumeOffsets[2],))
    except AttributeError:
        print("WARN: collisionVolumeOffsets not specified, skipping.")

    # Finished
    f.write("}\n")
    f.write("return lowerkeys({[objectname] = featureDef})\n")
    f.close()
    return {'FINISHED'}

def write_meshdef(context, dirname):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp
    # Get the root node
    root_node = bpy.data.objects[sfp.rootObject]

    #creating directory
    os.makedirs(dirname+"/objects3d",exist_ok=True)

    print("LOG: Writing Feature Definition")
    f = open(dirname + "/objects3d/" + sfp.name + ".lua", 'w', encoding='utf-8')
    f.write("--// Object Heirarchy File\n")
    f.write("--// Generated by Enetheru's Blender Export Script\n\n")
    f.write(sfp.name + " = {\n")
    f.write("\tpieces = {\n")
    numpieces = write_mesh_hierarchy(root_node, 0, 0, f)
    f.write("\t},\n")

    #radius
    try:
        f.write("\tradius = %.3f,\n" %sfp.radius)
    except AttributeError:
        print("WARN: Damage not specified, skipping.")

    #midpos
    try:
        f.write("\tmidpos = {%.3f, %.3f, %.3f},\n" % (
            sfp.midpos[0] * (-1),
            sfp.midpos[1],
            sfp.midpos[2]))
    except AttributeError:
        print("WARN: Damage not specified, skipping.")

    # textures
    f.write("\ttex1 = \"%s\",\n" % sfp.tex1)
    f.write("\t--tex2 = \"%s\",\n" % sfp.tex2)

    # numpieces
    f.write("\tnumpieces = %i,\n" %numpieces)
    f.write("\tglobalvertexoffsets = true,\n")
    f.write("\tlocalpieceoffsets = false,\n")

    #finish
    f.write("\n}\nreturn " + sfp.name)
    f.close()


def write_mesh_hierarchy(node, level, count, f):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp

    # if not mesh skip
    if node.type != 'MESH': return count
    #keep track of how manu objects
    count = count+1

    #Write piece name and opening brackets
    f.write("\t" * (level + 2))
    if node.name == node.data.name:
        f.write("%s = {\n" % node.name)
    else:
        f.write("%s_%s = {\n" % (node.name, node.data.name))
    level = level + 1
    
    #Write offset
    f.write("\t" * (level + 2))
    f.write("offset = {%.3f, %.3f, %.3f},\n" % (
        node.matrix_world[0][3],
        node.matrix_world[2][3],
        node.matrix_world[1][3]*(-1)))

    #recursively do the children
    for j in node.children:
        count = write_mesh_hierarchy(j, level, count, f)
    level = level - 1

    #closing brackets
    for i in range(level+2):
        f.write("\t")
    f.write("},\n")

    return count

def write_obj(context, dirname):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp
    # Get the root node
    root_node = bpy.data.objects[sfp.rootObject]

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # select the root node and make it active.
    root_node.select = True
    bpy.context.scene.objects.active = root_node

    #select all the children of the root node.
    for i in range(256):
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)

    #export obj file
    print("LOG: Exporting mesh to obj format")
    bpy.ops.export_scene.obj(
        filepath="%s/objects3d/%s.obj" % (dirname, sfp.name),
        use_selection = True,
        use_normals = True,
        use_materials = False,
        use_triangles = True)

def copy_images(context, dirname):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp
    # Get the root node
    root_node = bpy.data.objects[sfp.rootObject]

    #creating directory
    os.makedirs(dirname+"/unittextures",exist_ok=True)
    # Copy images
    #if image assigned to root node, use
    if sfp.tex1 != None:
        sourcepath = bpy.data.images[sfp.tex1].save_render(dirname+"/unittextures/"+sfp.tex1)
    if sfp.tex2 != None:
        sourcepath = bpy.data.images[sfp.tex2].save_render(dirname+"/unittextures/"+sfp.tex2)

def post(self, context):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp
    post_recurse(self, context, context.scene.objects[sfp.rootObject])

def post_recurse(self, context, node):
    # if not mesh skip
    if node.type != 'MESH': return count

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # select the root node and make it active.
    node.select = True
    bpy.context.scene.objects.active = node

    if self.invertUV:
        for uvloop in node.data.uv_layers.active.data: uvloop.uv[1] = uvloop.uv[1] * -1 + 1

    for i in node.children: post_recurse(self, context, i)
