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

def write_def(context, filepath):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp

    print("LOG: Writing Feature Definition")
    f = open(filepath + "/features/" + os.path.basename(filepath)
        + ".lua", 'w', encoding='utf-8')
    f.write("--// Feature Definition File\n")
    f.write("--// Generated by Enetheru's Blender Export Script\n\n")
    f.write("local objectname = \"%s\"\n" % os.path.basename(filepath))
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
    f.write("\tobject = \"%s.obj\",\n" % os.path.basename(filepath))

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

def write_heirarchy(node,f,level, count):
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
        node.matrix_local[0][3],
        node.matrix_local[2][3],
        node.matrix_local[1][3]*(-1)))

    #recursively do the children
    for j in node.children:
        count = write_heirarchy(j, f, level, count)
    level = level - 1

    #closing brackets
    for i in range(level+2):
        f.write("\t")
    f.write("},\n")

    return count
    

def write_obj(context, filepath):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp

    # Get the root node
    root_node = bpy.data.objects[sfp.rootObject]

    #FIXME So far i have no idea how to do this, so i'm going to leave it for now
    print("NOTE: Dont forget to invert the UV Map before exporting or at least\n"
        "\tmirror your image in the Y direction")

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
        filepath="%s/objects3d/%s.obj" % (filepath,os.path.basename(filepath)),
        use_selection = True,
        use_normals = True,
        use_materials = False,
        use_triangles = True)

    #write object heirarchy
    print("LOG: Writing Feature Definition")
    f = open(filepath + "/objects3d/" + os.path.basename(filepath)
        + ".lua", 'w', encoding='utf-8')
    f.write("--// Object Heirarchy File\n")
    f.write("--// Generated by Enetheru's Blender Export Script\n\n")
    f.write(os.path.basename(filepath)+" = {\n")
    f.write("\tpieces = {\n")
    numpieces = write_heirarchy(root_node,f,0,0)
    f.write("\t},\n")

    #radius
    try:
        f.write("\tradius = %.3f,\n" %sfp.radius)
    except AttributeError:
        print("WARN: Damage not specified, skipping.")

    #height
#    try:
#        f.write("\theight = " + str(sfp.height) + ",\n")
#    except AttributeError:
        #FIXME really rough, it doesnt take into account the object heirarchy
        #auto calculate
#        f.write("\theight = "+str(round(root_node.dimensions.z,3))+",\n")

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
    f.write("\tlocalpieceoffsets = true,\n")

    #finish
    f.write("\n}\nreturn "+os.path.basename(filepath))
    f.close()
    return {'FINISHED'}

def write_images(context, filepath):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp
    #FIXME
    #will need to figure out what to be bothered with here as there are two
    #textures that may need exporting to acceptable formats, or whether a 
    #baked render or something else is needed, at the moment however simply
    #copying the textures you are using the appropriate folder will be all
    #thats necessary to complete
    return {'FINISHED'}

def export(context, filepath):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp

    # check if root node exists
    if not sfp.rootObject in context.scene.objects:
        raise RuntimeError("ERROR: You need to make sure to set the root node")
        return {'FINISHED'}
    else:
        rootObject = context.scene.objects[sfp.rootObject]

    # Check if UV Maps are defined for all objects
    if check_uvmaps(rootObject):
        raise RuntimeError("ERROR: not all objects have UV Maps defined")
        return {'FINISHED'}

    # rename objects to conform to acceptable limits
    for k in bpy.data.objects:
        k.name = re.sub('\.','_',k.name).lower()
        k.data.name = re.sub('\.','_',k.data.name).lower()
    sfp.rootObject = re.sub('\.','_',sfp.rootObject).lower()

    print("LOG: Creating Directory Structure")
    #create base directory
    os.makedirs(filepath+"/features",exist_ok=True)
    os.makedirs(filepath+"/objects3d",exist_ok=True)
    os.makedirs(filepath+"/unittextures",exist_ok=True)

    # Write features definition
    write_def(context, filepath)
    # write obj3d stuff
    write_obj(context, filepath)
    # write images
    write_images(context, filepath)
    return {'FINISHED'}

def check_uvmaps(node):
    nouvmap = False
    if node.data.uv_textures.active == None:
        print("ERROR: %s has no uv map defined\n" % node.data.name)
        nouvmap = True

    for j in node.children:
        if j.type != 'MESH': continue
        childuvmap = check_uvmaps(j)
        nouvmap = nouvmap or childuvmap

    return nouvmap
