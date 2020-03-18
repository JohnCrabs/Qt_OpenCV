import os
import cv2


class Image:
    def __init__(self):
        self.src = ""
        self.folder = ""
        self.name = ""
        self.suffix = ""
        self.export = ""
        self.id = 0
        self.width = 0
        self.height = 0
        self.bands = 0
        self.img = None
        self.is_Open = False

    def print_img_info(self):
        print("Full_Path =", self.src)
        print("Folder =", self.folder)
        print("Name =", self.name)
        print("Suffix =", self.suffix)
        print("Width =", self.width)
        print("Height =", self.height)
        print("Color_Bands =", self.bands)

    def open_image_from(self, src, img_id=0, mem_alloc=True):
        if os.path.isfile(src):  # Check if file path exists
            # Set paths
            self.src = src
            self.folder = os.path.dirname(self.src)
            name_tmp = os.path.basename(self.src)
            self.name = os.path.splitext(name_tmp)[0]
            self.suffix = os.path.splitext(name_tmp)[1]
            # Set image size
            self.id = img_id
            img_tmp = cv2.imread(self.src)
            size = img_tmp.shape
            self.width = size[1]
            self.height = size[0]
            self.bands = 1
            if len(size) == 3:
                self.bands = size[2]
            # Check allocation. For memory usage apps, mem_alloc needs to be False.
            if mem_alloc:
                self.img = img_tmp
            self.is_Open = mem_alloc

            return True
        return False

    def alloc_image(self):
        if self.is_Open is False:
            self.img = cv2.imread(self.src)
            self.is_Open = True

    def dealloc_image(self):
        if self.is_Open:
            self.img = None
            self.is_Open = False

    def save_image(self, o_src):
        if self.is_Open:
            self.export = o_src
            cv2.imwrite(self.src, self.img)
            return True
        return False
