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
    split = re.split('[" ,{}=\t\n]+|--.*',luadef)

    index = -1
    for i in split:
        index += 1
    # General
        if i.lower() == 'description':
            sfp.description = split[index+1]
            continue
    # Attributes
        if i.lower() == 'damage':
            sfp.damage = float(split[index+1])
            continue

        if i.lower() == 'metal':
            sfp.metal = float(split[index+1])
            continue

        if i.lower() == 'energy':
            sfp.energy = float(split[index+1])
            continue

       if i.lower() == 'mass':
            sfp.mass = float(split[index+1])
            continue

        if i.lower() == 'crushresistance':
            sfp.crushResistance = float(split[index+1])
            continue

        if i.lower() == 'reclaimtime':
            sfp.reclaimTime = float(split[index+1])
            continue
    # Options
        if i.lower() == 'indestructable':
            if split[index+1].lower() == 'true':
                sfp.indestructable = True
            else:
                sfp.indestructable = False
            continue

        if i.lower() == 'flammable':
            if split[index+1].lower() == 'true':
                sfp.flammable = True
            else:
                sfp.flammable = False
            continue

        if i.lower() == 'reclaimable':
            if split[index+1].lower() == 'true':
                sfp.reclaimable = True
            else:
                sfp.reclaimable = False
            continue

        if i.lower() == 'autoreclaimable':
            if split[index+1].lower() == 'true':
                sfp.autoReclaimable = True
            else:
                sfp.autoReclaimable = False
            continue

        if i.lower() == 'featuredead':
            sfp.featureDead = split[index+1]
            continue

        if i.lower() == 'smoketime':
            sfp.smokeTime = int(split[index+1])


        #FIXME ressurrectable enum
        #
        if i.lower() == 'upright':
            if split[index+1].lower() == 'true':
                sfp.upright = True
            else:
                sfp.upright = False
            continue

        if i.lower() == 'floating':
            if split[index+1].lower() == 'true':
                sfp.floating = True
            else:
                sfp.floating = False
            continue

        if i.lower() == 'geothermal':
            if split[index+1].lower() == 'true':
                sfp.geothermal = True
            else:
                sfp.geothermal = False
            continue

        if i.lower() == 'noselect':
            if split[index+1].lower() == 'true':
                sfp.noSelect = True
            else:
                sfp.noSelect = False
            continue

        #FIXME Footprint
        #
        #FIXME Collision Volume
        #
        #FIXME Mesh
        #
        #FIXME Source Images

 
        

    print(filepath)
    return {'FINISHED'}

