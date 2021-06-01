"""
Add this script in the krita resource folder

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


# <command> <option> <file_path>

#Change to True if you want to delete the old preset
toDeleteOldPreset:bool = False
presetTagFileName:str = "kis_paintoppresets_tags.xml"
kritaResourceDirectory = ""
presetsFolderPath = ""
tagsFolderPath = ""
allOptions:list = ["-f","-p"]

def main(argv):
    adjustedArgs:list = adjustArgs(argv)

    global kritaResourceDirectory 
    kritaResourceDirectory= os.getcwd()

    #todo review global variable
    #todo do not create the path everytime to load image and tag file
    #todo build path to get the preset inside the folder
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
    #todo
    jsonData = loadJson(jsonFile)
    presetsList = jsonData["presetsToChange"]
   
    # -f find and replace 
    if option == "-f":
        print("Not Done Yet!")
        return

    # -p set prefix
    if option == "-p":
        print("Not Done Yet!")
        return

    # null replace name with another
    for preset in presetsList:
        currentFileName = preset["presetName"]
        newPresetName = preset["newPresetName"]

        newFileName = createNewPreset(newPresetName,currentFileName)
        updateTagFile(newFileName,currentFileName)


"""
Changes the name in the metadata and creates the new kpp file
"""
def createNewPreset(new_name:str,file_name:str):
    # Transforms to xml for easy replace of the name, fixes the problem of name of the file being different from the metadata
    inputFile = LoadImage(file_name)
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

    #Loads the original file to become the new file
    newPreset = PngImageFile(file_name)
    # cant save directly to kpp so needs to save as png
    newPreset.save(newNamePng, pnginfo=metadata)
    
    # Changes the file extension from png to kpp
    os.rename(newNamePng,newNameKpp)
    return newNameKpp

"""
Builds the path to the resources
"""
def updateTagFile(old_name:str,new_name:str):
    tagFilePath:str = buildPathToTagFile()
    #If no path, just skip the method
    if not tagFilePath:
        print("Tag update will be skipped.")
        return
    tagsXml = ET.parse(tagFilePath)
    root = tagsXml.getroot()
    replaced:str = ""
    for resource in root.iter("resource"):
        identifier = resource.attrib["identifier"]
        if re.search(old_name,identifier):
            replaced = re.sub(rf"\b{old_name}\b",new_name,identifier)
            resource.attrib["identifier"] = replaced
            # If the md5 doesnt match it will not show, since i cant replicate the md5 removing was the best option
            resource.attrib.pop("md5", None) #None to not raise expection in case it doesnt exist
            break
        
    if not replaced:
        print("No tags found for the old preset: %s, tags will remain unchanged."% old_name)
        return
    tagsXml.write(tagFilePath,encoding="utf-8")

##############################
###### Auxiliar Functions ####
##############################

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
Builds the path to the resources
"""
def buildPathToTagFile():
    #Assumes its in the krita resource folder
    tagPath:str = os.path.join(kritaResourceDirectory,"tags")
    tagFilePath:str = os.path.join(tagPath,presetTagFileName)

    # If the tag file doesnt exist then it will not update tags, return an empty path
    if not os.path.exists(tagPath):
        print("Tag file not found, the preset Tags will not be updated")
        tagFilePath = ""
    return tagFilePath

"""
Loads the image
"""
def LoadImage(file_name:str):

    
    # check if the file name is valid, if not program aborts
    if not os.path.exists(file_name):
        print("Preset file doesnt exist, aborting the program. Check the file name : %s" % file_name)
        sys.exit()
        
    input_file = Image.open(file_name)
    # Necessary to load to get the metadata, close the file later
    input_file.load()
    return input_file

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