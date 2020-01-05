from game import Game
from player import SensiblePlayer, OddsPlayer, VectorPlayer
from random import randrange

def simulate(times, vectors):
    sensible = SensiblePlayer('sensible')
    odds = OddsPlayer('odds')
    vector = VectorPlayer('vector', vectors)
    win_counts = {
        'sensible': 0,
        'odds': 0,
        'vector': 0
        }

    for i in range(1000):
        game = Game(10_000, 250)
        game.add_player(sensible)
        game.add_player(odds)
        game.add_player(vector)
        game.next_turn()
        win_counts[game.winner().name] += 1
    return win_counts

def vectors_mayhem(times, num_players):
    players = []
    win_counts = {}
    for i in range(num_players):
        vectors = [[randrange(-10, 10),randrange(-10, 10),randrange(-10, 10)],
                   [randrange(-10, 10),randrange(-10, 10),randrange(-10, 10)]]
        win_counts[str(vectors)] = 0
        players.append(VectorPlayer(str(vectors), vectors))
    for i in range(times):
        game = Game(10_000, 250)
        for p in players:
            game.add_player(p)
        game.next_turn()
        win_counts[game.winner().name] += 1
    return win_counts

        




if __name__ == "__main__":
    # print(vectors_mayhem(100, 3))
    vectors = [[randrange(-10, 10),randrange(-10, 10),randrange(-10, 10)],
               [randrange(-10, 10),randrange(-10, 10),randrange(-10, 10)]]

    print(simulate(1000, vectors))

