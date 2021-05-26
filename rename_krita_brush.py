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

# <command> <option> <file_path> <new_name>  ==== option is optional

commands = ["view","rename","help","v","r"]
options = ["-f"]

def main(argv):
    #Todo: help
    #Todo: rename
    #Todo: view Exif

    if argv[0] not in commands:
        print("Command not found. Valid Commands : %s" % str(commands))
        sys.exit()
    
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
Prints Exif information from kpp file
"""
def view(args):
    # -f full exif
    if args[0] == "-f":
        input_file = load_image(args[1])
        for key in input_file.info:
            print("%s: %s" % (key,input_file.info[key]))
        input_file.close()
        sys.exit()

    input_file = load_image(args[0])
    print(input_file.info['preset'])
    input_file.close()


"""
Renames .kpp file
"""
def rename(args):
    #todo

    # -b batch process

    # -p set prefix
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
Checks the args 
"""
def checks_valid_args(args,valid_number):
    if len(args) not in valid_number:
        print("argument lenght not expected. ")
        # sys.exit()

"""
Checks the args 
"""
def get_file_name(args):
    #DELETE
    if args[1] in options:
        return args[2]
    return args[1]

    
"""
Checks if its a valid path 
"""
def checks_path(file_name):
    if path.exists(file_name):
        # print("file exists")
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
Decides which command to call
"""
def decide_command(args):
    if args[0] == "view" or args[0] == "v":
        view(args[1:])

    if args[0] == "rename" or args[0] == "r":
        rename(args[1:])

    if args[0] == "help":
        call_help()



##############################
########## Main ##############
##############################

if __name__ == "__main__":
   main(sys.argv[1:]) #Slice args cause 0 = script_file_name