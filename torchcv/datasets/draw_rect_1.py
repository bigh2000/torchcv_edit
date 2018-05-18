'''
그림파일을 annotation과 함께 표시(PIL)
'''
import os
from PIL import Image, ImageDraw
import torch
import xml.etree.ElementTree as ElementTree

img_path = '/home/dokyoung/Desktop/server/vanno_data/celeb/0'
anno_path = '/home/dokyoung/Desktop/server/vanno_results/celeb/0'
ext = '.jpg'

fname = '000002'
img = Image.open(os.path.join(img_path, fname + ext))
draw = ImageDraw.Draw(img)
tree = ElementTree.parse(os.path.join(anno_path, fname + '.xml'))
root = tree.getroot()

boxes = []
labels = []
box = []
label = []
for obj in root.findall('object'):
    xmin = int(obj.find('bndbox').find('xmin').text)
    ymin = int(obj.find('bndbox').find('ymin').text)
    xmax = int(obj.find('bndbox').find('xmax').text)
    ymax = int(obj.find('bndbox').find('ymax').text)
    box.append([xmin, ymin, xmax, ymax])

boxes.append(box)
for box in boxes:
    for b in box:
        draw.rectangle(b, outline='red')
img.show()