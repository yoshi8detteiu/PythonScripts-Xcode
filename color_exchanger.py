# coding: utf-8
import json
import glob
import os
import xml.etree.cElementTree as ET
import numpy
import timeit
import sys
# import skimage

# 使い方
# Anacondaを導入して以下を実行。これを使ったときのPythonバージョンは3.7でした
# `python color_exchanger.py 色定義しているAssetCatalogのパス`


# AssetCatalogで近似している色定義を返す
def replacedColorName(dict, r, g, b, a):
        r = float(r)
        g = float(g)
        b = float(b)
        a = float(a)
        rgb1 = numpy.array([r,g,b,a],numpy.float64)
        # lab1 = skimage.color.rgb2lab(numpy.reshape(rgb1,(1,1,3)))

        min_diff = 9999999999999
        min_diff_key = ""
        for key in dict:
                json = dict[key]
                for color in json['colors']:
                        # Anyの値で判定
                        if 'appearances' in color.keys():
                                break
                        components = color['color']['components']
                        # 0~255形式は0~1形式にする
                        red = components['red']
                        green = components['green']
                        blue = components['blue']
                        alpha = components['alpha']
                        if red.isdigit():
                                red = float(red) / 255.0
                        if green.isdigit():
                                green = float(green) / 255.0
                        if blue.isdigit():
                                blue = float(blue) / 255.0       
                        red = float(red)
                        green = float(green)
                        blue = float(blue)
                        alpha = float(alpha)

                        rgb2 = numpy.array([red,green,blue,alpha],numpy.float64)
                        # lab2 = skimage.color.rgb2lab(numpy.reshape(rgb2,(1,1,3)))
                        # diff = skimage.color.deltaE_ciede2000(lab1, lab2)[0][0]

                        # CIEDE2000で色差計算しようとしたけど、うまくいかなかったのでユークリッド距離で計算
                        diff = numpy.linalg.norm(rgb1-rgb2)

                        if diff < min_diff:
                                min_diff = diff
                                min_diff_key = key

        return min_diff_key

# colorタグをApple形式の文字列に変換
def parseAppleColorTagString(colorElm):
        # ex) <color key="backgroundColor" red="0.93725490196078431" green="0.93725490196078431" blue="0.95686274509803926" alpha="1" colorSpace="custom" customColorSpace="sRGB"/>
        
        str = "<color"
        if colorElm.attrib.get('key') is not None:
                str = str + ' key="' + colorElm.attrib.get('key') + '"'
        
        if colorElm.attrib.get('white') is not None:
                str = str + ' white="' + colorElm.attrib.get('white') + '"'

        if colorElm.attrib.get('red') is not None:
                str = str + ' red="' + colorElm.attrib.get('red') + '"'
        
        if colorElm.attrib.get('green') is not None:
                str = str + ' green="' + colorElm.attrib.get('green') + '"'
        
        if colorElm.attrib.get('blue') is not None:
                str = str + ' blue="' + colorElm.attrib.get('blue') + '"'
        
        if colorElm.attrib.get('alpha') is not None:
                str = str + ' alpha="' + colorElm.attrib.get('alpha') + '"'
        
        if colorElm.attrib.get('colorSpace') is not None:
                str = str + ' colorSpace="' + colorElm.attrib.get('colorSpace') + '"'
        
        if colorElm.attrib.get('customColorSpace') is not None:
                str = str + ' customColorSpace="' + colorElm.attrib.get('customColorSpace') + '"'

        str = str + "/>"

        return str

# dependenciesにNamed colorsがあるかチェック
def isExistDependenciesNamedColors(root):
        for dependencies in root.iter('dependencies'):
                for capability in dependencies.findall('capability'):
                        if capability.find('name') == "Named colors":
                                return  True
        return False

# resourcesタグがあるかチェック
def isExistResources(root):
        for resources in root.iter('resources'):
                return True
        return False

# resourcesのにnameが定義された色があるかチェック
def isExistResourcesNamedColor(root,name):
        for resources in root.iter('resources'):
                for namedColor in resources.findall('namedColor'):
                        if namedColor.find('name') == name:
                                return  True
        return False

