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
    
    for attributed_string in root.iter('attributedString'):
        text = ''
        isExist = False
        for fragment in attributed_string.iter('fragment'):
            content = fragment.attrib.get('content')
            if content is not None:
                text = text + content 

            for string in fragment.iter('string'):
                if 'Cg' in string.text:
                    isExist = True

        for font in attributed_string.iter('font'):
            font_name = font.attrib.get('name')
            if font_name is not None and font_name == '.AppleSystemUIFont':
                isExist = True
                         
        if isExist:
            print('Found!! in ' + filepath + ' : ' + text, file=sys.stderr)
            needError = True

if needError:
    raise Exception()   
else:
    print('Successed: Not Found!!')
    