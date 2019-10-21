import cv2

#from HierarchyTree import HierarchyTree
from HierarchyTree import HierarchyTree
from Yolo import Yolo
import ImageGetter as GI
import text.TesseractOCR as TesseractOCR

'''
ImageClassifier
    이미지 분류기
    기능
        1. 특정 directory 안에 있는 이미지 읽어오기
        2. 이미지 classify
'''
#TODO : 1. OCR 적용 2. batch 적용

class ImageClassifier:

    def __init__(self, user_id):
        self.imageGetter = GI.ImageGetter(user_id)
        self.fileList = self.imageGetter.getFileList()
        self.textAnalyzer = TesseractOCR.TesseractOCR()
        self.objClassifier = Yolo.Yolo('Yolo\yolov3.weights', 'Yolo\yolov3.cfg', 'Yolo\yolov3.txt')
        self.hierarchyTree = HierarchyTree.HierarchyTree("HierarchyTree\HierarchyTree.dat", "HierarchyTree/Imagenet.txt", "HierarchyTree/wnid2name.txt")
        self.hierarchyTree.makeHierarchyTree()

    def readImages(self):
        imageList = []
        for i in self.fileList:
            imageList.append(cv2.imread(i))

        return imageList

    def imagesClassify(self):
        image_list = self.readImages()
        tag_list = []
        for i in range(0, len(self.fileList)):
            tag_list.append((i, self.fileList[i], self.getRelatedClasses(self.objClassifier.detectObj(image_list[i])), self.textAnalyzer.findTextOnImage(image_list[i])))

        return tag_list

    def getRelatedClasses(self, keywords):
        ret = []
        for key in keywords:
            ret += self.hierarchyTree.searchKeyword(key)
        ret = list(set(ret))

        return ret

if __name__ == "__main__":
    IC = ImageClassifier('yjm6560')
    result = IC.imagesClassify()
    for dat in result:
        print(dat[2])
