bl_info = {
    "name": "BGEN Cards",
    "author": "Munorr",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > N",
    "description": "Control parameters from B-GEN Cards geometry node hair system",
    "warning": "",
    "doc_url": "",
    "category": "",
}

import bpy
import os
import time

from bpy.types import Context
from . import addon_updater_ops
from bpy.utils import previews
from bpy.types import Menu, Panel, UIList, WindowManager

icons = previews.new()
icons.load(
    name='BGEN_CARD',
    path=os.path.join(os.path.dirname(__file__), "bgen_card_1080.png"),
    path_type='IMAGE'
)

# [FUNCTIONS]       
#=========================================================================================================
bgenCard_node_ID = "ID:CARD_0001"
bgenCardProxy_node_ID = "ID:CARD_0002"

bgenCard_mod = "bgen_card"
bgenCardProxy_mod = "bgen_card_proxy"
bgenCard_shader = "Bgen_Card_Shader"
resample_curve_mod = "bgenCard : [Resample Curve]"
#=========================================================================================================
#                                             [GETTERS]
#=========================================================================================================
#== Gets the info of bgen nodes for curves attached to a mesh
def get_bgenCard_mod(obj):
    modifier_name = ""
    node_tree_name = "<NOT Applicable>"
    node_id = ""
    try:
        if obj.modifiers:
            for modifier in obj.modifiers:
                if modifier.type == "NODES" and modifier.node_group:
                    a = obj.modifiers.get(modifier.name) #modifier
                    b = obj.modifiers.get(modifier.name).node_group #node group
                    
                    if b:
                        for node in b.nodes:
                            if node.name == bgenCard_node_ID:
                                modifier_name = a
                                node_tree_name = b.name
                                node_id = bgenCard_node_ID
                                break
                            elif node.name == bgenCardProxy_node_ID:
                                #print("Node present" , c.name)
                                modifier_name = a
                                node_tree_name = b.name
                                node_id = bgenCardProxy_node_ID
                                break
                            
    except:
        pass              
    return modifier_name, node_tree_name, node_id

#=========================================================================================================    
#                                            [OPERATORS]
#=========================================================================================================  
class BGENCARD_OT_choose_nodeTree(bpy.types.Operator):
    """ Choose which bgen Node to use"""
    bl_idname = "object.bgencard_choose_nodetree"
    bl_label = "Choose bgen Node"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False

        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        nodeID = get_bgenCard_mod(obj)[2]
        if not nodeID == bgenCard_node_ID:
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    bgenCard_nodes:bpy.props.EnumProperty(
        items=lambda self, context: [(b.name, b.name, "") for b in bpy.data.node_groups for bn in b.nodes if bn.name == bgenCard_node_ID],
        name="Change Modifier to:",
        description="Select bgen modifier",) # type: ignore
    
    def execute(self, context):
        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        node_group_name = get_bgenCard_mod(obj)[0].name
        obj.modifiers[node_group_name].node_group = bpy.data.node_groups[self.bgenCard_nodes]
        return{'FINISHED'}

class BGENCARD_OT_single_user(bpy.types.Operator):
    """ Make BGEN Card modifier a single user """
    bl_idname = "object.bgencard_single_user"
    bl_label = "Make single user"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):

        active = context.active_object
        if active is None:
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False 
        
        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        nodeID = get_bgenCard_mod(obj)[2]
        if not nodeID == bgenCard_node_ID:
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    def execute(self, context):
        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object
    
        node_group_name = get_bgenCard_mod(obj)[0].name
        obj.modifiers[node_group_name].node_group = obj.modifiers[node_group_name].node_group.copy()
        
        return{'FINISHED'}

class BGENCARD_OT_choose_nodeTree_proxy(bpy.types.Operator):
    """ Choose which bgen Node to use"""
    bl_idname = "object.bgencard_choose_nodetree_proxy"
    bl_label = "Choose bgen Node"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False

        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        nodeID = get_bgenCard_mod(obj)[2]
        if not nodeID == bgenCard_node_ID:
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    bgenCard_nodes:bpy.props.EnumProperty(
        items=lambda self, context: [(b.name, b.name, "") for b in bpy.data.node_groups for bn in b.nodes if bn.name == bgenCardProxy_node_ID],
        name="Change Modifier to:",
        description="Select bgen modifier",) # type: ignore
    
    def execute(self, context):
        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        node_group_name = get_bgenCard_mod(obj)[0].name
        obj.modifiers[node_group_name].node_group = bpy.data.node_groups[self.bgenCard_nodes]
        return{'FINISHED'}

class BGENCARD_OT_single_user_proxy(bpy.types.Operator):
    """ Make BGEN Card modifier a single user """
    bl_idname = "object.bgencard_single_user_proxy"
    bl_label = "Make single user"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):

        active = context.active_object
        if active is None:
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False 
        
        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        nodeID = get_bgenCard_mod(obj)[2]
        if not nodeID == bgenCardProxy_node_ID:
            return False
        return context.mode == "OBJECT"
    
    def execute(self, context):
        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object
    
        node_group_name = get_bgenCard_mod(obj)[0].name
        obj.modifiers[node_group_name].node_group = obj.modifiers[node_group_name].node_group.copy()
        
        return{'FINISHED'}

class BGENCARD_OT_link_proxy(bpy.types.Operator):
    """Links Proxy Card to Main Card"""
    bl_idname = "object.bgencard_link_proxy"
    bl_label = "Link Proxy"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False

        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        nodeID = get_bgenCard_mod(obj)[2]
        if not nodeID == bgenCard_node_ID:
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    def execute(self, context):
        # Your operator logic goes here
        #print("Simple operator executed")
        return {'FINISHED'}

