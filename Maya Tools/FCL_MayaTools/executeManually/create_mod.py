import os

def crear_mod_fcl_mayatools():
    user_scripts_path = os.path.join(os.path.expanduser("~"), "Documents", "maya", "scripts")
    fcl_mayatools_path = os.path.join(user_scripts_path, "FCL_MayaTools")
    
    user_modules_path = os.path.join(os.path.expanduser("~"), "Documents", "maya", "modules")
    if not os.path.exists(user_modules_path):
        os.makedirs(user_modules_path)
    
    mod_file_path = os.path.join(user_modules_path, "FCL_MayaTools.mod")
    
    contenido = f"+ FCL_MayaTools 1.0 {fcl_mayatools_path.replace(os.sep, '/')}\n"
    
    with open(mod_file_path, "w") as f:
        f.write(contenido)
    
    print(f"Archivo mod creado en: {mod_file_path}")
    print("Contenido:")
    print(contenido)

if __name__ == "__main__":
    crear_mod_fcl_mayatools()
