Nanovea ST-400 Surface Roughness Calculator
===================

*(to be completed)*

----

Command to create the shiv zipapp (sub whatever python version):

```
python3.7 -m shiv -c nanovea-roughness -o dist/nanovea_roughness_3.7.shiv .
```

Selector within the batch runner:

```
python -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 6) else 1)"
IF %ERRORLEVEL% EQU 0 (call python nanovea_roughness_3.6.shiv)
```