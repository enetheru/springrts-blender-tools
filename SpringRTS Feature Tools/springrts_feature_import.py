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

    f = open(filepath)
    luadef = f.read()
    f.close()
    split = re.split('"|[ ,{}=\t\n]+|--.*',luadef)
    
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

        #FIXME ressurrectable enum
        if key.lower() == 'resurrectable':
            print("WARN: '%s' no implemented yet" % key)
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

    #FIXME Collision Volume
        if key.lower() == 'collisionvolumetype':
            print("WARN: '%s' no implemented yet" % key)
            index+=2
            continue

        if key.lower() == 'collisionvolumescales':
            print("WARN: '%s' no implemented yet" % key)
            index+=4
            continue

        if key.lower() == 'collisionvolumeoffsets':
            print("WARN: '%s' no implemented yet" % key)
            index+=4
            continue


    #FIXME Mesh
        if key.lower() == 'object':
            print("WARN: '%s' no implemented yet" % key)
            index +=2
            continue

        if key.lower() == 'radius':
            print("LOG: '%s' = %s" % (key, pair))
            sfp.radius = float(pair)
            index +=2
            continue

        if key.lower() == 'midpos':
            print("WARN: '%s' no implemented yet" % key)
            index+=4
            continue

    # Other
        if key.lower() == 'collisionvolumetest':
            print("INFO: '%s' deprecated" % key)
            index+=2
            continue

        print("LOG: '%s' - not recognised" %key)
        index +=1

    return {'FINISHED'}

