import cv2
import mediapipe as mp
import pyautogui
import time
import speech_recognition as sr
def control_cursor():
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark

            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))

                if id == 1:
                    screen_x = screen_w / frame_w * x
                    screen_y = screen_h / frame_h * y
                    pyautogui.moveTo(screen_x, screen_y)

            left = [landmarks[145], landmarks[159]]

            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h) 
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

            if (left[0].y - left[1].y) < 0.003:
                pyautogui.doubleClick()
                pyautogui.sleep(0.5)

        cv2.imshow('Eye Controlled Mouse', frame)  

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()


def control_voice():
    print("Say 'start!' to control the cursor with voice commands and say 'end' to terminate")

    while True:
        rk = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = rk.listen(source)

        try:
            command = rk.recognize_google(audio).lower()
            print("You said:", command)

            if command == "end":
                print("Voice command terminated")
                break

            if "open" in command:
                if "browser" in command:
                    pyautogui.press("win")
                    pyautogui.typewrite("chrome")
                    pyautogui.press("enter")
                elif "word" in command:
                    pyautogui.press("win")
                    pyautogui.typewrite("Word")
                    pyautogui.press("enter")
                elif "notepad" in command:
                    pyautogui.press("win")
                    pyautogui.typewrite("Notepad")
                    pyautogui.press("enter")
                elif "paint" in command:
                    pyautogui.press("win")
                    pyautogui.typewrite("Paint")
                    pyautogui.press("enter")
                elif "powerpoint" in command:
                    pyautogui.press("win")
                    pyautogui.typewrite("PowerPoint")
                    pyautogui.press("enter")
                elif "excel" in command:
                    pyautogui.press("win")
                    pyautogui.typewrite("Excel")
                    pyautogui.press("enter")

            elif "close" in command:    
                if "browser" in command:
                    pyautogui.hotkey("ctrl", "w")
                elif "word" in command:
                    pyautogui.hotkey("alt", "F4")
                elif "notepad" in command:
                    pyautogui.hotkey("alt", "F4")
                elif "paint" in command:
                    pyautogui.hotkey("alt", "F4")
                elif "powerpoint" in command:
                    pyautogui.hotkey("alt", "F4")
                elif "excel" in command:
                    pyautogui.hotkey("alt", "F4")

            elif any(direction in command for direction in ["up", "down", "left", "right"]):
                if "up" in command:
                    pyautogui.moveRel(0, -50, duration=0.25)
                elif "down" in command:
                    pyautogui.moveRel(0, 50, duration=0.25)
                elif "left" in command:
                    pyautogui.moveRel(-50, 0, duration=0.25)
                elif "right" in command:
                    pyautogui.moveRel(50, 0, duration=0.25)

            elif "scroll" in command:
                if "up" in command:
                    pyautogui.scroll(100)
                elif "down" in command:
                    pyautogui.scroll(-100)

            elif "double click" in command:
                pyautogui.doubleClick()

            elif "press" in command:
                pyautogui.press("enter")

            elif "switch" in command:
                control_cursor()

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


def control_hand():
    screen_width, screen_height = pyautogui.size()
    pyautogui.FAILSAFE = False
    mp_hands = mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )
    cap = cv2.VideoCapture(0)
    click_start_time = None

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[8]
                x, y = index_finger_tip.x, index_finger_tip.y
                cursor_x = int(x * screen_width)
                cursor_y = int(y * screen_height)
                pyautogui.moveTo(cursor_x, cursor_y)

                if click_start_time is None:
                    click_start_time = time.time()
                elif time.time() - click_start_time > 4:
                    pyautogui.click()
                    click_start_time = None

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    mp_hands.close()


def main():
    print("Please select a control method:")
    print("1. Voice Control")
    print("2. Retina Movement Control")
    print("3. Hands-free control for cursor movement")
    control_method = input()

    if control_method == "1":
        control_voice()
    elif control_method == "2":
        control_cursor()
    elif control_method == "3":
        control_hand()
    else:
        print("Invalid input, please try again.")


if __name__ == '__main__':
    main()
