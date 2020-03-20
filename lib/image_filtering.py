import cv2


class Filters:
    def __init__(self):
        self.kernel = []

    def set_kernel(self, kernel):
        self.kernel = kernel
    
    def custom(self, cv_mat):
        img = cv2.filter2D(cv_mat, -1, self.kernel)

    def gaussian(self, cv_mat):
        pass

    def laplace(self, cv_mat):
        pass

    def sobel(self, cv_mat):
        pass
