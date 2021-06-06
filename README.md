# krita-preset-renamer
a collection of python scripts to rename krita brush presets, allowing batch rename.

Krita organizes presets by alphabetical order, and the name it takes into account for that is the name set in the metadata of the `.kpp` file.
This pack of scripts is made to be a set of utilities to rename presets.

## How to install and use

First you need to have python installed on your pc, you can download it from the [python website](https://www.python.org). If you are on Windows make sure to install python with the `add to PATH` checked.
After you installed python, you need to install these python libraries. just copy and paste the commands in a terminal. 
```
python -m pip install -U send2trash
python -m pip install --upgrade Pillow

```
You can read more about them in the links below:
[send2trash](https://github.com/arsenetar/send2trash)
[Pillow](https://pillow.readthedocs.io/en/stable/index.html)

After those steps, just download the source code zip or clone this repository.

### Scripts
Each script works a bit differently, and needs to be set up differently.

#### view_metadata
This script is only to see the metadata inside a `.kpp` file. For now, it only looks for files in the current directory it is in. So you will need to add it inside the painttoppreset folder if you want to use it.
```
Command: <-option> <file_name> 
``` 
`-option` is an optional parameter.
`file_name` needs to have the full name with the `.kpp` at the end
The valid values for `-option` are:
- `nothing`: will list only the preset tag inside the metadata
- `-f`: (full) will print all the metadata inside the file 
- `-i`: (info) will print the preset name, texture name and path if exists and brush definitions

Examples of usage:
```shell
python view_metadata.py LainKit_Wet_flat_size.kpp
python view_metadata.py -f LainKit_Wet_flat_size.kpp
python view_metadata.py -i LainKit_Wet_flat_size.kpp
```
#### rename_preset
It renames a file, given a new name and updates the new name in the `kis_paintoppresets_tags.xml` the file responsible for the tags for the presets. In case the preset doesnt have any tags that file will not be touched.
By default it will behave like krita and just create a new file with the new name, keeping the old file alone. Though unlike krita, the old file will not be blacklisted so you will see the 2 files inisde krita. If you want to avoid this behaviour you can set the variable `toDeleteOldPreset` to `True` inside the script.
It only works for one file at a time.

```
Command: <-option> <file_name> <new_name> <find>
``` 
`file_name` needs to have the full name with the `.kpp` at the end
`new_name` needs to be just the name of the brush, without `.kpp` at the end (the script will take care of adding it in the end)
`find` is only necessay when using the `-f` option
`-option` is an optional parameter.

The valid values for `-option` are:
- `nothing`: will replace the full name for a new one 
- `-f`: (find and replace) will replace just the name part passed in the `find` with the contents of `new_name`. (not done yet)
- `-p`: (set prefix) a common usecase is to want to set a prefix to a name, this will keep the original name adding what was passed in `new_name` in the begining of the old name.(separated by `_`) 

Examples of usage:
```shell
python rename_preset.py LainKit_Wet_flat_size.kpp LunarKit_Round_Flat_Size
python rename_preset.py -p LainKit_Wet_flat_size.kpp i)
python rename_preset.py -f LainKit_Wet_flat_size.kpp Round_Flat flat
```

#### batch_rename
```
Command: <-option> <json_file_path>
``` 
`json_file_path` a path to the json file it needs to follow the templade of the `batch_rename_template.json`
`-option` is an optional parameter.

The valid values for `-option` are:
- `nothing`: will replace the full name for a new one 
- `-f`: (find and replace) will replace just the name part passed in the `find` with the contents of `new_name`. (not done yet)
- `-p`: (set prefix) a common usecase is to want to set a prefix to a name, this will keep the original name adding what was passed in `new_name` in the begining of the old name.(separated by `_`) 

Json structure:
```json
{
    "presetsToChange":[
            {
            "presetName":"",
            "newPresetName":""
            }
        ],
        "prefix": ""
}
```
Not all fields are necessay for all the operations. Passing all the fields will not cause errors, they will just be ignored.
- default operation json:
  ```json
  {
    "presetsToChange":[
            {
            "presetName":"",
            "newPresetName":""
            },
            {
            "presetName":"",
            "newPresetName":""
            }
        ]
  }
  ```
- Set prefix json:
  
  ```json
  {
    "presetsToChange":[
            {
            "presetName":""
            }
        ],
    "prefix": ""
  }
  ```

## General Questions

### Why not use krita for this?
Krita by itself will create a backup file whenever you change the name poluting your resource folder and also krita doesnt have a batch rename. The rename scripts will create a new file copying your old one updating the name in both the file name and the metadata, with the option to delete the old file after creating a new one with the new name.

### So it will still create a copy, why not changing the file directly?
I tried, couldn't find a way to do that in python, as I am not very used to this language so had to work around.

### Why not make it a plugin?
Maybe someday, I have to study krita api to see if doing all this is even possible with it.

### Can this script damage my pc?
Not really, all it does is read image metadata, create images and write on the krita preset tags xml file.

### Can it break krita?
I don't think so, from my tests I didn't encounter any problem. If you want you can backup the `kis_paintoppresets_tags.xml` and the paintoppreset folder.

### Does it work for any krita version?
I tested with krita 4.4.3, anything 4.x version should work. I havent tested with 5.

### Does it delete my presets?
If you leave the variable `toDeleteOldPreset` as false no, if you set to true it actually moves your preset to your trashcan and you can recover it from there. 

### When I run the script and open krita again, I see the old preset name and the new one, why?
Well, its cause the scripts doesn't blacklist the old preset. The way krita gives you the impression the preset has been renamed, is by blacklisting the old preset name, in fact krita works like these scripts, it will create a new file with the metadata and a new name. If you dont want to keep the old preset just edit the script variable `toDeleteOldPreset` to `True`. 

### Couldn't you make it blacklist?
That was my personal choice. I dislike krita's approach of hiding the old brush cause this way you actually have no idea how much "trash" you have in the presets. So I prefered to leave it there showing so I can delete later or just send the old file to the trash.

