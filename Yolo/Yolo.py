import cv2
import argparse
import numpy as np

import Launcher

'''
Yolo
    Object Detector
    생성
        yolov3.weights, yolov3.cfg, yolov3.txt 세 개의 경로를 인자로 넣어주면 됨
    기능
        1. 인자로 받은 이미지 classify
'''
#TODO : 1. OCR 적용 2. batch 적용

class Yolo:

    def __init__(self, weights, cfg, names):
        self.weights_file = weights
        self.config_file = cfg
        self.classes_file = names
        self.classes = []
        with open(self.classes_file, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

    def get_output_layers(self, net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers

    def draw_prediction(self, img, class_id, confidence, x, y, x_plus_w, y_plus_h):

        label = str(self.classes[class_id])
        COLORS = np.random.uniform(0, 255, size=(len(self.classes), 3))
        color = COLORS[class_id]

        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def detectObj_in_Image(self, image):
        net = cv2.dnn.readNet(self.weights_file, self.config_file)
        return self.classifyOneImage(net, image)

    def detectObj_in_Images(self, images, batch_size=8):
        net = cv2.dnn.readNetFromDarknet(self.config_file, self.weights_file)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        if batch_size == 1:
            return [self.classifyOneImage(net, images)]
        else:
            return self.classifyImages(net, images, batch_size)

    def classifyImages(self, net, images, batch_size=8):
        result_list = []
        scale = 0.00392
        blob = cv2.dnn.blobFromImages(images, scale, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(self.get_output_layers(net))
        for out in outs:
            for classified in out:
                class_list = []
                for detection in classified:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        if self.classes[class_id] not in class_list:
                            class_list.append(self.classes[class_id])
                result_list.append(class_list)
        return result_list[:batch_size]

    def classifyOneImage(self, net, image):
        scale = 0.00392
        class_list = []

        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)

        outs = net.forward(self.get_output_layers(net))

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    if class_id not in class_list:
                        class_list.append(self.classes[class_id])

        return class_list

def parser(self):
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help='path to input image')
    ap.add_argument('-c', '--config', required=True, help='path to yolo config file')
    ap.add_argument('-w', '--weights', required=True,help='path to yolo pre-trained weights')
    ap.add_argument('-cl', '--classes', required=True,help='path to text file containing class names')
    args = ap.parse_args()

    return args


if __name__ == "__main__":
    yolo = Yolo('yolov3.weights', 'yolov3.cfg', 'yolov3.txt')
#    yolo = Yolo('yolo-obj_final.weights', 'yolo-obj.cfg', 'myObj.names')
#    yolo = Yolo('darknet\yolo9000\yolo9000.weights', 'darknet\yolo9000\yolo9000.cfg', 'darknet\yolo9000\9k.names')
    print(yolo.detectObj_in_Image(cv2.imread('cat.jpg')))