class BGENCARD_OT_add_bgen_card_mod(bpy.types.Operator):
    """ Add Bgen Card to Curve """
    bl_idname = "object.add_bgen_card_mod"
    bl_label = "Add BGEN Card"
    bl_options = {'REGISTER', 'UNDO'}
    
    #-------------------------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        for objs in selected_objects:
            if not objs.type == "CURVE":
                return False
        return context.mode == "OBJECT"
    #-------------------------------------------------------------------------------------------------------------------------------------------
    cardType : bpy.props.BoolProperty(
        name="Use Existing",
        description="Use existing Card Modifier",
        default=False) # type: ignore
    proxyType : bpy.props.BoolProperty(
        name="Use Existing",
        description="Use existing Card Proxy",
        default=False) # type: ignore
    
    bgenCard_nodes:bpy.props.EnumProperty(
        items=lambda self, context: [(b.name, b.name, "") for b in bpy.data.node_groups for bn in b.nodes if bn.name == bgenCard_node_ID],
        name="Bgen Card Modifiers",
        description="Select bgen modifier",) # type: ignore
    
    bgenCard_proxies:bpy.props.EnumProperty(
        items=lambda self, context: [(b.name, b.name, "") for b in bpy.data.objects if get_bgenCard_mod(b)[2] == bgenCardProxy_node_ID],
        name="Bgen Card Modifiers",
        description="Select bgen modifier",) # type: ignore
      
    ng_name: bpy.props.StringProperty(name="Card Mod name", description="Enter a name for the hair card modifier", default="bgen_card_") # type: ignore
    #-------------------------------------------------------------------------------------------------------------------------------------------
    def invoke(self, context, event):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        resource_folder = os.path.join(dirpath,"resources")
        nodelib_path = os.path.join(resource_folder, "bgen_card_nodes.blend")

        def load_node(nt_name, link=True):
            if not os.path.isfile(nodelib_path):
                return False

            with bpy.data.libraries.load(nodelib_path, link=link) as (data_from, data_to):
                if nt_name in data_from.node_groups:
                    data_to.node_groups = [nt_name]
                    return True
            return False

        def load_material(nt_name, link=True):
            if not os.path.isfile(nodelib_path):
                return False

            with bpy.data.libraries.load(nodelib_path, link=link) as (data_from, data_to):
                if nt_name in data_from.materials:
                    data_to.materials = [nt_name]
                    return True
            return False
        
        if bgenCard_mod not in bpy.data.node_groups:
            ''' Gets Card modifier from resouorce file''' 
            dirpath = os.path.dirname(os.path.realpath(__file__))
            resource_folder = os.path.join(dirpath,"resources")
            nodelib_path = os.path.join(resource_folder, "bgen_card_nodes.blend")

            with bpy.data.libraries.load(nodelib_path, link=False) as (data_from, data_to):
                data_to.node_groups = [bgenCard_mod]
                
        if bgenCard_shader not in bpy.data.materials:
            load_material(bgenCard_shader, link=False)
        

        return context.window_manager.invoke_props_dialog(self)
    #-------------------------------------------------------------------------------------------------------------------------------------------
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col_ = col.column()
        col_.scale_y = 1.2
        col_.prop(self,"name")
        col_.separator()
        
        box = col.box()

        col_ = box.column()
        col_.scale_y = 1.4
        col_.label(text = "Hair Card Modifiers")
        row_ = col_.row()
        row_.prop(self,"cardType", text="Use Existing")
        if self.cardType == True:
            row_ = col_.row()
            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            grid_l.alignment = "RIGHT"
            grid_l.scale_x = 1.1
            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            
            grid_l.label(text = "Hair Card Modifiers")
            grid_r.prop(self,"bgenCard_nodes", text = "")
            
        else:
            row_ = col_.row()
            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            grid_l.alignment = "RIGHT"
            grid_l.scale_x = 1.1
            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            
            grid_l.label(text = "Name Modifier")
            grid_r.prop(self,"ng_name", text = "")
        
        box = col.box()
        col_ = box.column()
        col_.scale_y = 1.4
        col_.label(text = "Hair Proxies")
        row_ = col_.row()
        row_.prop(self,"proxyType", text="Use Existing")
        if self.proxyType == True:
            row_ = col_.row()
            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            grid_l.alignment = "RIGHT"
            grid_l.scale_x = 1.1
            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            
            grid_l.label(text = "Hair Proxies")
            grid_r.prop(self,"bgenCard_proxies", text = "")
        else:
            col__ = col_.column()
            col__.label(text = "[Import new Hair Proxy]")
            
    def execute(self, context):
        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        if obj.type == "CURVE":
            hc_obj = obj
            #------------------------------------------------------------------------------------------------
            #Remove empty curve modifiers and make active
            #------------------------------------------------------------------------------------------------
            while hc_obj.modifiers:
               hc_obj.modifiers.remove(hc_obj.modifiers[0])
            bpy.context.view_layer.objects.active = hc_obj.parent
            #------------------------------------------------------------------------------------------------
            if self.cardType == False: #If new hair modifier
                ''' Gets the geoNode hair modifier''' 
                dirpath = os.path.dirname(os.path.realpath(__file__))
                resource_folder = os.path.join(dirpath,"resources")
                nodelib_path = os.path.join(resource_folder, "bgen_card_nodes.blend")

                with bpy.data.libraries.load(nodelib_path, link=False) as (data_from, data_to):
                    data_to.node_groups = ["BGEN Card"]

                appended_node_tree = data_to.node_groups[0]

                get_mod_01 = appended_node_tree
                mod_01 = hc_obj.modifiers.new(name="geometry_nodes_mod", type='NODES')
                mod_01.node_group = get_mod_01
                mod_01.node_group.name = self.ng_name
            else:
                '''Uses existing one''' 
                mod_01 = hc_obj.modifiers.new(name="geometry_nodes_mod", type='NODES')
                mod_01.node_group = bpy.data.node_groups[self.bgenCard_nodes]
            
            if self.proxyType == False: #If new hair modifier
                dirpath = os.path.dirname(os.path.realpath(__file__))
                resource_folder = os.path.join(dirpath, "resources")
                object_path = os.path.join(resource_folder, "bgen_card_nodes.blend")

                with bpy.data.libraries.load(object_path, link=False) as (data_from, data_to):
                    data_to.objects = ["hCard_proxy_01"]

                for obj in data_to.objects:
                    hairProxy_obj  = obj
                    break
                # Link the imported object to the current scene
                bpy.context.scene.collection.objects.link(hairProxy_obj)
                

            modName = get_bgenCard_mod(hc_obj)[0].name
            if self.proxyType == False:
                hc_obj.modifiers[modName]["Socket_2"] = hairProxy_obj
            else:
                hc_obj.modifiers[modName]["Socket_2"] = bpy.data.objects[self.bgenCard_proxies]
            hc_obj.modifiers[modName]["Socket_31"] = hc_obj.parent
            #hc_obj.modifiers[modName]["Socket_32"] = uv_name
            hc_obj.modifiers[modName]["Socket_7"] = False
            hc_obj.modifiers[modName]["Socket_39"] = False
            hc_obj.modifiers[modName]["Socket_41"] = False

            bgenMod = get_bgenCard_mod(hc_obj)[0]
            hairCard_proxy_mod = get_bgenCard_mod(hc_obj.modifiers[modName]["Socket_2"])[0]
            hairCard_proxy_mod.node_group.nodes["bgenCard_Material_Control"].inputs[0].default_value = bpy.data.materials[bgenCard_shader]

            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = hc_obj
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.editmode_toggle()
              
        else:
            self.report({"ERROR"},message="Not a curve object")
            return {"CANCELLED"}
        return{'FINISHED'}

