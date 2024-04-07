import face_recognition
import pickle
import os


def extract_face_encodings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings


def prepare_known_faces(images_directory):
    known_faces = {}

    for root, dirs, files in os.walk(images_directory):
        for subdir in dirs:
            person_dir = os.path.join(root, subdir)

            name = subdir

            image_files = [
                os.path.join(person_dir, f)
                for f in os.listdir(person_dir)
                if f.endswith(".jpg") or f.endswith(".png")
            ]

            person_face_encodings = []
            for image_file in image_files:
                face_encodings = extract_face_encodings(image_file)
                if face_encodings:
                    person_face_encodings.extend(
                        face_encodings
                    )

            if person_face_encodings:
                known_faces[name] = person_face_encodings
            else:
                print(f"No face found in images for {name}. Skipping.")

    return known_faces


if __name__ == "__main__":
    images_directory = "images"

    known_faces = prepare_known_faces(images_directory)

    with open("known_faces.pkl", "wb") as f:
        pickle.dump(known_faces, f)

    print("Known faces preparation completed and saved to 'known_faces.pkl'.")
