@echo off

REM Obtiene la carpeta Documents del usuario actual
set USER_DOCS=%USERPROFILE%\Documents

REM Ruta al script Python relativo a Documents
set SCRIPT_PATH=%USER_DOCS%\maya\scripts\FCL_MayaTools\executeManually\create_mod.py

REM Ejecuta el script con python
python "%SCRIPT_PATH%"

pause
