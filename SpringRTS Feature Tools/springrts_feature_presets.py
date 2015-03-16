import bpy

presets = [
    ('none', "None", "No Changes"),
    ('tree', "Tree", "Trees, between 32 and 64 units high or there abouts."),
    ('rock', "Rock", "Rocks, generic rocks.")
]

def preset_choose(self, context):
   #set attributes based on which preset is chosen
   obj = bpy.context.object
   sfp = bpy.context.object.sfp
   h = obj.dimensions.z
   print(self)

   if(sfp.preset == 'tree'):
      sfp.damage = h * 1.875 - 40
      sfp.metal = 1
      sfp.energy = h * 1.25 - 30
      sfp.crushResistance = h * 1.25 - 20
      sfp.reclaimTime = sfp.metal + sfp.energy * 4
      sfp.indestructable = False
      sfp.flammable = True
      sfp.reclaimable = True
      sfp.autoReclaimable = True
      sfp.featureDead = ''
      sfp.smokeTime = h * 1000
      sfp.resurrectable = 'no'
      sfp.upright = True
      sfp.floating = False
      sfp.geothermal = False
      sfp.noSelect = False
      sfp.blocking = True
      sfp.footprintX = 1
      sfp.footprintZ = 1
      sfp.collisionVolumeType = 'SME_cylY'
