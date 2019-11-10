#detect text region in image by OpenCV
import cv2
import numpy as np
from PIL import Image
import os
import copy

'''
*Text Region 추출 과정
1. color image를 grayscale 이미지로 변환
2. Adpative Threshold를 적용해서 잡영 제거
3. Morph close로 경계 강화
4. Long line Remove로 글씨 추출에 방해가 되는 요소 제거
5. find contours로 텍스트 영역 찾기

TODO
*조정이 필요한 parameter들
adaptiveThreshold() : block_size, subtract_val
morphClose() : widht, height, iter
*일정 크기 이하의 박스를 버릴지 냅둘지도 정해야됨
*findcontour함수에 rectangle 친걸 잘라서 넘길지 어떻게 할지..
'''

class FindTextRegion:
    def __init__(self, image):
        self.original_image = image

    def changeImageSize(self):
        height, width, channel = self.original_image.shape
        self.new_width = 720
        self.new_height = int((self.new_width * 720) / width)
        if width >= self.new_width:
            self.resizing_image = cv2.resize(self.original_image, dsize=(self.new_width, self.new_height), interpolation=cv2.INTER_AREA)
        else:
            self.resizing_image = cv2.resize(self.original_image, dsize=(self.new_width, self.new_height), interpolation=cv2.INTER_CUBIC)

    def imageConverting(self):
        gray_image = cv2.cvtColor(self.resizing_image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def morphGradient(self, gray_image, width=3, height=3):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width, height))
        morph_image = cv2.morphologyEx(gray_image, cv2.MORPH_GRADIENT, kernel)
        return morph_image

    def adaptiveThreshold(self, morph_image, block_size = 15, subtract_val = 3):
        #block_size : 픽셀에 적용할 threshold 값을 계산하기 위한 블럭 크기. 적용될 픽셀이 블럭의 중심이 됨. 따라서 홀수만 가능
        #subtract_val : 보정 상수
        adaptive_gaussian_image = cv2.adaptiveThreshold(morph_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, subtract_val)
        return adaptive_gaussian_image

    def morphClose(self, adaptive_gaussian_image, width = 3, height = 3, it = 1):
        #width와 height는 커널의 사이즈
        #커널 창으로 이미지 전체를 훑으면서 커널창에 들어온 matrix 값들을 변경한다
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width, height))

        #1. cv2.morphologyEX()를 사용하거나 2. cv2.dilate()하고 cv2.erode()하는 방법도 있음
        #1번 방법
        #self.closing_image = cv2.morphologyEx(adaptive_gaussian_image, cv2.MORPH_CLOSE, kernel)

        #2번 방법
        dilation = cv2.dilate(adaptive_gaussian_image, kernel, iterations=it)
        erosion = cv2.erode(dilation, kernel, iterations=it)

        return erosion

    def longLineRemove(self, closing_image, threshold = 100, min_line_length = 80, max_line_gap = 5):
        #min_line_length : 선으로 판단되는 최소 길이
        #max_line_gap : 이 값 이상 떨어져 있으면 별개의 직선으로 판단
        lines = cv2.HoughLinesP(closing_image, 1, np.pi/180, threshold, min_line_length, max_line_gap)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(closing_image, (x1, y1), (x2, y2), (0,255,0), 2)
        
        return closing_image

    def findContours(self, image):
        contours, b = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        min_w = 40
        min_h = 10

        rect = []
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            r = [x,y,w,h]
            if r not in rect:
                if (x==0 and y==0) or abs(w-self.new_width)<=5 or abs(h-self.new_height)<=5:
                    continue
                if w >= min_w and h >= min_h:
                    rect.append(r)

        rect1 = copy.deepcopy(rect)
        rect2 = copy.deepcopy(rect)

        #겹치는거 삭제
        for r1 in rect1:
            x1,y1,w1,h1 = r1
            for r2 in rect2:
                x2,y2,w2,h2 = r2
                if (x1>x2 and y1>y2) and (((x1+w1)<(x2+w2)) and ((y1+h1)<(y2+h2))):
                    if r1 in rect:
                        rect.remove(r1)

        #가로 합치기
        rect1 = copy.deepcopy(rect)
        rect2 = copy.deepcopy(rect)
        end = False
        while not end:
            end = True
            for r1 in rect1:
                x1,y1,w1,h1 = r1
                for r2 in rect2:
                    x2,y2,w2,h2 = r2
                    if abs((x1 + w1) - x2) < 10 and abs(y1- y2) < 10 and abs(h1 - h2) < 10:
                        new_x = x1
                        new_y = min([y1,y2])
                        new_w = x2 + w2 - x1
                        new_h = max([y1+h1, y2+h2]) - new_y
                        rect.remove(r1)
                        rect.remove(r2)
                        rect.append([new_x,new_y,new_w, new_h])

                        rect1 = copy.deepcopy(rect)
                        rect2 = copy.deepcopy(rect)

                        end = False
                        break

                if not end:
                    break

        #세로 합치기
        rect1 = copy.deepcopy(rect)
        rect2 = copy.deepcopy(rect)
        end = False
        while not end:
            end = True
            for r1 in rect1:
                x1,y1,w1,h1 = r1
                for r2 in rect2:
                    x2,y2,w2,h2 = r2
                    if abs((y1+h1) - y2) < 10 and abs(x1 - x2) < 10:
                        new_x = min([x1,x2])
                        new_y = y1
                        new_w = max([x1+w1, x2+w2]) - new_x
                        new_h = y2 + h2 - y1
                        rect.remove(r1)
                        rect.remove(r2)
                        rect.append([new_x,new_y,new_w,new_h])

                        rect1 = copy.deepcopy(rect)
                        rect2 = copy.deepcopy(rect)

                        end = False
                        break

                if not end:
                    break

        imagelist = []
        ori_image = Image.fromarray(self.resizing_image)
        for contour in rect:
            x,y,w,h = contour
            area = (x,y,x+w,y+h)
            croppend_image = ori_image.crop(area)
            imagelist.append(croppend_image)

            a = cv2.rectangle(self.resizing_image, (x,y), (x+w,y+h), (0,255,0), 2)
        
        Image.fromarray(self.resizing_image, mode='RGB').save('x.jpg')


        '''
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            #r = cv2.rectangle(self.resizing_image, (x,y), (x+w, y+h), (0,255,0), 2)
            area = (x, y, x + w, y + h)
            cropped_img = ori_image.crop(area)
            imagelist.append(cropped_img)

            #cropped_img.show()
        '''
        return imagelist
    
    def findTextRegion(self, g_width, g_height, block_size, subtract_val, c_width, c_height, c_iter):
        #change image size -> grayscale -> morph gradient -> adaptive gaussian threshold -> morph close -> find contour
        self.changeImageSize()
        gray_image = self.imageConverting()
        morph_image = self.morphGradient(gray_image, g_width, g_height)
        adaptive_gaussian_image = self.adaptiveThreshold(morph_image, block_size, subtract_val)
        closing_image = self.morphClose(adaptive_gaussian_image, c_width, c_height, c_iter)
        #longlineremove
        imagelist = self.findContours(closing_image)

        return imagelist


#사용 예시
'''
if __name__ == '__main__':
    path = os.path.join('1.jpg')

    img = cv2.imread(path)
    f = FindTextRegion(img)

    f.changeImageSize()

    gray_image = f.imageConverting()
    Image.fromarray(gray_image).save('y1.jpg')

    morph_image = f.morphGradient(gray_image)
    Image.fromarray(morph_image).save('y2.jpg')

    adaptive_gaussian_image = f.adaptiveThreshold(morph_image)
    Image.fromarray(adaptive_gaussian_image).save('y3.jpg')

    closing_image = f.morphClose(adaptive_gaussian_image)
    Image.fromarray(closing_image).save('y4.jpg')

    result = f.findContours(closing_image)
    print(result)
    #Image.fromarray(result).save('y4.jpg')
    '''