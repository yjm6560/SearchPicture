import numpy as np
import cv2
import sys
import os
from FilePath import FilePathGetter
'''
ImageGetter
    디렉토리 내의 이미지 경로들을 가져오는 클래스
'''

class ImageGetter:

    def __init__(self, user_id):
        self.path_dir = FilePathGetter.getImageDirPath() + "\\" + user_id

    def setDirPath(self, path):
        self.path_dir = path

    def getDirPath(self):
        return self.path_dir

    def getFileList(self):
        file_name_list = os.listdir(self.path_dir)
        return [self.path_dir + '\\' + file_name for file_name in file_name_list if ".jpg" in file_name or ".png" in file_name]


if __name__ == "__main__":
    imageGetter = ImageGetter('yjm6560')
    print(imageGetter.getDirPath())
    print(imageGetter.getFileList())