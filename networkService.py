import socket
import pickle


class NetworkService:
    def __init__(self, ip,port):
        self.ip = ip
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create TCP socket
        self.port = port
        self.player_index = None
        self.connect()

    def connect(self):
        try:
            self.client_socket.connect((self.ip, self.port))
            data = self.client_socket.recv(2048).decode()  # get the index from the socket
            self.player_index = data
        except Exception as e:
            print(e)

    def send(self, data):
        """
        function used to send move and get updated game object
        :param data: the move
        :return:
        """
        try:
            self.client_socket.send(str.encode(data))  # send string
            return pickle.loads(self.client_socket.recv(4096))  # get the game object
        except socket.error as e:
            return # client disconnected

    def get_player_index(self):
        return self.player_index
