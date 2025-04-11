
import cv2
import psycopg2
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def get_user(user_id):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM usuarios WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    for (x,y,w,h) in faces:
        id_, conf = recognizer.predict(gray[y:y+h, x:x+w])
        if conf < 70:
            user = get_user(id_)
            if user:
                print(f"Bem-vindo {user[0]}!")
                cap.release()
                cv2.destroyAllWindows()
                exit()
        else:
            print("Desconhecido")

    cv2.imshow('Reconhecimento Facial', frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
