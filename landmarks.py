import cv2
import dlib
import face_recognition
import numpy as np
from utils import *

landmark_predictor = dlib.shape_predictor('src/shape_predictor_68_face_landmarks.dat')

file_input = "test1.mp4"
file_out = "out1.mp4"
black_out = "black_out1.mp4"
eyes_out = "eyes_out1.mp4"
trump_sample = "src/trump_sample.png"
kamala_sample = "src/kamala_sample.png"

known_face_encodings = [
    face_recognition.face_encodings(face_recognition.load_image_file(trump_sample))[0],
    face_recognition.face_encodings(face_recognition.load_image_file(kamala_sample))[0]
]
known_face_names = ["Trump", "Kamala"]

input_video = cv2.VideoCapture(file_input)

width, height, fps = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)), input_video.get(cv2.CAP_PROP_FPS)
output_video = cv2.VideoWriter(file_out, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
output_black = cv2.VideoWriter(black_out, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
output_eyes = cv2.VideoWriter(eyes_out, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))


print(f"Frames per second: {fps}")

frame_skip = 3
current_face_info = []  

while True:
    ret, frame = input_video.read()
    if not ret:
        break

    black_background_frame = np.zeros_like(frame)
    eyes_frame = np.zeros_like(frame)

    current_frame = int(input_video.get(cv2.CAP_PROP_POS_FRAMES))
    if current_frame % frame_skip == 0:
        small_frame = cv2.cvtColor(cv2.resize(frame, (0, 0), fx=0.5, fy=0.5), cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        current_face_info = []

        for face_encoding, face_location in zip(face_encodings, face_locations):
            color = (71, 71, 18)  # Red for unknown
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]
                if name == "Trump":
                    color = (93, 22, 93)  # Blue for Trump
                elif name == "Kamala":
                    color = (26, 77, 82)  # Green for Kamala

            current_face_info.append((face_location, color))

    for face_location, color in current_face_info:
        top, right, bottom, left = [int(v * 2) for v in face_location] 
        face = dlib.rectangle(left, top, right, bottom)
        landmarks = landmark_predictor(frame, face)

        # print(frame.shape, frame1.shape)

        for n in range(68):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(frame, (x, y), 2, color, -1)

        # cv2.rectangle(black_background_frame, (left, top), (right, bottom), color, 2)  # Draw bounding box on black background
        for n in range(68):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(black_background_frame, (x, y), 2, color, -1)

        for n in range(36, 48):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(eyes_frame, (x, y), 2, color, -1)
    
    output_video.write(frame)
    output_black.write(black_background_frame)
    output_eyes.write(eyes_frame)
    # cv2.imshow('Video', frame)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release everything when done
input_video.release()
output_video.release()
output_black.release()
output_eyes.release()
cv2.destroyAllWindows()


stitch_audio(file_input, file_out, "final/out1.mp4")
stitch_audio(file_input, black_out, "final/black_out1.mp4")
stitch_audio(file_input, eyes_out, "final/eyes_out1.mp4")