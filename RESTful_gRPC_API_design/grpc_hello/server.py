import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection

import generated.greeter_pb2_grpc as greeter_pb2_grpc
import generated.greeter_pb2 as greeter_pb2


class HelloService(greeter_pb2_grpc.SayHelloServicer):
    def SayHello(self, request, context):
        name = request.name
        return greeter_pb2.SayHelloResponse(response=f"Hello, {name}!")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    greeter_pb2_grpc.add_SayHelloServicer_to_server(HelloService(), server)

    SERVICE_NAMES = (
        greeter_pb2.DESCRIPTOR.services_by_name['SayHello'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on port 50051 with reflection enabled")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop(0)


if __name__ == "__main__":
    serve()
