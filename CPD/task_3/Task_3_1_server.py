import socket  # Импортируем модуль socket для работы с сетевыми соединениями


def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)  
    server_socket.bind((host, port))  # Привязываем сокет к хосту и порту
    server_socket.listen(1)  # Начинаем прослушивание входящих соединений, максимум 1 клиент в очереди
    print(f"Server started at {host}:{port}")

    conn, addr = server_socket.accept()  # Принимаем входящее соединение
    print(f"Connection from {addr}")

    while True:
        data = conn.recv(1024).decode('utf-8')  # Получаем данные от клиента и декодируем их из байтов в строку
        if not data:  # Если данные отсутствуют, выходим из цикла
            break
        print(f"Received: {data}")  # Выводим полученные данные

    conn.close()  # Закрываем соединение
    print("Connection closed")


if __name__ == "__main__":
    start_server()  # Запускаем сервер