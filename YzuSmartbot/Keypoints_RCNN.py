#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import trt_pose.coco
import torch

with open('human_pose.json', 'r') as f:
    human_pose = json.load(f)

topology = trt_pose.coco.coco_category_to_topology(human_pose)

visualize = False


# In[ ]:


import getpass
import os

password = 'jetbot'
command = "sudo -S systemctl restart nvargus-daemon" #can be any command but don't forget -S as it enables input from stdin
os.system('echo %s | %s' % (password, command))


# In[ ]:


import trt_pose.models

num_parts = len(human_pose['keypoints'])
num_links = len(human_pose['skeleton'])

model = trt_pose.models.resnet18_baseline_att(num_parts, 2 * num_links).cuda().eval()


# In[ ]:


import torch2trt
import urllib
from torch2trt import TRTModule

model_trt = TRTModule()


# In[ ]:

filename="resnet18_baseline_att_224x224_A_epoch_249_trt.pth"
url="https://download1515.mediafire.com/mgjv5g7gcdlg/s9gmxc41vawt0wn/resnet18_baseline_att_224x224_A_epoch_249_trt.pth"

if not os.path.isfile(filename):
	print("Downloading pretrained keypoints from Google Drive")
	urllib.request.urlretrieve(url, filename)
	print("Finished Downloading.")

model_trt.load_state_dict(torch.load('resnet18_baseline_att_224x224_A_epoch_249_trt.pth'))


# In[ ]:


WIDTH = 224
HEIGHT = 224

data = torch.zeros((1, 3, HEIGHT, WIDTH)).cuda()


# In[ ]:


import ipywidgets
from IPython.display import display

image_w = ipywidgets.Image(format='jpeg')


# In[ ]:


import cv2
import torchvision.transforms as transforms
import PIL.Image

mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
device = torch.device('cuda')

def preprocess(image):
    global device
    device = torch.device('cuda')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device)
    image.sub_(mean[:, None, None]).div_(std[:, None, None])
    return image[None, ...]


# In[ ]:


from trt_pose.draw_objects import DrawObjects
from trt_pose.parse_objects import ParseObjects

parse_objects = ParseObjects(topology)
draw_objects = DrawObjects(topology)


# In[ ]:


from jetcam.usb_camera import USBCamera
from jetcam.csi_camera import CSICamera
from jetcam.utils import bgr8_to_jpeg

camera = CSICamera(width=WIDTH, height=HEIGHT, capture_fps=30)

camera.running = True


# In[ ]:


def get_keypoints(image, human_pose, topology, object_counts, objects, normalized_peaks):
    """Get the keypoints from torch data and put into a dictionary where keys are keypoints
    and values the x,y coordinates. The coordinates will be interpreted on the image given.

    Args:
        image: cv2 image
        human_pose: json formatted file about the keypoints

    Returns:
        dictionary: dictionary where keys are keypoints and values are the x,y coordinates
    """
    height = image.shape[0]
    width = image.shape[1]
    keypoints = {}
    K = topology.shape[0]
    count = int(object_counts[0])

    for i in range(count):
        obj = objects[0][i]
        C = obj.shape[0]
        for j in range(C):
            k = int(obj[j])
            if k >= 0:
                peak = normalized_peaks[0][j][k]
                x = round(float(peak[1]) * width)
                y = round(float(peak[0]) * height)
                keypoints[human_pose["keypoints"][j]] = (x, y)

    return keypoints


# In[ ]:


def execute(change, visualize=True):
    image = change['new']
    data = preprocess(image)
    cmap, paf = model_trt(data)
    cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
    counts, objects, peaks = parse_objects(cmap, paf)#, cmap_threshold=0.15, link_threshold=0.15)
    keypoints = get_keypoints(image, human_pose, topology, counts, objects, peaks)

    return keypoints, image, counts, objects, peaks

