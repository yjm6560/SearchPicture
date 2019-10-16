#tesseract ocr
import pytesseract

import Launcher
import text.FindTextRegion as FindTextRegion
import cv2

'''
class는 이미지가 저장된 경로와 이미지의 텍스트 부분이 잘린 조각 이미지들(list)이 넘어오면
각 조각 이미지들 내의 텍스트를 인식하고 이를 하나의 string으로 합친 후 database에 저장하도록 합니다

TODO
database에 저장하는 부분 어떻게 할지
test 필요
'''

class TesseractOCR:
    def __init__(self):
        #images는 numpy.ndarray들의 list여야한다
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract' #tesseract가 저장된 경로 입력

    def ocr(self, text_region_list):
        result = ''
        for img in text_region_list:
            string = pytesseract.image_to_string(img, lang='eng+kor')
            result = result + string + '\n'

        return result

    def findTextOnImage(self, image):
        #image는 cv2.imread()로 읽은 사진

        if Launcher.DEBUG:
            return self.ocr([image])
        findtextregion = FindTextRegion.FindTextRegion(image)
        text_region_list = findtextregion.findTextRegion(5, 5, 15, 3, 5, 5, 1)
        text = self.ocr(text_region_list)
        return text


#text
'''
if __name__ == "__main__":
    a = cv2.imread('4.jpg')
    b = TesseractOCR()
    result = b.findTextOnImage(a)

    print(result)
'''