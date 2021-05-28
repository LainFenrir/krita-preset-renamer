"""

Made by LunarKreatures(LainFenrir)
Feel free use or modify as you want
"""
from os import path
import sys
from PIL import Image

#python rename_krita_brush.py LainKit_Wet_flat_size.kpp 

#kpp tag preset <Preset paintopid="colorsmudge" name="LainKit_Wet_flat_size"> 
# change both file name and name in the preset tag

# <command> <option> <file_path> <optional_param> <optional_param2>   option is optional

commands = ["help"]
options = ["-f","-r","-p"]

def main(argv):
    #Todo: help
    #Todo: rename
    #Todo: view Exif

    
    
    decide_command(argv)



    # input_file = load_image(argv[1])
    # input_file = Image.open(argv[0])
    # input_file.load()

    # for key in inputFile.info:
    #     print("%s: %s" % (key,inputFile.info[key]))
    

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

"""
Batch proceess for many .kpp file
"""
def batch_process(args):
    #todo

    # -r rename

    # -p set prefix

    # -f find and replace 

    # null replace name with another
    pass


"""
Shows help
"""
def call_help():
    #todo
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



##############################
########## Main ##############
##############################

if __name__ == "__main__":
   main(sys.argv[1:]) #Slice args cause 0 = script_file_name