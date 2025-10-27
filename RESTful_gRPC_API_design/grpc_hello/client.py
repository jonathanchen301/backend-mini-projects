import grpc
import generated.greeter_pb2 as greeter_pb2
import generated.greeter_pb2_grpc as greeter_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = greeter_pb2_grpc.SayHelloStub(channel)
        request = greeter_pb2.SayHelloRequest(name="Johnny")
        response = stub.SayHello(request)

        print(response.response)

if __name__ == "__main__":
    run()
