import cv2
import sys

sys.path
sys.path.append('Sentiment.py')

import Sentiment as sent


#cascPath = sys.argv[1]
cascPath = '/Users/Francois/anaconda3/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        frame_crop = frame[y:y+h,x:x+w]#, y:y+h]
        ## Perform Deep Learning
        model = sent.Transfer_learning()
        Emotion,percentage = sent.Sentiment_Analysis(frame_crop, model)
        cv2.imshow('Crop', frame_crop)
        print(Emotion)

    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()