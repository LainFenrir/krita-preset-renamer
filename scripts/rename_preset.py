"""
Add this script inside the paintoppresets folder inside the krita resource folder

This script will copy an existing preset and will change the name and update the name in the preset tags.
You can change the toDeleteOldPreset to True so it will send the old preset to the trahsbin

Made by LunarKreatures(LainFenrir)
Feel free use or modify as you want
"""
import os
import sys
import xml.etree.ElementTree as ET
import re
from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo
from send2trash import send2trash

# This script changes both file name and name in the preset tag, creating a new copy of the preset

# Command: <option> <file_path> <new_name> <find>   option is optional

#Change to True if you want to delete the old preset
toDeleteOldPreset:bool = False

presetTagFileName:str = "kis_paintoppresets_tags.xml"
allOptions:list = ["-f","-p"]

def main(argv):
    adjustedArgs:list = adjustArgs(argv)

    # transforming argv to variables for easy acess
    option:str = adjustedArgs[0]
    find:str = ""
    fileName:str = adjustedArgs[1]
    newName:str = adjustedArgs[2]
    if option == "-f":
        find= adjustedArgs[3]
    
    rename(option,fileName,newName,find)
    print("Finished!")
    print('Argument List:', str(argv))

##############################
###### Main Functions  #######
##############################

"""
Renames .kpp file
"""
def rename(option,file_name,new_name,find):
    # -find and replace
    if option == "-f":
        #todo: do this later
        print("Not Done Yet!")
        return

    # -p set prefix
    if option == "-p":
        prefixedName:str = prefixName(new_name,file_name)
        newFileName:str = createNewPreset(prefixedName,file_name)
        updateTagFile(file_name,newFileName)
        
        if toDeleteOldPreset:
            send2trash(file_name)
        return

    # no option replaces name with another
    newFileName:str = createNewPreset(new_name,file_name)

    # Skiping file if file name already exists
    if not newFileName:
        return

    updateTagFile(file_name,newFileName)

    if toDeleteOldPreset:
        send2trash(file_name)


"""
Changes the name in the metadata and creates the new kpp file
"""
def createNewPreset(new_name,file_name):
    # Transforms to xml for easy replace of the name, fixes the problem of name of the file being different from the metadata
    inputFile = LoadImage(file_name)
    presetInfo: str = inputFile.info['preset']
    metadataXml = ET.fromstring(presetInfo)
    metadataXml.attrib["name"] = new_name
    untrimmedString:str = ET.tostring(metadataXml, encoding='utf8',method="xml").decode('utf8')
    # Xml Declaration added by ET,so removing here
    replacedPreset:str = untrimmedString.replace("<?xml version='1.0' encoding='utf8'?>", "").strip()
   
    # Creating a new metadata object to replace the original
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

    # If the file already exists just skip and log 
    if os.path.exists(newNameKpp):
        print("There is alreade a preset with the name %s, preset rename will be skipped. Delete existing file manually and try again."% newNameKpp)
        return ""
    # cant save directly to kpp so needs to save as png
    newPreset.save(newNamePng, pnginfo=metadata)
    
    # Changes the file extension from png to kpp
    os.rename(newNamePng,newNameKpp)
    return newNameKpp

"""
Updates the tag file to replace the old preset name with the new one. Also deletes any md5 for that preset.
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
    for resource in root.iter('resource'):
        identifier = resource.attrib['identifier']
        #In case of names with especial characters we need to escape them first
        escapedName:str = re.escape(old_name)
        if re.search(old_name,identifier):
            replaced = re.sub(rf"\b{old_name}\b",new_name,identifier)
            resource.attrib['identifier'] = replaced
            # If the md5 doesnt match it will not show, since i cant replicate the md5 removing was the best option
            resource.attrib.pop("md5", None) #None to not raise expection in case it doesnt exist
            break
        
    if not replaced:
        print("No tags found for the old preset: %s, tags will remain unchanged."% old_name)
        return
    tagsXml.write(tagFilePath,encoding="utf-8")

"""
Prefixes a name in front of an existing file.
"""
def prefixName(prefix:str,file_name:str):
    fileNameWithoutExtension:str = file_name.split(".")[0]
    prefixedName:str = "_".join([prefix,fileNameWithoutExtension]) 
    return prefixedName

##############################
##### Auxiliar Functions #####
##############################

"""
Builds the path to the resources
"""
def buildPathToTagFile():
    # Assumes its inside paintoppresets folder
    folderAbove:str = Path(".").resolve().parent
    tagPath:str = os.path.join(folderAbove,"tags")
    tagFilePath:str = os.path.join(tagPath,presetTagFileName)

    # If the tag file doesnt exist then it will not update tags, return an empty path
    if not os.path.exists(tagPath):
        print("Tag file not found, the preset Tags will not be updated")
        tagFilePath = ""
    return tagFilePath

"""
Loads the image
"""
def LoadImage(file_name):
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