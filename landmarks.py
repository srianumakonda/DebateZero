import os
import cv2
import dlib
import subprocess
import face_recognition
import numpy as np
from utils import *

landmark_predictor = dlib.shape_predictor('src/shape_predictor_68_face_landmarks.dat')
TRUMP_SAMPLE = "src/trump_sample.png"
KAMALA_SAMPLE = "src/kamala_sample.png"

def main(video_input, annotated_dir, face_dir, eyes_dir, frame_skip=3, audio=True, together=True, default_dir="output.mp4"):

    known_face_encodings = [
        face_recognition.face_encodings(face_recognition.load_image_file(TRUMP_SAMPLE))[0],
        face_recognition.face_encodings(face_recognition.load_image_file(KAMALA_SAMPLE))[0]
    ]
    known_face_names = ["Trump", "Kamala"]

    input_video = cv2.VideoCapture(video_input)

    width, height, fps = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)), input_video.get(cv2.CAP_PROP_FPS)
    output_video = cv2.VideoWriter(annotated_dir, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    output_black = cv2.VideoWriter(face_dir, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    output_eyes = cv2.VideoWriter(eyes_dir, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # print(f"Frames per second: {fps}")

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
                color = (71, 71, 18)  # yellow for unknown
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                if True in matches:
                    match_index = matches.index(True)
                    name = known_face_names[match_index]
                    if name == known_face_names[0]:
                        color = (93, 22, 93)  # pink for Trump
                    elif name == known_face_names[1]:
                        color = (26, 77, 82)  # blue for Kamala

                current_face_info.append((face_location, color))

        for face_location, color in current_face_info:
            top, right, bottom, left = [int(v * 2) for v in face_location] 
            face = dlib.rectangle(left, top, right, bottom)
            landmarks = landmark_predictor(frame, face)

            #applying face annotations on image
            for n in range(68):
                x, y = landmarks.part(n).x, landmarks.part(n).y
                cv2.circle(frame, (x, y), 2, color, -1)

            # cv2.rectangle(black_background_frame, (left, top), (right, bottom), color, 2)  # Draw bounding box on black background
            # face
            for n in range(68):
                x, y = landmarks.part(n).x, landmarks.part(n).y
                cv2.circle(black_background_frame, (x, y), 2, color, -1)

            # eyes 
            for n in range(36, 48):
                x, y = landmarks.part(n).x, landmarks.part(n).y
                cv2.circle(eyes_frame, (x, y), 2, color, -1)
        
        output_video.write(frame)
        output_black.write(black_background_frame)
        output_eyes.write(eyes_frame)
        # cv2.imshow('Video', frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    input_video.release()
    output_video.release()
    output_black.release()
    output_eyes.release()
    cv2.destroyAllWindows()

    if (audio):
        if not os.path.exists("final"):
            os.makedirs("final")

        stitch_audio(video_input, annotated_dir, "final/"+annotated_dir)
        stitch_audio(video_input, face_dir, "final/"+face_dir)
        stitch_audio(video_input, eyes_dir, "final/"+eyes_dir)

        for file in [annotated_dir, face_dir, eyes_dir]:
            if os.path.exists(file):
                print(f"Deleting {file}")
                os.remove(file)
            else:
                print(f"File {file} does not exist.")

        # ffmpeg -i src/input_long.mp4 -i final/black_out.mp4 -i final/out.mp4 -i final/eyes_out.mp4 -filter_complex "[0:v]fps=30[v0];[1:v]fps=30[v1];[2:v]fps=30[v2];[3:v]fps=30[v3];[v0][v1]hstack=inputs=2[top];[v2][v3]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2" -vsync vfr -c:v libx264 -crf 23 -preset veryfast final/output.mp4



        #     os.remove("final/"+annotated_dir) 
        #     os.remove("final/"+face_dir)
        #     os.remove("final/"+eyes_dir)

        # os.remove(annotated_dir)
        # os.remove(face_dir)
        # os.remove(eyes_dir)

if __name__ == "__main__":
    video_input = "src/jan6.mp4"
    annotated_dir = "jan6.mp4"
    face_dir = "jan6_black_out.mp4"
    eyes_dir = "jan6_eyes_out.mp4"
    main(video_input, annotated_dir, face_dir, eyes_dir)