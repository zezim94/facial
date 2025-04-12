
import face_recognition
import cv2

def capture_face_encoding_and_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    if boxes:
        encoding = face_recognition.face_encodings(rgb, boxes)[0]
        _, img_encoded = cv2.imencode('.jpg', frame)
        return encoding, img_encoded.tobytes()
    return None, None

def match_face(known_encoding):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    if boxes:
        encoding = face_recognition.face_encodings(rgb, boxes)[0]
        matches = face_recognition.compare_faces([known_encoding], encoding)
        return matches[0]
    return False
