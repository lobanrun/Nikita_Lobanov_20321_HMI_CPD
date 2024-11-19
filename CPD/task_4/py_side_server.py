from PySide6.QtWidgets import QApplication, QLabel, QGridLayout, \
    QWidget  # Импортируются необходимые виджеты из библиотеки PySide6 для создания графического интерфейса
from PySide6.QtNetwork import QTcpServer, QTcpSocket, \
    QHostAddress  # Импортируются классы для работы с сетевыми соединениями, такие как TCP сервер и сокеты
from PySide6.QtCore import QByteArray, Signal, \
    QObject  # Импортируются необходимые классы для работы с сигналами и буфером данных
from PySide6.QtGui import QImage, QPixmap  # Импортируются классы для работы с изображениями и отображением их в виджете
import sys
import video_frame_pb2  # Импорт сгенерированного модуля Protobuf, содержащего классы для работы с сообщениями Protobuf

app = QApplication(sys.argv)
window = QWidget()  # Создание главного окна

buffer = QByteArray()  # Буфер для хранения входящих данных

# Создание виджета для отображения изображения
up_camera = QLabel()
grid = QGridLayout(window)
grid.addWidget(up_camera, 0, 0)

# Настройка и запуск TCP сервера
tcpServer = QTcpServer()  # Создание TCP сервера для прослушивания входящих соединений
tcpServer.listen(QHostAddress.LocalHost,
                 12345)  # Настройка TCP сервера на прослушивание соединений по адресу localhost и порту 12345


# Сигнал для обновления изображения
class ImageUpdater(QObject):
    up_camera_signal = Signal(QImage)

    def __init__(self):
        super().__init__()
        self.up_camera_signal.connect(self.update_frame)

    def update_frame(self, image):
        up_camera.setPixmap(QPixmap.fromImage(image))


image_updater = ImageUpdater()


def handle_new_connection():
    """Метод, вызываемый при новом соединении"""
    client_socket = tcpServer.nextPendingConnection()  # Получение следующего ожидающего соединения клиента
    client_socket.readyRead.connect(lambda: process_video_data(client_socket))


def process_video_data(socket: QTcpSocket):
    """Метод для чтения и обработки видеоданных"""
    global buffer
    buffer.append(socket.readAll())  # Добавление всех данных, считанных из сокета, в буфер для последующей обработки
    video_frame = video_frame_pb2.VideoFrame()
    if video_frame.ParseFromString(
            buffer.data()):  # Попытка десериализовать данные из буфера с использованием Protobuf. Если успешно, данные кадра будут извлечены
        image = QImage()
        image.loadFromData(video_frame.frame_data, "JPEG")
        if not image.isNull():
            image_updater.up_camera_signal.emit(image)
        buffer.clear()


# Подключение обработчика для новых соединений
tcpServer.newConnection.connect(handle_new_connection)

# Запуск приложения
window.show()
sys.exit(app.exec_())
