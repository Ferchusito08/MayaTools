README – FCL Maya Tools Installation

## What is this?

This is a custom toolset for Autodesk Maya, called FCL Maya Tools
It adds a dropdown menu to Maya's top bar, giving you quick access to custom scripts

## Requirements

- Python installed (recommended version 3.x)
- Python added to the system's PATH so it can be called from the command line
- The folder FCL_Tools must be located here: "C:\Users\<your_username>\Documents\maya\scripts\FCL_MayaTools"

## One-time Installation

To properly install and configure the tool, you must run a script that sets it up inside Maya.

Steps:
1.- Open the folder where the tool was downloaded
2.- Double-click the .bat file to launch the installation (Path: C:\Users\ferju\Documents\maya\scripts\FCL_MayaTools\executeManually\create_module.bat)
3.- A terminal window will open and display progress messages
4.- When you see the message Mod file created at: ..., you’re done.

## What does this script do?

It automatically creates a .mod file inside Maya’s modules folder
That file tells Maya where to find the tool each time it starts

## Using the Tool
Launch Maya and a new menu called FCL_Tools should appear at the top of the interface