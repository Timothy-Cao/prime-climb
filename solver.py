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
                # Check all combinations of dice and operations
                for die in [die1, die2]:
                    if found_with_one_die:
                        break # Skip checking the second die if the first one is already successful
                    for operation in ['+', '-', '*', '/']:
                        # Reset pawn position to the original tile
                        self.pawns[0] = tile
                        try:
                            self.apply_move(0, (operation, die))
                            if self.pawns[0] == goal:
                                # print(f"Success with dice: {die1},{die2} operation: {operation}, tile: {tile}")  # Log the successful combination
                                found_with_one_die = True
                                break  # No need to check further for this dice pair
                        except InvalidMoveError:
                            pass  # Skip invalid moves

                if found_with_one_die:
                    count_dice_pairs_to_goal += 1
                elif self.pawns[0] != goal: # Only check double operation if not successful with single die
                    for operation1 in ['+', '-', '*', '/']:
                        for operation2 in ['+', '-', '*', '/']:
                            # Try both permutations of the dice
                            for d1, d2 in [(die1, die2), (die2, die1)]:
                                # Reset pawn position to the original tile
                                self.pawns[0] = tile
                                try:
                                    self.apply_move(0, (operation1, d1))
                                    self.apply_move(0, (operation2, d2))
                                    if self.pawns[0] == goal:
                                        # print(f"Success with dice: {die1}, {die2}, operations: {operation1}, {operation2}, tile: {tile}")  # Log the successful combination
                                        count_dice_pairs_to_goal += 1
                                        break
                                except InvalidMoveError:
                                    pass  # Skip invalid moves

        return count_dice_pairs_to_goal


    def find_best_move(self, dice_rolls):
        # Determine the best two movements given the dice rolls
        possible_moves = self.get_possible_moves(dice_rolls)
        best_move = None
        best_value = -float('inf')
        
        for move in possible_moves:
            # Evaluate the move and update if it's the best found so far
            # You'll need to implement this logic
            pass
            
        return best_move

def main():
    # Create an instance of the PrimeClimb class
    game = PrimeClimb()

    # Loop through all tiles from 0 to 101 and evaluate the score for each
    for tile in range(102):
        score = game.evaluate_tile(tile)
        if score > 0:  # Print only if the score is non-zero
            print(f"Score for tile {tile}: {score}")


if __name__ == "__main__":
    main()
