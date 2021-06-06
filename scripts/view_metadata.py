"""
Add at the folder you want to read the metadata from, or you can pass the path to the file

Made by LunarKreatures(LainFenrir)
Feel free use or modify as you want
"""
import os
import sys
from PIL import Image
import xml.etree.ElementTree as ET
# This script shows the metada of an image, its tailored for kpp files but works for any image with -f

# <option> <filename>
allOptions = ["-f","-i"]
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
    input_file = loadImage(file_name)
    
    # -f full exif
    if option == "-f":
        for key in input_file.info:
            print("%s: %s" % (key,input_file.info[key]))
        input_file.close()
        return

    # -i show preset information
    if option == "-i":
        listInfo(input_file)
        input_file.close()
        return

    # Nothing 
    print(input_file.info['preset'])
    input_file.close()

"""
Loads the image
"""
def listInfo(input_file):
    presetMetadata:str = input_file.info['preset']
    metadataXml = ET.fromstring(presetMetadata)
    requiredBrushFilesList = metadataXml.find("./param[@name='requiredBrushFilesList']")
    CompositeOp = metadataXml.find("./param[@name='CompositeOp']")
    EraserMode = metadataXml.find("./param[@name='EraserMode']")

    print("\nPreset name: %s"% metadataXml.attrib["name"])
    print("Preset paintopid: %s"% metadataXml.attrib["paintopid"])
    print("Required brush files: %s" % requiredBrushFilesList.text)
    print("Blending mode: %s" % CompositeOp.text)
    print("Eraser mode: %s" % translateBinaryBool(EraserMode.text))
    print("=====================================")

    OpacityValue = metadataXml.find("./param[@name='OpacityValue']")
    OpacityUseCurve = metadataXml.find("./param[@name='OpacityUseCurve']")
    
    FlowUseCurve = metadataXml.find("./param[@name='FlowUseCurve']")
    FlowValue = metadataXml.find("./param[@name='FlowValue']")

    print("\nPreset Params")
    print("     Opacity value: %s"% OpacityValue.text)
    print("     Use curve for opacity: %s"% OpacityUseCurve.text)
    print("     Flow value: %s"% FlowValue.text)
    print("     use curve for flow: %s"% FlowUseCurve.text)
    print("=====================================")
    textureName = metadataXml.find("./param[@name='Texture/Pattern/Name']")
    textureFilePath = metadataXml.find("./param[@name='Texture/Pattern/PatternFileName']")

    if textureFilePath is not None or textureFilePath is not None:
        print("\nTexture:")
    if textureName is not None:
        print("     Texture name: %s"% textureName.text)
    if textureFilePath is not None:
        print("     Texture filePath: %s"% textureFilePath.text)
    if textureName is not None or textureFilePath is not None:
        print("=====================================")

    brushDefinition = metadataXml.find("./param[@name='brush_definition']")

    # I believe brush definition will never be None but leaving it there just in case
    if brushDefinition is not None:
        print("\nBrush:")
        definitionText:str = str(brushDefinition.text)
        definitionXml = ET.fromstring(definitionText)

        print("     Brush type: %s"% definitionXml.attrib["type"])
        print("     Brush angle: %s"% definitionXml.attrib["angle"])
        print("     Brush space: %s"% definitionXml.attrib["spacing"])

        if definitionXml.attrib["type"] == "png_brush":
            print("     Brush image name: %s"% definitionXml.attrib["filename"])
            print("     Brush image scale: %s"% definitionXml.attrib["scale"])

        if definitionXml.attrib["type"] == "gbr_brush":
            print("     Brush image name: %s"% definitionXml.attrib["filename"])
            print("     Brush image scale: %s"% definitionXml.attrib["scale"])
            print("     Brush Application: %s"% definitionXml.attrib["brushApplication"])
            print("     Contrast Adjustment: %s"% definitionXml.attrib["ContrastAdjustment"])
            print("     Adjustment Mid Point: %s"% definitionXml.attrib["AdjustmentMidPoint"])
            print("     Brightness Adjustment: %s"% definitionXml.attrib["BrightnessAdjustment"])
            print("     Use Color as Mask: %s"% translateBinaryBool(definitionXml.attrib["ColorAsMask"]))
        
        if definitionXml.attrib["type"] == "auto_brush":
            print("     Brush randomness: %s"% definitionXml.attrib["randomness"])
            print("     Brush density: %s"% definitionXml.attrib["density"])
        
        print("     Use auto spacing: %s"% translateBinaryBool(definitionXml.attrib["useAutoSpacing"]))
        print("     Auto spacing coef: %s"% definitionXml.attrib["autoSpacingCoeff"])
        print("=====================================")  
        # check if the brush has a masked brush
        maskGenerator = definitionXml.find("./MaskGenerator")
        if maskGenerator is not None:
            print("\nBrush Mask:")
            print("     Brush Type: %s"% maskGenerator.attrib["type"])
            print("     Ratio: %s"% maskGenerator.attrib["ratio"])
            print("     Diameter: %s"% maskGenerator.attrib["diameter"])
            print("     Brush antialias edges: %s"% translateBinaryBool(maskGenerator.attrib["antialiasEdges"]))
            print("     H fade: %s"% maskGenerator.attrib["hfade"])
            print("     V fade: %s"% maskGenerator.attrib["vfade"])
            print("     Spikers: %s"% maskGenerator.attrib["spikes"])
            print("=====================================")
    return
##############################
##### Auxiliar Functions #####
##############################

"""
translates 0 and 1 to true and false
"""
def translateBinaryBool(value):
    if value == 1:
        return "true"
    return "false"
"""
Loads the image
"""
def loadImage(file_name):
    checksPath(file_name)
    input_file = Image.open(file_name)
    input_file.load()
    return input_file

"""
Checks if its a valid path 
"""
def checksPath(file_name):
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