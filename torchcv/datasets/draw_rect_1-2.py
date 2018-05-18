'''
그림파일을 annotation과 함께 표시(opencv)
'''
import cv2
import os
import time
import xml.etree.ElementTree as ElementTree

img_path = '/home/dokyoung/Desktop/server/vanno_data/celeb/0'
anno_path = '/home/dokyoung/Desktop/server/vanno_results/celeb/0'
ext = '.jpg'
cv2.namedWindow('test')

fname = '000001'
img = cv2.imread(os.path.join(img_path, fname + ext))
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
        cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (0,0,255), 3)
cv2.imshow('test', img)
cv2.waitKey(0)
cv2.destroyAllWindows()