import grpc
import product_info_pb2
import product_info_pb2_grpc
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = product_info_pb2_grpc.ProductInfoStub(channel)

        # Добавление продукта
        added_product = stub.addProduct(product_info_pb2.Product(name="Apple iPhone 11", description="Meet Apple iPhone 11. All-new dual-camera system with Ultra Wide and Night mode.", price=699.0))
        print("Product added, ID:", added_product.value)
        # Получение информации о продукте
        product_info = stub.getProduct(product_info_pb2.ProductID(value=added_product.value))
        print("Product retrieved:", product_info)
        # Удаление продукта
        stub.deleteProduct(product_info_pb2.ProductID(value=added_product.value))
        print("Product deleted, ID:", added_product.value)



if __name__ == '__main__':
    run()
