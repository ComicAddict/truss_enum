@echo off

:: Loop through a set of numbers
for /L %%i in (1,1,13) do (
    start /B python ../py_impl/cube.py %%i 
)