'''
폴더 내의 모든 그림파일에 대해 inference(PIL), 이미지를 닫을 때마다 enter키를 눌러야 함.
'''
import os
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms

from PIL import Image, ImageDraw
from torch.autograd import Variable
from torchcv.models.fpnssd import FPNSSD512
from torchcv.models.ssd import SSD512, SSDBoxCoder


print('Loading model..')
net = FPNSSD512(num_classes=21)
net.load_state_dict(torch.load('../../../torchcv_edit_rel/checkpoint/ckpt.pth')['net'])
net.eval()

print('Loading image..')
# img_path = '/home/dokyoung/Desktop/server/vanno_data/celeb/0'
# anno_path = '/home/dokyoung/Desktop/server/vanno_results/celeb/0'
img_path = '../../../Datasets/vanno_data/celeb/5'
anno_path = '../../../Datasets/vanno_results/celeb/5'
imgfnames = os.listdir(img_path); imgfnames.sort()
ow = oh = 512

for imgfname in imgfnames:
    img = Image.open(os.path.join(img_path, imgfname))
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

    draw = ImageDraw.Draw(img)
    for box in boxes:
        draw.rectangle(list(box), outline='red')
    img.show()
    input()