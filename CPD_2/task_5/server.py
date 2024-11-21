from concurrent import futures
import grpc
import order_management_pb2_grpc
import order_management_pb2
import time
import uuid
import logging
from google.protobuf import wrappers_pb2
import google.protobuf.empty_pb2

# Установка логирование
logging.basicConfig(level=logging.INFO)

class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        method_name = handler_call_details.method
        metadata = handler_call_details.invocation_metadata
        start_time = time.time()

        response = continuation(handler_call_details)

        elapsed_time = time.time() - start_time
        logging.info(f"Method: {method_name}, Metadata: {metadata}, Time: {elapsed_time:.4f} seconds")

        return response

class OrderManagementServicer(order_management_pb2_grpc.OrderManagementServicer):
    def __init__(self):
        # Словарь для хранения заказов
        self.orderDict = {}
        # Добавление нескольких примеров заказов в словарь
        self.orderDict['101'] = order_management_pb2.Order(
            id='101', price=1000, items=['Item - A', 'Item - B'], description='Sample order description.')
        self.orderDict['102'] = order_management_pb2.Order(
            id='102', price=1000, items=['Item - C'], description='Sample order description.')
        self.orderDict['103'] = order_management_pb2.Order(
            id='103', price=1000, items=['Item - A', 'Item - E'], description='Sample order description.')
        self.orderDict['104'] = order_management_pb2.Order(
            id='104', price=1000, items=['Item - F', 'Item - G'], description='Sample order description.')

    # Получение информации о заказе по ID
    def getOrder(self, request, context):
        order = self.orderDict.get(request.value)
        if order:
            return order
        else:
            # Обработка ошибки, если заказ не найден
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Order {request.value} not found.')
            return order_management_pb2.Order()
    # Добавление нового заказа
    def addOrder(self, request, context):
        id = uuid.uuid1()
        request.id = str(id)
        self.orderDict[request.id] = request
        response = wrappers_pb2.StringValue(value=str(id))
        return response

    # Поиск заказов по некоторому критерию
    def searchOrders(self, request, context):
        matching_orders = self.searchInventory(request.value)
        for order in matching_orders:
            yield order

    # Обновление информации о заказах
    def updateOrders(self, request_iterator, context):
        response = 'Updated IDs:'
        for order in request_iterator:
            self.orderDict[order.id] = order
            response += ' ' + order.id
        return wrappers_pb2.StringValue(value=response)

    # Обработка заказов
    def processOrders(self, request_iterator, context):
        shipment_id = uuid.uuid1()
        shipments = []

        shipment = order_management_pb2.CombinedShipment(id=str(shipment_id), status='PROCESSED')
        shipments.append(shipment)
        for order_id in request_iterator:
            for order in shipments:
                yield order

    # Функция для поиска заказов
    def searchInventory(self, query):
        matchingOrders = []
        for order_id, order in self.orderDict.items():
            for item in order.items:
                if query in item:
                    matchingOrders.append(order)
                    break
        return matchingOrders

    # Удаление заказа по ID
    def deleteOrder(self, request, context):
        if request.value in self.orderDict:
            del self.orderDict[request.value]
            return google.protobuf.empty_pb2.Empty()
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Order with ID {request.value} not found')
            return google.protobuf.empty_pb2.Empty()

server = grpc.server(
    futures.ThreadPoolExecutor(max_workers=10),
    interceptors=(LoggingInterceptor(),)
)
order_management_pb2_grpc.add_OrderManagementServicer_to_server(OrderManagementServicer(), server)
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()

