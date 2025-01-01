@echo off

:: Loop through a set of numbers
for /L %%i in (1,1,12) do (
    python ../py_impl/rhombic_dodecahedra.py %%i
)