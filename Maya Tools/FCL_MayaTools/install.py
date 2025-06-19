from maya import cmds
import importlib.util
import os

def import_tool(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def create_menu():
    if cmds.menu("FCL_Tools", exists=True):
        cmds.deleteUI("FCL_Tools")

    main_menu = cmds.menu("FCL_Tools", label="FCL_Tools", parent="MayaWindow", tearOff=True)

    base = os.path.dirname(__file__)
    cmds.menuItem(label="Attribute Creator", parent=main_menu,
        command=lambda *_: import_tool(os.path.join(base, "tools", "attribute_creator.pyc"), "attribute_creator"))

    print("[FCL_Tools] Menu loaded.")

def setup_user_script():
    scripts_path = cmds.internalVar(userScriptDir=True)
    user_setup_path = os.path.join(scripts_path, "userSetup.py")
    install_path = os.path.abspath(os.path.dirname(__file__))

    marker = "# ==== Fernando Casado Lopez Maya Tools ===="
    code_block = (
        f"\n{marker}\n"
        "try:\n"
        f"    import sys\n"
        f"    sys.path.append(r'{install_path}')\n"
        f"    import install\n"
        f"    install.create_menu()\n"
        "except Exception as e:\n"
        "    import traceback\n"
        "    traceback.print_exc()\n"
        "# ==== End ====\n"
    )

    if os.path.exists(user_setup_path):
        with open(user_setup_path, "r") as f:
            contents = f.read()
        if marker in contents:
            print("userSetup.py ya contiene el codigo necesario.")
            return
        with open(user_setup_path, "a") as f:
            f.write(code_block)
        print("Codigo anadido a userSetup.py")
    else:
        with open(user_setup_path, "w") as f:
            f.write(code_block)
        print("userSetup.py creado y configurado correctamente.")
