import face_recognition
import pickle
import os
from tqdm import tqdm


def extract_face_encodings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image, model="cnn")
    face_encodings = face_recognition.face_encodings(image, face_locations, model="large")
    return face_encodings


def prepare_known_faces(images_directory):
    known_faces = {}

    all_image_files = []
    for root, dirs, files in os.walk(images_directory):
        for subdir in dirs:
            person_dir = os.path.join(root, subdir)
            image_files = [
                os.path.join(person_dir, f)
                for f in os.listdir(person_dir)
                if f.lower().endswith((".jpg", ".png"))
            ]
            all_image_files.extend(image_files)

    total_images = len(all_image_files)
    progress_bar = tqdm(total=total_images, unit="image", desc="Overall Progress", leave=False, position=0, ascii=True)

    for root, dirs, files in os.walk(images_directory):
        for subdir in dirs:
            person_dir = os.path.join(root, subdir)
            name = subdir

            image_files = [
                os.path.join(person_dir, f)
                for f in os.listdir(person_dir)
                if f.lower().endswith((".jpg", ".png"))
            ]

            person_face_encodings = []
            person_progress_bar = tqdm(total=len(image_files), unit="image", desc=f"Processing {name}", leave=False,
                                       position=1, ascii=True)

            for image_file in image_files:
                face_encodings = extract_face_encodings(image_file)
                if face_encodings:
                    person_face_encodings.extend(face_encodings)
                person_progress_bar.update(1)
                progress_bar.update(1)
                person_progress_bar.set_postfix(
                    images_left=f"{len(image_files) - person_progress_bar.n}/{len(image_files)}")

            person_progress_bar.close()

            if person_face_encodings:
                known_faces[name] = person_face_encodings
            else:
                print(f"No face found in images for {name}. Skipping.")

    progress_bar.close()
    return known_faces


if __name__ == "__main__":
    images_directory = "images"

    known_faces = prepare_known_faces(images_directory)

    with open("known_faces.pkl", "wb") as f:
        pickle.dump(known_faces, f)

    print("Known faces preparation completed and saved to 'known_faces.pkl'.")
