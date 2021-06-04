"""
Add this script in the krita resource folder, You will need to create a json file following the template.

Made by LunarKreatures(LainFenrir)
Feel free use or modify as you want
"""
import json
import os
import sys
import xml.etree.ElementTree as ET
import re
from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo
from send2trash import send2trash

# This script changes both file name and name in the preset tag, creating a new copy of the preset, for multiple presets in a json file.

# <command> <option> <file_path>

#Change to True if you want to delete the old preset
toDeleteOldPreset:bool = False
# Global variables to avoid remaking paths 
presetTagFileName:str = "kis_paintoppresets_tags.xml"
presetsFolderPath = ""
tagsFilePath = ""
allOptions:list = ["-f","-p"]

def main(argv):
    adjustedArgs:list = adjustArgs(argv)

    #builds the paths and put them in global variabels so the path doesnt need to be built at every call
    buildPaths()   

    # transforming argv to variables for easy acess
    option:str = adjustedArgs[0]
    jsonFile:str = adjustedArgs[1]

    rename(option,jsonFile)
    print("Finished!")
    print("Argument List:", str(argv))

##############################
###### Main Functions  #######
##############################


"""
Renames .kpp file
"""
def rename(option:str,jsonFile):
    jsonData = loadJson(jsonFile)
    presetsList = jsonData["presetsToChange"]
   
    # -f find and replace 
    if option == "-f":
        print("Not Done Yet!")
        return

    # -p set prefix
    if option == "-p":
        prefix:str = jsonData["prefix"]
        for preset in presetsList:
            currentFileName:str = preset["presetName"]
            prefixedName:str = prefixName(prefix,currentFileName)
            newFileName:str = createNewPreset(prefixedName,currentFileName)
            updateTagFile(currentFileName,newFileName)
            deleteOldPreset(currentFileName)
        return

    # null replace name with another
    for preset in presetsList:
        currentFileName = preset["presetName"]
        newPresetName:str = preset["newPresetName"]

        newFileName = createNewPreset(newPresetName,currentFileName)
        
        # Skiping file if file name already exists
        if not newFileName:
            continue

        updateTagFile(currentFileName,newFileName)
        deleteOldPreset(currentFileName)


"""
Changes the name in the metadata and creates the new kpp file
"""
def createNewPreset(new_name:str,file_name:str):
    # Transforms to xml for easy replace of the name, fixes the problem of name of the file being different from the metadata
    presetPath: str = os.path.join(presetsFolderPath,file_name)
    inputFile = loadImage(presetPath)

    presetInfo: str = inputFile.info["preset"]
    metadataXml = ET.fromstring(presetInfo)
    metadataXml.attrib["name"] = new_name
    untrimmedString:str = ET.tostring(metadataXml, encoding='utf8',method="xml").decode('utf8')
    # Xml Declaration added by ET,so removing here
    replacedPreset:str = untrimmedString.replace("<?xml version='1.0' encoding='utf8'?>", "")

    metadata = PngInfo()
    for key in inputFile.info:
        if key == "dpi":
            # Since dpi is a tuple, had to transform to string to be able to pass it on
            metadata.add_text(key,str(inputFile.info[key])) # Dont know if this tag is necessary but just to be safe.
            continue
        if key == "preset":
            # avoiding duplicating the preset tag
            continue
        metadata.add_text(key,inputFile.info[key])
    metadata.add_text("preset", replacedPreset)

    # closing the file so its removed from memory
    inputFile.close()

    # bulding the file names beforehand
    newNamePng:str = ".".join([new_name,"png"])
    newNameKpp:str = ".".join([new_name,"kpp"])

    #Creating file paths for the files, since they will be in a different folder from the script
    newFilePathPng = os.path.join(presetsFolderPath,newNamePng)
    newFilePathKpp = os.path.join(presetsFolderPath,newNameKpp)
    #Loads the original file to become the new file
    newPreset = PngImageFile(presetPath)

    # If the file already exists just skip and log 
    if os.path.exists(newFilePathKpp):
        print("There is alreade a preset with the name %s, preset rename will be skipped. Delete existing file manually and try again."% newNameKpp)
        return ""
    # cant save directly to kpp so needs to save as png
    newPreset.save(newFilePathPng, pnginfo=metadata)
    
    # Changes the file extension from png to kpp\
    os.rename(newFilePathPng,newFilePathKpp)
    return newNameKpp

