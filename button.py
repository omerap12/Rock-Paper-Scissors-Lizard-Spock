import pygame


class Button:
    def __init__(self, text, x_coordinate, y_coordinate, color):
        self.text = text
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, window):
        """
        function that draw the text on buttons
        :param window: the window
        :return:
        """
        pygame.draw.rect(window, self.color, (self.x_coordinate, self.y_coordinate, self.width, self.height))
        font = pygame.font.SysFont("dejavusansmono", 20)  # text font
        text = font.render(self.text, 1, (255, 255, 255))
        window.blit(text, (self.x_coordinate + round(self.width / 2) - round(text.get_width() / 2),
                           self.y_coordinate + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, position):
        """
        funcrtion to check if the button was pressed
        :param position: position that was clicked
        :return: True if pressed else False
        """
        clicked_x = position[0]
        clicked_y = position[1]
        if self.x_coordinate <= clicked_x <= self.x_coordinate + self.width and \
                self.y_coordinate <= clicked_y <= self.y_coordinate + self.height:
            # checking if the user clicked in the button area
            return True
        else:
            return False
