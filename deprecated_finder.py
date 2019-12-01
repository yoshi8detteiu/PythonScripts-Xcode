# coding: utf-8
import glob
import os
import xml.etree.cElementTree as ET
import sys

filepaths = glob.glob("**/*.storyboard", recursive=True)
filepaths.extend(glob.glob("**/*.xib", recursive=True))

needError = False

deprecated_symbols = ['previewAction', 'previewActionGroup', 'actionSheet', 'alertView', 'documentMenuViewController', 'localNotification', 'mutableUserNotificationAction', 'mutableUserNotificationCategory', 'popoverController', 'searchDisplayController', 'storyboardPopoverSegue', 'userNotificationAction', 'userNotificationCategory', 'userNotificationSettings']

for filepath in filepaths:
    tree = ET.parse(filepath) 
    root = tree.getroot()
    for deprecated in deprecated_symbols:
        for deprecated_tag in root.iter(deprecated):
            print('Error: Found!! in ' + filepath, file=sys.stderr)
            needError = True
            break

if not needError:
    print('Successed: Not Found!!')