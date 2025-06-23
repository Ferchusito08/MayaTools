import maya.cmds as cmds
import os
import sys
import importlib.util

def find_pyc_module(tool_folder):
    version = f"{sys.version_info.major}{sys.version_info.minor}"

    for filename in os.listdir(tool_folder):
        if filename.endswith(f".cpython-{version}.pyc"):
            module_name = os.path.splitext(filename)[0]
            full_path = os.path.join(tool_folder, filename)
            return module_name, full_path

    print(f"[FCL_MayaTools] No .pyc file found in: {tool_folder}")
    return None, None

def import_tool_module(tool_folder):
    module_name, module_path = find_pyc_module(tool_folder)
    if not module_path:
        return None

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
        tools_base_folder = os.path.join(base, "tools")
        maya_version = cmds.about(version=True)

        for tool_name in sorted(os.listdir(tools_base_folder)):
            tool_folder = os.path.join(tools_base_folder, tool_name)
            if not os.path.isdir(tool_folder):
                continue

            def make_command(folder=tool_folder):
                def run_tool(*args):
                    mod = import_tool_module(folder)
                    if not mod:
                        print(f"[FCL_MayaTools] Failed to load tool in '{folder}' for Maya {maya_version}.")
                return run_tool

            cmds.menuItem(label=tool_name, parent=main_menu, command=make_command())

        print("[FCL_MayaTools] Menu Ready to Use.")

    cmds.evalDeferred(_create)
