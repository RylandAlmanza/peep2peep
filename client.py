import socket
import threading

# Connect to the server on port 16551. Obviously UDP_IP should be changed to the
# server's ip.
UDP_IP = "76.105.244.177"
UDP_PORT = 16551

class ChatClient():
    def __init__(self, logging_enabled):
        # If logging_enabled is true, the client will update you on what it's
        # doing.
        self.logging_enabled = logging_enabled

        # While this variable is true, all threads will continue running
        self.running = True

        # Create the socket object
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # And send the initial packet so that the server can collect your ip and
        # port
        self.log("Sending information packet to pairing server...")
        self.sock.sendto("info packet", (UDP_IP, UDP_PORT))
        self.log("Packet sent.")

        # Server should send you a packet with your peer's ip and port in a
        # string with the format "ip port" once it has both of the peers' ip's
        # and ports
        data = "stayalive"
        # Keep looping until we get something other than a keep-alive packet
        while data == "stayalive":
            self.log("Waiting for pairing server to send peer information...")
            (data, address) = self.sock.recvfrom(1024)
            if (data == "stayalive"):
                self.log("Received keep-alive packet from server.")
            else:
                self.log("Peer information received.")

        # Because the ip and port recieved are seperated by a space, split it
        # into two parts at the space
        split_data = data.split(" ")

        # Peer is a tuple, with the format (ip, port) which should now be stored
        # in the array split_data
        self.peer = (split_data[0], int(split_data[1]))
        self.log("Will be talking to " + \
                 self.peer[0] + \
                 " on port " + \
                 str(self.peer[1]) + \
                 ".")

        # Create a new thread for sending keep alive packets to your peer
        keep_alive_thread = threading.Thread()
        # And set it's activity to our keep_alive_activity
        keep_alive_thread.run = self.keep_alive_activity

        # Create a new thread to receive messages on
        receive_thread = threading.Thread()
        # And set it's activity to our receive_activity
        receive_thread.run = self.receive_activity

        # Start receiving messages
        receive_thread.start()
        # And sending keep-alive packets
        keep_alive_thread.start()

        self.prompt_for_message()

    # This activity sends regular packets to our peer to keep the connection
    # alive
    def keep_alive_activity(self):
        # If the application is still supposed to be running
        if (self.running):
            # We send a packet to our peer
            self.sock.sendto("stayalive", self.peer)
            # And then schedule the next time we send another keep-alive packet
            threading.Timer(10, self.keep_alive_activity).start()

    # This activity will wait for messages from your peer
    def receive_activity(self):
        # While the application is still supposed to be running
        while self.running:
            # Get your peer's message
            (peers_message, _) = self.sock.recvfrom(1024)
            # If it's not just a keep-alive packet
            if (peers_message != "stayalive"):
                # Print your peer's message
                print("\nYour peer sent: " + peers_message)

    # This method starts prompting you for messages to send
    def prompt_for_message(self):
        # The message variable will store the message you want to send your peer
        message = ""
        # If the message doesn't say "quit", just keep prompting to send a
        # message
        while message != "quit":
            # Get the message you want to send and store it in the message
            # variable
            message = raw_input("> ")
            # Send your super personalized message to your peer
            self.sock.sendto(message, self.peer)
        
        # If we got to this line, it means "quit" was entered. We should
        # probably stop the program.
        running = False
        self.sock.close()

    # Prints a message only if logging is enabled
    def log(self, message):
        # If logging is enabled, as determined by the logging_enabled member
        if self.logging_enabled:
            # Print the message
            print(message)

if __name__ == '__main__':
    ChatClient(True)
