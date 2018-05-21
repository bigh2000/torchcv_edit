'''
폴더 내의 모든 그림파일에 대해 inference(opencv), 39번째 줄에서 transform할 때
TypeError: pic should be PIL Image or ndarray. Got <class 'NoneType'>
와 같은 에러 발생
'''
import cv2
import os
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import xml.etree.ElementTree as ElementTree

from torch.autograd import Variable
from torchcv.models.fpnssd import FPNSSD512
from torchcv.models.ssd import SSD512, SSDBoxCoder


print('Loading model..')
net = FPNSSD512(num_classes=21)
net.load_state_dict(torch.load('../../../torchcv_edit_rel/checkpoint/ckpt.pth')['net'])
net.eval()

print('Loading image..')
img_path = '/home/dokyoung/Desktop/server/vanno_data/celeb/0'
anno_path = '/home/dokyoung/Desktop/server/vanno_results/celeb/0'
imgs = os.listdir(img_path); imgs.sort()
ow = oh = 512

for f in imgs:
    fname = f.split('.')[0]
    img = cv2.imread(os.path.join(img_path, f))
    tree = ElementTree.parse(os.path.join(anno_path, fname + '.xml'))
    root = tree.getroot()
    img = img.resize((ow,oh))

    print('Predicting..')
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485,0.456,0.406), (0.229,0.224,0.225))
    ])
    x = transform(img)
    x = Variable(x, volatile=True)
    loc_preds, cls_preds = net(x.unsqueeze(0))

    print('Decoding..')
    box_coder = SSDBoxCoder(net)
    boxes, labels, scores = box_coder.decode(
        loc_preds.data.squeeze(), F.softmax(cls_preds.squeeze(), dim=1).data)
    print(labels)
    print(scores)

    for box in boxes:
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 1)

    cv2.imshow(f, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()