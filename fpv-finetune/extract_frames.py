import sys
import cv2

path = sys.argv[1]

cap = cv2.VideoCapture(path)

video_fps = cap.get(cv2.CAP_PROP_FPS)
video_frames_cnt = cap.get(cv2.CAP_PROP_FRAME_COUNT)
video_seconds_cnt = video_frames_cnt / video_fps

print(video_fps, video_frames_cnt, video_seconds_cnt)

frame_index = 0

while True:

    success, frame = cap.read()
    if not success:
        break

    if frame_index % 15 == 0:
        cv2.imwrite(f"frames/video002_{frame_index}.jpg", frame)

    frame_index += 1

    if frame_index > video_frames_cnt:
        break

cap.release()
