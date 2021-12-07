import socket
import pickle
import sys
from _thread import *
from gameEngine import Game


class Server:
    def __init__(self, port):
        self.ip = "127.0.0.1"
        self.port = port
        self.server_socket = None
        self.connected = set()
        self.games = {}
        self.idCount = 0

    def creatSocket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))

    def threaded_client(self, conn, player_index, gameId, games):
        global count_id
        conn.send(str.encode(str(player_index)))  # send client his index
        while True:
            try:
                if gameId in games:  # check if the game is still running
                    data = conn.recv(4096).decode()  # get the game mode - move,reset,end
                    if data == 'reset':
                        games[gameId].reset_game()
                    elif data != 'start':  # means move was send (the only left option)
                        games[gameId].update_player_move(player_index, data)
                    game_to_send = games[gameId]  # get the updated game to send
                    conn.sendall(pickle.dumps(game_to_send))  # send with pickle
                else:
                    break
            except Exception as e:
                print(e)
                break
        print(f'Connection Lost')
        try:
            del games[gameId]
        except:
            pass
        count_id -= 1
        conn.close()

    def main_loop(self):
        global count_id
        self.creatSocket()
        while True:
            self.server_socket.listen()
            conn, addr = self.server_socket.accept()
            print(f'Connected to {addr}')
            count_id += 1
            player_index = 0
            game_id = (count_id - 1) // 2  # we have x players and x/2 games
            if count_id % 2 == 1:  # means need to wait to create nea game and wait for another player
                self.games[game_id] = Game(game_id)  # create new game
            else:  # no need to create another game, so the current game is ready
                self.games[game_id].is_game_ready = True
                player_index = 1
            start_new_thread(self.threaded_client, (conn, player_index, game_id, self.games))


if __name__ == '__main__':
    try:
        PORT = int(sys.argv[1])
    except Exception as e:
        print(f'Wrong Port: {e}')
        sys.exit(1)
    count_id = 0
    server = Server(PORT)
    server.main_loop()
