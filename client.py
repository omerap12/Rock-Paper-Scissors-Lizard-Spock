import sys

import pygame
from networkService import NetworkService
from button import Button


class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.width = 700
        self.height = 700
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Player")
        self.buttons = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)),
                        Button("Paper", 450, 500, (0, 255, 0)), Button("Lizard", 150, 600, (50, 205, 50)),
                        Button("Spock", 350, 600, (128, 128, 0))]

    def redrawWindow(self, window, game, player_index):
        window.fill((235, 206, 206))  # color of the window
        if not (game.running()):  # waiting for player
            font = pygame.font.SysFont("dejavusans", 40)
            text = font.render("Waiting for another player...", 1, (255, 0, 0), True)
            window.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - text.get_height() / 2))
        else:  # game is running
            font = pygame.font.SysFont("dejavusans", 40)
            text = font.render("Your Move", 1, (0, 87, 89))
            window.blit(text, (80, 200))

            text = font.render("Opponent", 1, (0, 82, 66))
            window.blit(text, (380, 200))

            move1 = game.moves[0]  # getting moves
            move2 = game.moves[1]

            if game.doesBothPlayerPlayed():  # if both players played
                text1 = font.render(move1, 1, (0, 0, 0))
                text2 = font.render(move2, 1, (0, 0, 0))

            else:
                if game.player_one_played and player_index == 0:  # if player one played and were player one
                    text1 = font.render(move1, 1, (0, 0, 0))  # show the move
                elif game.player_one_played:  # means were not player one
                    text1 = font.render("Selected", 1, (0, 0, 0))
                else:
                    text1 = font.render("Waiting...", 1, (0, 0, 0))

                if game.player_two_played and player_index == 1:  # if player 2 is gone and were player 2
                    text2 = font.render(move2, 1, (0, 0, 0))  # show the move
                elif game.player_two_played:
                    text2 = font.render("Selected", 1, (0, 0, 0))
                else:
                    text2 = font.render("Waiting...", 1, (0, 0, 0))

            # if were player one, were are showing one screen
            if player_index == 1:
                window.blit(text2, (100, 350))
                window.blit(text1, (400, 350))

            else:
                window.blit(text1, (100, 350))
                window.blit(text2, (400, 350))

            # show buttons
            for btn in self.buttons:
                btn.draw(window)

        pygame.display.update()

    def main_loop(self):
        clock = pygame.time.Clock()
        network = NetworkService(self.server_ip, self.server_port) # connection to the server
        print(network.get_player_index())
        player_index = int(network.get_player_index())  # get the index of the player
        while True:
            clock.tick(60)
            try:
                game = network.send("start")  # start the game
            except Exception as e:
                print(e)
                break
            # pygame loop
            for event in pygame.event.get():  # if user exit the program
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:  # if user pressed on mouse
                    position_of_pressed_mouse = pygame.mouse.get_pos()  # get the position of the mouse
                    for button in self.buttons:  # checking if the position is in the buttons area
                        if button.click(position_of_pressed_mouse) and game.running():  # if game running button clicked
                            text = button.text  # get the text from button
                            if player_index == 0:  # if its the first player
                                if not game.player_one_played:
                                    network.send(text)
                            else:
                                if not game.player_two_played:
                                    network.send(text)
                if game.doesBothPlayerPlayed():  # if both players have played there turn
                    self.redrawWindow(self.window, game, player_index)
                    pygame.time.delay(500)
                    try:
                        game = network.send("reset")  # tell the server reset the game
                    except Exception as e:
                        print(e)
                        break

                    # getting output round text message to screen
                    font = pygame.font.SysFont("dejavuserif", 90)
                    if (game.play() == 1 and player_index == 1) or (game.play() == 0 and player_index == 0):  # means
                        # current client won
                        text = font.render("You Won!", False, (255, 0, 0))  # tell client he won
                    elif game.play() == -1:  # means tie
                        text = font.render("Tie!", False, (255, 0, 255))
                    else:  # means client lost
                        text = font.render("You Lost!", False, (255, 0, 0))
                    # show text on screen
                    self.window.blit(text,
                                     (self.width / 2 - text.get_width() / 2, self.height / 2 - text.get_height() / 2))
                    pygame.display.update()
                    pygame.time.delay(2000)
                self.redrawWindow(self.window, game, player_index)


if __name__ == '__main__':
    try:
        PORT = int(sys.argv[2])
        IP = sys.argv[1]
    except Exception as e:
        print(f'Wrong IP/Port: {e}')
        sys.exit(1)

    pygame.font.init()
    client = Client(IP, PORT)
    client.main_loop()
