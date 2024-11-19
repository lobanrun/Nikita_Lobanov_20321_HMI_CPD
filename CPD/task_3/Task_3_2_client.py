import socket  # Импортируем модуль socket для работы с сетевыми соединениями
import pickle  # Импортируем модуль pickle для сериализации объектов
import time  # Импортируем модуль time для работы с задержками


def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)   
    client_socket.connect((host, port))  # Подключаемся к серверу

    try:
        while True:
            data = {"1": 25, "2": 60}  # Создаем объект с данными для отправки
            serialized_data = pickle.dumps(data)  # Сериализуем объект в байты
            client_socket.send(serialized_data)  # Отправляем сериализованные данные на сервер

            time.sleep(1)  # Задержка в 1 секунду
    except KeyboardInterrupt:
        print("Client stopped.")  # Обработка остановки клиента при нажатии Ctrl+C
    finally:
        client_socket.close()  # Закрываем соединение


if __name__ == "__main__":
    start_client()  # Запускаем клиента