from random import randint, shuffle
from itertools import cycle

POINTS = [100, 20, 30, 40, 50, 60]

class Game:
    
    def __init__(self, max_score, min_staying_score):
        self.players = []
        self.max_score = max_score
        self.min_staying_score = min_staying_score
        self.current_player_index = 0
        self.own_throw = True
        self.scores = []
        self.available_dice = 5
        self.accumulated = 0
        self.winner_index = None


    def add_player(self, player):
        self.players.append(player)
        shuffle(self.players)
        self.scores.append(0)

    def next_turn(self):
        player = self.players[self.current_player_index]
        status = GameStatus(self)

        if self.own_throw == False and player.starts_over(status):
            self.clear()
            self.next_turn()
            return
        
        continues = self.make_throw()
        if not continues:
            self.clear()
            self.set_next_player()
            self.next_turn()
            return

        
        if self.accumulated >= self.min_staying_score and player.stays(status):
            self.update_player_score()
            self.set_next_player()


        if self.winner_index is None:
            self.next_turn()
            return


    def update_player_score(self):
        self.scores[self.current_player_index] += self.accumulated
        if self.scores[self.current_player_index] >= self.max_score:
            self.winner_index = self.current_player_index



    def set_next_player(self):
        next_i = (self.current_player_index + 1) % len(self.players)
        self.current_player_index = next_i
        if self.accumulated > 0:
            self.own_throw = False


    def make_throw(self):
        throw = Game.get_throw(self.available_dice)
        if throw.points > 0:
            self.available_dice = throw.available_dice
            self.accumulated += throw.points
            return True
        else:
            return False


    def clear(self):
        self.available_dice = 5
        self.accumulated = 0
        self.own_throw = True

    def winner(self):
        return self.players[self.winner_index]
  
    @staticmethod
    def get_throw(number_of_dice):
        dice = [randint(1,6) for i in range(number_of_dice)]
        return Game.dice_to_throw(dice)

    @staticmethod
    def dice_to_throw(dice):
        number_count = Game.to_number_count(dice)
        points = 0

        for i in range(6):
            if number_count[i] >= 3:
                points += POINTS[i] * 10
                number_count[i] -= 3
        if number_count[0] > 0:
            points += POINTS[0] * number_count[0]
            number_count[0] = 0
        if number_count[4] > 0:
            points += POINTS[4] * number_count[4]
            number_count[4] = 0

        available_dice = sum(number_count)
        if available_dice == 0:
            available_dice = 5
        return Throw(points, available_dice)


    @staticmethod
    def to_number_count(dice):
        result = [0 for i in range(6)]
        for die in dice:
            result[die - 1] += 1
        return result

    def current_max_score(self):
        return max(self.scores)

    def next_player_score(self):
        return self.scores[self.next_player_index()]
        
    def next_player_index(self):
        return (self.current_player_index + 1) % len(self.players)

    def current_player_score(self):
        return self.scores[self.current_player_index]




class Throw:
    def __init__(self, points, available_dice):
        self.points = points
        self.available_dice = available_dice

class GameStatus:
    def __init__(self, game):
        self.current_max_score = game.current_max_score()
        self.next_player_score = game.next_player_score()
        self.current_player_score = game.current_player_score()
        self.accumulated = game.accumulated
        self.available_dice = game.available_dice
        self.max_score = game.max_score

    def __str__(self):
        result = f'available dice: {self.available_dice}\n'
        result += f'accumulated: {self.accumulated}\n'
        result += f'score: {self.current_player_score}'
        return result
