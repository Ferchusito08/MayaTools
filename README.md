# MayaTools

## Description
A collection of scripts and tools designed to enhance and automate workflows in Maya. This toolkit aims to improve productivity and streamline common tasks.

## Features
- Automation of repetitive tasks  
- Utilities for modelling, animation, rigging, etc 
- Easy integration into your existing pipeline  

## Requirements
- Autodesk Maya 2018+ 
- Python 3.x (integrated in the software) 

## Installation
INSTALLATION INSTRUCTIONS - FCL_MayaTools (Protected)

Copy the folder "FCL_MayaTools" to a location on your PC (for example, C:/Users/YourUser/Documents/maya/scripts/)
Open Maya and run the following in the Script Editor (Python Mode):

    import sys
    sys.path.append("C:/Users/YourUser/Documents/maya/scripts/FCL_MayaTools") // This path should be the same as the path you copy the folder
    import install
    install.create_menu()
    install.setup_user_script()
    It will be automatically added to userSetup.py and will load every time.

Don’t forget to share these tools if you liked them and give me your feedback.
Thanks :D

## License

This project is under a custom license that allows free use for personal and commercial purposes, but **does not permit modification, redistribution, or creation of derivative works** without explicit permission from the author.

For more details, please see the [LICENSE](LICENSE.md) file.

If you wish to request permission to modify or redistribute the code, please contact:

Fernando Casado López  
fernando.profesional.3d@gmail.com
