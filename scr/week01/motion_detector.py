import cv2
import numpy as np
import time

# --- Параметри (легко тюнити без перезапуску) ---
THRESHOLD      = 25      # чутливість: нижче = більше шуму ловить
MIN_AREA       = 800     # px², ігноруємо дрібні контури (листя, шум)
BLUR_KERNEL    = (21, 21) # розмиття перед diff — давить піксельний шум
DILATE_ITERS   = 2       # розширення маски — склеює розриви між зонами
SHOW_MASK      = False   # True → показує бінарну маску в окремому вікні

def preprocess(frame: np.ndarray) -> np.ndarray:
    """Grayscale + Gaussian blur. Blur критичний — без нього threshold ловить шум матриці."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(gray, BLUR_KERNEL, 0)

def get_motion_mask(prev: np.ndarray, curr: np.ndarray) -> np.ndarray:
    """Бінарна маска руху між двома preprocessed кадрами."""
    diff   = cv2.absdiff(prev, curr)
    _, mask = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)
    # Dilate: невеликі прогалини між рухомими пікселями зникають
    mask   = cv2.dilate(mask, None, iterations=DILATE_ITERS)
    return mask

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

def main() -> None:
    global SHOW_MASK
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        raise RuntimeError("Камеру не знайдено — перевір індекс у VideoCapture(0)")

    # Перший кадр — ще нема "попереднього", тому читаємо заздалегідь
    ret, frame = cap.read()
    if not ret:
        cap.release()
        raise RuntimeError("Не вдалось прочитати перший кадр")

    prev_frame = preprocess(frame)

    fps_timer  = time.time()
    frame_count = 0

    print("Motion Detector запущено. Натисни 'q' для виходу, 'm' — toggle маски.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_frame = preprocess(frame)
        mask       = get_motion_mask(prev_frame, curr_frame)
        detections = draw_detections(frame, mask)

        # FPS
        frame_count += 1
        elapsed = time.time() - fps_timer
        if elapsed >= 1.0:
            fps = frame_count / elapsed
            frame_count, fps_timer = 0, time.time()
        else:
            fps = frame_count / max(elapsed, 1e-6)

        # HUD
        status = f"FPS: {fps:.1f}  |  Detections: {detections}"
        color  = (0, 255, 0) if detections else (120, 120, 120)
        cv2.putText(frame, status, (10, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("Motion Detector", frame)
        if SHOW_MASK:
            cv2.imshow("Mask", mask)

        # Зберігаємо поточний як "попередній" для наступної ітерації
        prev_frame = curr_frame

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('m'):
            SHOW_MASK = not SHOW_MASK  # toggle маски у рантаймі

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()