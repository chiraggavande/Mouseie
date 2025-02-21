import cv2
import mediapipe as mp
import pyautogui as mouse

import pyautogui
res = pyautogui.size()

isCalibrated = False
curr_monitor = 0
direction = ""
CalibrationList = list()

def PointExist(curr_x, curr_y , calibrationObj):
    dist = (calibrationObj.nose_x - curr_x)**2 + (calibrationObj.nose_y - curr_y)**2
    if(dist <= 0.001):
        return True
    else:
        return False

class calibrationData:
    nose_x = 0
    nose_y = 0
    cursor = 0
    

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
mp_draw = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)
def getNose():
    ret,frame = cap.read()

    # Flip the frame horizontally for natural mirroring effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB (Mediapipe requires RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame with FaceMesh
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            nose = face_landmarks.landmark[1]
    return nose


#calibrate
if(not isCalibrated):                
    NO_OF_MONITORS = int(input("Please enter the no. of displays you have (including the main) :- "))
    for _ in range(NO_OF_MONITORS):
        __ = input(f"Please look in the display no. {_} and keep the cursor in the middle of the screen and press enter")
        temp = calibrationData()
        temp.nose_x = getNose().x
        temp.nose_y = getNose().y
        temp.cursor = pyautogui.position()

        CalibrationList.append(temp)
    isCalibrated = True

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for natural mirroring effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB (Mediapipe requires RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame with FaceMesh
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get landmark points
            height, width, _ = frame.shape
            left_eye = face_landmarks.landmark[33]   # Right eye in the image (mirrored)
            right_eye = face_landmarks.landmark[263] # Left eye in the image
            nose = face_landmarks.landmark[1]        # Nose tip

            # Convert normalized coordinates to pixel values
            left_eye_x = int(left_eye.x * width)
            right_eye_x = int(right_eye.x * width)
            nose_x = int(nose.x * width)

            left_eye_dist = nose.x - left_eye.x
            right_eye_dist = right_eye.x - nose.x

            look_factor = left_eye_dist/right_eye_dist

            #print(CalibrationList[0].nose)

            #print(f"left_eye_x:{left_eye_x} ,nose_x:{nose_x}, right_eye_x:{right_eye_x} , look_factor:{look_factor} ,direction:{direction}")

            # Determine the display

            for _ in CalibrationList:
                if(PointExist(nose.x,nose.y,_) and curr_monitor != CalibrationList.index(_)):

                    pyautogui.moveTo(_.cursor.x,_.cursor.y)
                    curr_monitor = CalibrationList.index(_)

            # # Determine head direction
            # #left
            # if look_factor < 1:
            #      if(direction == "Looking Right"):
            #         mouse.moveTo(res.width//2,res.height//2,duration=0.05)    
            #      direction = "Looking Left"
            # #right    
            # elif look_factor > 1:
            #     if(direction == "Looking Left"):
            #         mouse.moveTo(res.width//2 + 1920,res.height//2,duration=0.05)    
            #     direction = "Looking Right"
               
            # else:
            #     direction = "Looking Center"

            # Draw face landmarks
            mp_draw.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)
            
            # Display the direction text
            cv2.putText(frame, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Face Direction Detection", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
