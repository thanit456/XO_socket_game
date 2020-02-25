import socket

# global variables 
username_list = dict()


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))

            if data:
                print('sending message back to the client')
                if data[:3] == b'REG':
                    username = data[3:].decode()
                    username_list.append(username)
                    print('GOT USERNAME : ', username)
                    print(username_list)
                    message = data[3:] + b'is connected'
                else: 
                    message = 'server got data'    
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        print("Closing current connection")
        connection.close()