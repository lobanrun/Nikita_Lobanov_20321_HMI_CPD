import socket  # Импортируем модуль socket для работы с сетевыми соединениями
import task3_pb2  # Импортируем сгенерированный файл Protocol Buffers
import time  # Импортируем модуль time для работы с задержками


def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)  
    client_socket.connect((host, port))  # Подключаемся к серверу

    try:
        while True:
            temp_event = task3_pb2.TempEvent()  # Создаем экземпляр сообщения TempEvent
            temp_event.device_id = 123  # Устанавливаем значение device_id
            temp_event.event_id = 1  # Устанавливаем значение event_id
            temp_event.humidity = 60.0  # Устанавливаем значение humidity
            temp_event.temp_cel = 25.0  # Устанавливаем значение temp_cel
            serialized_data = temp_event.SerializeToString()  # Сериализуем объект в строку байтов
            client_socket.send(serialized_data)  # Отправляем сериализованные данные на сервер
            print(
                f"Sent TempEvent: device_id={temp_event.device_id}, event_id={temp_event.event_id}, humidity={temp_event.humidity}, temp_cel={temp_event.temp_cel}")  # Выводим отправленные данные
            time.sleep(1)  # Задержка в 1 секунду
    except KeyboardInterrupt:
        print("Client stopped.")  # Обработка остановки клиента при нажатии Ctrl+C
    finally:
        client_socket.close()  # Закрываем соединение


if __name__ == "__main__":
    start_client()  # Запускаем клиента
