# import necessary packages
from time import sleep
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model


# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

#gesture recognizer model
model = load_model('app\mp_hand_gesture')

#the 10 different handgestures the model is trained on
classNames = ['okay', 'peace', 'thumbs up', 'thumbs down', 'call me', 'stop', 'rock', 'live long', 'fist', 'smile']

def motion_detector():

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    while True:
        #read the frames
        _, frame = cap.read()
        x, y, c = frame.shape
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #prosesses the frames
        result = hands.process(framergb)
        className = ''

        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                #predicts data
                prediction = model.predict([landmarks])
                classID = np.argmax(prediction)
                className = classNames[classID]

        #show the prediction and destroys the window
        if className == 'thumbs up':
            cv2.putText(frame, className + ': Call activated', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cap.release()
            cv2.destroyAllWindows()
            return True  

        #show the final output
        cv2.imshow("Output", frame)
        #can be exited with q-command
        if cv2.waitKey(1) == ord('q'):
            cap.release()

            cv2.destroyAllWindows()
