import cv2
import numpy as np
from picamera import PiCamera
from time import sleep
from fractions import Fraction


class Camera:
    
    def __init__(self):
        self.camera = PiCamera(resolution=(1280, 720), framerate=Fraction(1, 6), sensor_mode=3)
        
        self.camera.iso = 100
        self.camera.shutter_speed = 3000000
        self.camera.exposure_mode = 'off'
        
    def take_photo(self):
        self.camera.capture("temp.jpg")
        
    def undistort(self):
        
        self.take_photo()
        
        K = np.array([[  689.21,     0.  ,  1295.56],
                      [    0.  ,   690.48,   942.17],
                      [    0.  ,     0.  ,     1.  ]])

        # zero distortion coefficients work well for this image
        D = np.array([0., 0., 0., 0.])

        # use Knew to scale the output
        Knew = K.copy()
        Knew[(0,1), (0,1)] = 0.4 * Knew[(0,1), (0,1)]

        img = cv2.imread('temp.jpg')
        img_undistorted = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew)
        cv2.imwrite('temp.jpg', img_undistorted)
        cv2.waitKey()
    
    