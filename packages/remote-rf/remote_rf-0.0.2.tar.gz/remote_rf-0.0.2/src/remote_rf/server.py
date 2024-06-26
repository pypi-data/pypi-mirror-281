import itertools
import os
import pickle
import socket
import sys
import threading
import time

from concurrent import futures
from dotenv import load_dotenv, find_dotenv

import grpc
import grpc_server_pb2
import grpc_server_pb2_grpc
import numpy as np
import torch

from api_tokens import generate_api_token
from api_tokens import validate_token
from api_tokens import write_to_env
from serializer import serialize_data, deserialize_data

load_dotenv(find_dotenv('.env.server'))

local_ip = os.getenv('LOCAL_IP')
local_port = os.getenv('GRPC_PORT')
local_tcp_port = os.getenv('TCP_PORT')

def animate_message(message, cycles=1):
    ellipsis = itertools.cycle(['.', '..', '...'])
    for _ in range(cycles * 3):
        sys.stdout.write('\r' + message + next(ellipsis))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\r' + ' ' * (len(message) + 3) + '\r')  # clear the line when done
    sys.stdout.flush()
    
def clear_line():
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()

def clear_previous_line():
    sys.stdout.write('\033[F')
    clear_line()
    
def clear_env_file(filename='.env'):
    with open(filename, 'w') as file:
        file.write('')  # Overwrites the file with an empty string

def display_env_file(filename='.env'):
    """
    Displays the contents of the .env file.
    """
    try:
        with open(filename, 'r') as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
# region gRPC Server

class APITokenServiceServicer(grpc_server_pb2_grpc.APITokenServiceServicer):
    def GetIPPort(self, request, context):
        clear_line()
        if (validate_token(request.api_token)): # Validate the API token and determine the IP and port
            print(f"Received Valid API token {request.api_token}. Port forwarded.")
            return grpc_server_pb2.IPPortResponse(ip=local_ip, port=int(local_tcp_port))
        else:
            print(f"Received Invalid API token: {request.api_token}")
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Invalid API token')
            return grpc_server_pb2.IPPortResponse(ip="", port=0)

def grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_server_pb2_grpc.add_APITokenServiceServicer_to_server(APITokenServiceServicer(), server)
    server.add_insecure_port(f'{local_ip}:{local_port}')
    print(f"GRPC Server listening on {local_ip}:{local_port}")
    server.start()
    server.wait_for_termination()
    
# endregion

# region TCP sockets

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((local_ip, int(local_tcp_port)))
        server_socket.listen()
        print(f'TCP Server listening on {local_ip}:{local_tcp_port}')
        
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f'Connected by {addr}')
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    received_data = deserialize_data(data)
                    print(f'Received data: {received_data}')

                    # TODO: Send data to be processed
                    response_data = received_data # ! TEMPORARY
                    # TODO: grab the return data and send it back
                    conn.sendall(serialize_data(response_data))

# endregion

if __name__ == '__main__':
    
    threading.Thread(target=grpc_server, daemon=True).start()
    threading.Thread(target=tcp_server, daemon=True).start()
    print("Server running nominally.\n")
    print("Press enter to stop the server. \nType 'clear' to remove all local API tokens. \nType 'view' to view the current API tokens. \nType 'new' to generate a new API token.")
    
    toggle = True
    while toggle:
        inpu = input()
        if inpu == "clear":
            clear_env_file()
        elif inpu == "view":
            display_env_file()
        elif inpu == "new":
            new_token = generate_api_token()
            write_to_env(new_token)
            print(f'Generated new token: ')
            print(f'{new_token}')
        else:
            toggle = False
        
# endregion