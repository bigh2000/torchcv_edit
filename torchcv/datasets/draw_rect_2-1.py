'''
그림파일 리스트를 annotation과 함께 표시(opencv), 이미지가 클 경우 resize.
'''
import cv2
import os
import xml.etree.ElementTree as ElementTree

from torchcv.datasets import listdataset_1

# img_path = '/home/dokyoung/Desktop/server/vanno_data/celeb/0'
# anno_path = '/home/dokyoung/Desktop/server/vanno_results/celeb/0'
img_path = '../../../Datasets/vanno_data/celeb/0'
anno_path = '../../../Datasets/vanno_results/celeb/0'
trainset = listdataset_1.ListDataset(img_path, anno_path)

# imgs = []
# for i in range(len(trainset.labels)):
#     if len(trainset.labels[i]) > 1:
#         imgs.append(trainset.fnames[i])

ext = '.jpg'
# fnames = [98, 277, 355, 486, 493, 510, 546, 556, 581, 600, 601, 627]
fnames = [355, 486, 493, 556]
fnames = ['%06d' % fname for fname in fnames]
imgs = [fname + ext for fname in fnames]

for f in imgs:
    img = cv2.imread(os.path.join(img_path, f))
    tree = ElementTree.parse(os.path.join(anno_path, f.split('.')[0] + '.xml'))
    root = tree.getroot()

    for obj in root.findall('object'):
        xmin = int(obj.find('bndbox').find('xmin').text)
        ymin = int(obj.find('bndbox').find('ymin').text)
        xmax = int(obj.find('bndbox').find('xmax').text)
        ymax = int(obj.find('bndbox').find('ymax').text)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
    h, w = img.shape[:2]
    if img.shape[0] > 2000:
        cv2.namedWindow(f + '_resized', cv2.WINDOW_NORMAL)
        cv2.moveWindow(f + '_resized', 0, 0)
        zoom = cv2.resize(img, None, fx=0.25, fy=0.25)
        cv2.imshow(f + '_resized', zoom)
    elif img.shape[0] > 1000:
        cv2.namedWindow(f + '_resized', cv2.WINDOW_NORMAL)
        cv2.moveWindow(f + '_resized', 0, 0)
        zoom = cv2.resize(img, None, fx=0.5, fy=0.5)
        cv2.imshow(f + '_resized', zoom)
    else:
        # cv2.namedWindow(f, cv2.WINDOW_NORMAL)
        # cv2.moveWindow(f, 0, 0)
        cv2.imshow(f, img)
    # cv2.imshow(f, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # import matplotlib.pyplot as plt
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # plt.show()


# 오류
# 355 다른사람 얼굴 잡힘
# 486 다른사람 얼굴 잡힘
# 493 다른사람 얼굴 잡힘
# 556 다른사람 얼굴 잡힘

# 의심
# 98 작은얼굴 일부러 안잡은거?
# 277 아주작은얼굴, 옆얼굴,
# 510 흐릿한얼굴 일부러 안잡은거?
# 546 작은얼굴 일부러 안잡은거?
# 581 옆얼굴 일부러 안잡은거?
# 600 가려진 작은얼굴 일부러 안잡은거?
# 601 작은얼굴 일부러 안잡은거?
# 627 작은얼굴 일부러 안잡은거?

# 중복은 일부러 넣은거?
# 50 VS 85
# 615 vs 641