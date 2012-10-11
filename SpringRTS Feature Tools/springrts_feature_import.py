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

def load(context, filepath):
    # Get spring feature properties
    sfp = bpy.context.scene.sfp

    #find base path
    basepath = os.path.dirname(filepath)
    basepath = os.path.dirname(basepath)

    #FIXME
    meshname = ""

    print("LOG: Opening luadefs file for reading")
    print("LOG: %s" % filepath)
    f = open(filepath)
    luadef = f.read()
    f.close()

    # tokenize mesh lua and clean up
    temp = []
    tokens = re.split('([{}])|[= \n\t,]+|--.*\n',luadef)
    for i in tokens:
        if i == None:
            continue
        if i == '':
            continue
        temp = temp + [i]
    tokens = temp

    level = 0
    index = 0
    # Loop through tokens
    while index < len(tokens)-1:
        key = tokens[index]
        pair = tokens[index+1]
        if key.lower() == '{':
            level +=1
            index +=1
            continue
        if key.lower() == '}':
            level -=1
            index +=1
            continue
    # General
        if key.lower() == 'description':
            sfp.description = pair.replace('\"','')
            print("LOG: '%s' = %s" % (key, sfp.description))
            index +=2
            continue

    # Attributes
        if key.lower() == 'damage':
            sfp.damage = float(pair)
            print("LOG: '%s' = %s" % (key, sfp.damage))
            index +=2
            continue

        if key.lower() == 'metal':
            sfp.metal = float(pair)
            print("LOG: '%s' = %s" % (key, sfp.metal))
            index +=2
            continue

        if key.lower() == 'energy':
            sfp.energy = float(pair)
            print("LOG: '%s' = %s" % (key, sfp.energy))
            index +=2
            continue

        if key.lower() == 'mass':
            sfp.mass = float(pair)
            print("LOG: '%s' = %s" % (key, sfp.mass))
            index +=2
            continue

        if key.lower() == 'crushresistance':
            sfp.crushResistance = float(pair)
            print("LOG: '%s' = %s" % (key, sfp.crushResistance))
            index +=2
            continue

        if key.lower() == 'reclaimtime':
            sfp.reclaimTime = float(pair)
            print("LOG: '%s' = %s" % (key, sfp.reclaimTime))
            index +=2
            continue
    # Options
        if key.lower() == 'indestructable':
            if pair.lower() == 'true':
                sfp.indestructable = True
            else:
                sfp.indestructable = False
            print("LOG: '%s' = %s" % (key, sfp.indestructable))
            index +=2
            continue

        if key.lower() == 'flammable':
            if pair.lower() == 'true':
                sfp.flammable = True
            else:
                sfp.flammable = False
            print("LOG: '%s' = %s" % (key, sfp.flammable))
            index +=2
            continue

        if key.lower() == 'reclaimable':
            if pair.lower() == 'true':
                sfp.reclaimable = True
            else:
                sfp.reclaimable = False
            print("LOG: '%s' = %s" % (key, sfp.reclaimable))
            index +=2
            continue

        if key.lower() == 'autoreclaimable':
            if pair.lower() == 'true':
                sfp.autoReclaimable = True
            else:
                sfp.autoReclaimable = False
            print("LOG: '%s' = %s" % (key, sfp.autoReclaimable))
            index +=2
            continue

        if key.lower() == 'featuredead':
            sfp.featureDead = pair.replace('\"','')
            print("LOG: '%s' = %s" % (key, sfp.featureDead))
            index +=2
            continue

        if key.lower() == 'smoketime':
            sfp.smokeTime = int(pair)
            print("LOG: '%s' = %s" % (key, sfp.smokeTime))
            index +=2
            continue

        if key.lower() == 'resurrectable':
            pair =  pair.replace('\"','')
            if pair == '-1':
                print("LOG: '%s' = first" % key)
                sfp.resurrectable = 'first'
            elif pair == '0':
                print("LOG: '%s' = no" % key)
                sfp.resurrectable = 'no'
            else:
                print("LOG: '%s' = yes" % key)
                sfp.resurrectable = 'yes'
            index+=2
            continue

        if key.lower() == 'upright':
            if pair.lower() == 'true':
                sfp.upright = True
            else:
                sfp.upright = False
            print("LOG: '%s' = %s" % (key, sfp.upright))
            index +=2
            continue

        if key.lower() == 'floating':
            if pair.lower() == 'true':
                sfp.floating = True
            else:
                sfp.floating = False
            print("LOG: '%s' = %s" % (key, sfp.floating))
            index +=2
            continue

        if key.lower() == 'geothermal':
            if pair.lower() == 'true':
                sfp.geothermal = True
            else:
                sfp.geothermal = False
            print("LOG: '%s' = %s" % (key, sfp.geothermal))
            index +=2
            continue

        if key.lower() == 'noselect':
            if pair.lower() == 'true':
                sfp.noSelect = True
            else:
                sfp.noSelect = False
            print("LOG: '%s' = %s" % (key, sfp.noSelect))
            index +=2
            continue
    # Footprint
        if key.lower() == 'blocking':
            if pair.lower() == 'true':
                sfp.blocking = True
            else:
                sfp.blocking = False
            print("LOG: '%s' = %s" % (key, sfp.blocking))
            index +=2
            continue

        if key.lower() == 'footprintx':
            sfp.footprintX = int(pair)
            print("LOG: '%s' = %s" % (key, sfp.footprintX))
            index +=2
            continue

        if key.lower() == 'footprintz':
            sfp.footprintZ = int(pair)
            print("LOG: '%s' = %s" % (key, sfp.footprintZ))
            index +=2
            continue

    #Collision Volume
        if key.lower() == 'collisionvolumetype':
            pair =  pair.replace('\"','')
            if pair == 'box':
                sfp.collisionVolumeType = 'SME_box'
            elif pair == 'ellipse':
                sfp.collisionVolumeType = 'SME_ellipsoid'
            elif pair == 'cylX':
                sfp.collisionVolumeType = 'SME_cylX'
            elif pair == 'cylY':
                sfp.collisionVolumeType = 'SME_cylY'
            else:
                sfp.collisionVolumeType = 'SME_cylZ'
            print("LOG: '%s' = %s" % (key, sfp.collisionVolumeType))
            index+=2
            continue

        if key.lower() == 'collisionvolumescales':
            sfp.collisionVolumeScales[0] = float(tokens[index+2])
            sfp.collisionVolumeScales[1] = float(tokens[index+3])
            sfp.collisionVolumeScales[2] = float(tokens[index+4])
            print("LOG: '%s' = {%s, %s, %s}" % (key,
                sfp.collisionVolumeScales[0],
                sfp.collisionVolumeScales[1],
                sfp.collisionVolumeScales[2]))
            index+=6
            continue

        if key.lower() == 'collisionvolumeoffsets':
            sfp.collisionVolumeOffsets[0] = float(tokens[index+2])
            sfp.collisionVolumeOffsets[1] = float(tokens[index+3])
            sfp.collisionVolumeOffsets[2] = float(tokens[index+4])
            print("LOG: '%s' = {%s, %s, %s}" % (key,
                sfp.collisionVolumeOffsets[0],
                sfp.collisionVolumeOffsets[1],
                sfp.collisionVolumeOffsets[2]))
            index+=6
            continue
    # Other
        if key.lower() == 'collisionvolumetest':
            print("INFO: '%s' deprecated" % key)
            index+=2
            continue

        if key.lower() == 'object':
            meshname = pair.replace('\"','')
            print("LOG: obj filename = %s" % meshname)
            index +=2
            continue

        print("LOG: '%s' - not recognised" %key)
        index +=1

    #import mesh
    meshfilepath = basepath + "/objects3d/" + meshname
    print("LOG: importing obj mesh")
    print("LOG: %s" % meshfilepath)

    bpy.ops.import_scene.obj('EXEC_DEFAULT', filepath=meshfilepath)
    #bpy.ops.object.transform_apply(rotation=True)

    # load mesh lua def
    meshluapath = re.sub('obj$','lua',meshfilepath)
    print("LOG: Opening mesh lua")
    print("LOG: %s" % meshluapath)

    f = open(meshluapath)
    meshlua = f.read()
    f.close()
    # tokenize mesh lua and clean up
    temp = []
    tokens = re.split('([{}])|[= \n\t,]+|--.*\n',meshlua)
    for i in tokens:
        if i == None:
            continue
        if i == '':
            continue
        temp = temp + [i]
    tokens = temp

    level = 0
    ptable = False
    plevel = 0
    # Loop through tokens
    index = 0
    while index < len(tokens)-1:
        key = tokens[index]
        pair = tokens[index+1]
    #Mesh
        if key.lower() == '{':
            level +=1
            index +=1
            continue
        if key.lower() == '}':
            level -=1
            index +=1
            if level < plevel: ptable=False
            continue
        if ptable:
            index+=1
            continue

        if key.lower() == 'radius':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.radius = float(pair)
            index +=2
            continue

        if key.lower() == 'midpos':
            print("LOG: '%s' = {%s, %s, %s}" % (key, 
                tokens[index+2],
                tokens[index+3],
                tokens[index+4]))
            sfp.midpos[0] = float(tokens[index+2])
            sfp.midpos[1] = float(tokens[index+3])
            sfp.midpos[2] = float(tokens[index+4])
            index+=6
            continue

        if key.lower() == 'tex1':
            sfp.tex1 = pair.replace('\"','')
            print("LOG: '%s' = %s" % (key, sfp.tex1))
            index +=2
            continue

        if key.lower() == 'tex2':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.tex2 = pair.replace('\"','')
            index +=2
            continue
    # Other
        if key.lower() == 'pieces':
            print("LOG: '%s' processed later" % key)
            ptable = True
            plevel = level+1
            index+=1
            continue

        if key.lower() == 'numpieces':
            print("LOG: '%s' = %s" % (key, pair))
            index+=2
            continue
        
        if key.lower() == 'globalvertexoffsets':
            print("WARN: '%s' not implemented yet" % key)
            index+=2
            continue

        if key.lower() == 'localpieceoffsets':
            print("WARN: '%s' not implemented yet" % key)
            index+=2
            continue

        print("LOG: '%s' - not recognised" %key)
        index +=1

    #find the beginning of the pieces subtable
    begin = tokens.index('pieces')+2
    sfp.rootObject = tokens[begin]
    load_heirarchy(context, tokens, index=begin)

    imagefilepath = basepath + "/unittextures/"
    bpy.ops.image.open(filepath=imagefilepath+sfp.tex1)
    bpy.ops.image.open(filepath=imagefilepath+sfp.tex2)

    return {'FINISHED'}

def load_heirarchy(context, meshlua, parent = None, index=0):
    obj = None
    level = 0
    while index < len(meshlua):
        token = meshlua[index]
        if token == '{':
            level += 1
            index += 1
            continue
        if token == '}':
            level -=1
            index+=1
            if level <= 0: return index
        if token == 'offset':
            print("LOG: '%s' = {%s, %s, %s}" % (token, meshlua[index+2], meshlua[index+3], meshlua[index+4]))
            context.scene.cursor_location[0] = float(meshlua[index+2])
            context.scene.cursor_location[1] = float(meshlua[index+4]) * -1
            context.scene.cursor_location[2] = float(meshlua[index+3])
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            index += 6
            continue
        if level == 0:
            print("LOG: %s" % meshlua[index])
            # select object
            bpy.ops.object.select_all(action='DESELECT')
            obj = context.scene.objects[meshlua[index]]
            obj.select = True
            context.scene.objects.active = obj
            bpy.ops.object.transform_apply(rotation=True)
            if parent != None:
                context.scene.objects.active = parent
                bpy.ops.object.parent_set()
            index += 1
            continue
        if level > 0:
            index = load_heirarchy(context, meshlua, obj, index)
            continue
        index +=1
