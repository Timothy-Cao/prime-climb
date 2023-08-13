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
                                        if (tile == 95 or tile == 96):
                                            print(operation1,d1,operation2,d2)
                                        count_dice_pairs_to_goal += 1
                                        break
                                except InvalidMoveError:
                                    pass
        return count_dice_pairs_to_goal

    def evaluate_tile_degree_2(self, tile, goal=101):
        degree_2_score = 0

        for die1 in range(1, 11):
            for die2 in range(1, 11):
                for die3 in range(1, 11):
                    for die4 in range(1, 11):
                        self.pawns[0] = tile
                        best_tile_after_first_move = 0
                        best_score_after_first_move = -1
                        # Iterate through possible first pair of rolls
                        for operation1 in ['+', '-', '*', '/']:
                            for operation2 in ['+', '-', '*', '/']:
                                for d1, d2 in [(die1, die2), (die2, die1)]:
                                    self.pawns[0] = tile
                                    try:
                                        self.apply_move(0, (operation1, d1))
                                        self.apply_move(0, (operation2, d2))
                                        score_after_first_move = self.evaluate_tile(self.pawns[0], goal)
                                        if score_after_first_move > best_score_after_first_move or \
                                        (score_after_first_move == best_score_after_first_move and self.pawns[0] > best_tile_after_first_move):
                                            best_tile_after_first_move = self.pawns[0]
                                            best_score_after_first_move = score_after_first_move
                                    except InvalidMoveError:
                                        pass

                        # Using the best tile from the first pair of rolls to find score after second pair
                        self.pawns[0] = best_tile_after_first_move
                        for operation1 in ['+', '-', '*', '/']:
                            for operation2 in ['+', '-', '*', '/']:
                                for d1, d2 in [(die3, die4), (die4, die3)]:
                                    self.pawns[0] = best_tile_after_first_move
                                    try:
                                        self.apply_move(0, (operation1, d1))
                                        self.apply_move(0, (operation2, d2))
                                        if self.pawns[0] == goal:
                                            degree_2_score += 1
                                    except InvalidMoveError:
                                        pass

        return degree_2_score

    def find_best_move(self, dice_rolls):
        possible_moves = self.get_possible_moves(dice_rolls)
        best_move = None
        best_value = -float('inf')
        for move in possible_moves:
            pass
        return best_move


def get_scoring():
    game = PrimeClimb()
    scoring = {}
    for tile in range(101): # Including 100, so the range goes up to 101
        score = game.evaluate_tile(tile)
        if score > 0:
            scoring[tile] = score
            print(f"Score for tile {tile}: {score}")
    return scoring

def get_degree_2_scoring():
    game = PrimeClimb()
    degree_2_scoring = {}
    for tile in range(101):
        score = game.evaluate_tile_degree_2(tile)
        if score > 0:
            degree_2_scoring[tile] = score
            print(f"Degree-2-Score for tile {tile}: {score}")
    return degree_2_scoring


def main():
    scoring = get_scoring()
    print("\nComplete scoring:")
    for tile, score in sorted(scoring.items()):
        print(f"Tile {tile}: {score}")

if __name__ == '__main__':
    main()
