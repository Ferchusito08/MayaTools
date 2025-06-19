#---------------------------/VARIABLES\--------------------------#

# Maya Libraries
import maya.cmds as cmds

# Global Variables
sel_ctrl = [None] # The first necessary step to add atributes, select a control
attr_rows = [] # Row list to add new atributes

row_height = 32 # Separation between new atributes added
max_height = 400 # Maximum height of the UI
max_width = 632 # Maximum width of the UI

# Function to be sure there is a Ctrl selected or not
def sel_control():
    sel = cmds.ls(selection=True)
    if sel:
        sel_ctrl[0] = sel[0]
        cmds.text("ctrl_label", e=True, label=f"Add attributes to: {sel[0]}")
    else:
        cmds.warning("Please select a node in Outliner")

#------------------------------/CODE\------------------------------#

# Function to update height of attributes UI
def update_height():
    n = len(attr_rows)
    new_h = min(max(n * row_height, row_height * 2), max_height) # Almost two rows of height
    cmds.scrollLayout("attr_scroll", e=True, h=new_h) # When maximum height is reached, we create a scroll for more attributes

# Function to add rows of attributes to UI
def add_attrs(from_data=None):
#-------------------------------------------------------------------#  
    # Connect to add attribute button
    cmds.setParent("attrs_list")
    
    # Create rows of attributes
    cols = cmds.columnLayout(adj=True)
    row = cmds.rowLayout(nc=8, adjustableColumn=(1,3,6,7), columnAlign=(1, 'left'), h=row_height, parent=cols)
    # Widths for each part of the attribute creation
    cmds.rowLayout(row, e=True,
        columnWidth=[
            (1, 140),  # attrs_field
            (2, 30),   # selection button
            (3, 140),  # target_field
            (4, 150),  # dropdown menu
            (5, 60),   # type menu
            (6, 30),   # delete button
            (7, 80),   # checker
            (8, 100)   # group_field
        ]
    )
#-------------------------------------------------------------------#  
    # Attribute name field
    attrs_field = cmds.textField(placeholderText='Attribute Name')
    # Button to add target_field node
    target_sel = cmds.button(label="🎯")
    # Target Node name field
    target_field = cmds.textField(placeholderText='Target Node Name', editable=False)   
#-------------------------------------------------------------------#  
    # Menu dropdown for attribute selection
    attr_menu = cmds.optionMenu(label="", w=200)    
    cmds.menuItem(label="Choose Node", parent=attr_menu)                        
#-------------------------------------------------------------------#  
    # Menu dropdown for types of attributes
    type_menu = cmds.optionMenu(label="", w=100)
    # Types
    types = ["bool", "float", "int", "string"]
    
    for label in types:
        cmds.menuItem(label=label, parent=type_menu)       
#-------------------------------------------------------------------#  
    # Update menu dropdown
    def update_UI(*args):
        node = cmds.textField(target_field, q=True, text=True)
        cmds.optionMenu(attr_menu, e=True, deleteAllItems=True) # Empty list attributes
                
        if cmds.objExists(node):
            attrs = cmds.listAttr(node, keyable=True) or []
            for a in attrs:
                cmds.menuItem(label=a, parent=attr_menu)
        else:
            cmds.menuItem(label="Node doesn't exist", parent=attr_menu)    
#-------------------------------------------------------------------#      
    # Function for the selection button (🎯)
    def sel_node():
        sel = cmds.ls(selection=True)
        if sel:
            cmds.textField(target_field, e=True, text=sel[0])
            update_UI()
        else:
            cmds.warning("Select a node from outliner")
            
    cmds.button(target_sel, e=True, c=lambda *_: sel_node())
    cmds.textField(target_field, e=True, changeCommand=update_UI)       
#-------------------------------------------------------------------#  
    # Delete rows from attribute creation
    def delete_row():
        for i, row in enumerate(attr_rows):
            if row["cols"] == cols:
                cmds.deleteUI(cols)
                attr_rows.pop(i)
                update_height()
                break            
