
from maya import cmds
import importlib.util
import os

def load_pyc(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def create_menu():
    if cmds.menu("FCL_Tools", exists=True):
        cmds.deleteUI("FCL_Tools")
    main_menu = cmds.menu("FCL_Tools", label="FCL_Tools", parent="MayaWindow", tearOff=True)

    base = os.path.dirname(__file__)
    cmds.menuItem(label="Attribute Creator", parent=main_menu,
        command=lambda *_: load_pyc(os.path.join(base, "tools", "attribute_creator.pyc"), "selector").run())

    print("'FCL_Tools' menu ready.")

def setup_user_script():
    scripts_path = cmds.internalVar(userScriptDir=True)
    user_setup_path = os.path.join(scripts_path, "userSetup.py")
    custom_code = (
        "\n# ==== Fernando Casado López Maya Tools ===="
        "import sys\n"
        "sys.path.append(r'{0}')\n"
        "import install\n"
        "install.create_menu()\n"
        "# ==== End ====\n"
    ).format(os.path.abspath(os.path.dirname(__file__)))
    if os.path.exists(user_setup_path):
        with open(user_setup_path, "r") as f:
            contents = f.read()
        if "install.create_menu()" in contents:
            print("userSetup.py already contains this menu")
            return
        else:
            with open(user_setup_path, "a") as f:
                f.write(custom_code)
            print("Info added to userSetup.py.")
    else:
        with open(user_setup_path, "w") as f:
            f.write(custom_code)
        print("userSetup.py created successfully")
