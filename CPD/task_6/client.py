from google.protobuf import wrappers_pb2  # Импорт типов-оберток, например, StringValue.
import grpc  # Библиотека для работы с gRPC.
import order_management_pb2  # Сгенерированный код Protocol Buffers для сообщений.
import order_management_pb2_grpc  # Сгенерированный код gRPC для сервиса.

def run():
    # Установка соединения с сервером gRPC.
    channel = grpc.insecure_channel('localhost:50051')  # Создаем канал для связи с сервером по адресу localhost и порту 50051.

    # Создание клиентского stub (объекта для вызова методов сервера).
    stub = order_management_pb2_grpc.OrderManagementStub(channel)

    # Создание нового объекта заказа для добавления на сервер.
    order1 = order_management_pb2.Order(
        items=['Item - A', 'Item - B', 'Item - C'],  # Список предметов в заказе.
        price=2450.50,  # Цена заказа.
        description='This is a Sample order - 1 : description.',  # Описание заказа.
        destination='San Jose, CA'  # Адрес доставки.
    )

    # Получение заказа по его ID.
    order = stub.getOrder(order_management_pb2.Order(id='101'))  # Отправляем запрос с ID заказа.
    print("Order service response", order)  # Вывод ответа сервера.

    # Добавление нового заказа.
    response = stub.addOrder(order1)  # Отправляем заказ на сервер для добавления.
    print('Add order response :', response)  # Вывод ID нового заказа.

    # Поиск заказов по элементу (например, 'Item - A').
    for order_search_result in stub.searchOrders(wrappers_pb2.StringValue(value='Item - A')):
        # Для каждого найденного заказа выводим результат.
        print('Search Result : ', order_search_result)

    # Обновление заказов.
    upd_order_iterator = generate_orders_for_updates()  # Генерируем поток обновленных заказов.
    upd_status = stub.updateOrders(upd_order_iterator)  # Отправляем их на сервер.
    print('Order update status : ', upd_status)  # Вывод результата обновления.

    # Обработка заказов.
    proc_order_iterator = generate_orders_for_processing()  # Генерируем поток заказов для обработки.
    for shipment in stub.processOrders(proc_order_iterator):
        # Для каждой обработанной доставки выводим результат.
        print(shipment)

    # Удаление заказа.
    order_id_to_delete = wrappers_pb2.StringValue(value='101')  # Создаем объект с ID заказа для удаления.
    stub.deleteOrder(order_id_to_delete)  # Отправляем запрос на удаление.
    print("Order deleted:", order_id_to_delete.value)  # Подтверждаем удаление.

def generate_orders_for_updates():
    # Генерация списка заказов для обновления.
    ord1 = order_management_pb2.Order(
        id='101',  # ID заказа, который будет обновлен.
        price=1000,  # Новая цена.
        items=['Item - A', 'Item - B', 'Item - C', 'Item - D'],  # Новый список предметов.
        description='Sample order description.',  # Новое описание.
        destination='Mountain View, CA'  # Новый адрес доставки.
    )
    ord2 = order_management_pb2.Order(
        id='102', price=1000,
        items=['Item - E', 'Item - Q', 'Item - R', 'Item - D'],
        description='Sample order description.',
        destination='San Jose, CA'
    )
    ord3 = order_management_pb2.Order(
        id='103', price=1000,
        items=['Item - A', 'Item - K'],
        description='Sample order description.',
        destination='San Francisco, CA'
    )
    list = [ord1, ord2, ord3]  # Список заказов для обновления.

    for updated_orders in list:  # Для каждого заказа из списка.
        yield updated_orders  # Возвращаем поток обновленных заказов.

def generate_orders_for_processing():
    # Генерация списка заказов для обработки.
    ord1 = order_management_pb2.Order(
        id='104', price=2332,  # ID и цена заказа.
        items=['Item - A', 'Item - B'],  # Список предметов.
        description='Updated desc',  # Описание.
        destination='San Jose, CA'  # Адрес доставки.
    )
    ord2 = order_management_pb2.Order(
        id='105', price=3000,
        description='Updated desc',
        destination='San Francisco, CA'
    )
    ord3 = order_management_pb2.Order(
        id='106', price=2560,
        description='Updated desc',
        destination='San Francisco, CA'
    )
    ord4 = order_management_pb2.Order(
        id='107', price=2560,
        description='Updated desc',
        destination='Mountain View, CA'
    )
    list = [ord1, ord2, ord3, ord4]  # Список заказов для обработки.

    for processing_orders in list:  # Для каждого заказа из списка.
        yield processing_orders  # Возвращаем поток заказов для обработки.

run()  # Запускаем выполнение клиентского кода.
