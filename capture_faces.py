
import cv2
import os

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def capture_face(user_id):
    if not os.path.exists("dataset"):
        os.mkdir("dataset")

    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            cv2.imwrite(f"dataset/user_{user_id}_{count}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)

        cv2.imshow('Captura de rostos', frame)

        if cv2.waitKey(1) == 27 or count >= 30:
            break

    cap.release()
    cv2.destroyAllWindows()
