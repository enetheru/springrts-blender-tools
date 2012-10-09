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

    #FIXME
    meshname = ""

    print("LOG: Opening luadefs file for reading")
    print("LOG: %s" % filepath)
    f = open(filepath)
    luadef = f.read()
    f.close()
    split = re.split('\n|[\t =",{}]+|--.*\n',luadef)
    index = 0
    while index < len(split)-1:
        key = split[index]
        pair = split[index+1]
        if key == '':
            index += 1
            continue
    # General
        if key.lower() == 'description':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.description = pair
            index +=2
            continue

    # Attributes
        if key.lower() == 'damage':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.damage = float(pair)
            index +=2
            continue

        if key.lower() == 'metal':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.metal = float(pair)
            index +=2
            continue

        if key.lower() == 'energy':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.energy = float(pair)
            index +=2
            continue

        if key.lower() == 'mass':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.mass = float(pair)
            index +=2
            continue

        if key.lower() == 'crushresistance':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.crushResistance = float(pair)
            index +=2
            continue

        if key.lower() == 'reclaimtime':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.reclaimTime = float(pair)
            index +=2
            continue
    # Options
        if key.lower() == 'indestructable':
            print("LOG: '%s' = %s" % (key, pair))
            if pair.lower() == 'true':
                sfp.indestructable = True
            else:
                sfp.indestructable = False
            index +=2
            continue

        if key.lower() == 'flammable':
            print("LOG: '%s' = %s" % (key, pair))
            if pair.lower() == 'true':
                sfp.flammable = True
            else:
                sfp.flammable = False
            index +=2
            continue

        if key.lower() == 'reclaimable':
            print("LOG: '%s' = %s" % (key, pair))
            if pair.lower() == 'true':
                sfp.reclaimable = True
            else:
                sfp.reclaimable = False
            index +=2
            continue

        if key.lower() == 'autoreclaimable':
            print("LOG: '%s' = %s" % (key, pair))
            if pair.lower() == 'true':
                sfp.autoReclaimable = True
            else:
                sfp.autoReclaimable = False
            index +=2
            continue

        if key.lower() == 'featuredead':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.featureDead = pair
            index +=2
            continue

        if key.lower() == 'smoketime':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.smokeTime = int(pair)
            index +=2
            continue

        if key.lower() == 'resurrectable':
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
            print("LOG: '%s' = %s" % (key, pair))
            if pair.lower() == 'true':
                sfp.upright = True
            else:
                sfp.upright = False
            index +=2
            continue

        if key.lower() == 'floating':
            print("LOG: '%s' = %s" % (key, pair))
            if pair.lower() == 'true':
                sfp.floating = True
            else:
                sfp.floating = False
            index +=2
            continue

        if key.lower() == 'geothermal':
            print("LOG: '%s' = %s" % (key, pair))
            if pair.lower() == 'true':
                sfp.geothermal = True
            else:
                sfp.geothermal = False
            index +=2
            continue

        if key.lower() == 'noselect':
            print("LOG: '%s' = %s" % (key, pair))
            if pair.lower() == 'true':
                sfp.noSelect = True
            else:
                sfp.noSelect = False
            index +=2
            continue
    # Footprint
        if key.lower() == 'blocking':
            print("LOG: '%s' = %s" % (key, pair))
            if pair.lower() == 'true':
                sfp.blocking = True
            else:
                sfp.blocking = False
            index +=2
            continue

        if key.lower() == 'footprintx':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.footprintX = int(pair)
            index +=2
            continue

        if key.lower() == 'footprintz':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.footprintZ = int(pair)
            index +=2
            continue

    #Collision Volume
        if key.lower() == 'collisionvolumetype':
            print("LOG: '%s' = %s" % (key, pair))
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
            index+=2
            continue

        if key.lower() == 'collisionvolumescales':
            print("LOG: '%s' = {%s, %s, %s}" % (key, 
                split[index+1],
                split[index+2],
                split[index+3]))
            sfp.collisionVolumeScales[0] = float(split[index+1])
            sfp.collisionVolumeScales[1] = float(split[index+2])
            sfp.collisionVolumeScales[2] = float(split[index+3])
            index+=4
            continue

        if key.lower() == 'collisionvolumeoffsets':
            print("LOG: '%s' = {%s, %s, %s}" % (key, 
                split[index+1],
                split[index+2],
                split[index+3]))
            sfp.collisionVolumeOffsets[0] = float(split[index+1])
            sfp.collisionVolumeOffsets[1] = float(split[index+2])
            sfp.collisionVolumeOffsets[2] = float(split[index+3])
            index+=4
            continue
    # Other
        if key.lower() == 'collisionvolumetest':
            print("INFO: '%s' deprecated" % key)
            index+=2
            continue

        if key.lower() == 'object':
            print("LOG: obj filename = %s" % pair)
            meshname = pair
            index +=2
            continue

        print("LOG: '%s' - not recognised" %key)
        index +=1

    #FIXME, import mesh
    temp = os.path.dirname(filepath)
    temp = os.path.dirname(temp)
    meshfilepath = temp + "/objects3d/" + meshname
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
    split = re.split('\n|[\t =",{}]+|--.*\n',meshlua)
    index = 0
    while index < len(split)-1:
        key = split[index]
        pair = split[index+1]
        if key == '':
            index += 1
            continue

    #Mesh
        if key.lower() == 'radius':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.radius = float(pair)
            index +=2
            continue

        if key.lower() == 'midpos':
            print("LOG: '%s' = {%s, %s, %s}" % (key, 
                split[index+1],
                split[index+2],
                split[index+3]))
            sfp.midpos[0] = float(split[index+1])
            sfp.midpos[1] = float(split[index+2])
            sfp.midpos[2] = float(split[index+3])
            index+=4
            continue

        if key.lower() == 'tex1':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.tex1 = pair
            index +=2
            continue

        if key.lower() == 'tex2':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.tex2 = pair
            index +=2
            continue
    # Other
        if key.lower() == 'pieces':
            print("LOG: '%s' processed later" % key)
            index+=1
            continue

        if key.lower() == 'offset':
            print("WARN: '%s' not implemented yet" % key)
            index+=4
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

    # tokenize mesh lua and clean up
    cleansplit = []
    split = re.split('([{}])|[= "\n\t,]+|--.*\n',meshlua)
    for i in split:
        if i == None:
            continue
        if i == '':
            continue
        cleansplit = cleansplit + [i]

    #cut off beginning
    begin = cleansplit.index('pieces')+2
    sfp.rootObject = cleansplit[begin]
    load_heirarchy(context,cleansplit, index=begin)

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
            print("LOG: loading heirarchy info for %s" % meshlua[index])
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
