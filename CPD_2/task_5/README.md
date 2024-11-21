# Task_5
## Задание
### Task_5_1_Interceptors
Server-Side Interceptors
Interceptor

Т.к. в Python это EXPERIMENTAL API и не очень хорошо поддерживаются, то реализуем только логирование на стороне сервиса. + нет доступа к request. (Название вызываемого метода (получить через соответствующий метод), словарь метаданных (получить через соответствующий метод), время)

(см api документацию: grpc.ServerInterceptor, def intercept_service)

#### Task_5_2_Deadlines
В examples как timeout можно найти пример.

gRPC deadlines for the client application (Крайние сроки в клиентском gRPC-приложении)
### Task_5_3_Cancellation
На основе bidirectional streaming реализовать отмену (прерывае) удаленный вызов на клиентской стороне.

gRPC cancellation (Отмена gRPC)
#### Task_5_4_Error_Handling
Error creation and propagation on the server side (Создание и передача ошибки на стороне сервера)

Error handling on the client side (Обработка ошибок на стороне клиента)
## Листинги
[order_management.proto](order_management.proto)
```proto
syntax = "proto3";

import "google/protobuf/wrappers.proto";
import "google/protobuf/empty.proto";

package ecommerce;

service OrderManagement {
    rpc addOrder(Order) returns (google.protobuf.StringValue);
    rpc getOrder(google.protobuf.StringValue) returns (Order);
    rpc searchOrders(google.protobuf.StringValue) returns (stream Order);
    rpc updateOrders(stream Order) returns (google.protobuf.StringValue);
    rpc processOrders(stream google.protobuf.StringValue) returns (stream CombinedShipment);
    rpc deleteOrder(google.protobuf.StringValue) returns (google.protobuf.Empty);
}

message Order {
    string id = 1;
    repeated string items = 2;
    string description = 3;
    float price = 4;
    string destination = 5;
}

message CombinedShipment {
    string id = 1;
    string status = 2;
    repeated Order ordersList = 3;
}
```
[server.py](server.py)
```python
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


```
[client.py](client.py)
```python
import grpc
import order_management_pb2
import order_management_pb2_grpc
import time
from google.protobuf import wrappers_pb2
import threading


def run():
    # Установка соединения с gRPC сервером
    channel = grpc.insecure_channel('localhost:50051')
    # Создание клиентского stub, который предоставляет методы сервера
    stub = order_management_pb2_grpc.OrderManagementStub(channel)

    try:
        # Создание экземпляра заказа для добавления
        order = order_management_pb2.Order(
            items=['Item - A', 'Item - B', 'Item - C'],
            price=2450.50,
            description='This is a Sample order - 1 : description.',
            destination='San Jose, CA'
        )

        # Получение заказа по его ID после 5 секундного timeout
        order_response = stub.getOrder(wrappers_pb2.StringValue(value='101'), timeout=5)
        print("Order service response", order_response)

        # Добавление заказа после 5 секундного timeout
        add_response = stub.addOrder(order, timeout=5)
        print('Add order response:', add_response)

        # Поиск заказов по элементу
        for search_result in stub.searchOrders(wrappers_pb2.StringValue(value='Item - A')):
            print('Search Result:', search_result)

        # Обновление заказов
        upd_order_iterator = generate_orders_for_updates()
        upd_status = stub.updateOrders(upd_order_iterator, timeout=5)
        print('Order update status:', upd_status)

        # Обработка заказов
        process_order_iterator = generate_orders_for_processing()
        call = stub.processOrders(process_order_iterator)

        def cancel_call():
            time.sleep(5)
            call.cancel()

        cancel_thread = threading.Thread(target=cancel_call)
        cancel_thread.start()
        cancel_thread.join()
        try:
            for shipment in call:
                print(shipment, )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.CANCELLED:
                print("Call was cancelled")
            else:
                print(f"gRPC error: {e}")

        # Удаление заказа
        delete_response = stub.deleteOrder(wrappers_pb2.StringValue(value='101'))
        print("Order deleted:", delete_response)

    except grpc.RpcError as e:
        print(f"gRPC error: {e}")


def generate_orders_for_updates():
    """Генерация обновленных заказов для отправки на сервер"""
    orders = [
        order_management_pb2.Order(id='101', price=1000,
                                   items=['Item - A', 'Item - B', 'Item - C', 'Item - D'],
                                   description='Sample order description.',
                                   destination='Mountain View, CA'),
        order_management_pb2.Order(id='102', price=1000,
                                   items=['Item - E', 'Item - Q', 'Item - R', 'Item - D'],
                                   description='Sample order description.',
                                   destination='San Jose, CA'),
        order_management_pb2.Order(id='103', price=1000,
                                   items=['Item - A', 'Item - K'],
                                   description='Sample order description.',
                                   destination='San Francisco, CA')
    ]

    for order in orders:
        yield order


def generate_orders_for_processing():
    orders = [
        order_management_pb2.Order(
            id='104', price=2332,
            items=['Item - A', 'Item - B'],
            description='Updated desc',
            destination='San Jose, CA'),
        order_management_pb2.Order(
            id='105', price=3000,
            description='Updated desc',
            destination='San Francisco, CA'),
        order_management_pb2.Order(
            id='106', price=2560,
            description='Updated desc',
            destination='San Francisco, CA'),
        order_management_pb2.Order(
            id='107', price=2560,
            description='Updated desc',
            destination='Mountain View, CA')
    ]

    for order in orders:
        yield wrappers_pb2.StringValue(value=order.id)


if __name__ == '__main__':
    run()

```
## Результат работы
![1.jpg](1.jpg)
![2.jpg](2.jpg)

## Реализация 
### Task_5_1_Interceptors
Для реализации логирования на серверу был создан класс LoggingInterceptor, который наследуется от grpc.ServerInterceptor. Метод intercept_service перехватывает вызовы к сервису и логирует информацию о вызываемом методе, метаданных запроса и времени выполнения метода.

### Task_5_2_Deadlines
Для установки крайнего срока выполнения на стороне клиента был использован параметр timeout при вызове методов. Например, при вызове stub.getOrder(..., timeout=5) устанавливается крайний срок выполнения в 5 секунд. Если ответ не будет получен за это время, будет вызвано исключение grpc.RpcError.

### Task_5_3_Cancellation
Для реализации отмены удаленного вызова на стороне клиента был использован метод call.cancel() в отдельном потоке. В примере cancel_call запускается поток, который спит 5 секунд, а затем вызывает call.cancel() для отмены вызова. При этом метод processOrders на стороне сервера должен уметь обрабатывать отмену вызова и завершаться корректно.

### Task_5_4_Error_Handling
На стороне сервера было реализовано создание и передача ошибок при неудачных попытках найти заказ или удалить заказ с несуществующим ID. Для этого используются методы context.set_code() и context.set_details(). На стороне клиента ошибка обрабатывается как grpc.RpcError, и код ошибки можно получить через e.code().