#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# run Keypoints_RCNN.ipynb


# In[ ]:


def estimating_phase(keypoints):
    '''
    Estimates the phase based on the skeleton parts detected:
    
    Phase 1: Knees and ankles are detected.
    Phase 2: Skeleton is detected but one of the knees or ankles is missing (obstructed by obstacle).
    Phase 3: No skeleton is detected.
    
    '''
    
    
    # If camera detects skeleton
    if keypoints:
        
        leg_parts = ["left_knee", "right_knee", "left_ankle", "right_ankle"] 
        obstructed = [x for x in leg_parts if x not in keypoints.keys()]
        
        # If legs are obstructed
        if obstructed:
            return [0,1,0]  # Phase 2
        
        else:
            return [0,0,1]   # Phase 1
            
    # No skeleton detected
    else:
        return [1,0,0]   # Phase 3


# In[ ]:


# import ipywidgets
# import time
# from IPython.display import display

# image_w = ipywidgets.Image(format='jpeg')
# display(image_w)


# while (True):
#     keypoints, image, counts, objects, peaks = execute({'new': camera.value})
#     print(f"Phase: {estimating_phase(keypoints)}")
#     draw_objects(image, counts, objects, peaks)
#     image_w.value = bgr8_to_jpeg(image[:, ::-1, :])
#     time.sleep(1)

