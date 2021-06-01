"""
Add at the folder you want to read the metadata from, or you can pass the path to the file

Made by LunarKreatures(LainFenrir)
Feel free use or modify as you want
"""
import os
import sys
from PIL import Image


# <option> <filename>
allOptions = ["-f"]
def main(argv):
    adjustedArgs:list = adjustArgs(argv)

    option:str = adjustedArgs[0]
    fileName:str = adjustedArgs[1]

    view(option,fileName)

    print('Argument List:', str(argv))

##############################
###### Main Functions  #######
##############################

"""
Prints Exif information from kpp file
"""
def view(option:str,file_name:str):
    
    # -f full exif
    if option == "-f":
        input_file = load_image(file_name)
        for key in input_file.info:
            print("%s: %s" % (key,input_file.info[key]))
        input_file.close()
        return

    # Nothing 
    input_file = load_image(file_name)
    print(input_file.info['preset'])
    input_file.close()

##############################
##### Auxiliar Functions #####
##############################

"""
Loads the image
"""
def load_image(file_name):
    checks_path(file_name)
    input_file = Image.open(file_name)
    input_file.load()
    return input_file

"""
Checks if its a valid path 
"""
def checks_path(file_name):
    if os.path.exists(file_name):
        return
    
    print("file doesnt exist. File name : %s" % file_name)
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