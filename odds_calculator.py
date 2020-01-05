from itertools import groupby

from game import Game

class OddsCalculator():

    def __init__(self):
        self.odds = OddsCalculator.calculate_odds()

    def expected_points(self, num_dice):
        result = 0
        counts = self.odds[num_dice - 1]
        for k in counts:
            result += k * counts[k]
        return result

    def losing_probs(self, num_dice):
        return self.odds[num_dice - 1][0]


    @classmethod
    def calculate_odds(cls):
        points_count = [[],[],[],[],[]]
        points = cls.build_dice_string([], points_count, 0)
        result = []
        for i in range(5):
            current = {}
            counts = groupby(sorted(points[i]))
            for k, v in counts:
                count = len(list(v))
                possible = 6 ** (i + 1)
                current[k] = count/possible
            result.append(current)
        return result



    @classmethod
    def build_dice_string(cls, prefix, points_count, current_index):
        for i in range(1, 7):
            dice = prefix + [i]
            points = Game.dice_to_throw(dice).points
            points_count[current_index].append(points)
            if current_index < 4:
                points_count = cls.build_dice_string(dice, points_count, current_index + 1)
        return points_count

