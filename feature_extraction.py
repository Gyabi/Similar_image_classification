from PIL.Image import Image
import torch
from torch._C import device
from torch.functional import Tensor
from torch.utils import data
from torchvision import models
from torch import nn
from torchvision import transforms
from PIL import Image
import numpy as np


    
def get_device(use_gpu):
    """
    deviceの設定
    """
    if use_gpu and torch.cuda.is_available():
        torch.backends.cudnn.deterministic = True
        return torch.device("cuda")
    else:
        return torch.device("cpu")
     
def feature_extraction(image_list):
    """
    画像pathlistを入力して特徴量マップのリストを返却するAPI
    """
    # device設定
    device = get_device(use_gpu=True)
        
    # model設定
    model = models.resnet50(pretrained=True)
    model.fc = nn.Identity()
    model.to(device)
    model.eval()
    
    transform = transforms.Compose(
    [
        transforms.Resize(256),  # (256, 256) で切り抜く。
        transforms.CenterCrop(224),  # 画像の中心に合わせて、(224, 224) で切り抜く
        transforms.ToTensor(),  # テンソルにする。
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        ),  # 標準化する。
    ])
    
    outputs = []
    for path in image_list:
        img = Image.open(path)
        inputs = transform(img)
        inputs = inputs.unsqueeze(0).to(device)
        out = model(inputs)
        outputs.append(np.squeeze(out.to("cpu").detach().numpy().copy()))
        
    return np.array(outputs)
    

    
    
    

