import maya.cmds as cmds
import os
import sys
import importlib.util

def import_tool_module(tool_folder, module_base_name):
    version = f"{sys.version_info.major}{sys.version_info.minor}"

    pyc_filename = f"{module_base_name}.cpython-{version}.pyc"
    module_path = os.path.join(tool_folder, pyc_filename)

    if not os.path.exists(module_path):
        print(f"[FCL_MayaTools] File doesn't exist: {module_path}")
        return None

    spec = importlib.util.spec_from_file_location(module_base_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def create_menu():
    def _create():
        if cmds.menu("FCL_MayaTools", exists=True):
            cmds.deleteUI("FCL_MayaTools")

        main_menu = cmds.menu("FCL_MayaTools", label="FCL_MayaTools", parent="MayaWindow", tearOff=True)

        base = os.path.dirname(__file__)
        tools_base_folder = os.path.join(base, "tools")
        maya_version = cmds.about(version=True)

        for tool_name in sorted(os.listdir(tools_base_folder)):
            tool_folder = os.path.join(tools_base_folder, tool_name)
            if not os.path.isdir(tool_folder):
                continue

            module_base_name = tool_name.lower().replace(" ", "_")

            def make_command(folder=tool_folder, module_name=module_base_name, tool_display_name=tool_name):
                def run_tool(*args):
                    mod = import_tool_module(folder, module_name)
                    if mod and hasattr(mod, "run"):
                        mod.run()
                    else:
                        print(f"[FCL_MayaTools] Failed to create '{module_name}' for Maya {maya_version}.")

                return run_tool

            cmds.menuItem(label=tool_name, parent=main_menu, command=make_command())

        print("[FCL_MayaTools] Menu Ready to Use.")

    cmds.evalDeferred(_create)
