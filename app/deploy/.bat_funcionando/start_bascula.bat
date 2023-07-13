REM @echo off


SET PROJECT_DIR=C:\Users\bascula\bascula
SET APP_DIR=%PROJECT_DIR%\app

SET DJANGO_SETTINGS_MODULE=config.settings

RUNAS /savecred /user:bascula "%PROJECT_DIR%\.env\Scripts\python %APP_DIR%\manage.py runserver 0.0.0.0:8000"

start C:\"Program Files"\Google\Chrome\Application\chrome.exe "http://127.0.0.1:8000/"
cmd /k

