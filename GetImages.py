import numpy as np
import cv2
import sys
import os

class imageManager:

    def __init__(self, path):
        self.path_dir = path

    def setDirPath(self, path):
        path_dir = path

    def getDirPath(self):
        return self.path_dir

    def getFileList(self):
        file_path_list = []
        file_name_list = os.listdir(self.path_dir)
        for file_name in file_name_list:
            file_path_list.append(self.path_dir + '\\' + file_name)
        return file_path_list


if __name__ == "__main__":
    imageGetter = imageManager('C:\\Users\yjm75\\OneDrive\문서\임종민\졸프\yolo\\object-detection-opencv\\image')
    print(imageGetter.getDirPath())
    print(imageGetter.getFileList())