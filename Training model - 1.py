import os
import sys
import face_recognition
import pickle
def train_model_img():

    if not os.path.exists("Джоли"):
        print("Данная директория не существует")
        sys.exit()

    name = 'Jolie'
    known_encodings = []
    images = os.listdir("Джоли") #сохраняем список из всех доступных изображений

    for(i, image) in enumerate(images):
        print(f"[+] processing img {i + 1}/{len(images)}")

        face_img = face_recognition.load_image_file(f"Джоли/{image}")
        face_enc = face_recognition.face_encodings(face_img)[0]

        if len(known_encodings) == 0:
            known_encodings.append(face_enc)
        else:
            for item in range(0, len(known_encodings)):
                result = face_recognition.compare_faces([face_enc], known_encodings[item]) #сравнение лиц
                print(result)
                if result[0]:
                    known_encodings.append(face_enc)
                    print('Same person')
                    break
                else:
                    print("Another person")
                    break

    data = {
        "name": name,
        "encodings:": known_encodings
    }

    with open(f"{name}_encodings.pickle", 'wb') as file:
        file.write(pickle.dumps(data))
    return f'File {name}_encodings.pickle successfully created'




def main():
    print(train_model_img())

if __name__ == '__main__':
    main()