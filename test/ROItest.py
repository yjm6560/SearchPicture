#this code for testing(ROI)
import cv2
import numpy as numpy
from PIL import Image
import os
import copy
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
files = os.listdir('./')
test_no = 25
new_width = 720
kernel1_size = 3
block_size = 15
subtract = 3
kernel2_size = 3
it = 1
min_w = 40
min_h = 10

for f in files:
    print('*****' + f + ' start*****')
    #path = os.path.join(os.getcwd(), 'images', f)
    img = cv2.imread(f)
    image_name = f.split('.')[0]

    #크기 보정하기
    height, width, channel = img.shape
    new_height = int((height * new_width)/width) 
    resizing_image = cv2.resize(img, dsize=(new_width, new_height), interpolation=cv2.INTER_AREA)

    #grayscale로 변환
    gray_image = cv2.cvtColor(resizing_image, cv2.COLOR_BGR2GRAY)

    #morph gradient
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel1_size, kernel1_size))
    morph_image = cv2.morphologyEx(gray_image, cv2.MORPH_GRADIENT, kernel1)

    #adaptive gaussian threshold
    adaptive_gaussian_image = cv2.adaptiveThreshold(morph_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, subtract)
    
    #morph close
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel2_size, kernel2_size))
    dilation = cv2.dilate(adaptive_gaussian_image, kernel2, iterations=it)
    erosion = cv2.erode(dilation, kernel2, iterations=it)

    #find contour
    contours, b = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #contour처리하기
    rect_list = []
    new_rect = []
    rrect = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        r = [x,y,w,h]
        if r not in rrect:
            '''
            if abs(w-new_width) < 10 and abs(h-new_height) < 10:
                print('continue')
                print(str(x) + ' ' + str(y) + str(w) + str(h))
                print(str(new_width) + ' ' + str(new_height))
                #21번에서 수정
                continue
            '''
            if (x==0 and y==0) or abs(w-new_width) <= 5 or abs(h-new_height) <= 5:
                continue
            
            if w >= min_w and h >= min_h:
                rect_list.append([x,y,w,h])
                new_rect.append([x,y,w,h])
                rrect.append([x,y,w,h])
    
    '''
    #1번 알고리즘
    for r1 in rect_list:
        x1,y1,w1,h1 = r1
        for r2 in new_rect:
            x2,y2,w2,h2 = r2
            if ((x2-x1)>0 and (x2-x1)<=20) or ((y2-y1)>0 and (y2-y1)<=20):
                if w1<w2 and h1<h2:
                    print(r1)
                    if r1 in rrect:
                        rrect.remove(r1)
                        print('remove')
    '''
    
    #2번 알고리즘
    for r1 in rect_list:
        x1,y1,w1,h1 = r1
        for r2 in new_rect:
            x2,y2,w2,h2 = r2
            if (x1>x2 and y1>y2) and (((x1+w1)<(x2+w2)) and ((y1+h1)<(y2+h2))):
                if r1 in rrect:
                    rrect.remove(r1)
    '''
    #5번알고리즘
    for r1 in rect_list:
        x1,y1,w1,h1 = r1
        for r2 in new_rect:
            x2,y2,w2,h2 = r2
            if (abs(x1-x2) < 10 and (abs(y1-y2) < 10 or abs(y1+h1 - (y2+h2)) < 10)) or (abs(x1+w1-(x2+w2))<10 and (abs(y1-y2)<10 or abs(y1+h1 - (y2+h2))<10)):
                if r1 in rrect:
                    rrect.remove(r1)
    '''
    #4번 알고리즘 가로 합치기
    rrects1 = copy.deepcopy(rrect)
    rrects2 = copy.deepcopy(rrect)
    merge = copy.deepcopy(rrect)
    end = False
    while not end:
        end = True
        for rect1 in rrects1:
            x1,y1,w1,h1 = rect1
            for rect2 in rrects2:
                x2,y2,w2,h2 = rect2
                if abs((x1 + w1) - x2) < 10 and abs(y1- y2) < 10 and abs(h1 - h2) < 10:
                    new_x = x1
                    new_y = min([y1,y2])
                    new_w = x2 + w2 - x1
                    new_h = max([y1+h1, y2+h2]) - new_y
                    merge.remove(rect1)
                    merge.remove(rect2)
                    merge.append([new_x,new_y,new_w,new_h])

                    rrects1 = copy.deepcopy(merge)
                    rrects2 = copy.deepcopy(merge)

                    end = False
                    break

            if not end:
                break

    
    #3번 알고리즘 세로 합치기
    rects1 = copy.deepcopy(merge)
    rects2 = copy.deepcopy(merge)
    final = copy.deepcopy(merge)

    end = False
    while not end:
        end = True
        for rect1 in rects1:
            x1,y1,w1,h1 = rect1
            for rect2 in rects2:
                x2,y2,w2,h2 = rect2
                if abs((y1+h1) - y2) < 10 and abs(x1 - x2) < 10:
                    new_x = min([x1,x2])
                    new_y = y1
                    new_w = max([x1+w1, x2+w2]) - new_x
                    new_h = y2 + h2 - y1
                    final.remove(rect1)
                    final.remove(rect2)
                    final.append([new_x, new_y, new_w, new_h])

                    rects1 = copy.deepcopy(final)
                    rects2 = copy.deepcopy(final)

                    end = False
                    break

            if not end:
                break

    '''
    for rect1 in rects1:
        x1,y1,w1,h1 = rect1
        for rect2 in rects2:
            x2,y2,w2,h2 = rect2
            if abs((y1+h1) - y2) < 10 and abs(x1 - x2) < 10:
                if rect1 in final:
                    final.remove(rect1)
                if rect2 in final:
                    final.remove(rect2)
                new_h = y2 + h2 - y1
                new_w = max([x1+w1, x2+w2]) - x1
                final.append([x1,y1,new_w,new_h])
    '''
    '''
    #6번 알고리즘
    final1 = copy.deepcopy(final)
    final2 = copy.deepcopy(final)

    for r1 in final1:
        x1,y1,w1,h1 = r1
        for r2 in final2:
            x2,y2,w2,h2 = r2

            if w1<w2 and h1<h2:
                if abs(x1-x2) <= 10:
                    if abs(y1-y2) <= 10 or abs((y1+h1)-(y2-h2)) <= 10:
                        if r1 in final:
                            final.remove(r1)
                elif abs((x1+w1)-(x2+w2)) < 10:
                    if abs(y1-y2) <= 10 or abs((y1+h1)-(y2-h2)) <= 10:
                        if r1 in final:
                            final.remove(r1)
    '''



    '''
    #2번 알고리즘
    final1 = copy.deepcopy(final)
    final2 = copy.deepcopy(final)

    for r1 in final1:
        x1,y1,w1,h1 = r1
        for r2 in final2:
            x2,y2,w2,h2 = r2
            if (x1>x2 and y1>y2) and (((x1+w1)<(x2+w2)) and ((y1+h1)<(y2+h2))):
                if r1 in final:
                    final.remove(r1)
    '''
    imagelist = []
    ori_image = Image.fromarray(resizing_image, mode='RGB')

    for rect in final:
        x,y,w,h = rect
        a = cv2.rectangle(resizing_image, (x,y), (x+w,y+h), (0,255,0), 2)
        area = (x,y,x+w,y+h)
        cropped_image = ori_image.crop(area)
        imagelist.append(cropped_image)
    '''
    #tesseract
    result = ''
    i = 0
    for img in imagelist:
        i = i + 1
        string = pytesseract.image_to_string(img, lang='kor')
        result = '#' + str(i) + ' ' + result + string + '\n'

    print(result)
    '''
    '''
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)

        if w >= min_w and h >= min_h:
            a = cv2.rectangle(resizing_image, (x,y), (x+w,y+h), (0,255,0), 2)
    '''

    #이미지 저장
    Image.fromarray(resizing_image, mode='RGB').save(image_name + '_' + str(test_no) + '.jpg')

    print('*****' + f + ' end*****')