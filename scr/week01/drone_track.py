import sys
import time
import cv2
from ultralytics import YOLO

path = sys.argv[1]  # use path in terminal

cap = cv2.VideoCapture(path)
model = YOLO("yolov8n.pt")
# get params
cap_fps = cap.get(cv2.CAP_PROP_FPS)
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

vid_writer = cv2.VideoWriter("./test_record_001.mp4", cv2.VideoWriter_fourcc(*"mp4v"), cap_fps, (int(cap_width), int(cap_height)))

prev_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    # no signal -> exit
    if not ret:
        break

    res = model.track(frame, persist=True, tracker="bytetrack.yaml")
    objects = res[0].boxes

    for obj in objects:
        # frame params
        x1, y1, x2, y2 = obj.xyxy[0]
        obj_name = model.names[int(obj.cls)]
        obj_id = int(obj.id) if obj.id is not None else -1
        obj_name = obj_name + "#" + str(obj_id)
        # get box
        bbox = cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255,0), 1, 1)
        # set box
        cv2.putText(bbox, obj_name, (int(x1) - 10, int(y1) - 10), 1, 0.999, (11, 255, 11), 1, 1)
        

    # fps num
    fps = 1 / (time.time() - prev_time)
    prev_time = time.time()

    cv2.putText(frame, str(round(fps, 1)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # output video
    cv2.imshow("WINDOW", frame)

    # exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # write file
    vid_writer.write(frame)

# free writer + cap
vid_writer.release()
cap.release()