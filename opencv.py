import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
if face_cascade.empty():
    raise IOError('Unable to load the face cascade classifier xml file')

if eye_cascade.empty():
    raise IOError('Unable to load the eye cascade classifier xml file')

if smile_cascade.empty():
    raise IOError('Unable to load the smile cascade classifier xml file')

cap = cv2.VideoCapture(0)
ds_factor = 1

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 10)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        smile = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.2,minNeighbors=40,minSize=(25, 25))
        for (sx, sy, sw, sh) in smile:
            cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 3)

        eyes = eye_cascade.detectMultiScale(roi_gray,1.2,minNeighbors=40)

        for (x_eye, y_eye, w_eye, h_eye) in eyes:
            center = (int(x_eye + 0.5 * w_eye), int(y_eye + 0.5 * h_eye))
            radius = int(0.3 * (w_eye + h_eye))
            color = (255, 0, 0)
            thickness = 3
            cv2.circle(roi_color, center, radius, color, thickness)

    cv2.imshow('Face, Eye, Smile Detector', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()

cv2.destroyAllWindows()
