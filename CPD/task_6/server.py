from concurrent import futures  # Для управления потоками.
import time  # Для работы со временем (например, задержки).
from typing import OrderedDict  # Для упорядоченного словаря.
import uuid  # Для генерации уникальных идентификаторов.
from google.protobuf import wrappers_pb2  # Типы-обертки, например, StringValue.
import google.protobuf  # Основной модуль Protocol Buffers.
import grpc  # gRPC библиотека.
import order_management_pb2_grpc  # Сгенерированный код gRPC для сервиса.
import order_management_pb2  # Сгенерированный код Protocol Buffers для сообщений.

class OrderManagementServicer(order_management_pb2_grpc.OrderManagementServicer):
    # Реализация методов, определенных в proto-файле.

    def __init__(self):
        # Конструктор, где инициализируется словарь для хранения заказов.
        self.orderDict = {}  # Словарь для хранения заказов (ключ: ID заказа, значение: объект Order).

        # Добавление нескольких тестовых заказов в словарь.
        self.orderDict['101'] = order_management_pb2.Order(
            id='101', price=1000, items=['Item - A', 'Item - B'], description='Sample order description.')
        self.orderDict['102'] = order_management_pb2.Order(
            id='102', price=1000, items=['Item - C'], description='Sample order description.')
        self.orderDict['103'] = order_management_pb2.Order(
            id='103', price=1000, items=['Item - A', 'Item - E'], description='Sample order description.')
        self.orderDict['104'] = order_management_pb2.Order(
            id='104', price=1000, items=['Item - F', 'Item - G'], description='Sample order description.')

    def getOrder(self, request, context):
        # Метод для получения заказа по ID.
        order = self.orderDict.get(request.value)  # Получение заказа по ID из словаря.
        if order is not None:
            return order  # Возвращаем заказ, если он найден.
        else:
            # Если заказ не найден, устанавливаем статус ошибки.
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Order: {request.value} Not Found.')
            return order_management_pb2.Order()  # Возвращаем пустой объект Order.

    def addOrder(self, request, context):
        # Метод для добавления нового заказа.
        id = uuid.uuid1()  # Генерация уникального ID.
        request.id = str(id)  # Устанавливаем сгенерированный ID для заказа.
        self.orderDict[request.id] = request  # Добавляем заказ в словарь.
        response = wrappers_pb2.StringValue(value=str(id))  # Возвращаем ID нового заказа.
        return response

    def searchOrders(self, request, context):
        # Метод для поиска заказов по строке запроса.
        matching_orders = self.searchInventory(request.value)  # Поиск заказов по критерию.
        for order in matching_orders:
            yield order  # Возвращаем поток заказов.

    def updateOrders(self, request_iterator, context):
        # Метод для обновления информации о заказах.
        response = 'Updated IDs :'  # Начальная строка ответа.
        for order in request_iterator:  # Обрабатываем поток входящих заказов.
            self.orderDict[order.id] = order  # Обновляем заказ в словаре.
            response += ' ' + order.id  # Добавляем ID обновленного заказа в ответ.
        return wrappers_pb2.StringValue(value=response)  # Возвращаем результат обновления.

    def processOrders(self, request_iterator, context):
        # Метод для обработки заказов и создания доставки.
        shipment_id = uuid.uuid1()  # Генерация ID доставки.
        shipments = []  # Список доставок.

        shipment = order_management_pb2.CombinedShipment(id=str(shipment_id), status='PROCESSED')
        # Создаем новый объект доставки с заданным ID и статусом.

        shipments.append(shipment)  # Добавляем объект доставки в список.
        for order_id in request_iterator:  # Обрабатываем поток входящих ID заказов.
            for order in shipments:  # Итерируемся по заказам в доставке.
                yield order  # Возвращаем поток обработанных заказов.

    def searchInventory(self, query):
        # Метод для поиска заказов по критерию (используется в searchOrders).
        matchingOrders = []  # Список подходящих заказов.
        for order_id, order in self.orderDict.items():  # Перебор всех заказов в словаре.
            for itm in order.items:  # Перебор всех элементов в заказе.
                if query in itm:  # Если элемент соответствует запросу.
                    matchingOrders.append(order)  # Добавляем заказ в список результатов.
                    break
        return matchingOrders

    def deleteOrder(self, request, context):
        # Метод для удаления заказа по ID.
        if request.value in self.orderDict:  # Проверяем, существует ли заказ.
            del self.orderDict[request.value]  # Удаляем заказ из словаря.
            return google.protobuf.empty_pb2.Empty()  # Возвращаем пустой объект в случае успеха.
        else:
            # Если заказ не найден, устанавливаем статус ошибки.
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Order with ID {request.value} not found')
            return google.protobuf.empty_pb2.Empty()

# Настройка сервера.
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # Создаем сервер с пулом из 10 потоков.
order_management_pb2_grpc.add_OrderManagementServicer_to_server(OrderManagementServicer(), server)
# Регистрируем реализацию сервиса в сервере.

print('Starting server. Listening on port 50051.')  # Сообщение о запуске сервера.
server.add_insecure_port('[::]:50051')  # Настройка порта для приема соединений.
server.start()  # Запуск сервера.
server.wait_for_termination()  # Ожидание завершения работы сервера.
