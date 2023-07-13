REM @echo off
CD ..
SET APP_DIR=%CD%
SET DJANGO_SETTINGS_MODULE = config.settings
CD ..
set PROJECT_DIR=%CD%
%PROJECT_DIR%\.env\Scripts\python %APP_DIR%\manage.py runserver 0.0.0.0:8000

cmd /k