"""
Updates the tag file to replace the old preset name with the new one. Also deletes any md5 for that preset.
"""
def updateTagFile(old_name:str,new_name:str):
    tagsXml = ET.parse(tagsFilePath)
    root = tagsXml.getroot()
    replaced:str = ""
    for resource in root.iter("resource"):
        identifier = resource.attrib["identifier"]
        #In case of names with especial characters we need to escape them first
        escapedName:str = re.escape(old_name)
        if re.search(escapedName,identifier):
            replaced = re.sub(rf"\b{old_name}\b",new_name,identifier)
            resource.attrib["identifier"] = replaced
            # If the md5 doesnt match it will not show, since i cant replicate the md5 removing was the best option
            resource.attrib.pop("md5", None) #None to not raise expection in case it doesnt exist
            break
        
    if not replaced:
        print("No tags found for the old preset: %s, tags will remain unchanged."% old_name)
        return
    tagsXml.write(tagsFilePath,encoding="utf-8")

"""
Prefixes a name in front of an existing file.
"""
def prefixName(prefix:str,file_name:str):
    fileNameWithoutExtension:str = file_name.split(".")[0]
    prefixedName:str = "_".join([prefix,fileNameWithoutExtension]) 
    return prefixedName


##############################
###### Auxiliar Functions ####
##############################

"""
Sends the original preset file to the trashcan
"""
def deleteOldPreset(old_file_name:str):
    pathToDelete:str = os.path.join(presetsFolderPath,old_file_name)
    print(pathToDelete)
    if toDeleteOldPreset:
        if not os.path.exists(pathToDelete):
            print("Preset [%s] not found."% old_file_name)
            return
        send2trash(pathToDelete)
    print("File %s has been sent to the trash can."% old_file_name)

"""
Builds the path to the resources
"""
def loadJson(json_file):
    if not os.path.exists(json_file):
        print("Json file not found in the path, check the path: %s", json_file)
        sys.exit()
    with open(json_file) as j:
        jsonLoaded = json.load(j)
    return jsonLoaded

"""
Loads the image
"""
def loadImage(file_name:str):
    # check if the file name is valid, if not program aborts
    if not os.path.exists(file_name):
        print("Preset file doesnt exist, aborting the program. Check the file name : %s" % file_name)
        sys.exit()
        
    input_file = Image.open(file_name)
    # Necessary to load to get the metadata, close the file later
    input_file.load()
    return input_file

"""
Loads the image
"""
def buildPaths():
    global tagsFilePath
    global presetsFolderPath
    #Assumes its in the krita resource folder
    kritaResourceDirectory= os.getcwd()

    #temporary variables to not mess with the globals
    tagsPath:str = os.path.join(kritaResourceDirectory,"tags",presetTagFileName)
    # tagsPathToFile:str = os.path.join(tagsPath,presetTagFileName)
    
    presetPath: str = os.path.join(kritaResourceDirectory,"paintoppresets")
    # without paintoppreset folder its impossible to continue. a batch operation without updating the tags is also dangerous.
    if os.path.exists(presetPath) and os.path.exists(tagsPath):
        presetsFolderPath = presetPath
        tagsFilePath = tagsPath
        return

    print("paintoppresets folder not found. The script needs to be inside the krita folder check the script location, the program will abort. current location of script %s."% kritaResourceDirectory)
    sys.exit()

"""
when option is null it will add a dummy value to not mess up the parameters order
"""
def adjustArgs(args) -> list:
    adjustedArgs:list = []
    adjustedArgs.extend(args)
    if args[0] not in allOptions:
        adjustedArgs.clear()
        adjustedArgs.insert(0,"")
        adjustedArgs.extend(args)
    return adjustedArgs


##############################
########## Main ##############
##############################

if __name__ == "__main__":
   main(sys.argv[1:]) #Slice args cause 0 = script_file_name