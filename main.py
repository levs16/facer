import cv2, face_recognition, os, json

# read the json
with open('dataset/faces.json', 'r') as f:
  face_data = json.load(f)

# start the webcam
cap = cv2.VideoCapture(0)

# loop while the q is not pressed
while True:
    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = []
        names = []
        for person in face_data['emp_details']:
          matches.append(face_recognition.compare_faces([person['face_encoding']], face_encoding)[0])
          names.append(person['name'])
        name = "Unknown" # standart name for the face
        if True in matches:
            match_index = matches.index(True)
            name = names[match_index]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # show the window
    cv2.imshow("Facer (ver.0.6)", frame)

    # check for s or q input
    key = cv2.waitKey(1) & 0xFF

    # if q is pressed - break the loop
    if key == ord("q"):
        break

    # if s is pressed, try to save the face with its data
    if key == ord("s"):
        face_encoding = face_encodings[-1]
        (top, right, bottom, left) = face_locations[-1]
        face_image = frame[top:bottom, left:right]
        name = input("Enter a name for this face: ")
        cv2.imwrite(os.path.join("dataset", name + ".jpg"), face_image)
        with open('dataset/faces.json', 'r+') as f:
          data = json.load(f)
          data['emp_details'].append({'name': name, 'face_encoding': list(face_encoding)})
          f.seek(0)
          json.dump(data, f)

cap.release()
cv2.destroyAllWindows()