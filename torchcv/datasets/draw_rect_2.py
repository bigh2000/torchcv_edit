'''
폴더 내의 모든 그림파일을 annotation과 함께 표시(opencv), 이미지가 클 경우 resize
'''
import cv2
import os
import time
import xml.etree.ElementTree as ElementTree

img_path = '/home/dokyoung/Desktop/server/vanno_data/celeb/0'
anno_path = '/home/dokyoung/Desktop/server/vanno_results/celeb/0'

# ext = '.jpg'
imgs = os.listdir(img_path); imgs.sort()
for f in imgs:
    fname = f.split('.')[0]
    img = cv2.imread(os.path.join(img_path, f))
    tree = ElementTree.parse(os.path.join(anno_path, fname + '.xml'))
    root = tree.getroot()

    for obj in root.findall('object'):
        xmin = int(obj.find('bndbox').find('xmin').text)
        ymin = int(obj.find('bndbox').find('ymin').text)
        xmax = int(obj.find('bndbox').find('xmax').text)
        ymax = int(obj.find('bndbox').find('ymax').text)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)

    h, w = img.shape[:2]
    if img.shape[0] > 2000:
        zoom = cv2.resize(img, None, fx=0.25, fy=0.25)
        cv2.imshow(f + '_resized', zoom)
    elif img.shape[0] > 1000:
        zoom = cv2.resize(img, None, fx=0.5, fy=0.5)
        cv2.imshow(f + '_resized', zoom)
    else:
        cv2.imshow(f, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()