class BGENCARD_OT_add_bgen_card(bpy.types.Operator):
    """ Add Bgen Card to Curve """
    bl_idname = "object.add_bgen_card"
    bl_label = "Add BGEN Card"
    bl_options = {'REGISTER', 'UNDO'}
    
    #-------------------------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        if not active.type == "MESH":
            return False
        return context.mode == "OBJECT"
    #-------------------------------------------------------------------------------------------------------------------------------------------
    '''cardType: bpy.props.EnumProperty(
        items=(('EXISTING', "Use Existing", "Use existing bgen modifier"),
               ('NEW', "Create New", "Add new hairCard modifier")),
        default='EXISTING',) # type: ignore'''
    cardType : bpy.props.BoolProperty(
        name="Use Existing",
        description="Use existing Card Modifier",
        default=False) # type: ignore
    proxyType : bpy.props.BoolProperty(
        name="Use Existing",
        description="Use existing Card Proxy",
        default=False) # type: ignore
    
    '''proxyType: bpy.props.EnumProperty(
        items=(('EXISTING', "Use Existing", "Use existing bgen proxy modifier"),
               ('NEW', "Create New", "Add new hairCard modifier")),
        default='EXISTING',) # type: ignore'''
    
    bgenCard_nodes:bpy.props.EnumProperty(
        items=lambda self, context: [(b.name, b.name, "") for b in bpy.data.node_groups for bn in b.nodes if bn.name == bgenCard_node_ID],
        name="Bgen Card Modifiers",
        description="Select bgen modifier",) # type: ignore
    
    bgenCard_proxies:bpy.props.EnumProperty(
        items=lambda self, context: [(b.name, b.name, "") for b in bpy.data.objects if get_bgenCard_mod(b)[2] == bgenCardProxy_node_ID],
        name="Bgen Card Modifiers",
        description="Select bgen modifier",) # type: ignore
      
    ng_name: bpy.props.StringProperty(name="Card Mod name", description="Enter a name for the hair card modifier", default="bgen_card_") # type: ignore
    #-------------------------------------------------------------------------------------------------------------------------------------------
    def invoke(self, context, event):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        resource_folder = os.path.join(dirpath,"resources")
        nodelib_path = os.path.join(resource_folder, "bgen_card_nodes.blend")

        def load_node(nt_name, link=True):
            if not os.path.isfile(nodelib_path):
                return False

            with bpy.data.libraries.load(nodelib_path, link=link) as (data_from, data_to):
                if nt_name in data_from.node_groups:
                    data_to.node_groups = [nt_name]
                    return True
            return False

        def load_material(nt_name, link=True):
            if not os.path.isfile(nodelib_path):
                return False

            with bpy.data.libraries.load(nodelib_path, link=link) as (data_from, data_to):
                if nt_name in data_from.materials:
                    data_to.materials = [nt_name]
                    return True
            return False
        
        if bgenCard_mod not in bpy.data.node_groups:
            ''' Gets Card modifier from resouorce file''' 
            dirpath = os.path.dirname(os.path.realpath(__file__))
            resource_folder = os.path.join(dirpath,"resources")
            nodelib_path = os.path.join(resource_folder, "bgen_card_nodes.blend")

            with bpy.data.libraries.load(nodelib_path, link=False) as (data_from, data_to):
                data_to.node_groups = [bgenCard_mod]
                
        if bgenCard_shader not in bpy.data.materials:
            load_material(bgenCard_shader, link=False)
        

        return context.window_manager.invoke_props_dialog(self)
    #-------------------------------------------------------------------------------------------------------------------------------------------
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col_ = col.column()
        col_.scale_y = 1.2
        col_.prop(self,"name")
        col_.separator()
        
        box = col.box()

        col_ = box.column()
        col_.scale_y = 1.4
        col_.label(text = "Hair Card Modifiers")
        row_ = col_.row()
        row_.prop(self,"cardType", text="Use Existing")
        if self.cardType == True:
            row_ = col_.row()
            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            grid_l.alignment = "RIGHT"
            grid_l.scale_x = 1.1
            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            
            grid_l.label(text = "Hair Card Modifiers")
            grid_r.prop(self,"bgenCard_nodes", text = "")
            
        else:
            row_ = col_.row()
            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            grid_l.alignment = "RIGHT"
            grid_l.scale_x = 1.1
            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            
            grid_l.label(text = "Name Modifier")
            grid_r.prop(self,"ng_name", text = "")
        
        box = col.box()
        col_ = box.column()
        col_.scale_y = 1.4
        col_.label(text = "Hair Proxies")
        row_ = col_.row()
        row_.prop(self,"proxyType", text="Use Existing")
        if self.proxyType == True:
            row_ = col_.row()
            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            grid_l.alignment = "RIGHT"
            grid_l.scale_x = 1.1
            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            
            grid_l.label(text = "Hair Proxies")
            grid_r.prop(self,"bgenCard_proxies", text = "")
        else:
            col__ = col_.column()
            col__.label(text = "[Import new Hair Proxy]")
            
    def execute(self, context):
        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        if obj.type == "MESH":
            aObj = obj
        if obj.type == "CURVES":
            aObj = obj.parent
        #aObj = bpy.context.active_object
        x = aObj.location[0]
        y = aObj.location[1]
        z = aObj.location[2]

        if obj.type == "MESH":
            #Create new empty curve
            #------------------------------------------------------------------------------------------------
            uv_name = aObj.data.uv_layers.active.name
            bpy.context.view_layer.objects.active = aObj
            bpy.ops.object.curves_empty_hair_add(align='WORLD', location=(x, y, z), scale=(1, 1, 1))
            hc_obj = bpy.context.active_object  #hair curve object
            #------------------------------------------------------------------------------------------------
            #Remove empty curve modifiers and make active
            #------------------------------------------------------------------------------------------------
            while hc_obj.modifiers:
               hc_obj.modifiers.remove(hc_obj.modifiers[0])
            bpy.context.view_layer.objects.active = hc_obj.parent
            #------------------------------------------------------------------------------------------------
            if self.cardType == False: #If new hair modifier
                ''' Gets the geoNode hair modifier''' 
                dirpath = os.path.dirname(os.path.realpath(__file__))
                resource_folder = os.path.join(dirpath,"resources")
                nodelib_path = os.path.join(resource_folder, "bgen_card_nodes.blend")

                with bpy.data.libraries.load(nodelib_path, link=False) as (data_from, data_to):
                    data_to.node_groups = ["BGEN Card"]

                appended_node_tree = data_to.node_groups[0]

                get_mod_01 = appended_node_tree
                mod_01 = hc_obj.modifiers.new(name="geometry_nodes_mod", type='NODES')
                mod_01.node_group = get_mod_01
                mod_01.node_group.name = self.ng_name
            else:
                '''Uses existing one''' 
                mod_01 = hc_obj.modifiers.new(name="geometry_nodes_mod", type='NODES')
                mod_01.node_group = bpy.data.node_groups[self.bgenCard_nodes]
            
            if self.proxyType == False: #If new hair modifier
                dirpath = os.path.dirname(os.path.realpath(__file__))
                resource_folder = os.path.join(dirpath, "resources")
                object_path = os.path.join(resource_folder, "bgen_card_nodes.blend")

                with bpy.data.libraries.load(object_path, link=False) as (data_from, data_to):
                    data_to.objects = ["hCard_proxy_01"]

                for obj in data_to.objects:
                    hairProxy_obj  = obj
                    break
                # Link the imported object to the current scene
                bpy.context.scene.collection.objects.link(hairProxy_obj)
                

            modName = get_bgenCard_mod(hc_obj)[0].name
            if self.proxyType == False:
                hc_obj.modifiers[modName]["Socket_2"] = hairProxy_obj
            else:
                hc_obj.modifiers[modName]["Socket_2"] = bpy.data.objects[self.bgenCard_proxies]
            hc_obj.modifiers[modName]["Socket_31"] = hc_obj.parent
            hc_obj.modifiers[modName]["Socket_32"] = uv_name
            hc_obj.modifiers[modName]["Socket_7"] = True

            bgenMod = get_bgenCard_mod(hc_obj)[0]
            hairCard_proxy_mod = get_bgenCard_mod(hc_obj.modifiers[modName]["Socket_2"])[0]
            hairCard_proxy_mod.node_group.nodes["bgenCard_Material_Control"].inputs[0].default_value = bpy.data.materials[bgenCard_shader]

            hc_obj.modifiers[modName]["Socket_3"] = hairCard_proxy_mod["Socket_11"]
            hc_obj.modifiers[modName]["Socket_4"] = hairCard_proxy_mod["Socket_12"]
            
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = hc_obj
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.editmode_toggle()
            bpy.ops.curves.sculptmode_toggle()
              
        else:
            self.report({"ERROR"},message="Not a mesh object")
            return {"CANCELLED"}
        return{'FINISHED'}

