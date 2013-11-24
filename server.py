# Server to test UDP hole punching

import socket

# Run server on port 16551
UDP_IP = "0.0.0.0"
UDP_PORT = 16551

# This array will store the ip and port that each client used to send the
# initial packet
clients = []

# The first client in the array will be referred to as CLIENT_A
CLIENT_A = 0
# And the second as CLIENT_B
CLIENT_B = 1

# Create the socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# And bind it to the port defined earlier
sock.bind((UDP_IP, UDP_PORT))

# This loop waits for 2 packets, and then stores the ip and port that the packet
# was sent from. There should be one from CLIENT_A and one from CLIENT_B.
for i in range(2):
    # address is a tuple: (ip, port)
    (_, address) = sock.recvfrom(1024)
    # Append the ip and port tuple to the clients list
    clients.append(address)

# Store CLIENT_A's ip and port in the variables ip and port. In that order, of
# course. Just want to clarify.
(ip, port) = clients[CLIENT_A]
# Send CLIENT_A's ip and port (concatenated into a string) to CLIENT_B
sock.sendto(ip + " " + str(port), clients[CLIENT_B])

# Store CLIENT_B's ip and port in the variables ip and port.
(ip, port) = clients[CLIENT_B]
# Send CLIENT_B;s ip and port (concatenated into a string) to CLIENT_B
sock.sendto(ip + " " + str(port), clients[CLIENT_A])

# Well done server. Your service is no longer needed. Grab yourself a beer.
print("Drinking a beer...")
