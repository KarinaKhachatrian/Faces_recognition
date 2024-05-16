import cv2
import os

def take_screen_from_video():
    cap = cv2.VideoCapture("Jolie.mp4")
    count = 0

    if not os.path.exists("dataset_from_video"):
        os.mkdir("dataset_from_video")


    while True:
        ret, frame = cap.read() #захват, декодирование и возврат след кадра
        fps = cap.get(cv2.CAP_PROP_FPS)
        multiplier = fps * 3


        if ret:
            frame_id = int(round(cap.get(1)))
            cv2.imshow("frame", frame)
            k = cv2.waitKey(20) #скорость видео

            if frame_id % multiplier == 0:
                cv2.imwrite(f"dataset_from_video/{count}.jpg", frame)
                print(f"Сделан скриншот {count}")
                count += 1

            if k == ord(" "):
                cv2.imwrite(f"dataset_from_video/{count}_extrascreen.jpg", frame)
                print(f"Сделан экстренный скриншот {count}")
                count += 1
            elif k == ord("q"):
                print("Нажата клавиша q, закрываемся...")
                break

        else:
            print("Не удалось получить кадр")
            break
    cap.release()
    cv2.destroyAllWindows()


def main():
    take_screen_from_video()

if __name__ == '__main__':
    take_screen_from_video()