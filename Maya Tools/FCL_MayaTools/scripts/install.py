import maya.cmds as cmds
import os

def import_tool(module_path, module_name):
    import importlib.util
    import os

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def create_menu():
    def _create():
        if cmds.menu("FCL_MayaTools", exists=True):
            cmds.deleteUI("FCL_MayaTools")

        main_menu = cmds.menu("FCL_MayaTools", label="FCL_MayaTools", parent="MayaWindow", tearOff=True)

        base = os.path.dirname(__file__)
        def run_attribute_creator(*args):
            mod = import_tool(os.path.join(base, "tools", "attribute_creator.pyc"), "attribute_creator")
            # Supongamos que el módulo tiene una función 'run' que abre UI o hace algo visible
            if hasattr(mod, "run"):
                mod.run()
            else:
                print("[FCL_MayaTools] attribute_creator module has no 'run' function.")

        cmds.menuItem(label="Attribute Creator", parent=main_menu, command=run_attribute_creator)

        print("[FCL_MayaTools] Menu loaded.")

    cmds.evalDeferred(_create)