# namedColorタグをAssetCatalog情報を元に生成する
def createNamedColorTagStr(json):
        # ex)
        # <namedColor name="coolGrey">
        #     <color red="0.57300001382827759" green="0.60000002384185791" blue="0.63899999856948853" alpha="1" colorSpace="custom" customColorSpace="sRGB"/>
        # </namedColor>

        for color in json['colors']:
                # Anyの値を使う
                if 'appearances' in color.keys():
                        break
                components = color['color']['components']
                # 0~255形式は0~1形式にする
                red = components['red']
                green = components['green']
                blue = components['blue']
                alpha = components['alpha']
                if red.isdigit():
                        red = float(red) / 255.0
                if green.isdigit():
                        green = float(green) / 255.0
                if blue.isdigit():
                        blue = float(blue) / 255.0       
                red = str(red) 
                green = str(green)
                blue = str(blue)
                alpha = str(alpha)
                # とりあえずsRGBのみ対応
                color_tag = '<color red="' + red + '" green="' + green + '" blue="' + blue + '" alpha="' + alpha + '" colorSpace="custom" customColorSpace="sRGB"/>'

                return '<namedColor name="' + name + '">\n            ' + color_tag + '\n        </namedColor>'

        return ""

# AssetCatalogのjsonを取得し、名前をkeyにしたdictionaryを生成
def createAssetCatalogDict(xcassets_path):
        colorset_filepaths = glob.glob(xcassets_path + "/*.colorset")
        asset_catalog_dict = {}
        for filepath in colorset_filepaths:
                basename = os.path.basename(filepath) 
                filename = os.path.splitext(basename)[0]
                contents = open(filepath + "/Contents.json", "r")
                color_json = json.load(contents)
                asset_catalog_dict[filename] = color_json
        return asset_catalog_dict

args = sys.argv
xcassets_path = args[1] 
asset_catalog_dict = createAssetCatalogDict(xcassets_path)
filepaths = glob.glob("**/*.storyboard", recursive=True)
filepaths.extend(glob.glob("**/*.xib", recursive=True))

# Customで色指定している箇所を、AssetCatalogの色に置換
for filepath in filepaths:
        tree = ET.parse(filepath) 
        root = tree.getroot()
        exchange_dict = {} # 置換する情報
        replaced = False
        for object_tag in root.iter('objects'):
                for color in object_tag.iter('color'):
                        if color.attrib.get('name') is None and color.attrib.get('cocoaTouchSystemColor') is None:
                                replaced = True
                                
                                # AssetCatalogの近似色名を取得
                                if color.attrib.get('white') is None:
                                        name = replacedColorName(asset_catalog_dict, color.get("red"), color.get("green"), color.get("blue"), color.get("alpha"))
                                else:
                                        name = replacedColorName(asset_catalog_dict, 1, 1, 1, 1)

                                # 現在のタグを文字列に変換
                                tag_str = parseAppleColorTagString(color)
                                if color.attrib.get('key') is None:
                                        exchange_dict[tag_str] = '<color name="' + name + '"/>'
                                else:
                                        key = color.attrib.get('key')
                                        exchange_dict[tag_str] = '<color key="' + key + '" name="' + name + '"/>'

                                # dependenciesにNamed colorsがあるかチェックし、無かったら入れる
                                dependencies_key = "<dependencies>\n"
                                if not isExistDependenciesNamedColors(root) and not dependencies_key in exchange_dict.keys():
                                        exchange_dict[dependencies_key] = '<dependencies>\n        <capability name="Named colors" minToolsVersion="9.0"/>\n'
                                        
                                # resourcesがなかったら入れる
                                resources_key = "</document>"
                                if not isExistResources(root) and not resources_key in exchange_dict.keys():
                                        exchange_dict[resources_key] = '    <resources>\n    </resources>\n</document>'
                                # namedColorがなかったら入れる
                                if not isExistResourcesNamedColor(root,name):
                                        tag = createNamedColorTagStr(asset_catalog_dict[name])
                                        color_named_key = "<resources>\n"
                                        if color_named_key in exchange_dict.keys():
                                                # 既にresourcesがあるなら、valueに付け足す
                                                tag_str = exchange_dict[color_named_key]
                                                if tag_str.find(name) == -1: # nameがすでにあるなら付け足さない
                                                        exchange_dict["<resources>\n"] = tag_str + '        ' + tag + '\n'
                                        else:
                                                exchange_dict["<resources>\n"] = '<resources>\n        ' + tag + '\n'
                                                                        
        if replaced:
                print(filepath)
                fileR = open(filepath,"r+")
                filedata = fileR.read()
                for key in exchange_dict:
                        filedata = filedata.replace(key, exchange_dict[key])
                fileW = open(filepath,"w+")
                fileW.write(filedata)
