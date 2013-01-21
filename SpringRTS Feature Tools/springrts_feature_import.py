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
from . import slpp

def load(context, filepath):

    #find base path
    dirname = os.path.dirname(filepath)
    dirname = os.path.dirname(dirname)

    # parse the featuredef data structures
    f = open(filepath)
    data = "{" + f.read() + "}"
    f.close()
    
    lua = slpp.slpp()
    featuredef = lua.decode(text=data)

    # pull the object name before disposing of the extra table.
    name = featuredef['objectname']
    featuredef = featuredef['featureDef']

    #build other file paths
    meshpath = dirname + "/objects3d/" + featuredef['object']
    meshdefpath = re.sub('obj$','lua',meshpath)

    # parse the meshdef data structures
    f = open(meshdefpath)
    data = "{" + f.read() + "}"
    f.close()
    
    lua = slpp.slpp()
    meshdef = lua.decode(text=data)
    meshdef = meshdef[meshdef[1]]

    # import object file
    print("LOG: importing obj mesh")
    print("LOG: %s" % meshpath)

    bpy.ops.import_scene.obj('EXEC_DEFAULT', filepath=meshpath)
    #bpy.ops.object.transform_apply(rotation=True)

    # Select the root object
    root_object_name = list(meshdef['pieces'].keys())[0]
    root_object = context.scene.objects[root_object_name]
    context.scene.objects.active = root_object

    # Get spring feature properties
    sfp = bpy.context.object.sfp

    sfp.name = name
    for i,j in featuredef.items():
        sfp[i] = j
    for i,j in meshdef.items():
        sfp[i] = j

#FIXME
 #       if key.lower() == 'resurrectable':
 #           pair =  pair.replace('\"','')
  #          if pair == '-1':
  #              print("LOG: '%s' = first" % key)
   #             sfp.resurrectable = 'first'
    #        elif pair == '0':
     #           print("LOG: '%s' = no" % key)
      #          sfp.resurrectable = 'no'
       #     else:
        #        print("LOG: '%s' = yes" % key)
         #       sfp.resurrectable = 'yes'
          #  index+=2
           # continue

    #Collision Volume
 #       if key.lower() == 'collisionvolumetype':
  #          pair =  pair.replace('\"','')
   #         if pair == 'box':
    #            sfp.collisionVolumeType = 'SME_box'
     #       elif pair == 'ellipse':
      #          sfp.collisionVolumeType = 'SME_ellipsoid'
       #     elif pair == 'cylX':
        #        sfp.collisionVolumeType = 'SME_cylX'
         #   elif pair == 'cylY':
          #      sfp.collisionVolumeType = 'SME_cylY'
 #           else:
  #              sfp.collisionVolumeType = 'SME_cylZ'
   #         print("LOG: '%s' = %s" % (key, sfp.collisionVolumeType))
    #        index+=2
     #       continue

    #find the beginning of the pieces subtable
    load_heirarchy_r(context, meshdef['pieces'])

    imagefilepath = dirname + "/unittextures/"
    if sfp.tex1 != '':
        bpy.ops.image.open(filepath=imagefilepath+sfp.tex1)
    if sfp.tex2 != '':
        bpy.ops.image.open(filepath=imagefilepath+sfp.tex2)

    return {'FINISHED'}

def load_heirarchy_r(context, pieces, parent = None):
    obj = None
    for i,j in pieces.items():
        bpy.ops.object.select_all(action='DESELECT')
        if i == 'offset':
            parent.select=True
            context.scene.objects.active = parent
            # set origin to correct location
            cursor = context.scene.cursor_location
            cursor[0] = j[0]
            cursor[1] = j[2] * -1
            cursor[2] = j[1]
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.ops.object.transform_apply(rotation=True)

        else:
            obj = context.scene.objects[i]
            if parent != None:
                obj.select = True
                context.scene.objects.active = parent
                bpy.ops.object.parent_set()

            load_heirarchy_r( context, j, obj )
