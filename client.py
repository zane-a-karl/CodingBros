# client.py
import socket
import json

def send_data(data):
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # serialize phython obj to json string
        json_data = json.dumps(data)
        s.sendall(json_data.encode('utf-8'))
        
        response = s.recv(1024)
        return json.loads(response.decode('utf-8'))

if __name__ == "__main__":
    data_to_send = {"message": "Hello, Server!", "number": 42}
    response = send_data(data_to_send)
    print(f"Server response: {response}")
