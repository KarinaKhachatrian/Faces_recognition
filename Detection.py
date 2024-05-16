import cv2
import face_recognition
import pickle
import sqlite3

list_of_actors = []

def detect_person_in_video():
    data = pickle.loads(open("Jolie_encodings.pickle", "rb").read())
    video = cv2.VideoCapture("Jolie.mp4")

    while True:
        ret, image = video.read()

        locations = face_recognition.face_locations(image, model = "hog")
        encodings = face_recognition.face_encodings(image, locations)

        for face_encoding, face_location in zip(encodings, locations):
            result = face_recognition.compare_faces(data['encodings:'], face_encoding)
            match = None

            if True in result:
                match = data["name"]
                print(f"Match found {match}")

            else:
                print("Not match found")

            left_top = (face_location[3], face_location[0])
            right_bottom = (face_location[1], face_location[2])
            color = [0, 255, 0]
            cv2.rectangle(image, left_top, right_bottom, color, 4)

            left_bottom = (face_location[3], face_location[2])
            right_bottom = (face_location[1], face_location[2] + 20)
            cv2.rectangle(image, left_bottom, right_bottom, color, cv2.FILLED)
            cv2.putText(
                image,
                match,
                (face_location[3] + 10, face_location[2] + 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                4
            )

        cv2.imshow("detect_person_in_video is running", image)


        k = cv2.waitKey(20)
        if k == ord(" "):
            print("Space have pressed, closing...")
            list_of_actors.append('Jolie')
            break

def detect_person_in_video1():
    data = pickle.loads(open("Pitt_encodings.pickle", "rb").read())
    video = cv2.VideoCapture("Бред Питт.mp4")

    while True:
        ret, image = video.read()

        locations = face_recognition.face_locations(image, model = "hog")
        encodings = face_recognition.face_encodings(image, locations)

        for face_encoding, face_location in zip(encodings, locations):
            result = face_recognition.compare_faces(data['encodings:'], face_encoding)
            match = None

            if True in result:
                match = data["name"]
                print(f"Match found {match}")

            else:
                print("Not match found")

            left_top = (face_location[3], face_location[0])
            right_bottom = (face_location[1], face_location[2])
            color = [0, 255, 0]
            cv2.rectangle(image, left_top, right_bottom, color, 4)

            left_bottom = (face_location[3], face_location[2])
            right_bottom = (face_location[1], face_location[2] + 20)
            cv2.rectangle(image, left_bottom, right_bottom, color, cv2.FILLED)
            cv2.putText(
                image,
                match,
                (face_location[3] + 10, face_location[2] + 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                4
            )

        cv2.imshow("detect_person_in_video is running", image)


        k = cv2.waitKey(20)
        if k == ord(" "):
            print("Space have pressed, closing...")
            list_of_actors.append('Pitt')
            break


def main():
    detect_person_in_video()
    detect_person_in_video1()

if __name__ == '__main__':
    main()

print(list_of_actors)

def convert_to_bin_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def insert_blob_actors_list(ID, Name, Surname, Date_of_birth, Image):

    conn = sqlite3.connect('Actors.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Actors_list(
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Surname TEXT NOT NULL,
        Date_of_birth DATE NOT NULL,
        Image BLOB);
    """)

    insert_query = """INSERT INTO Actors_list (ID, Name, Surname, Date_of_birth, Image) VALUES (?, ?, ?, ?, ?);"""

    Image = convert_to_bin_data(Image)
    data_tuple = (ID, Name, Surname, Date_of_birth, Image)
    cur.execute(insert_query, data_tuple)

    conn.commit()
    cur.close()

insert_blob_actors_list(1, 'Angelina', 'Jolie', '1975-06-04', 'Actors/Джоли.jpg')
insert_blob_actors_list(2, 'Monica', 'Bellucci', '1964-09-30', 'Actors/Беллучи.jpg')
insert_blob_actors_list(3, 'Brad', 'Pitt', '1963-12-18', 'Actors/Питт.jpg')
insert_blob_actors_list(4, 'Johnny', 'Depp', '1963-06-09', 'Actors/Депп.jpg')
insert_blob_actors_list(5, 'Ann', 'Hataway', '1982-11-12', 'Actors/Хэтэуэй.jpg')

def insert_blob_detection(ID, Adding_name, Adding_surname, Date_of_birth, Detection, Image):
    conn = sqlite3.connect('Actors.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Adding_actors(
            ID INTEGER PRIMARY KEY,
            Adding_name TEXT NOT NULL,
            Adding_surname TEXT NOT NULL,
            Date_of_birth DATE NOT NULL,
            Detection ,
            Image BLOB,
            FOREIGN KEY (Adding_name) REFERENCES Actors_list (Name),
            FOREIGN KEY (Adding_surname) REFERENCES Actors_list (Surname));""")
    insert_query_detection = """INSERT INTO Adding_actors (ID, Adding_name, Adding_surname, Date_of_birth, Detection, Image) VALUES (?, ?, ?, ?, ?, ?);"""
    Image = convert_to_bin_data(Image)
    data_tuple_detection = (ID, Adding_name, Adding_surname, Date_of_birth, Detection, Image)
    cur.execute(insert_query_detection, data_tuple_detection)

    conn.commit()
    cur.close()

insert_blob_detection(1, 'Angelina', 'Jolie', '1975-06-04', '-', 'Actors/Джоли.jpg')
insert_blob_detection(2, 'Monica', 'Bellucci', '1964-09-30', '-', 'Actors/Беллучи.jpg')
insert_blob_detection(3, 'Brad', 'Pitt', '1963-12-18', '-', 'Actors/Питт.jpg')
insert_blob_detection(4, 'Johnny', 'Depp', '1963-06-09', '-', 'Actors/Депп.jpg')
insert_blob_detection(5, 'Ann', 'Hataway', '1982-11-12', '-', 'Actors/Хэтэуэй.jpg')

if 'Jolie' in list_of_actors:
    conn = sqlite3.connect('Actors.db')
    cur = conn.cursor()
    update = """UPDATE Adding_actors SET Detection = '+' WHERE Adding_surname = 'Jolie'"""
    cur.execute(update)
    conn.commit()
    cur.close()

if 'Bellucci' in list_of_actors:
    conn = sqlite3.connect('Actors.db')
    cur = conn.cursor()
    update = """UPDATE Adding_actors SET Detection = '+' WHERE Adding_surname = 'Bellucci'"""
    cur.execute(update)
    conn.commit()
    cur.close()

if 'Pitt' in list_of_actors:
    conn = sqlite3.connect('Actors.db')
    cur = conn.cursor()
    update = """UPDATE Adding_actors SET Detection = '+' WHERE Adding_surname = 'Pitt'"""
    cur.execute(update)
    conn.commit()
    cur.close()

if 'Depp' in list_of_actors:
    conn = sqlite3.connect('Actors.db')
    cur = conn.cursor()
    update = """UPDATE Adding_actors SET Detection = '+' WHERE Adding_surname = 'Depp'"""
    cur.execute(update)
    conn.commit()
    cur.close()

if 'Hataway' in list_of_actors:
    conn = sqlite3.connect('Actors.db')
    cur = conn.cursor()
    update = """UPDATE Adding_actors SET Detection = '+' WHERE Adding_surname = 'Hataway'"""
    cur.execute(update)
    conn.commit()
    cur.close()