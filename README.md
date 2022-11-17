[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/)
[![Maya 2023](https://img.shields.io/badge/maya-2023-blue.svg)](https://www.autodesk.com/products/maya/)

# Maya Turntable

This is a Maya Turntable Tool using Qt and Python.

## Contents

This repositoy consists of a `Maya Script File` (`.mel`) and a `Python Source File` (`.py`):

- the `shelf_Turntable.mel` is the Turntable Tool plus its own custom Shelf and shelf button.
- the `create_turntable.py` is just a Python script of the Turntable Tool, without the Shelf and button that is included in the `Maya Script File`.

## Installation

For `shelf_Turntable.mel` to work it must be located in Maya's `MAYA_SHELF_PATH` shelf directory. While `create_turntable.py` may be moved to Maya's `MAYA_SCRIPT_PATH` script directory. Listed below are Maya's default paths:

### Linux
- `shelf_Turntable.mel`
```
    ~<username>/maya/<version>/prefs/shelves/
```

- `create_turntable.py`
```
    ~<username>/maya/<version>/scripts/
```

### Windows
- `shelf_Turntable.mel`
```
    \Users\<username>\Documents\Maya\<version>\prefs\shelves\
```

- `create_turntable.py`
```
    \Users\<username>\Documents\Maya\<version>\scripts\
```

### Mac OS X
- `shelf_Turntable.mel`
```
    ~<username>/Library/Preferences/Autodesk/Maya/<version>/prefs/shelves/
```

- `create_turntable.py`
```
    ~<username>/Library/Preferences/Autodesk/Maya/<version>/scripts/
```

## Notes

The `create_turntable.py` file isn't necessary. I included it for posterity's sake.
