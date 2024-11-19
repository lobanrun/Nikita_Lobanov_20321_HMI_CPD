import socket  # Импортируем модуль socket для работы с сетевыми соединениями
import task3_pb2  # Импортируем сгенерированный файл Protocol Buffers


def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)
    server_socket.bind((host, port))  # Привязываем сокет к хосту и порту
    server_socket.listen(1)  # Начинаем прослушивание входящих соединений, максимум 1 клиент в очереди
    print(f"Server started at {host}:{port}")

    conn, addr = server_socket.accept()  # Принимаем входящее соединение
    print(f"Connection from {addr}")

    while True:
        data = conn.recv(4096)  # Получаем данные от клиента
        if not data:  # Если данные отсутствуют, выходим из цикла
            break
        temp_event = task3_pb2.TempEvent()  # Создаем экземпляр сообщения TempEvent
        temp_event.ParseFromString(data)  # Парсим данные из байтового представления
        print(
            f"Received TempEvent: device_id={temp_event.device_id}, event_id={temp_event.event_id}, humidity={temp_event.humidity}, temp_cel={temp_event.temp_cel}")  # Выводим данные сообщения

    conn.close()  # Закрываем соединение
    print("Connection closed")


if __name__ == "__main__":
    start_server()  # Запускаем сервер
