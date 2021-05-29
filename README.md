# krita-preset-renamer
a collection of python scripts to rename krita brush presets, allowing batch rename.

Krita organizes presets by alphabetical order, and the name it takes into account for that is the name set in the metadata of the `.kpp` file.
This script is made to rename the name in the metadata and the the file itself.

## How to install and use

```
python -m pip install -U send2trash
python3 -m pip install --upgrade Pillow
```
https://github.com/arsenetar/send2trash
https://pillow.readthedocs.io/en/stable/index.html
### Commands

## General information

### Why not use krita itself?
Krita by will create a backupfile whenever you change the name poluting your resource folder and also krita doesnt have a batch rename. This script will rename the file itself, no backups created and can also deal with multiple files.
