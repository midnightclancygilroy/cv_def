import torch
import cv2
import time

from ultralytics import YOLO


prev_time = time.time()
model = YOLO("yolov8n.pt")



cap = cv2.VideoCapture(1)

while cap.isOpened():
    
    ret, frame = cap.read()

    results = model(frame, verbose=False)
    annotated = results[0].plot()

    for box in results[0].boxes:
        class_name = model.names[int(box.cls)]  # назва класу
        confidence = box.conf                   # впевненість
        coordinates = box.xyxy                   # координати
        
        if confidence > 0.5:
            print(class_name, confidence, coordinates)


    if not ret:
        break

    fps = 1/(time.time()-prev_time)    
    prev_time = time.time()

    cv2.putText(annotated, str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("WINDOW", annotated)
                
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    #print("ok")
else:
    print("not ok")