#-------------------------------------------------------------------# 
    # Checker Box
    checker_box = cmds.checkBox(label="Group Checker", v=False) 
    # Group Field name
    group_field = cmds.textField(placeholderText="Group Name") 
    # Deactivate
    cmds.textField(group_field, e=True, editable=False) 
    # Create a button to delete attribute rows
    cmds.button(label="❌", c=lambda *_: delete_row())   
#-------------------------------------------------------------------#      
    # Control data from attribute list
    if from_data:
        # Put data into textFields
        cmds.textField(attrs_field, e=True, text=cmds.textField(from_data["attrs_field"], q=True, text=True))
        cmds.textField(target_field, e=True, text=cmds.textField(from_data["target_field"], q=True, text=True))
        update_UI()
        
        # Update dropdowns
        new_attr = cmds.optionMenu(from_data["attr_menu"], q=True, value=True)
        new_type = cmds.optionMenu(from_data["type_menu"], q=True, value=True)
        cmds.optionMenu(attr_menu, e=True, value=new_attr)
        cmds.optionMenu(type_menu, e=True, value=new_type)
        cmds.checkBox(checker_box, e=True, value=cmds.checkBox(from_data["checker_box"], q=True, value=True))
        cmds.textField(group_field, e=True, text=cmds.textField(from_data["group_field"], q=True, text=True))

    update_height()            
#-------------------------------------------------------------------# 
    # Function to activate group text field woth checker box
    def toggle_group_name(*args):
        is_enabled = cmds.checkBox(checker_box, q=True, value=True)
        cmds.textField(group_field, e=True, editable=is_enabled)
    
    # Change status of group name textfield
    cmds.checkBox(checker_box, e=True, cc=toggle_group_name)
#-------------------------------------------------------------------#  
    # Structure of attribute list
    attr_rows.append({
        "cols": cols,
        "attrs_field": attrs_field,
        "target_field": target_field,
        "attr_menu": attr_menu,
        "type_menu": type_menu,
        "checker_box": checker_box,
        "group_field": group_field
    })   
#-------------------------------------------------------------------# 
 
# Function to delete attributes
def delete_attrs(*_):
    # Take attributes from selection in channel box
    sel_attrs = cmds.channelBox('mainChannelBox', q=True, selectedMainAttributes=True)
    nodes = cmds.ls(selection=True)

    # Be sure something in the channel box is selected
    if not sel_attrs or not nodes:
        cmds.warning("Select at least one attribute in the Channel Box")
        return
    
    # Loop on nodes selected
    for node in nodes:
        for attr in sel_attrs:
            full_attr = f"{node}.{attr}"
            if cmds.objExists(full_attr):
                try:
                    # Delete this attribute
                    cmds.deleteAttr(full_attr)
                except Exception as e:
                    cmds.warning(f"Could not delete {full_attr}: {e}")
#-------------------------------------------------------------------# 
 
# Function to delete attributes
def hide_attrs(*_):
    # Take attributes from selection in channel box
    sel_attrs = cmds.channelBox('mainChannelBox', q=True, selectedMainAttributes=True)
    nodes = cmds.ls(selection=True)

    # Be sure something in the channel box is selected
    if not sel_attrs or not nodes:
        cmds.warning("Select at least one attribute in the Channel Box")
        return
    
    # Loop on nodes selected
    for node in nodes:
        for attr in sel_attrs:
            full_attr = f"{node}.{attr}"
            if cmds.objExists(full_attr):
                try:
                    # Delete this attribute
                    cmds.setAttr(full_attr, lock=True, keyable=False, channelBox=False)
                except Exception as e:
                    cmds.warning(f"Could not delete {full_attr}: {e}")                    
#-------------------------------------------------------------------# 
                                
