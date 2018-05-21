'''
dataloader에 넣기 위해 custom으로 ListDataset 작성.
img_path_super와 anno_path_super를 인자로 받아
하위폴더의 이름을 class로 하여 train시키기 위함.
'''

import os
import PIL.Image
import torch
import torch.utils.data as data
import xml.etree.ElementTree as ElementTree

PIL.Image.MAX_IMAGE_PIXELS = None

class ListDataset(data.Dataset):
    def __init__(self, img_path_super, anno_path_super, transform=None):
        self.img_path_super = img_path_super
        self.anno_path_super = anno_path_super
        self.transform = transform

        self.fnames = []
        self.boxes = []
        self.labels = []

        ls_img_super = os.listdir(img_path_super); ls_img_super.sort()
        self.num_dirs = len(ls_img_super)
        self.num_imgs = 0

        for d in ls_img_super:
            img_path = os.path.join(img_path_super, d)
            anno_path = os.path.join(anno_path_super, d)
            ls_img = os.listdir(img_path); ls_img.sort()
            ls_img_no_ext = [f.split('.')[0] for f in ls_img]
            self.num_imgs += len(ls_img)

            i=1
            for f in ls_img_no_ext:
                tree = ElementTree.parse(anno_path + '/' + f + '.xml')
                # print('%03d, filename: ' % i, f + '.xml')
                i += 1
                root = tree.getroot()
                for obj in root.findall('object'):
                    xmin = int(obj.find('bndbox').find('xmin').text)
                    ymin = int(obj.find('bndbox').find('ymin').text)
                    xmax = int(obj.find('bndbox').find('xmax').text)
                    ymax = int(obj.find('bndbox').find('ymax').text)
                    self.fnames.append(os.path.join(os.path.join(self.img_path_super, d), f + '.jpg'))
                    self.boxes.append(torch.Tensor([[xmin, ymin, xmax, ymax]]))
                    self.labels.append(torch.LongTensor([int(d)]))
                    # print(int(d), xmin, ymin, xmax, ymax)

    def __getitem__(self, idx):
        # Load image and boxes.
        fname = self.fnames[idx]
        # print(fname)
        img = PIL.Image.open(os.path.join(fname))
        if img.mode != 'RGB':
            img = img.convert('RGB')

        boxes = self.boxes[idx]  # use clone to avoid any potential change.
        labels = self.labels[idx]

        if self.transform:
            img, boxes, labels = self.transform(img, boxes, labels)
        return img, boxes, labels

    def __len__(self):
        return self.num_imgs

# img_path_super = '../../../Datasets/vanno_data/celeb'
# anno_path_super = '../../../Datasets/vanno_results/celeb'
# trainset = ListDataset(img_path_super, anno_path_super)
# print('')