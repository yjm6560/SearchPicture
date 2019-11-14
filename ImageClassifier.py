import cv2

#from HierarchyTree import HierarchyTree
import Launcher
from HierarchyTree import HierarchyTree
from Yolo import Yolo
import ImageGetter as GI
import text.TesseractOCR as TesseractOCR
import threading
import Logger
from Yolo.Yolo_cmd import Yolo_cmd

'''
ImageClassifier
    이미지 분류기
    기능
        1. 특정 directory 안에 있는 이미지 읽어오기
        2. 이미지 classify
'''
#TODO : 1. OCR 적용 2. batch 적용

class ImageClassifier(threading.Thread):

    def __init__(self, user_id):
        threading.Thread.__init__(self)
        self.imageGetter = GI.ImageGetter(user_id)
        self.fileList = self.imageGetter.getFileList()
        self.textAnalyzer = TesseractOCR.TesseractOCR()
#        self.objClassifier = Yolo.Yolo('Yolo\darknet\yolo9000\yolo9000.weights', 'Yolo\darknet\yolo9000\yolo9000_2.cfg','Yolo\darknet\yolo9000\9k.names')
        self.objClassifier = Yolo.Yolo('Yolo\yolov3.weights', 'Yolo\yolov3.cfg', 'Yolo\yolov3.txt')
        self.hierarchyTree = HierarchyTree.HierarchyTree("HierarchyTree\HierarchyTree.dat", "HierarchyTree/Imagenet.txt", "HierarchyTree/wnid2name.txt")
        self.hierarchyTree.makeHierarchyTree()
        self.Yolo_sub = Yolo_cmd('C:/Users\yjm6560\Desktop\yjm6560\CE\graduation_project\SearchPicture\Yolo\darknet\yolo9000\input.txt',
                                 'C:/Users\yjm6560\Desktop\yjm6560\CE\graduation_project\SearchPicture\Yolo\darknet/ret.txt')

    def readImages(self):
        imageList = []
        for i in self.fileList:
            imageList.append(cv2.imread(i))
        if Launcher.DEBUG:
            print(f'read {len(imageList)} images')
        return imageList

    #TODO: yolo batch operation만 적용된 상태. ocr 적용하면 바꿔줘야 함
    def classifyObjImagesByBatch(self, logger, batch_size=8):
        image_list = self.readImages()
        for i in range(int(len(self.fileList)/batch_size)+1):
           if i*batch_size == len(self.fileList):
               break
           elif (i+1)*batch_size > len(self.fileList):
               ret = self.objClassifier.detectObj_in_Images(image_list[i*batch_size :], len(self.fileList)-(i*batch_size))
           else:
               ret = self.objClassifier.detectObj_in_Images(image_list[i*batch_size : (i+1)*batch_size], batch_size)
           for j in range(len(ret)):
               order = i*batch_size + j
               if Launcher.DEBUG:
                   print(f'{order} : {ret[j]}')
                   print(f'\t{self.getRelatedClasses(ret[j])}')
               logger.insertNonTextyPhoto(order, self.fileList[order], self.getRelatedClasses(ret[j]))

    def classifyObjImages_sub(self, logger, batch_size=8):
        img_path_f = open(self.Yolo_sub.img_list, "w+")
        for img_path in self.fileList:
            img_path_f.write(img_path + "\n")
        self.Yolo_sub.writeDetectRet()
        ret = self.Yolo_sub.getObjList()
        for i in range(len(ret)):
            logger.insertNonTextyPhoto(i, ret[i][0], self.getRelatedClasses(ret[i][1]))

    def analyzeTextImages(self, logger, batch_size=8):
        image_list = self.readImages()
        for i in range(0, len(image_list)):
#            logger.insertTextyPhoto(i, self.fileList[i], self.textAnalyzer.single_ocr(image_list[i], "none"))
            logger.insertTextyPhoto(i, self.fileList[i], self.textAnalyzer.findTextOnImage(image_list[i]))

    def analyzeTextImagesByBatch(self, logger, batch_size=8):
        image_list = self.readImages()
        for i in range(int(len(self.fileList) / batch_size) + 1):
            if i * batch_size == len(self.fileList):
                break
            elif (i + 1) * batch_size > len(self.fileList):
                ret = self.textAnalyzer.findTextOnImage(image_list[i * batch_size:], len(self.fileList) - (i * batch_size))
            else:
                ret = self.textAnalyzer.findTextOnImage(image_list[i * batch_size: (i + 1) * batch_size], batch_size)
            for j in range(len(ret)):
                order = i * batch_size + j
                logger.insertTextyPhoto(order, self.fileList[order], [], ret[j])

    def classifyImages(self):
        # Not batch Operation
        image_list = self.readImages()
        tag_list = []
        for i in range(0, len(self.fileList)):
            tag_list.append((i, self.fileList[i], self.getRelatedClasses(self.objClassifier.detectObj_in_Image(image_list[i])), self.textAnalyzer.ocr([image_list[i]])))
            if Launcher.DEBUG:
                print(self.fileList[i],self.objClassifier.detectObj_in_Image(image_list[i]))
        return tag_list

    def getRelatedClasses(self, keywords):
        ret = []
        for key in keywords:
            try:
                ret += self.hierarchyTree.searchKeyword(key)
            except:
                continue
        ret = list(set(ret))

        return ret

if __name__ == "__main__":
    IC = ImageClassifier('easy')
#    result = IC.classifyImagesByBatch()
    result = IC.classifyImages()
    for dat in result:
        print(dat[2])
