#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# run Keypoints_RCNN.ipynb


# In[ ]:


def calculate_angle(WIDTH, keypoints, FOV=160):
    '''
    Arguments:
        + Image width
        + Dictionary of keypoints
        + Field of vision of camera (in degrees). Default = 160 if using CSI camera with fish-eye lens
        
    Returns:
        + Angle at which the object is located from respect to the center    
    '''
    
    keys = keypoints.values()
    
    # if at least 2 points are detected
    if len(keys) > 1:  
        object_location = int(sum([x for x,y in keys])/len(keys))
        angle = int(-FOV*(WIDTH/2 - object_location)/WIDTH)
        return [angle], keypoints
    
    
    else:
        return [-1], keypoints


# In[ ]:


# import ipywidgets
# import time
# from IPython.display import display

# image_w = ipywidgets.Image(format='jpeg')
# display(image_w)



# out = ipywidgets.Output(layout={'border': '1px solid black'})
# display(out)

# while (True):
#     keypoints, image, counts, objects, peaks = execute({'new': camera.value})
# #     camera.observe(execute, names='value')
#     angle, _ = calculate_angle(WIDTH, keypoints)
#     with out:
#         out.clear_output()
#         print(f'Object is at angle: {angle}', end="\x1b[2K\r")
# #     draw_objects(image, counts, objects, peaks)
# #     image_w.value = bgr8_to_jpeg(image[:, ::-1, :])
    
#     time.sleep(0.05)


# In[ ]:




