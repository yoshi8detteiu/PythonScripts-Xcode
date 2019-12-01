# coding: utf-8
import glob
import os
import xml.etree.cElementTree as ET
import sys

filepaths = glob.glob("**/*.storyboard", recursive=True)
filepaths.extend(glob.glob("**/*.xib", recursive=True))

needError = False

for filepath in filepaths:
        tree = ET.parse(filepath) 
        root = tree.getroot()
        replaced = False
        for object_tag in root.iter('objects'):
                for color in object_tag.iter('color'):
                        if color.attrib.get('name') is None and color.attrib.get('cocoaTouchSystemColor') is None:
                                isExist = False
                                if color.attrib.get('white') is not None:
                                    isExist = True
                                if color.attrib.get('red') is not None:
                                    isExist = True
                                if color.attrib.get('green') is not None:
                                    isExist = True
                                if color.attrib.get('blue') is not None:
                                    isExist = True

                                if isExist:
                                    print('Error: Found!! in ' + filepath, file=sys.stderr)
                                    needError = True

if needError:
    raise Exception()   
else:
    print('Successed: Not Found!!')