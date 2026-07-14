import asyncio
import sys
import websockets

import base64
import hashlib


def handshake(client_socket):
    # Generate a random 16-byte key and encode it in base64
    key = base64.b64encode(hashlib.sha1(b'random_key_generator').digest()).decode('utf-8')
    
    # Construct the HTTP GET request
    request = (
        "GET /chat HTTP/1.1\r\n"
        "Host: example.com\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Key: " + key + "\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n"
    )
    
    client_socket.send(request.encode('utf-8'))
    
    # Wait for the server's response
    response = client_socket.recv(1024).decode('utf-8')
    print(response)
    
    # Verify the server accepted the upgrade
    if "101 Switching Protocols" in response:
        print("Handshake successful")
    else:
        print("Handshake failed")


async def listen_for_messages(websocket):
    """
    Background task that continuously listens for incoming messages from the server.
    """
    try:
        async for message in websocket:
            # Clear the current input line briefly to print the message beautifully
            print(f"\r[Received]: {message}")
            print("[You]: ", end="", flush=True)
    except websockets.ConnectionClosed:
        print("\n[System]: Connection to server closed.")
    except Exception as e:
        print(f"\n[System]: Error in listener: {e}")

async def main():
    uri = "ws://localhost:8080"
    print(f"[System]: Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("[System]: Connected successfully!")
            
            
            listener_task = asyncio.create_task(listen_for_messages(websocket))

            done, pending = await asyncio.wait(
                [listener_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
                
    except ConnectionRefusedError:
        print("[System]: Could not connect via websocket to the server.")
    except Exception as e:
        print(f"[System]: An error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[System]: Client closed.")