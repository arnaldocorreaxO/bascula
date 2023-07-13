REM @echo off

SET PROJECT_DIR=C:\Users\bascula\bascula
SET APP_DIR=%PROJECT_DIR%\app
SET DJANGO_SETTINGS_MODULE=config.settings_vpn


rem RUNAS /savecred /user:bascula "%PROJECT_DIR%\.env\Scripts\python %APP_DIR%\manage.py runserver 0.0.0.0:8000"
START CMD.EXE /C "%PROJECT_DIR%\.env\Scripts\python %APP_DIR%\manage.py runserver 0.0.0.0:8000"

start C:\"Program Files"\Google\Chrome\Application\chrome.exe "http://localhost:8000/"

cmd /k

