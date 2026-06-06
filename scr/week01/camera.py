import cv2
import time

cap = cv2.VideoCapture(1)

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Рахуємо FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Малюємо текст на кадрі
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()