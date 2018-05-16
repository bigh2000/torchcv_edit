import os
import PIL
import torch
import torch.utils.data as data
import xml.etree.ElementTree as ElementTree

class ListDataset(data.Dataset):
    def __init__(self, img_path, anno_path, transform=None):
        self.img_path = img_path
        self.anno_path = anno_path
        self.transform = transform

        self.fnames = []
        self.boxes = []
        self.labels = []

        ls_img = os.listdir(img_path)
        ls_img.sort()
        ls_img_no_ext = [f.split('.')[0] for f in ls_img]
        # print(ls_img)
        ls_anno = os.listdir(anno_path)
        ls_anno.sort()
        ls_anno_no_ext = [f.split('.')[0] for f in ls_anno]
        # print(ls_anno)
        ls_inter = [f for f in ls_img_no_ext if f in ls_anno_no_ext]
        print('list of intersection: ', ls_inter)
        self.num_imgs = len(ls_inter)
        print('img: ', len(ls_img), 'anno: ', len(ls_anno), 'intersection: ', len(ls_inter))
        ls_inter_jpg = [f + '.jpg' for f in ls_inter]
        ls_inter_xml = [f + '.xml' for f in ls_inter]

        i=1
        for xml in ls_inter_xml:
            tree = ElementTree.parse(anno_path + '/' + xml)
            print('%03d, filename: ' % i, xml)
            i += 1
            self.fnames.append(xml)
            root = tree.getroot()
            j = 0
            for obj in root.findall('object'):
                j += 1
                box = []
                label = []
                xmin = int(obj.find('bndbox').find('xmin').text)
                ymin = int(obj.find('bndbox').find('ymin').text)
                xmax = int(obj.find('bndbox').find('xmax').text)
                ymax = int(obj.find('bndbox').find('ymax').text)
                c = obj.find('name').text
                box.append([xmin, ymin, xmax, ymax])
                label.append(c)
                print(c, xmin, ymin, xmax, ymax)

                self.boxes.append(torch.Tensor(box))
                self.labels.append(label)
            print('%d classes' % j if j != 1 else '1 class')

    def __getitem__(self, idx):
        # Load image and boxes.
        fname = self.fnames[idx]
        img = PIL.Image.open(os.path.join(self.img_path, fname))
        if img.mode != 'RGB':
            img = img.convert('RGB')

        boxes = self.boxes[idx].clone()  # use clone to avoid any potential change.
        labels = self.labels[idx].clone()

        if self.transform:
            img, boxes, labels = self.transform(img, boxes, labels)
        return img, boxes, labels

    def __len__(self):
        return self.num_imgs

img_path = '/home/dokyoung/Desktop/server/vanno_data/celeb/0'
anno_path = '/home/dokyoung/Desktop/server/vanno_results/celeb/0'
# trainset = ListDataset(img_path, anno_path)