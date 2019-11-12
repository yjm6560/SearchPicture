#tesseract ocr
import pytesseract

import Launcher
import text.FindTextRegion as FindTextRegion
import cv2
import multiprocessing

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
        self.findtextregion = FindTextRegion.FindTextRegion()

    def single_ocr(self, img, send_end):
        string = pytesseract.image_to_string(img, lang='kor+eng')
        return string
#        send_end.send(string)

    def parallel_ocr(self, text_region_list, batch_size=8):
        '''
        #no batch
        for img in text_region_list:
            string = pytesseract.image_to_string(img, lang='eng+kor')
            result = result + string + '\n'
        '''

        #parallel ocr
        print(str(len(text_region_list)) + ' regions')
        result = ''
        for i in range(int(len(text_region_list)/batch_size) + 1):
            ret = None
            if i*batch_size == len(text_region_list):
                break
            elif (i+1)*batch_size > len(text_region_list):
                ret = text_region_list[i*batch_size:]
            else:
                ret = text_region_list[i*batch_size:(i+1)*batch_size]

            procs = []
            pipe_list = []
            for img in ret:
                recv_end, send_end = multiprocessing.Pipe(False)
                proc = multiprocessing.Process(target=self.single_ocr, args=(img,send_end))
                procs.append(proc)
                pipe_list.append(recv_end)
                proc.start()

            for proc in procs:
                proc.join()

            for x in pipe_list:
                result = result + x.recv()

        return result

    def findTextOnImage(self, image):
        #image는 cv2.imread()로 읽은 사진
        
        self.findtextregion.setImage(image)
        text_region_list = self.findtextregion.findTextRegion(3, 3, 15, 3, 3, 3, 1)
        result = self.parallel_ocr(text_region_list)

        return result


#text
'''
if __name__ == "__main__":
    a = cv2.imread('6.jpg')
    b = TesseractOCR()
    result = b.findTextOnImage(a)

    print('********result*********')
    print(result)
'''