from concurrent import futures
import grpc
import product_info_pb2
import product_info_pb2_grpc
import uuid
import google.protobuf.empty_pb2

# Реализация сервиса ProductInfo.
class ProductInfoServicer(product_info_pb2_grpc.ProductInfoServicer):
    """Сервис для управления информацией о продуктах."""

    def __init__(self):
        # Локальное хранилище данных о продуктах (ключ - ID продукта).
        self.productMap = {}

    def addProduct(self, request, context):
        """Добавление нового продукта."""
        # Генерируется уникальный ID для нового продукта.
        id = str(uuid.uuid1())
        # Продукт сохраняется в словаре, ID присваивается объекту.
        self.productMap[id] = request
        self.productMap[id].id = id
        # Возвращается объект с уникальным ID.
        return product_info_pb2.ProductID(value=id)

    def getProduct(self, request, context):
        """Получение информации о продукте по его ID."""
        # Ищем продукт по ID.
        product = self.productMap.get(request.value)
        if product:
            # Если найден, возвращаем.
            return product
        else:
            # Если нет, устанавливается ошибка NOT_FOUND.
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Product not found')

    def deleteProduct(self, request, context):
        """Удаление продукта по его ID."""
        if request.value in self.productMap:
            # Если продукт существует, удаляем.
            del self.productMap[request.value]
            # Возвращаем пустой ответ.
            return google.protobuf.empty_pb2.Empty()
        else:
            # Устанавливается ошибка NOT_FOUND.
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Product not found')
            return google.protobuf.empty_pb2.Empty()

# Создание и настройка gRPC-сервера.
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# Регистрация сервиса на сервере.
product_info_pb2_grpc.add_ProductInfoServicer_to_server(
    ProductInfoServicer(), server)
# Сервер слушает порт 50051.
server.add_insecure_port('[::]:50051')
# Запуск сервера.
server.start()
server.wait_for_termination()
