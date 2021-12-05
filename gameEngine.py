class Game:
    def __init__(self, id):
        self.player_one_played = False
        self.player_two_played = False
        self.moves = [None, None]
        self.is_game_ready = False
        self.id = id
        self.movement_data_base = {
            "Rock": "R",
            "Paper": "P",
            "Scissors": "S",
            "Lizard": "L",
            "Spock": "C"
        }

    def doesBothPlayerPlayed(self):
        return self.player_two_played and self.player_one_played

    def update_player_move(self, player_index, move):
        self.moves[player_index] = move  # updating player movement
        if player_index == 0:
            self.player_one_played = True
        else:
            self.player_two_played = True


    def play(self):
        player_one_move = self.moves[0]  # get first player move
        player_two_move = self.moves[1]  # get second player move

        player_won_index = -1  # means tie
        if player_one_move == player_two_move:
            return player_won_index

        # all possible outcomes for Rock
        if player_one_move == "Rock" and player_two_move == "Lizard":
            player_won_index = 0
        elif player_one_move == "Rock" and player_two_move == "Spock":
            player_won_index = 1
        elif player_one_move == "Rock" and player_two_move == "Scissors":
            player_won_index = 0
        elif player_one_move == "Rock" and player_two_move == "Paper":
            player_won_index = 1

        # all possible outcomes for Lizard
        elif player_one_move == "Lizard" and player_two_move == "Spock":
            player_won_index = 0
        elif player_one_move == "Lizard" and player_two_move == "Scissors":
            player_won_index = 1
        elif player_one_move == "Lizard" and player_two_move == "Paper":
            player_won_index = 0
        elif player_one_move == "Lizard" and player_two_move == "Rock":
            player_won_index = 1

        # all possible outcomes for Spock
        elif player_one_move == "Spock" and player_two_move == "Scissors":
            player_won_index = 0
        elif player_one_move == "Spock" and player_two_move == "Paper":
            player_won_index = 1
        elif player_one_move == "Spock" and player_two_move == "Rock":
            player_won_index = 0
        elif player_one_move == "Spock" and player_two_move == "Lizard":
            player_won_index = 1

        # all possible outcomes for Scissors
        elif player_one_move == "Scissors" and player_two_move == "Paper":
            player_won_index = 0
        elif player_one_move == "Scissors" and player_two_move == "Rock":
            player_won_index = 1
        elif player_one_move == "Scissors" and player_two_move == "Lizard":
            player_won_index = 0
        elif player_one_move == "Scissors" and player_two_move == "Spock":
            player_won_index = 1

        # all possible outcomes for Paper
        elif player_one_move == "Paper" and player_two_move == "Rock":
            player_won_index = 0
        elif player_one_move == "Paper" and player_two_move == "Lizard":
            player_won_index = 1
        elif player_one_move == "Paper" and player_two_move == "Spock":
            player_won_index = 0
        elif player_one_move == "Paper" and player_two_move == "Scissors":
            player_won_index = 1
        return player_won_index

    def reset_game(self):
        self.player_one_played = False
        self.player_two_played = False

    def running(self):
        return self.is_game_ready