class BGENCARD_OT_resample_guides(bpy.types.Operator):
    """Resamples the nuber of control points on a guide"""
    bl_idname = "object.bgencard_resample_guides"
    bl_label = "Resample guide"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False

        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        nodeID = get_bgenCard_mod(obj)[2]
        if not nodeID == bgenCard_node_ID:
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    
    resample : bpy.props.IntProperty(name= "Point count", soft_min= 4, soft_max= 50, default= (12)) # type: ignore

    def invoke(self, context, event):
        # Display a popup asking for the collection name
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        obj_ = obj
        #obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        if resample_curve_mod not in bpy.data.node_groups:
            ''' Gets VTS modifier from resouorce file''' 
            dirpath = os.path.dirname(os.path.realpath(__file__))
            resource_folder = os.path.join(dirpath,"resources")
            nodelib_path = os.path.join(resource_folder, "bgen_card_nodes.blend")

            with bpy.data.libraries.load(nodelib_path, link=False) as (data_from, data_to):
                data_to.node_groups = [resample_curve_mod]
        group = bpy.data.node_groups.get(resample_curve_mod)
        mod = obj_.modifiers.new(name="Resample_Guides", type='NODES')
        mod.node_group = group
        bpy.data.node_groups[resample_curve_mod].nodes["ID:resample_curve"].inputs[2].default_value = self.resample
        bpy.ops.object.select_all(action='DESELECT')
        obj_.select_set(True)
        bpy.context.view_layer.objects.active = obj_
        bpy.ops.object.modifier_apply(modifier=mod.name,report = True)

        obj_.hide_select = False
        bpy.context.view_layer.objects.active =  obj_
        obj_.select_set(True)
        bpy.ops.object.mode_set(mode="SCULPT_CURVES")

        return {'FINISHED'}
#=========================================================================================================    
#                                        [CUSTOM PROPERTIES]
#=========================================================================================================      
class BGENCARD_PT_bgenCardProperties(bpy.types.PropertyGroup):
    int_1: bpy.props.IntProperty(name="Count",soft_min= 2, soft_max= 50, default= (5)) # type: ignore #Count
    int_2: bpy.props.IntProperty(name="Resolution",soft_min= 2, soft_max= 6, default= (2)) # type: ignore #Resolution

    pinned_obj: bpy.props.PointerProperty(name="Pinned Object", type=bpy.types.Object,) # type: ignore

    def set_pin_obj(self, value):
        if value:
            self.pinned_obj = bpy.context.object
        else:
            self.pinned_obj = None
    
    def get_pin_obj(self):
        return self.pinned_obj is not None

    pin_obj : bpy.props.BoolProperty(name="Pin Object", description="Pins active object", default=False, set=set_pin_obj, get=get_pin_obj) # type: ignore

class BGENCARD_PT_bgenCardExpandProp(bpy.types.PropertyGroup):
    my_exp1 : bpy.props.BoolProperty(default=False) # type: ignore 
    my_exp2 : bpy.props.BoolProperty(default=False) # type: ignore
    my_exp3 : bpy.props.BoolProperty(default=False) # type: ignore
    my_exp4 : bpy.props.BoolProperty(default=False) # type: ignore
    my_exp5 : bpy.props.BoolProperty(default=False) # type: ignore
    my_exp6 : bpy.props.BoolProperty(default=False) # type: ignore Align Control

    hcp_exp1 : bpy.props.BoolProperty(default=False) # type: ignore 
    hcp_exp2 : bpy.props.BoolProperty(default=False) # type: ignore 
    hcp_exp3 : bpy.props.BoolProperty(default=False) # type: ignore 
    hcp_exp4 : bpy.props.BoolProperty(default=False) # type: ignore 
    hcp_exp5 : bpy.props.BoolProperty(default=False) # type: ignore 

    fc_exp1 : bpy.props.BoolProperty(default=False) # type: ignore
    fc_exp2 : bpy.props.BoolProperty(default=False) # type: ignore
    fc_exp3 : bpy.props.BoolProperty(default=False) # type: ignore
    fc_exp4 : bpy.props.BoolProperty(default=False) # type: ignore
    fc_exp5 : bpy.props.BoolProperty(default=False) # type: ignore
    
