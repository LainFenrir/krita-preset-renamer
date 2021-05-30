"""

Made by LunarKreatures(LainFenrir)
Feel free use or modify as you want
"""
from os import path
import sys
import json
from PIL import Image

#python rename_krita_brush.py LainKit_Wet_flat_size.kpp 

#kpp tag preset <Preset paintopid="colorsmudge" name="LainKit_Wet_flat_size"> 
# change both file name and name in the preset tag

# <command> <option> <file_path>


options = ["-f","-r","-p","-d"]

def main(argv):

    

    print('Argument List:', str(argv))

##############################
###### Main Functions  #######
##############################


"""
Renames .kpp file
"""
def rename(args):
    #todo

    # -f find and replace 

    # -p set prefix

    # null replace name with another
    pass

##############################
###### Auxiliar Functions ####
##############################



"""
Builds operation instructions
"""
def build_operation(args):
    operation:dict = {}
    operation.command = args[0]
    
    if args[1] in options:
        operation.option = args[1]
        operation.json_file = args[2]
    else:
        operation.option = ""
        operation.json_file = args[1]
    


"""
Checks if its a valid path 
"""
def checks_path(file_name):
    if path.exists(file_name):
        return
    
    print("file doesnt exist. File name : %s" % file_name)
    sys.exit()
    
"""
Loads the image
"""
def load_image(file_name):
    input_file = Image.open(file_name)
    input_file.load()
    return input_file

"""
Changes the name in the metadata
"""
def format_metadata_name(current_name,new_name):
    #todo
    pass

"""
Loads the configuration file
"""
def loadConfig():
    global config 

    if os.path.exists(configFileName):
        with open(configFileName, "r") as jsonFile:
            config = json.load(jsonFile)
        return

    folderAbove:str = Path(".").resolve().parent
    configPathInFolderAbove:str= os.path.join(folderAbove,configFileName)
    
    if os.path.exists(configPathInFolderAbove):
         with open(configPathInFolderAbove, "r") as jsonFile:
            config = json.load(jsonFile)
         return

    print("Config file doesnt exist.Program will not run until %s file is in either %s or %s",configFileName,os.getcwd(),folderAbove)
    #todo create default config file in cwd
    sys.exit()
    

##############################
########## Main ##############
##############################

if __name__ == "__main__":
   main(sys.argv[1:]) #Slice args cause 0 = script_file_name