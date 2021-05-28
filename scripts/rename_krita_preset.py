"""

Made by LunarKreatures(LainFenrir)
Feel free use or modify as you want
"""
import os
import sys
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo
from send2trash import send2trash

#python rename_krita_brush.py LainKit_Wet_flat_size.kpp 

#kpp tag preset <Preset paintopid="colorsmudge" name="LainKit_Wet_flat_size"> 
# change both file name and name in the preset tag

# <option> <file_path> <new_name> <find>   option is optional

all_options = ["-f","-p","-d"]

def main(argv):
    option = ""
    find = ""
    file_name = argv[0]
    new_name = argv[1]

    if argv[0] in all_options:
        option = argv[0]
        file_name = argv[1]
        new_name = argv[2]
        if option == "-f":
            find= argv[3]
            
    rename(option,file_name,new_name,find)

    print('Argument List:', str(argv))

##############################
###### Main Functions  #######
##############################

"""
Renames .kpp file
"""
def rename(option,file_name,new_name,find):
    delete_actions = ["-d"]
    to_delete_old = False
    if option in delete_actions:
        to_delete_old = True
    file_no_extension:str = file_name.split(".")[0]
    new_name_png:str = ".".join([new_name,"png"])
    new_name_kpp:str = ".".join([new_name,"kpp"])


    # -find and replace
    if option == "-f":
        
       
        return
    # -p set prefix
    if option == "-p":
       
       
        return


    # null replace name with another
    preset_info,input_file = grab_preset(file_name)
    replaced_preset:str =preset_info.replace(file_no_extension,new_name)

    target_image = PngImageFile(file_name)

    metadata = PngInfo()
    for key in input_file.info:
        if key == "dpi":
            metadata.add_text(key,str(input_file.info[key]))
            continue
        if key == "preset":
            continue
        metadata.add_text(key,input_file.info[key])

    metadata.add_text("preset", replaced_preset)
    target_image.save(new_name_png, pnginfo=metadata)
    input_file.close()

    os.rename(new_name_png,new_name_kpp)
    
    if to_delete_old:
        send2trash(file_name)

##############################
###### Auxiliar Functions ####
##############################

"""
Builds operation instructions
"""
def grab_preset(file_name):
    input_file = load_image(file_name)
    return input_file.info['preset'],input_file

"""
Checks if its a valid path 
"""
def checks_path(file_name):
    if os.path.exists(file_name):
        return
    
    print("file doesnt exist. File name : %s" % file_name)
    sys.exit()
    
"""
Loads the image
"""
def load_image(file_name):
    checks_path(file_name)
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