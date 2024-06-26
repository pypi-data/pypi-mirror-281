import getpass
import socket
import pickle

import grpc
import grpc_server_pb2
import grpc_server_pb2_grpc
import numpy as np
import torch

from serializer import serialize_data, deserialize_data

device_ip = ''
device_port = 0
grpc_server_port = 61002
has_connection = False

def init(api_token=None):
    if api_token is None:
        api_token = getpass.getpass("Enter your API token: ")
    with grpc.insecure_channel(f'localhost:{grpc_server_port}') as channel:
        stub = grpc_server_pb2_grpc.APITokenServiceStub(channel)
        try:
            response = stub.GetIPPort(grpc_server_pb2.APITokenRequest(api_token=api_token))
            if response.ip and response.port:
                global device_ip
                global device_port
                device_ip = response.ip
                device_port = response.port
                global has_connection
                has_connection = True
                print(f"Connected to device at {device_ip}")
            else:
                raise Exception("Invalid API token.")
        except grpc.RpcError as e:
            print(f"gRPC Error: {e.code()} - {e.details()}")
            
# TODO: Change depending on needs and data requirements. (Use delegates)
def send_data(data={}):
    if has_connection:
        send_via_ip_data(device_ip, device_port, data)
    else:
        print("No connection established.")
            
def send_via_ip_data(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        serialized_data = serialize_data(data)
        client_socket.sendall(serialized_data)
        
        response = client_socket.recv(4096)
        response_data = deserialize_data(response)
        # TODO: Process the response data
        print(f'Received response: {response_data}')
    
if __name__ == "__main__": # sample code
    init("V54LDNvFvy9SRHdtmqYSlA") # API token
    sample_data = {
        'torch_tensor': torch.tensor([[1, 2], [3, 4]]),
        'numpy_array': np.array([[1.1, 2.2], [3.3, 4.4]])
    }
    sample_data2 = {
        'torch_tensor': torch.tensor([[1+2j, 3+4j], [5+6j, 7+8j]]),
        'numpy_array': np.array([[1+2j, 3+4j], [5+6j, 7+8j]])
    }
    send_data(sample_data)
    send_data(sample_data2)