# Function to create/connect attributes for control selected
def create_attrs(*_):
    # Be sure to have something selected at first step
    if not sel_ctrl[0]:
        cmds.warning("Please first select a control")
        return
    else:
        ctrl = sel_ctrl[0]
        
    # Create groups for attributes
    create_grps = set()
       
    # Loop for controlling and connecting each attribute from the list
    for row in attr_rows:
        # Local Variables
        # Be sure the name not giving error ["Name_1" and "Name 1" are all correct]
        attr_name = cmds.textField(row["attrs_field"], q=True, text=True).strip().replace(" ", "_")
        target_node = cmds.textField(row["target_field"], q=True, text=True)
        # Dropdown Menus
        dropdown_menu = cmds.optionMenu(row["attr_menu"], q=True, value=True)
        type_menu = cmds.optionMenu(row["type_menu"], q=True, value=True)
        # Groups
        checker_group = cmds.checkBox(row["checker_box"], q=True, value=True)
        group_name = cmds.textField(row["group_field"], q=True, text=True).strip().replace(" ", "_")
        
        # Be sure all attribute parameters are filled
        if not attr_name or not target_node or dropdown_menu in ["Choose Node", "Node doesn't exist"]:
            cmds.warning(f"Missing info for row with attr '{attr_name}'")
            continue
        
        # Be sure which groups exists
        if checker_group and group_name and group_name not in create_grps:
            group_attr = f"{ctrl}.{group_name}"
            if not cmds.attributeQuery(f"{group_name}", node=ctrl, exists=True):
                cmds.addAttr(ctrl, ln=f"{group_name}", at="enum", en="value", k=False)
                cmds.setAttr(f"{ctrl}.{group_name}", cb=True)
            else:
                cmds.warning(f"Attribute {group_name} already exists.")

        
        # Be sure the attribute exists on the control
        new_attr = f"{ctrl}.{attr_name}"
        full_dropdown = f"{target_node}.{dropdown_menu}" 
        
        # Create attribute
        if not cmds.objExists(new_attr):
            try:
                cmds.addAttr(ctrl, ln=attr_name, at=type_menu, k=True)
            except Exception as e:
                cmds.warning(f"Cannot create the {attr_name} in {ctrl}: {e}")

        # Connect attribute        
        if cmds.objExists(full_dropdown):
            try:
                cmds.connectAttr(new_attr, full_dropdown, force=True)
            except Exception as e:
                cmds.warning(f"Cannot connect the {new_attr} to {full_dropdown}: {e}")
        else:
            cmds.warning(f"{full_dropdown} do not exist")
        
#----------------------------/INTERFACE\----------------------------#
def create_separator(height,style):
    # Separator
    cmds.separator(h=height, style=style) 

def create_UI():
    # Variables
    attr_rows = []
    
    # Be sure to open a new window if the UI is open already
    if cmds.window("ui", exists=True):
        cmds.deleteUI("ui")
    
    # Create UI
    cmds.window("ui", title="Attribute Creator [by Fernando Casado]", widthHeight=(900, max_width), sizeable=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)
    
    create_separator(10, "none")
    
    # First step - Select a node to add attributes to it
    cmds.text("sel_node", label="--- SELECT NODE ---", align="center")
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=(1, 2), columnAlign=(1, "center"))
    cmds.button(label="🎯 Select", command=lambda *_: sel_control(), align="center")
    cmds.text("ctrl_label", label="Add attributes to: select a outliner's node", align="center")
    cmds.setParent("..")
    
    create_separator(10, "in")
        
    # Second step - Add attributes to the list
    cmds.text("add_attrs", label="--- ADD ATTRIBUTES ---", align="center")
    cmds.button(label="New Attribute", command=lambda *_: add_attrs())
    
    cmds.scrollLayout("attr_scroll", childResizable=True)
    cmds.columnLayout("attrs_list", adjustableColumn=True)
    cmds.setParent("..")
    cmds.setParent("..")  
    
    # Third Step - Create/Connect the attributes from the list
    cmds.button(label="Create Attributes", bgc=(0.4, 0.8, 0.4), command=create_attrs)

    create_separator(10, "in")  
  
    # Delete attributes button
    cmds.text("delete_node", label="--- SELECT ATTRIBUTES ON CHANNEL BOX ---", align="center")
    cmds.button(label="Delete Attribute", bgc=(0.8, 0.4, 0.4), command=delete_attrs)
    
    # Hide attributes button
    cmds.text("hide_node", label="--- SELECT ATTRIBUTES ON CHANNEL BOX ---", align="center")
    cmds.button(label="Hide Attribute", bgc=(0.4, 0.4, 0.8), command=hide_attrs)
    
    # Show tool interface
    cmds.showWindow("ui")
    
#------------------------------/OPEN INTERFACE\------------------------------#
create_UI()