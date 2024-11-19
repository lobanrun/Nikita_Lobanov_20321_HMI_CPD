import cv2
import socket
import video_frame_pb2  # Импорт сгенерированного модуля Protobuf, содержащего классы для работы с сообщениями Protobuf

def send_video_frame_by_frame(video_path, server_ip, server_port):
    cap = cv2.VideoCapture(video_path)  # Открытие видеофайла для захвата кадров с помощью OpenCV
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))  # Установка соединения с сервером по заданному IP-адресу и порту
        while cap.isOpened():
            ret, frame = cap.read()
            # Если кадр есть
            if not ret:
                break
            # Кодирование кадра в формате JPEG
            _, buffer = cv2.imencode('.jpg', frame)  # Кодирование кадра в формат JPEG и сохранение его в буфер
            # Создание сообщения VideoFrame
            video_frame = video_frame_pb2.VideoFrame()
            video_frame.frame_data = buffer.tobytes()  # Запись закодированных данных кадра в сообщение Protobuf
            # Сериализация сообщения и его отправка
            sock.sendall(video_frame.SerializeToString())  # Сериализация сообщения Protobuf и его отправка на сервер
    # Освобождение ресурсов захвата видео
    cap.release()

if __name__ == "__main__":
    video_path = '1.mp4'
    send_video_frame_by_frame(video_path, '127.0.0.1', 12345)