import cv2
import mediapipe as mp
import pyautogui as mouse

import pyautogui
res = pyautogui.size()

direction = 'center'

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
mp_draw = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    x,y = pyautogui.position()
    print(x,y)
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

            # Determine head direction
            if nose_x > left_eye_x:
                if(direction == "Looking Left"):
                    mouse.moveTo(res.width//2,res.height//2,duration=0.05)
                direction = "Looking Right"
            elif nose_x < right_eye_x:
                if(direction == "Looking Right"):
                    mouse.moveTo(2800,500,duration=0.05)
                direction = "Looking Left"
            else:
                direction = "Looking Center"

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
