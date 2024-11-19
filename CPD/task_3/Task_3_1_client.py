import socket  # Импортируем модуль socket для работы с сетевыми соединениями
import time  # Импортируем модуль time для работы с задержками


def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)  
    client_socket.connect((host, port))  # Подключаемся к серверу

    try:
        while True:
            data = "ЙОУ"  # Отправляемая строка данных
            client_socket.send(data.encode('utf-8'))  # Кодируем строку в байты и отправляем на сервер
            time.sleep(1)  # Задержка в 1 секунду
    except KeyboardInterrupt:
        print("Client stopped.")  # Обработка остановки клиента при нажатии Ctrl+C
    finally:
        client_socket.close()  # Закрываем соединение


if __name__ == "__main__":
    start_client()  # Запускаем клиента
