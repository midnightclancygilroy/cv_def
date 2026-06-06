import cv2
import numpy as np

MIN_AREA       = 800     # px², ігноруємо дрібні контури (листя, шум)

def draw_detections(frame: np.ndarray, mask: np.ndarray) -> int:
    """Знаходить контури на масці, малює bbox. Повертає кількість детекцій."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    count = 0
    for cnt in contours:
        if cv2.contourArea(cnt) < MIN_AREA:
            continue  # дрібниця — пропускаємо
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "MOTION", (x, y - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)
        count += 1
    return count

def main():
    if cap.isOpened():

        backSub = cv2. createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

        frame_count = 0
        warmup = True
        
        while True:

            ret, frame = cap.read()

            frame_count +=1
            if frame_count > 250:
                warmup = False

            if not ret:
                break
 
            
            
            fg_mask = backSub.apply(frame)

            _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)   
            fg_mask = cv2.dilate(fg_mask, None, iterations=2)


            if warmup:
                cv2.putText(frame, "Studying", (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

            if not warmup:
                draw_detections(frame, fg_mask)

            cv2.imshow("window", frame)
            cv2.imshow("111", fg_mask)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
    else:
        raise RuntimeError("Камеру не знайдено")    
    cap.release()
    cv2.destroyAllWindows()

cap = cv2.VideoCapture(1)

main()
# cap = cv2.VideoCapture(1)
# if not cap.isOpened():
#     raise RuntimeError("Камеру не знайдено")

# cap.release()