from maya import cmds

def delayed_setup():
    import install
    install.create_menu()

cmds.evalDeferred(delayed_setup)
