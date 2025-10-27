import grpc
from concurrent import futures

import generated.greeter_pb2_grpc as greeter_pb2_grpc
import generated.greeter_pb2 as greeter_pb2

class HelloService(greeter_pb2_grpc.SayHelloServicer):
    def SayHello(self, request, context):
        name = request.name

        return greeter_pb2.SayHelloResponse(
            response = f"Hello, {name}!"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    greeter_pb2_grpc.add_SayHelloServicer_to_server(HelloService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()