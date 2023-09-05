# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
min_confidence = 0.5
label_cnt = 0 
fire =0

inter =0

model_file = '/home/swcon/darknet/weights/yolov4-tiny_last.weights'
config_file = '/home/swcon/darknet/cfg/yolov4-tiny.cfg'
net = cv2.dnn.readNet(model_file, config_file)


net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

classes = []
class_ids = []
with open("/home/swcon/darknet/obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[int(i) - 1] for i in net.getUnconnectedOutLayers()]

colors = np.random.uniform(0, 255, size=(len(classes)*2000, 3))

cap = cv2.VideoCapture(0, int(cv2.CAP_V4L))
if not cap.isOpened():
    print('--(!)Error opening video capture')
    exit(0)

def detectAndDisplay(frame):
    global inter
    start_time = time.time()

    img = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA)
    height, width, channels = img.shape

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)
    

    global label_cnt
    confidences = []
    boxes = []
    positions = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > min_confidence:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                positions.append((center_x, center_y)) # 객체의 중심 좌표를 positions 리스트에 추가

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4)
    font = cv2.FONT_HERSHEY_DUPLEX

    for i in indexes:
        i = i.item()
        x, y, w, h = boxes[i]
        label = "{}: {:.2f}".format(classes[class_ids[i]], confidences[i]*100)
        if classes[class_ids[i]] in ['matchesfire', 'bonfire']:
            label_cnt += 1

        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y - 5), font, 1, color, 1)




   # cv2.imshow("FIre detection", img)
    if inter ==0:
        print('Fire detection started.')
        inter +=1
    return positions

def detect_fire():
     
    global label_cnt
     
    x=0
    y=0
    
    while True:
        ret, frame = cap.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        
        positions = detectAndDisplay(frame)

        if ser.in_waiting > 0  :
            input_data = ser.readline().decode('utf-8').rstrip()
            if input_data=='fire' and  label_cnt>20 and  len(positions) > 0:
                
                
                x, y = positions[0]
                ser.write(b'fire_detected)
                label_cnt =0
                break
            

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    ser.close()
    cv2.destroyAllWindows()
    return  x,y
        

if __name__ == '__main__': 
   
    x, y = detect_fire()
    print('done')
    # Rest of your code...


        