#=========================================================================================================    
#                                           [PANEL LAYOUT]
#=========================================================================================================
class BGENCARD_PT_ui_panel(bpy.types.Panel):
    bl_label = " BGEN Card"
    bl_idname = "OBJECT_PT_bgenCard_ui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' 
    bl_category = 'BGEN HAIR'
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon_value=icons["BGEN_CARD"].icon_id)
        
    def draw(self, context):
        addon_updater_ops.update_notice_box_ui(self,context)
        if context.active_object is not None:
            bgenCard_tools = context.scene.bgenCard_tools
            obj_exp = context.object.bgenCard_expand
            if bgenCard_tools.pin_obj == True:
                obj = bpy.data.objects[bpy.context.scene.bgenCard_tools.pinned_obj.name]
            else:
                obj = context.active_object
        else:
            obj = context.active_object

        

        if context.active_object is None:
            layout = self.layout                
            col = layout.column()
            box = col.box()
            box1 = box.box()
            
            col_nt = box1.column()
            col_nt.scale_y = 1.4
            row_nt = col_nt.row(align = True)
            row_nt.scale_x = 1.2

            row_nt.alignment = "CENTER"
            row_nt.label(text="[Not Applicable]")

            box = col.box()
            col1 = box.column()
            col1.scale_y = 1
            col1.alignment = "CENTER"
            col1.label(text = "No selected Object", icon = "ERROR")

        elif get_bgenCard_mod(obj)[2] == bgenCardProxy_node_ID:
            bgenMod = get_bgenCard_mod(obj)[0]
            bgenModName = get_bgenCard_mod(obj)[1]

            layout = self.layout
            col = layout.column()
            box1 = col.box()
            
            box2 = box1.box()
            box2.scale_y = 1.4
            col_nt = box2.column()
            row_nt = col_nt.row(align = True)
            row_nt.scale_x = 1.2

            row_nt.operator_menu_enum("object.bgencard_choose_nodetree_proxy",'bgenCard_nodes', text="" , icon = "NODETREE")
            try:
                mn = bpy.data.node_groups[bgenModName]
                row_nt.prop(mn,"name", text = "",toggle=True, emboss = True)
                row_nt.prop(mn,"use_fake_user", text = "",toggle=True, emboss = True)
                
            except:
                row_nt.alignment = "CENTER"
                row_nt.label(text="[Not Applicable]")

            row_nt.operator("object.bgencard_single_user_proxy", text="", icon = "DUPLICATE" )

            #==========================================================================    
            box_main = col.box()
            row_main = box_main.row()

            row_label = row_main.row(align=False)
            row_label.alignment = "LEFT"
            
            # OBJECT LABELING
            if bgenCard_tools.pin_obj == True:
                obj_ac = bgenCard_tools.pinned_obj
            else:
                obj_ac = bpy.context.active_object

            if get_bgenCard_mod(obj_ac)[2] == bgenCard_node_ID:
                if not obj_ac.modifiers[get_bgenCard_mod(obj_ac)[0].name]["Socket_2"] is None:
                    card_proxy_name = obj_ac.modifiers[get_bgenCard_mod(obj_ac)[0].name]["Socket_2"].name
                else:
                    card_proxy_name = "[No Card Proxy]"
                row_label.label(text = obj_ac.name, icon = "OUTLINER_OB_CURVES")
                row_label.label(text = "", icon = 'RIGHTARROW')
                row_label.label(text = card_proxy_name, icon = "OBJECT_DATAMODE")
            
            elif get_bgenCard_mod(obj_ac)[2] == bgenCardProxy_node_ID:
                row_label.label(text = "CARD PROXY | ", icon = "ALIGN_JUSTIFY")
                row_label.label(text = obj_ac.name, icon = "OBJECT_DATAMODE")
            else:
                row_label.label(text = obj_ac.name, icon = "OBJECT_DATAMODE")


            row_pin = row_main.row()
            row_pin.alignment = "RIGHT"
            row_pin.prop(bgenCard_tools, "pin_obj", text="", icon = "PINNED" if bgenCard_tools.pin_obj else "UNPINNED", icon_only = True, emboss=False)

            #========================================================================================================= 
            # OBJECT NAME
            #========================================================================================================= 
            col_menu = box_main.column()
            box_ = col_menu.box()
            col_ = box_.column()
            col_.scale_y = 1.2
            row_ = col_.row(align=True)
            row_.scale_x = 1.1
            row_.prop(obj, 'name', text = '')
            row_.prop(obj, 'hide_select', text = '')
            row_.prop(obj, 'hide_render', text = '')

            #========================================================================================================= 
            # HAIR CARD PROXY
            #========================================================================================================= 
            #col_menu = box_main.column()
            box_ = col_menu.box()
            col_ = box_.column()
            col_.scale_y = 1.2
            row_ = col_.row()

            if obj_exp.hcp_exp1:
                row_.prop(obj_exp, "hcp_exp1",icon="TRIA_DOWN", text="HAIR CARD PROXY", emboss=False)
                row_.label(text = "", icon = "OUTLINER_OB_CURVES")

                matCntr = bpy.data.node_groups[bgenModName].nodes["bgenCard_Material_Control"].inputs[0]
                matNode = bpy.data.node_groups[bgenModName].nodes["bgenCard_Material_Control"]
                boxIn = col_.box()
                rowIn = boxIn.row()
                grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.alignment = "RIGHT"
                grid_l.scale_x = 1.8
                grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                #grid_l.label(text = " Object Name")
                grid_l.label(text = " Card Name")
                grid_l.label(text = "        Count")
                grid_l.label(text = " Resolution") 
                grid_l.label(text = "     Material")

                #grid_r.prop(obj, 'name', text = '')
                grid_r.prop(bgenMod, '["Socket_20"]', text = '')
                grid_r.prop(bgenMod, '["Socket_11"]', text = '')
                grid_r.prop(bgenMod, '["Socket_12"]', text = '') 
                matCntr.draw(context, grid_r, matNode, text = '')
                #grid_r.prop(bgenMod, '["Socket_15"]', text = '')
            else:
                row_.prop(obj_exp, "hcp_exp1",icon="TRIA_RIGHT", text="HAIR CARD PROXY", emboss=False)
                row_.label(text = "", icon = "OUTLINER_OB_CURVES")

            #========================================================================================================= 
            # UV CONTROL
            #========================================================================================================= 
            box_ = col_menu.box()
            col_ = box_.column()
            col_.scale_y = 1.2
            row_ = col_.row()

            if obj_exp.hcp_exp2:
                row_.prop(obj_exp, "hcp_exp2",icon="TRIA_DOWN", text="UV CONTROL", emboss=False)
                row_.label(text = "", icon = "UV")

                boxIn = col_.box()
                #-----------------------------------------------------------------------------------------------------
                rowIn = boxIn.row()
                grid_l = rowIn.grid_flow(row_major=True, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.alignment = "RIGHT"
                grid_l.scale_x = 1
                grid_r = rowIn.grid_flow(row_major=True, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.label(text = "Move X")
                grid_r.prop(bgenMod, '["Socket_3"]', text = '')

                grid_l = rowIn.grid_flow(row_major=True, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.alignment = "RIGHT"
                grid_l.scale_x = 1
                grid_r = rowIn.grid_flow(row_major=True, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.label(text = "Move Y")
                grid_r.prop(bgenMod, '["Socket_4"]', text = '')
                #-----------------------------------------------------------------------------------------------------
                rowIn = boxIn.row()
                grid_l = rowIn.grid_flow(row_major=True, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.alignment = "RIGHT"
                grid_l.scale_x = 1
                grid_r = rowIn.grid_flow(row_major=True, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.label(text = "Scale X") 
                grid_r.prop(bgenMod, '["Socket_5"]', text = '')

                grid_l = rowIn.grid_flow(row_major=True, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.alignment = "RIGHT"
                grid_l.scale_x = 1
                grid_r = rowIn.grid_flow(row_major=True, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.label(text = "Scale Y")
                grid_r.prop(bgenMod, '["Socket_6"]', text = '')

                #------------------------------------------------------------------------------------------------------
                col2 = boxIn.column()
                col2.prop(bgenMod, '["Socket_7"]', text = 'Scale') 
                col2.prop(bgenMod, '["Socket_8"]', text = 'Angle')

            else:
                row_.prop(obj_exp, "hcp_exp2",icon="TRIA_RIGHT", text="UV CONTROL", emboss=False)
                row_.label(text = "", icon = "UV")

            #========================================================================================================= 
            # UV PREVIEW CONTROL
            #========================================================================================================= 
            box_ = col_menu.box()
            col_ = box_.column()
            col_.scale_y = 1.2
            row_ = col_.row()

            if obj_exp.hcp_exp3:
                row_.prop(obj_exp, "hcp_exp3",icon="TRIA_DOWN", text="UV PREVIEW", emboss=False)
                row_.prop(bgenMod, '["Socket_9"]', text = '')

                boxIn = col_.box()
                rowIn = boxIn.row()
                grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.alignment = "RIGHT"
                grid_l.scale_x = 1.8
                grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                grid_l.label(text = "Preview Scale")
                grid_l.label(text = "   X Position")
                grid_l.label(text = "   Y Position") 

                grid_r.prop(bgenMod, '["Socket_17"]', text = '')
                grid_r.prop(bgenMod, '["Socket_18"]', text = '')
                grid_r.prop(bgenMod, '["Socket_19"]', text = '') 
            else:
                row_.prop(obj_exp, "hcp_exp3",icon="TRIA_RIGHT", text="UV PREVIEW", emboss=False)
                row_.prop(bgenMod, '["Socket_9"]', text = '')

        elif get_bgenCard_mod(obj)[2] == bgenCard_node_ID:
            bgenMod = get_bgenCard_mod(obj)[0]
            bgenModName = get_bgenCard_mod(obj)[1]

            layout = self.layout
            col = layout.column()
            box1 = col.box()
            
            box2 = box1.box()
            box2.scale_y = 1.4
            col_nt = box2.column()
            row_nt = col_nt.row(align = True)
            row_nt.scale_x = 1.2

            row_nt.operator_menu_enum("object.bgencard_choose_nodetree",'bgenCard_nodes', text="" , icon = "NODETREE")
            try:
                mn = bpy.data.node_groups[bgenModName]
                row_nt.prop(mn,"name", text = "",toggle=True, emboss = True)
                row_nt.prop(mn,"use_fake_user", text = "",toggle=True, emboss = True)
                
            except:
                row_nt.alignment = "CENTER"
                row_nt.label(text="[Not Applicable]")

            row_nt.operator("object.bgencard_single_user", text="", icon = "DUPLICATE" )

            #==========================================================================    
            box_main = col.box()
            row_main = box_main.row()

            row_label = row_main.row(align=False)
            row_label.alignment = "LEFT"
            
            # OBJECT LABELING
            if bgenCard_tools.pin_obj == True:
                obj_ac = bgenCard_tools.pinned_obj
            else:
                obj_ac = bpy.context.active_object

            if get_bgenCard_mod(obj_ac)[2] == bgenCard_node_ID:
                row_label.label(text = "CARD | ", icon = "ALIGN_JUSTIFY")
                if not obj_ac.modifiers[get_bgenCard_mod(obj_ac)[0].name]["Socket_2"] is None:
                    card_proxy_name = obj_ac.modifiers[get_bgenCard_mod(obj_ac)[0].name]["Socket_2"].name
                else:
                    card_proxy_name = "[No Card Proxy]"
                row_label.label(text = obj_ac.name, icon = "OUTLINER_OB_CURVES")
                row_label.label(text = "", icon = 'RIGHTARROW')
                row_label.label(text = card_proxy_name, icon = "OBJECT_DATAMODE")
            
            elif get_bgenCard_mod(obj_ac)[2] == bgenCardProxy_node_ID:
                row_label.label(text = obj_ac.name, icon = "OBJECT_DATAMODE")
            else:
                row_label.label(text = obj_ac.name, icon = "OBJECT_DATAMODE")


            row_pin = row_main.row()
            row_pin.alignment = "RIGHT"
            row_pin.prop(bgenCard_tools, "pin_obj", text="", icon = "PINNED" if bgenCard_tools.pin_obj else "UNPINNED", icon_only = True, emboss=False)
            
            #========================================================================================================= 
            # OBJECT NAME
            #========================================================================================================= 
            col_menu = box_main.column()
            box_ = col_menu.box()
            col_ = box_.column()
            col_.scale_y = 1.4
            row_ = col_.row(align=True)
            row_.scale_x = 1.1
            
            row_.prop(obj, 'name', text = '', icon="OUTLINER_OB_CURVES")
            row_.prop(obj, 'hide_select', text = '')
            row_.prop(obj, 'hide_render', text = '')
            #========================================================================================================= 
            # CARD GEOMETRY
            #========================================================================================================= 
            #col_menu = box_main.column()
            box_ = col_menu.box()
            col_ = box_.column()
            col_.scale_y = 1.2
            row_ = col_.row()

            if obj_exp.my_exp1:
                row_.prop(obj_exp, "my_exp1",icon="TRIA_DOWN", text="CARD GEOMETRY", emboss=False)
                row_.prop(bgenMod, '["Socket_40"]', text = '')
                
                if not bgenMod["Socket_2"] is None:
                    card_proxy_name = obj.modifiers[get_bgenCard_mod(obj)[0].name]["Socket_2"].name
                    card_proxy_mod = get_bgenCard_mod(bpy.data.objects[card_proxy_name])[0]

                    boxIn = col_.box()
                    colIn = boxIn.column()
                    #colIn.label(text="CARD PROXY RESOLUTION")
                    #colIn.operator("object.bgencard_link_proxy", text="Link Proxy")

                    rowIn = colIn.row(align=True)
                    rowIn.scale_y = 1.4
                    rowIn.prop(bgenMod, '["Socket_7"]', text = 'Bezier Curve', expand = True, icon = "OUTLINER_OB_CURVES", invert_checkbox = True)
                    rowIn.prop(bgenMod, '["Socket_7"]', text = 'Hair Curve', expand = True, icon = "OUTLINER_OB_CURVES")
                    if obj.type == "CURVES":
                        colIn = boxIn.column()
                        colIn.scale_y = 1
                        colIn.operator("object.bgencard_resample_guides", text="Resample Curve", icon = "OUTLINER_OB_CURVES",depress=True)

                    rowIn = boxIn.row()
                    grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    grid_l.alignment = "RIGHT"
                    grid_l.scale_x = 1.8
                    grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                    grid_l.label(text = " HairCard Proxy")
                    grid_l.separator()
                    grid_l.label(text = "      Count Main")
                    #grid_l.label(text = "               Count")
                    #grid_l.separator()
                    grid_l.label(text = "Resolution Main")
                    #grid_l.label(text = "        Resolution") 

                    grid_r.prop(bgenMod, '["Socket_2"]', text = '')
                    grid_r.separator()
                    grid_r.prop(card_proxy_mod, '["Socket_11"]', text = '')
                    #grid_r.prop(bgenMod, '["Socket_3"]', text = '')
                    #grid_r.separator()
                    grid_r.prop(card_proxy_mod, '["Socket_12"]', text = '')
                    #grid_r.prop(bgenMod, '["Socket_4"]', text = '') 

                    
                
                else:
                    boxIn = col_.box()
                    colIn = boxIn.column()
                    #colIn.label(text="CARD PROXY RESOLUTION")

                    rowIn = boxIn.row()
                    grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    grid_l.alignment = "RIGHT"
                    grid_l.scale_x = 1.8
                    grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                    grid_l.label(text = " HairCard Proxy")
                    grid_r.prop(bgenMod, '["Socket_2"]', text = '')

                boxIn = col_.box()
                rowIn = boxIn.row()
                grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.alignment = "RIGHT"
                grid_l.scale_x = 1.8
                grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                grid_l.label(text = "     Card Width")
                grid_l.label(text = "         Card Arc")
                grid_l.label(text = "    Card Subdiv")

                grid_r.prop(bgenMod, '["Socket_5"]', text = '')
                grid_r.prop(bgenMod, '["Socket_6"]', text = '')
                grid_r.prop(bgenMod, '["Socket_26"]', text = '')

                # [Profile Float Curve]
                #------------------------------------------------------------------------------------------
                boxIn = col_.box()
                rowIn = boxIn.row()
                fc_profile = bpy.data.node_groups[bgenModName].nodes['bgenCard_profile_curve']
                
                if obj_exp.fc_exp1:
                    rowIn.prop(obj_exp, "fc_exp1",icon="TRIA_DOWN", text="Card Profile", emboss=False)
                    rowIn.label(text="",icon="FCURVE")
                    fc_profile.draw_buttons_ext(context, boxIn)
                else:
                    rowIn.prop(obj_exp, "fc_exp1",icon="TRIA_RIGHT", text="Card Profile", emboss=False)
                    rowIn.label(text="",icon="FCURVE")
                #------------------------------------------------------------------------------------------
                    
                if not bgenMod["Socket_2"] is None:
                    card_proxy_name = obj.modifiers[get_bgenCard_mod(obj)[0].name]["Socket_2"].name
                    proxy_name = get_bgenCard_mod(bpy.data.objects[card_proxy_name])[0]["Socket_20"]
                    proxy_count = get_bgenCard_mod(bpy.data.objects[card_proxy_name])[0]["Socket_11"]
                    proxy_resolution = get_bgenCard_mod(bpy.data.objects[card_proxy_name])[0]["Socket_12"]
                    col2 = col_.column()
                    row2 = col_.row()
                    row2.alignment = "LEFT"
                    row2.label(text=  str(proxy_name) + "   |",icon="ALIGN_JUSTIFY")
                    row2.label(text= "Count: " + str(proxy_count))
                    row2.label(text= "Resolution: " + str(proxy_resolution))
            else:
                row_.prop(obj_exp, "my_exp1",icon="TRIA_RIGHT", text="CARD GEOMETRY", emboss=False)
                row_.prop(bgenMod, '["Socket_40"]', text = '')

            
            #========================================================================================================= 
            # ALIGN CONTROL
            #=========================================================================================================
            if obj.type == "CURVES":
                box_ = col_menu.box()
                col_ = box_.column(align=True)
                col_.scale_y = 1.2
                row_ = col_.row()

                if obj_exp.my_exp6:
                    row_.prop(obj_exp, "my_exp6",icon="TRIA_DOWN", text="ALIGN TO SURFACE", emboss=False)
                    row_.prop(bgenMod, '["Socket_39"]', text = '')

                    boxIn = col_.box()
                    rowIn = boxIn.row()
                    grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    grid_l.alignment = "RIGHT"
                    grid_l.scale_x = 1.2
                    grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    
                    grid_l.label(text = "  Align Root")
                    grid_l.label(text = "   Align Tip")
                    grid_l.label(text = "Align Factor")

                    grid_r.prop(bgenMod, '["Socket_43"]', text = '')
                    grid_r.prop(bgenMod, '["Socket_44"]', text = '')
                    grid_r.prop(bgenMod, '["Socket_45"]', text = '')
                    
                else:
                    row_.prop(obj_exp, "my_exp6",icon="TRIA_RIGHT", text="ALIGN TO SURFACE", emboss=False)
                    row_.prop(bgenMod, '["Socket_39"]', text = '')

            #========================================================================================================= 
            # INTERPOLATE CONTROL
            #=========================================================================================================
            if obj.type == "CURVES":
                box_ = col_menu.box()
                col_ = box_.column(align=True)
                col_.scale_y = 1.2
                row_ = col_.row()

                if obj_exp.my_exp2:
                    row_.prop(obj_exp, "my_exp2",icon="TRIA_DOWN", text="INTERPOLATE CONTROL", emboss=False)
                    row_.prop(bgenMod, '["Socket_38"]', text = '')

                    #-------------------------------------------------------------------------------------------
                    dmCntr = bpy.data.node_groups[bgenModName].nodes["bgenCard_density_mask_control"].inputs[1]
                    dmNode = bpy.data.node_groups[bgenModName].nodes["bgenCard_density_mask_control"]

                    pmCntr = bpy.data.node_groups[bgenModName].nodes["bgenCard_parting_mask_control"].inputs[1]
                    pmNode = bpy.data.node_groups[bgenModName].nodes["bgenCard_parting_mask_control"]
                    #-------------------------------------------------------------------------------------------
                    boxIn = col_.box()
                    rowIn = boxIn.row()
                    grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    grid_l.alignment = "RIGHT"
                    grid_l.scale_x = 1.2
                    grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    
                    grid_l.label(text = "                     Attach To")
                    grid_l.label(text = "               UVMap Name")
                    grid_r.prop(bgenMod, '["Socket_31"]', text = '')
                    grid_r.prop(bgenMod, '["Socket_32"]', text = '')
                    #--------------------------------------------------------------------------------------------------------
                    boxIn = col_.box()

                    #rowIn = boxIn.row(align=True)
                    #rowIn.prop(bgenMod, '["Socket_33"]', text = 'Choose Mask From Addon', icon="TEXTURE") 
                    #rowIn.prop(bgenMod, '["Socket_33"]', text = 'Choose Mask From Modifier', invert_checkbox=True, icon="TEXTURE") 

                    rowIn = boxIn.row()
                    grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    grid_l.alignment = "RIGHT"
                    grid_l.scale_x = 1.2
                    grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                    grid_l.label(text = "             Density Mask")
                    grid_l.label(text = "              Parting Mask")
                    
                    dmCntr.draw(context, grid_r, dmNode, text = '')
                    pmCntr.draw(context, grid_r, pmNode, text = '')
                    #--------------------------------------------------------------------------------------------------------
                    boxIn = col_.box()
                    rowIn = boxIn.row()
                    grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    grid_l.alignment = "RIGHT"
                    grid_l.scale_x = 1.2
                    grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                    grid_l.label(text = "  Interpolation Amount")
                    grid_l.label(text = "   Interpolation Guides")
                    grid_l.label(text = "      Surface Resolution")
                    grid_r.prop(bgenMod, '["Socket_35"]', text = '')
                    grid_r.prop(bgenMod, '["Socket_37"]', text = '')
                    grid_r.prop(bgenMod, '["Socket_42"]', text = '')
                    #--------------------------------------------------------------------------------------------------------
                    boxIn = col_.box()
                    rowIn = boxIn.row(align=False)
                    grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    grid_l.alignment = "RIGHT"
                    grid_l.scale_x = 1.2
                    grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    
                    grid_l.label(text = "Follow Surface Normal")
                    #rowIn.prop(bgenMod, '["Socket_39"]', text = "Align Cards to Surface",icon="NORMALS_FACE")
                    grid_r.prop(bgenMod, '["Socket_41"]', text = "")
                    #--------------------------------------------------------------------------------------------------------
                    

                    # [Clump Float Curve]
                    #------------------------------------------------------------------------------------------
                    boxIn = col_.box()
                    rowIn = boxIn.row()
                    fc_profile = bpy.data.node_groups[bgenModName].nodes['bgenCard_clump_curve']
                    
                    if obj_exp.fc_exp2:
                        rowIn.prop(obj_exp, "fc_exp2",icon="TRIA_DOWN", text="Clump Profile", emboss=False)
                        rowIn.label(text="",icon="FCURVE")
                        fc_profile.draw_buttons_ext(context, boxIn)
                    else:
                        rowIn.prop(obj_exp, "fc_exp2",icon="TRIA_RIGHT", text="Clump Profile", emboss=False)
                        rowIn.label(text="",icon="FCURVE")
                    #------------------------------------------------------------------------------------------
                
                else:
                    row_.prop(obj_exp, "my_exp2",icon="TRIA_RIGHT", text="INTERPOLATE CONTROL", emboss=False)
                    row_.prop(bgenMod, '["Socket_38"]', text = '')
                    
            #========================================================================================================= 
            # DUPLICATE CONTROL
            #=========================================================================================================
            box_ = col_menu.box()
            col_ = box_.column()
            col_.scale_y = 1.2
            row_ = col_.row()

            if obj_exp.my_exp3:
                row_.prop(obj_exp, "my_exp3",icon="TRIA_DOWN", text="DUPLICATE CONTROL", emboss=False)
                row_.prop(bgenMod, '["Socket_27"]', text = '')

                boxIn = col_.box()
                rowIn = boxIn.row()
                grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.alignment = "RIGHT"
                grid_l.scale_x = 2.8
                grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                grid_l.label(text = " Amount")
                grid_l.label(text = "  Radius")
                grid_l.separator()
                grid_l.label(text = "Scale X") 
                grid_l.label(text = "Scale Y")
                grid_l.label(text = "Scale Z")
                grid_l.separator()
                grid_l.label(text = "    Seed")

                grid_r.prop(bgenMod, '["Socket_11"]', text = '')
                grid_r.prop(bgenMod, '["Socket_12"]', text = '')
                grid_r.separator()
                grid_r.prop(bgenMod, '["Socket_13"]', text = '') 
                grid_r.prop(bgenMod, '["Socket_14"]', text = '')
                grid_r.prop(bgenMod, '["Socket_15"]', text = '')
                grid_r.separator()
                grid_r.prop(bgenMod, '["Socket_18"]', text = '')

                if obj.type == "CURVES":
                    rowIn = boxIn.row()
                    rowIn.prop(bgenMod, '["Socket_39"]', text = "Align Cards to Surface",icon="NORMALS_FACE")

                # [Clump Float Curve]
                #------------------------------------------------------------------------------------------
                boxIn = col_.box()
                rowIn = boxIn.row()
                fc_profile = bpy.data.node_groups[bgenModName].nodes['bgenCard_clump_curve']
                
                if obj_exp.fc_exp3:
                    rowIn.prop(obj_exp, "fc_exp3",icon="TRIA_DOWN", text="Clump Profile", emboss=False)
                    rowIn.label(text="",icon="FCURVE")
                    fc_profile.draw_buttons_ext(context, boxIn)
                else:
                    rowIn.prop(obj_exp, "fc_exp3",icon="TRIA_RIGHT", text="Clump Profile", emboss=False)
                    rowIn.label(text="",icon="FCURVE")
                #------------------------------------------------------------------------------------------
                    
            else:
                row_.prop(obj_exp, "my_exp3",icon="TRIA_RIGHT", text="DUPLICATE CONTROL", emboss=False)
                row_.prop(bgenMod, '["Socket_27"]', text = '')

            #========================================================================================================= 
            # CURL CONTROL
            #=========================================================================================================
            box_ = col_menu.box()
            col_ = box_.column()
            col_.scale_y = 1.2
            row_ = col_.row()

            if obj_exp.my_exp4:
                row_.prop(obj_exp, "my_exp4",icon="TRIA_DOWN", text="CURL CONTROL", emboss=False)
                row_.prop(bgenMod, '["Socket_21"]', text = '')

                boxIn = col_.box()
                rowIn = boxIn.row()
                grid_l = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                grid_l.alignment = "RIGHT"
                grid_l.scale_x = 1.6
                grid_r = rowIn.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                grid_l.label(text = " Curl Resolution")
                grid_l.label(text = " Curl Amplitude")
                grid_l.label(text = "       Curl Radius") 
                grid_l.label(text = "  Random Offset")
                grid_l.label(text = "            RO Seed")

                grid_r.prop(bgenMod, '["Socket_25"]', text = '')
                grid_r.prop(bgenMod, '["Socket_22"]', text = '')
                grid_r.prop(bgenMod, '["Socket_23"]', text = '') 
                grid_r.prop(bgenMod, '["Socket_24"]', text = '')
                grid_r.prop(bgenMod, '["Socket_28"]', text = '')

                # [Curl Float Curve]
                #------------------------------------------------------------------------------------------
                boxIn = col_.box()
                rowIn = boxIn.row()
                fc_profile = bpy.data.node_groups[bgenModName].nodes['bgenCard_curl_curve']
                
                if obj_exp.fc_exp4:
                    rowIn.prop(obj_exp, "fc_exp4",icon="TRIA_DOWN", text="Curl Profile", emboss=False)
                    rowIn.label(text="",icon="FCURVE")
                    fc_profile.draw_buttons_ext(context, boxIn)
                else:
                    rowIn.prop(obj_exp, "fc_exp4",icon="TRIA_RIGHT", text="Curl Profile", emboss=False)
                    rowIn.label(text="",icon="FCURVE")
                #------------------------------------------------------------------------------------------

            else:
                row_.prop(obj_exp, "my_exp4",icon="TRIA_RIGHT", text="CURL CONTROL", emboss=False)
                row_.prop(bgenMod, '["Socket_21"]', text = '')

        else:
            layout = self.layout
            col = layout.column()

            # OBJECT LABELING
            if bgenCard_tools.pin_obj == True:
                obj_ac = bgenCard_tools.pinned_obj
            else:
                obj_ac = bpy.context.active_object

            box = col.box()
            row1 = box.row()
            row1.scale_y = 1.4
            
            row1.prop(obj_ac,"name", text = "",toggle=True, emboss = True, icon="OBJECT_DATAMODE")

            '''col1 = row1.column()
            col1.scale_y = 1.4
            col1.alignment = "CENTER"
            col1.label(text = "", icon = "OBJECT_DATAMODE")
            col1.prop(obj,"name", text = "",toggle=True, emboss = True,icon="OBJECT_DATAMODE")
            #col1.label(text = obj.name, icon = "OBJECT_DATAMODE")'''

            row_pin = row1.row()
            row_pin.alignment = "RIGHT"
            row_pin.prop(bgenCard_tools, "pin_obj", text="", icon = "PINNED" if bgenCard_tools.pin_obj else "UNPINNED", icon_only = True, emboss=False)

            box1 = box.box()
            col1 = box1.column()
            col1.separator(factor=.3)
            col1.scale_y = 2
            rows = col1.row()
            
            rows.operator("object.add_bgen_card", text="Add Groom HairCard", icon = "ADD",depress=True)
            rows.operator("object.add_bgen_card_mod", text="Add Hair Card", icon = "ADD",depress=True)
            
            #col1.separator(factor=.5)
            #col1.operator("object.add_bgen_card", text="Remove bgen mod", icon = "REMOVE")
            #col1.separator(factor=.3)


@addon_updater_ops.make_annotations
class BGENCARD_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    # Addon updater preferences.
    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True)

    updater_interval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0)

    updater_interval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=1,
        min=0,
        max=31)

    updater_interval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23)

    updater_interval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59)
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        box = col.box()
        col1 = box.column()
        col1.label(text= "Prefereces go here")  
        
        addon_updater_ops.update_settings_ui(self,context)           
#=========================================================================================================    
#                                             [REGISTER]       
#=========================================================================================================
bgenCard_classes = (BGENCARD_PT_bgenCardProperties, BGENCARD_PT_bgenCardExpandProp, BGENCARD_PT_ui_panel, BGENCARD_OT_choose_nodeTree, BGENCARD_OT_single_user,
                    BGENCARD_OT_choose_nodeTree_proxy, BGENCARD_OT_single_user_proxy,BGENCARD_OT_link_proxy,BGENCARD_OT_add_bgen_card, 
                    BGENCARD_OT_add_bgen_card_mod, BGENCARD_OT_resample_guides,BGENCARD_preferences)
                

def register():  
    addon_updater_ops.register(bl_info)
    for cls in bgenCard_classes:
        addon_updater_ops.make_annotations(cls)
        bpy.utils.register_class(cls)
    bpy.types.Scene.bgenCard_tools = bpy.props.PointerProperty(type= BGENCARD_PT_bgenCardProperties)
    bpy.types.Object.bgenCard_expand = bpy.props.PointerProperty(type= BGENCARD_PT_bgenCardExpandProp)
                   
def unregister(): 
    addon_updater_ops.unregister()
    for cls in bgenCard_classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bgenCard_tools
    del bpy.types.Object.bgenCard_expand
