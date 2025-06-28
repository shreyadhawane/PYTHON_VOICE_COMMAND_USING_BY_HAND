import cv2
import mediapipe as mp
import pygame

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize Mediapipe Hands.
hands = mp_hands.Hands(static_image_mode= False,
                       max_num_hands=2,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

# Initial pygame mixer
pygame.mixer.init()

# Open Webcam
cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4

last_alert = None

def count_fingers(hand_landmarks):
    fingers = []
    # Thumb
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    # other fingers
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)

def play_sound(file):
    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing sound {e}")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 2)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_up = count_fingers(hand_landmarks)
            cv2.putText(frame, f'Fingers up: {fingers_up}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(f'Fingers up: {fingers_up}' , end='\r')

            if fingers_up == 1 and last_alert != 1:
                play_sound('alert1.mp3')
                last_alert = 1
            elif fingers_up == 2 and last_alert != 2:
                play_sound('alert2.mp3')
                last_alert = 2
            elif fingers_up == 3 and last_alert != 3:
                play_sound('alert3.mp3')
                last_alert = 3
            elif fingers_up not in [2,1,3]:
                last_alert = None

    cv2.imshow('HGand Gesture', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

cap.release()