import cv2
import numpy as np
import pygame
import time

# audio
pygame.mixer.init()
alert_file = 'alert.wav'  # For object filling screen
motion_file = 'motion.wav'  # For motion detected
alert_sound = pygame.mixer.Sound(alert_file)
motion_sound = pygame.mixer.Sound(motion_file)

# open webcam
cap = cv2.VideoCapture(0)

# params
prev_frame = None
min_contour_area = 500 
high_speed_threshold = 12000 

color_variance_threshold = 700 

sound_played = False
motion_played = False
fill_start_time = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_frame is None:
        prev_frame = gray
        continue

    frame_diff = cv2.absdiff(prev_frame, gray)
    thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) < min_contour_area:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # non-trivial motion: over speed threshold
        if cv2.contourArea(contour) > 30:
            cv2.putText(frame, "Motion detected", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            if cv2.contourArea(contour) > high_speed_threshold:
                cv2.putText(frame, "High speed detected", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                motion_detected = True

    prev_frame = gray

    # see if (single color) object fills screen
    color_variance = np.var(frame)
    if color_variance < color_variance_threshold:
        if fill_start_time is None:
            fill_start_time = time.time()  
        elif time.time() - fill_start_time >= 1:  # check 1 second before playing sound
            if not sound_played:
                alert_sound.play()  
                sound_played = True  
        cv2.putText(frame, "Object filling screen", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        fill_start_time = None  # Reset the start time
        sound_played = False  

    if motion_detected:
        if not motion_played:
            motion_sound.play()  
            motion_played = True  
    else:
        motion_played = False  

    color_variance_text = f"Color-variance: {color_variance:.2f}"
    cv2.putText(frame, color_variance_text, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    cv2.imshow('Frame', frame)

    # break on 'x'
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
