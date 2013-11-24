import socket

# Connect to the server on port 16551. Obviously UDP_IP should be changed to the
# server's ip.
UDP_IP = "76.105.244.177"
UDP_PORT = 16551

# Create the socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# And send the initial packet so that the server can collect your ip and port
sock.sendto("info packet", (UDP_IP, UDP_PORT))

# Server should send you a packet with your peer's ip and port in a string with
# the format "ip port" once it has both of the peers' ip's and ports
(data, address) = sock.recvfrom(1024)

# Because the ip and port recieved are seperated by a space, split it in to two
# parts at the space
split_data = data.split(" ")

# Peer is a tuple, with the format (ip, port) which should now be stored in the
# array split_data
peer = (split_data[0], int(split_data[1]))

# Send your peer the text "pickle", so they know it's you. Who else would send
# the word pickle?
sock.sendto("pickle", peer)

# Your peer should be sending you something too. I bet they'll never think to
# send pickle
(peers_message, _) = sock.recvfrom(1024)

print("Your peer sent: " + peers_message)

# If by some crazy coincidence, your peer also sent the word pickle
if (peers_message == "pickle"):
    # Vocalize your shock
    print("WTF!?!")
