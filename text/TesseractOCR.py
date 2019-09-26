#tesseract ocr
import pytesseract

'''
class는 이미지가 저장된 경로와 이미지의 텍스트 부분이 잘린 조각 이미지들(list)이 넘어오면
각 조각 이미지들 내의 텍스트를 인식하고 이를 하나의 string으로 합친 후 database에 저장하도록 합니다

TODO
database에 저장하는 부분 어떻게 할지
test 필요
'''

class TesseractOCR:
    def __init__(self, imagepath, images):
        #images는 numpy.ndarray들의 list여야한다
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract' #tesseract가 저장된 경로 입력
        self.imagepath = imagepath
        self.images = images

    def ocr(self):
        result = ''
        for img in self.images:
            string = pytesseract.image_to_string(img, lang='kor')
            result = result + string + '\n'

        return result