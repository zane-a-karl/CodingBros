# server.py
import socket
import json

def start_server():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                received_json = json.loads(data.decode('utf-8'))
                print(f"Received data: {received_json}")
                
                # Process the received data (in this example, we'll just echo it back)
                response = {"status": "OK", "echo": received_json}
                # serialize phython obj to json string
                json_data = json.dumps(response).encode('utf-8')
                conn.sendall(json_data)

if __name__ == "__main__":
    start_server()
