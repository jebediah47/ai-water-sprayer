import face_recognition
import cv2
import numpy as np
import pickle


def load_known_faces(file_path: str) -> dict:
    """
    Load the dictionary of known faces (names mapped to face encodings) from file.
    """
    with open(file_path, "rb") as f:
        known_faces = pickle.load(f)
    return known_faces


if __name__ == "__main__":
    known_faces_file_path = "known_faces.pkl"
    known_faces = load_known_faces(known_faces_file_path)

    face_names = []
    process_this_frame = True

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        resize_factor = 0.75
        small_frame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations
            )

            face_names = []
            for face_encoding in face_encodings:
                name = "Unknown"

                for known_name, known_encodings in known_faces.items():
                    matches = face_recognition.compare_faces(
                        known_encodings, face_encoding
                    )
                    if True in matches:
                        name = known_name
                        break

                face_names.append(name)

        process_this_frame = not process_this_frame

        scale_factor = 1 / resize_factor
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top = int(top * scale_factor)
            right = int(right * scale_factor)
            bottom = int(bottom * scale_factor)
            left = int(left * scale_factor)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
            )

        cv2.imshow("Water Sprayer", frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
