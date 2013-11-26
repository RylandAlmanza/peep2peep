# Server to test UDP hole punching

import socket
import threading

# Run server on port 16551
UDP_IP = "0.0.0.0"
UDP_PORT = 16551

# The first client in the array will be referred to as CLIENT_A
CLIENT_A = 0
# And the second as CLIENT_B
CLIENT_B = 1

class ChatServer():
    def __init__(self, logging_enabled):
        # If logging_enabled is true, the server will update you on what it's
        # doing.
        self.logging_enabled = logging_enabled

        # Store whether or not we have successfully paired two clients in paired
        self.paired = False

        # This array will store the ip and port that each client used to send the
        # initial packet
        self.clients = []

        # Create the socket object
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # And bind it to the port defined earlier
        self.sock.bind((UDP_IP, UDP_PORT))
        self.log("Binded to " + UDP_IP + " on port " + str(UDP_PORT) + ".")

        # Create a new thread for sending keep alive packets to our clients,
        keep_alive_thread = threading.Thread()
        # set it's activity to our keep_alive_activity,
        keep_alive_thread.run = self.keep_alive_activity
        # And start it
        keep_alive_thread.start()

        # This loop waits for 2 packets, and then stores the ip and port that 
        # the packet was sent from. There should be one from CLIENT_A and one
        # from CLIENT_B.
        self.log("Waiting for clients...")
        for i in range(2):
            # address is a tuple: (ip, port)
            (_, address) = self.sock.recvfrom(1024)
            # Append the ip and port tuple to the clients list
            self.clients.append(address)
            if i < 1:
                self.log("Client obtained. Waiting for a second one...")
            else:
                self.log("Both clients obtained.")

        # Store CLIENT_A's ip and port in the variables ip and port. In that
        # order, of course. Just want to clarify.
        (ip, port) = self.clients[CLIENT_A]
        # Send CLIENT_A's ip and port (concatenated into a string) to CLIENT_B
        self.log("Sending Client A's information to Client B...")
        self.sock.sendto(ip + " " + str(port), self.clients[CLIENT_B])
        self.log("Information sent.")

        # Store CLIENT_B's ip and port in the variables ip and port.
        (ip, port) = self.clients[CLIENT_B]
        # Send CLIENT_B;s ip and port (concatenated into a string) to CLIENT_B
        self.log("Sending Client B's information to Client A...")
        self.sock.sendto(ip + " " + str(port), self.clients[CLIENT_A])
        self.log("Information received.")

        # Both clients should be paired now
        self.paired = True
        self.log("Both clients should now be paired.")

        # Well done server. Your service is no longer needed. Grab yourself a
        # beer.
        self.log("Job done.")
        self.log("Drinking a beer...")

    # This activity sends regular packets to our clients to keep the connection
    # alive
    def keep_alive_activity(self):
        # If we have at least one client
        if (len(self.clients) > 0):
            for i in range(len(self.clients)):
                # We send a packet to our clients
                self.sock.sendto("stayalive", self.clients[i])
                self.log("keep alive packet sent to " + self.clients[i][0])
                # And then schedule the next time we send another keep-alive
                # packet
        # If we still haven't paired the clients
        if (self.paired == False):
            # Make sure we keep sending keep-alive packets.
            threading.Timer(10, self.keep_alive_activity).start()

    # Prints a message only if logging is enabled
    def log(self, message):
        # If logging is enabled, as determined by the logging_enabled member
        if self.logging_enabled:
            # Print the message
            print(message)          

if __name__ == '__main__':
    ChatServer(True)
