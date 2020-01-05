from random import choice
from odds_calculator import OddsCalculator

class Player:
    
    def __init__(self, name):
        self.name = name

    def starts_over(self, game_status):
        pass

    def stays(self, game_status):
        pass

class RandomPlayer(Player):

    def starts_over(self, game_status):
        if game_status.available_dice == 5:
            return False
        return choice([True, False])

    def stays(self, game_status):
        return choice([True, False])

class RiskyPlayer(Player):

    def starts_over(self, game_status):
        return False

    def stays(self, game_status):
        if game_status.available_dice >= 3:
            return False
        if game_status.accumulated > 1000:
            return True
        return False

class SensiblePlayer(Player):

    def starts_over(self, game_status):
        ad = game_status.available_dice
        acc = game_status.accumulated
        if ad == 5:
            return False
        if ad == 4 and acc >= 200:
            return False
        if ad == 3 and acc >= 400:
            return False
        if ad == 2 and acc >= 800:
            return False
        if ad == 1 and acc >= 1000:
            return False
        return True
        

    def stays(self, game_status):
        ad = game_status.available_dice
        acc = game_status.accumulated
        score_to_win = game_status.max_score - game_status.current_player_score
        if acc >= score_to_win:
            return True
        if acc >= 250:
            return True
        if ad <= 4:
            return True
        return False

class OddsPlayer(Player):

    def __init__(self, name):
        self.odds = OddsCalculator()
        self.risk_tolerance = 0.1
        super().__init__(name)

    def starts_over(self, game_status):
        ad = game_status.available_dice
        acc = game_status.accumulated
        if acc > self.odds.expected_points(5 - ad):
            return False
        return True

    def stays(self, game_status):
        ad = game_status.available_dice
        acc = game_status.accumulated
        score_to_win = game_status.max_score - game_status.current_player_score
        if acc >= score_to_win:
            return True

        if self.odds.losing_probs(ad) > self.risk_tolerance:
            return True

        return False


class VectorPlayer(Player):

    def __init__(self, name, vectors):
        self.vectors = vectors
        super().__init__(name)

    def starts_over(self, game_status):
        ad = game_status.available_dice
        acc = game_status.accumulated
        score_to_win = game_status.max_score - game_status.current_player_score
        vector_a = [ad, acc, score_to_win]
        value = VectorPlayer.dot_product(vector_a, self.vectors[0])
        if value >= 0:
            return True
        return False

    @staticmethod
    def dot_product(a, b):
        return sum([a[i]*b[i] for i in range(len(b))])
 
    def stays(self, game_status):
        ad = game_status.available_dice
        acc = game_status.accumulated
        nps = game_status.next_player_score
        score_to_win = game_status.max_score - game_status.current_player_score
        if acc >= score_to_win:
            return True
        vector_a = [ad, acc, nps]
        value = VectorPlayer.dot_product(vector_a, self.vectors[0])
        if value >= 0:
            return True
        return False



