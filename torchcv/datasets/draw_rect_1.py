'''
그림파일을 annotation과 함께 원본크기로 표시(PIL)
'''
import os
from PIL import Image, ImageDraw
import torch
import xml.etree.ElementTree as ElementTree

img_path = '/home/dokyoung/Desktop/server/vanno_data/celeb/0'
anno_path = '/home/dokyoung/Desktop/server/vanno_results/celeb/0'
ext = '.jpg'
# fnames = [98, 277, 355, 486, 493, 510, 546, 556, 581, 600, 601, 627] % 하나씩 뜨게할 방법이 없어서 주석처리
fnames = [98]
fnames = ['%06d' % fname for fname in fnames]
imgs = [fname + ext for fname in fnames]
for f in imgs:
    img = Image.open(os.path.join(img_path, f))
    draw = ImageDraw.Draw(img)
    tree = ElementTree.parse(os.path.join(anno_path, f.split('.')[0] + '.xml'))
    root = tree.getroot()

    box = []
    for obj in root.findall('object'):
        xmin = int(obj.find('bndbox').find('xmin').text)
        ymin = int(obj.find('bndbox').find('ymin').text)
        xmax = int(obj.find('bndbox').find('xmax').text)
        ymax = int(obj.find('bndbox').find('ymax').text)
        box.append([xmin, ymin, xmax, ymax])

    for b in box:
        draw.rectangle(b, outline='red')
    img.show()