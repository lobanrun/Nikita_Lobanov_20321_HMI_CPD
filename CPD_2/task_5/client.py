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
        # Удаление заказа
        delete_response = stub.deleteOrder(wrappers_pb2.StringValue(value='101'))
        print("Order deleted:", delete_response)

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
