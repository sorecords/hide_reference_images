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

#  Hide Reference Images add-on
#  (c) 2020 Andrey Sokolov (so_records)

bl_info = {
    "name": "Hide Reference Images",
    "author": "Andrey Sokolov",
    "version": (1, 0, 0),
    "blender": (2, 83, 3),
    "location": "3D-View -> N-panel",
    "description": "Hide/Unhide all Reference Images ar all except them",
    "warning": "",
    "wiki_url": "https://github.com/sorecords/hide_reference_images/blob/master/README.md",
    "tracker_url": "https://github.com/sorecords/hide_reference_images/issues",
    "category": "Object"
}

import bpy, rna_keymap_ui

class HRI_HideRefs(bpy.types.Operator):
    '''Hide/Unhide all Reference Images'''
    bl_idname = "hri.hiderefs"
    bl_label = "Hide Reference Images"
    hidden = False
    
    def execute(self, context):
        self.op = bpy.types.HRI_OT_hiderefs
        action = False if self.op.hidden else True
        for o in context.scene.objects:
            if o.type == 'EMPTY' and o.empty_display_type == 'IMAGE':
                o.hide_viewport = action
                self.op.hidden = action
        return {'FINISHED'}
    
class HRI_HideOther(bpy.types.Operator):
    '''Hide/Unhide all except Reference Images'''
    bl_idname = "hri.hideother"
    bl_label = "Hide all except Reference Images"
    hidden = False
    
    def execute(self, context):
        self.op = bpy.types.HRI_OT_hiderefs
        action = False if self.op.hidden else True
        for o in context.scene.objects:
            if o.type == 'EMPTY' and o.empty_display_type == 'IMAGE':
                continue
            else:
                o.hide_viewport = action
                self.op.hidden = action
        return {'FINISHED'}

hri_keymaps = []

def hri_keyconfig():
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new("Object Mode") if "Object Mode" not in kc.keymaps else kc.keymaps["Object Mode"]
    for kmi in km.keymap_items:
        if kmi.idname.startswith("hri."):
            kmi.active = True
            hri_keymaps.append((km, kmi))
    if hri_keymaps:
        return
    new = km.keymap_items.new
    kmi = new("hri.hiderefs", 'H', 'PRESS', ctrl=True, alt=True)
    kmi.active = True
    hri_keymaps.append((km, kmi))
    kmi = new("hri.hideother", 'H', 'PRESS', shift=True, ctrl=True, alt=True)
    kmi.active = True
    hri_keymaps.append((km, kmi))
    
def hri_activate(self, context):
    '''Startup'''
    hri_keyconfig()
    while hri_activate in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(hri_activate)

class HRI_PT_panel(bpy.types.Panel):
    '''Create UI Panel'''
    bl_label = "Hide Reference Images"
    bl_idname = "VIEW3D_PT_hri"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_context = "objectmode"
    bl_category = "Hide Refs"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("hri.hiderefs")
        col = layout.column()
        col.operator("hri.hideother")
        
hri_classes = [
    HRI_HideRefs,
    HRI_HideOther,
    HRI_PT_panel,    
]

def register():
    for cl in hri_classes:
        bpy.utils.register_class(cl)
    bpy.app.handlers.persistent(hri_activate)
    bpy.app.handlers.load_post.append(hri_activate)
    
def unregister():
    bpy.ops.ttr.uninstall()
    for cl in hri_classes:
        bpy.utils.unregister_class(cl)
        
#--------------------------- For test purposes only ----------------------------   
if __name__ == '__main__':
    register()