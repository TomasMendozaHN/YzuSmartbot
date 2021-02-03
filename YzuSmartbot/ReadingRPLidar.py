#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import getpass
import os

password = 'jetbot'
command = "sudo -S chmod 666 /dev/ttyUSB0" #can be any command but don't forget -S as it enables input from stdin
os.system('echo %s | %s' % (password, command))


# In[ ]:


from rplidar import RPLidar


# In[ ]:


# Establish connection with Lidar using Library
lidar = RPLidar('/dev/ttyUSB0')  # Choose usb port where RPLidar is located in


# In[ ]:


# Define what angles you want to measure
angles = [180]         


# In[ ]:


# Initialize all sensor readings to 0
previous_readings = {x:0 for x in angles} 


# In[ ]:


def read_lidar_wrapper(angles,previous_readings):
    
    ''' Wrapper function for the RPLidar library. 
    
        This function takes as inputs:
            -> the angles to measure as a list
            -> the RPLidar object (instantiated using RPLidar library)
            -> the previous_readings dictionary 
            
        This function returns:
            -> the updated previous_readings dictionary with new measurements

        '''
       
    lidar = RPLidar('/dev/ttyUSB0')  # Establish connection with Lidar
    for i, scan in enumerate(lidar.iter_scans()):  # Scan the sensor infinitely
        if i>0:
            readings = ({int(x[1]): int(x[2]) for x in list(scan) if int(x[1]) in angles})
            break  # Stop the scan to exit infinite loop
    
    
    #  Sometimes the sensor doesn't read all angles (unfortunately that's how it works)
    #  so we must add those missing values as the previous sensor readings 
    #  to avoid having a dictionary with missing values
    for key in previous_readings.keys():
        try:
            if readings[key]: 
                previous_readings[key]=readings[key]
        except:
            continue

    lidar.stop()        # Stop the sensor to be able to read it again
    lidar.disconnect()  # Stop the sensor to be able to read it again
    return previous_readings


# In[ ]:


# while (True):
#     print(read_lidar_wrapper(angles,previous_readings), end=",")


# In[ ]:




