"""
Add this script inside the paintoppresets folder inside the krita resource folder

Made by LunarKreatures(LainFenrir)
Feel free use or modify as you want
"""
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo
from send2trash import send2trash

#kpp tag preset <Preset paintopid="colorsmudge" name="LainKit_Wet_flat_size"> 
# change both file name and name in the preset tag

# Command: <option> <file_path> <new_name> <find>   option is optional

#Change to True if you want to delete the old preset
toDeleteOldPreset = False

presetTagFileName = "kis_paintoppresets_tags.xml"
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
    #todo: add message for errors
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
       #todo:
        print("Not Done Yet!")
        return


    # no option replaces name with another
    createNewPreset(new_name,file_name)

    if toDeleteOldPreset:
        send2trash(file_name)



"""
Changes the name in the metadata and creates the new kpp file
"""
def createNewPreset(new_name,file_name):
    # Transforms to xml for easy replace of the name, fixes the problem of name of the file being different from the metadata
    presetInfo,inputFile = grabPresetFromMetadata(file_name)
    metadataXml = ET.fromstring(presetInfo)
    metadataXml.attrib["name"] = new_name
    untrimmedString:str = ET.tostring(metadataXml, encoding='utf8',method="xml").decode('utf8')
    # Xml Declaration added by ET,so removing here
    replacedPreset:str = untrimmedString.replace("<?xml version='1.0' encoding='utf8'?>", "").strip()
   
    metadata = PngInfo()
    for key in inputFile.info:
        if key == "dpi":
            metadata.add_text(key,str(inputFile.info[key]))
            continue
        if key == "preset":
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


##############################
###### Auxiliar Functions ####
##############################

"""
Builds the path to the resources
"""
def buildPathToTagFile():
    # Assumes its inside paintoppresets folder
    folderAbove:str = Path(".").resolve().parent
    tagPath = os.path.join(folderAbove,"tags")
    return tagPath
    pass

"""
Builds operation instructions
"""
def grabPresetFromMetadata(file_name):
    #todo: is necessary to be a function?
    inputFile = LoadImage(file_name)
    return inputFile.info['preset'],inputFile

"""
Checks if its a valid path 
"""
def checksPathExists(file_name):
    if os.path.exists(file_name):
        return
    
    print("file doesnt exist. File name : %s" % file_name)
    sys.exit()
    
"""
Loads the image
"""
def LoadImage(file_name):
    checksPathExists(file_name)
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