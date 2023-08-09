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

import numpy as np
import random

def play_random_game():
    game = PrimeClimb()
    turns = 0
    while game.pawns[0] != 101 and game.pawns[1] != 101:
        die1, die2 = game.roll_dice()
        dice_to_use = [die1, die2]
        random.shuffle(dice_to_use)  

        for _ in range(2):
            die_to_use = dice_to_use.pop()
            valid_move_made = False

            # Keep trying until a valid move is made with the current die
            while not valid_move_made:
                pawn = random.choice([0, 1])  # Select a random pawn
                operation = random.choice(['+', '-', '*', '/'])
                move = (operation, die_to_use)
                try:
                    game.apply_move(pawn, move)
                    valid_move_made = True
                except InvalidMoveError as e:
                    pass  # Ignore the exception and retry with the same die
            
        turns += 1

    # print(f"Game over. It took {turns} turns.")
    return turns


def main():
    turn_counts = []
    for _ in range(10000):
        turn_counts.append(play_random_game())

    mean_turn_count = np.mean(turn_counts)
    median_turn_count = np.median(turn_counts)
    min_turn_count = np.min(turn_counts)
    max_turn_count = np.max(turn_counts)

    print(f"Mean turn count: {mean_turn_count}")
    print(f"Median turn count: {median_turn_count}")
    print(f"Min turn count: {min_turn_count}")
    print(f"Max turn count: {max_turn_count}")

main()
