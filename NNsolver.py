class InvalidMoveError(Exception):
    pass

class PrimeClimb:
    def __init__(self):
        self.pawns = [0, 0]

    def roll_dice(self):
        import random
        return random.randint(1, 10), random.randint(1, 10)

    def apply_move(self, pawn, move):
        operation, die = move
        new_position = self.pawns[pawn]
        if operation == '+':
            new_position += die
        elif operation == '-':
            new_position -= die
        elif operation == '*':
            new_position *= die
        elif operation == '/':
            if new_position % die == 0:
                new_position //= die
            else:
                raise InvalidMoveError("Cannot divide {} by {} evenly.".format(new_position, die))
        if new_position < 0 or new_position > 101:
            raise InvalidMoveError("Resulting position {} is outside the valid range (0-101).".format(new_position))
        self.pawns[pawn] = new_position

    def evaluate_tile(self, tile, goal=101):
        if goal == tile:
            return 100
        count_dice_pairs_to_goal = 0
        for die1 in range(1, 11):
            for die2 in range(1, 11):
                found_with_one_die = False
                for die in [die1, die2]:
                    if found_with_one_die:
                        break
                    for operation in ['+', '-', '*', '/']:
                        self.pawns[0] = tile
                        try:
                            self.apply_move(0, (operation, die))
                            if self.pawns[0] == goal:
                                found_with_one_die = True
                                break
                        except InvalidMoveError:
                            pass
                if found_with_one_die:
                    count_dice_pairs_to_goal += 1
                elif self.pawns[0] != goal:
                    for operation1 in ['+', '-', '*', '/']:
                        for operation2 in ['+', '-', '*', '/']:
                            for d1, d2 in [(die1, die2), (die2, die1)]:
                                self.pawns[0] = tile
                                try:
                                    self.apply_move(0, (operation1, d1))
                                    self.apply_move(0, (operation2, d2))
                                    if self.pawns[0] == goal:
                                        count_dice_pairs_to_goal += 1
                                        break
                                except InvalidMoveError:
                                    pass
        return count_dice_pairs_to_goal

    def find_best_move(self, dice_rolls):
        possible_moves = self.get_possible_moves(dice_rolls)
        best_move = None
        best_value = -float('inf')
        for move in possible_moves:
            pass
        return best_move

def main():
    '''
    game = PrimeClimb()
    for tile in range(102):
        score = game.evaluate_tile(tile)
        if score > 0:
            print(f"Score for tile {tile}: {score}")
    '''

if __name__ == "__main__":
    main()


def simulate_game(game, max_turns=100):
    state = 0
    actions = []
    for turn in range(max_turns):
        dice_rolls = game.roll_dice()
        best_move = game.find_best_move(dice_rolls)
        actions.append((state, dice_rolls[0], dice_rolls[1], best_move))
        state = best_move
        if state >= 101:
            return actions, 1000 - turn  # Reward for reaching 101 quickly
    return actions, state  # Reward based on final position

def generate_data(num_games=1000):
    game = PrimeClimb()
    data = []
    for _ in range(num_games):
        actions, score = simulate_game(game)
        data.extend([(state, die1, die2, best_move, score) for state, die1, die2, best_move in actions])
    return data

import numpy as np

data = generate_data()
data = np.array(data)
X = data[:, :4]
y = data[:, 4]

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential([
    Dense(32, activation='relu', input_shape=(4,)),
    Dense(32, activation='relu'),
    Dense(1, activation='linear') # regression output
])

model.compile(optimizer='adam', loss='mse')

model.fit(X, y, epochs=50, validation_split=0.1)
