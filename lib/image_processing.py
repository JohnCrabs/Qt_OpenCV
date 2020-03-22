import cv2
import numpy as np

class ImageProcessing:
    def __init__(self):
        self.light = 0
        self.light_rgb = [0, 0, 0]

        self.contrast = 1.0
        self.contrast_rgb = [1.0, 1.0, 1.0]

    def set_light(self, light: int):
        self.light = light

    def set_contrast(self, contrast: float):
        self.contrast = contrast

    def set_light_contrast(self, light: int, contrast: float):
        self.light = light
        self.contrast = contrast

    def set_light_contrast_rgb(self, light_r, light_g, light_b, contrast_r, contrast_g, contrast_b):
        self.light_rgb = [light_r, light_g, light_b]
        self.contrast_rgb = [contrast_r, contrast_g, contrast_b]

    def set_default_light_contrast(self):
        self.light = 0
        self.contrast = 1.0

    def set_default_light_contrast_rgb(self):
        self.light_rgb = [0, 0, 0]
        self.contrast_rgb = [1.0, 1.0, 1.0]

    def compute_light_contrast(self, img):
        #img_tmp = cv2.convertScaleAbs(img, alpha=self.contrast, beta=self.light)
        img_tmp = cv2.addWeighted(img, self.contrast, img, 0, self.light)
        #print(img_tmp)
        return img_tmp

    def compute_light_contrast_per_channel(self, img):
        img_r, img_g, img_b = cv2.split(img)
        img_r_tmp = cv2.addWeighted(img_r, self.contrast_rgb[0], img_r, 0, self.light_rgb[0])
        img_g_tmp = cv2.addWeighted(img_g, self.contrast_rgb[1], img_g, 0, self.light_rgb[1])
        img_b_tmp = cv2.addWeighted(img_b, self.contrast_rgb[2], img_b, 0, self.light_rgb[2])

        img_tmp = cv2.merge((img_r_tmp, img_g_tmp, img_b_tmp))

        return img_tmp
