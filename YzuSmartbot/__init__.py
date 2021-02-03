from YzuSmartbot import Keypoints_RCNN
from YzuSmartbot import CalculatingAngles
from YzuSmartbot import ReadingRPLidar
from YzuSmartbot import StageEstimation

class Environment():
    
    '''
    This wrapper works as an RL-Environment for the Jetson Nano.
    Arguments are: 
        model  -> pytorch model trained in Unity.
        angles -> list of angles required to measure
        FOV    -> How wide the camera lens is. Default = 160
    '''
    
    def __init__(self, model, angles, FOV=160):
        self.previous_readings = {x:0 for x in angles} 
        self.angles = angles
        self.model = model
        self.FOV = FOV
        
        
    def calculate_angle_and_phase(self):
        keypoints, image, counts, objects, peaks = execute({'new': camera.value})
        angle, keypoints = calculate_angle(WIDTH, keypoints, self.FOV)
        phase = self.calculate_phase(keypoints)
        return phase, angle
    
    
    def calculate_phase(self, keypoints):
        phase = estimating_phase(keypoints)
        return phase
    
    
    def read_lidar(self):
        self.previous_readings = read_lidar_wrapper(self.angles,self.previous_readings)
        
    
    def observe(self):
        self.read_lidar()
        phase, angle = self.calculate_angle_and_phase()
        
        if isinstance(angle, dict):
            angles = list(angle.values())
        
        else: angles = [-1]
        
        observation = phase + angle + list(self.previous_readings.values())
        return observation
    
    
    def sample_action(self, observation):
        observation = torch.Tensor(observation).cuda()
        hidden,_ = self.model.network_body(vis_inputs=[0],vec_inputs=[observation])
        distribution = self.model.distribution(hidden)
        action = distribution.sample()
        return action
