@echo off

echo SET FLASK APP
set FLASK_APP=app.modules.main.main_tests

echo.
echo DOWNGRADE DATABASE
flask db downgrade

echo.
echo UPGRADE DATABASE
flask db upgrade

echo.
echo SEED DATABASE
flask seed

echo.
echo RUN APPLICATION
python -m app.modules.main.main_tests

pause