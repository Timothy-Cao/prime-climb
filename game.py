class InvalidMoveError(Exception):
    pass

class PrimeClimb:
    def __init__(self, player_count):
        self.pawns = {chr(65 + i): [0, 0] for i in range(player_count)}
        self.current_player_index = 0
        self.player_order = list(self.pawns.keys())

    def roll_dice(self):
        import random
        return random.randint(1, 10), random.randint(1, 10)

    def apply_move(self, pawn, piece_index, move):
        operation, die = move
        new_position = pawn[piece_index]
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
        pawn[piece_index] = new_position

    def get_valid_moves(self, pawn, die):
        valid_moves = {}
        for piece_index in range(2):  # Iterate over both pieces
            for operation in ['+', '-', '*', '/']:
                original_position = pawn[piece_index]
                try:
                    self.apply_move(pawn, piece_index, (operation, die))
                    key = f"{original_position}{operation}{die}"
                    if key not in valid_moves:
                        valid_moves[key] = []
                    valid_moves[key].append((piece_index, original_position, operation, die))
                except InvalidMoveError:
                    pass
                finally:
                    pawn[piece_index] = original_position
        return valid_moves

    def play_game(self):

        from random import choice

        while True:
            player = self.player_order[self.current_player_index]
            pawn = self.pawns[player]
            print("\nCurrent board positions")
            for p, pos in self.pawns.items():
                print(f"{p}: {pos[0]}, {pos[1]}")

            die1, die2 = self.roll_dice()
            print(f"Player {player}: Your dice rolls: {die1}, {die2}")

            # First move
            valid_moves_1 = {**self.get_valid_moves(pawn, die1), **self.get_valid_moves(pawn, die2)}
            move_1 = None
            while move_1 not in valid_moves_1:
                print("Enter the number for a valid move:")
                for idx, move in enumerate(valid_moves_1.keys()):
                    print(f"{idx + 1}) {move}")
                try:
                    move_1 = list(valid_moves_1.keys())[int(input()) - 1]
                except (ValueError, IndexError):
                    continue

            # Randomly select a pawn if there are duplicates
            selected_pawn_index, _, operation, selected_die = choice(valid_moves_1[move_1])
            self.apply_move(pawn, selected_pawn_index, (operation, selected_die))


            # Determine the remaining die for the second move
            remaining_die = die1 if selected_die == die2 else die2

            # Second move
            print(f"\nCurrent board positions")
            for p, pos in self.pawns.items():
                print(f"{p}: {pos[0]}, {pos[1]}")
            print(f"Player {player}: Your dice rolls: {remaining_die}")
            valid_moves_2 = self.get_valid_moves(pawn, remaining_die)

            move_2 = None
            while move_2 not in valid_moves_2:
                print("Enter the number for a valid move:")
                for idx, move in enumerate(valid_moves_2.keys()):
                    print(f"{idx + 1}) {move}")
                try:
                    move_2 = list(valid_moves_2.keys())[int(input()) - 1]
                except (ValueError, IndexError):
                    continue

            # Randomly select a pawn if there are duplicates
            selected_pawn_index, _, operation, selected_die = choice(valid_moves_2[move_2])
            self.apply_move(pawn, selected_pawn_index, (operation, selected_die))



            if pawn[0] == 101 and pawn[1] == 101:
                print(f"Player {player} wins!")
                break

            self.current_player_index = (self.current_player_index + 1) % len(self.player_order)

def main():
    player_count = int(input("Enter player count (1-4): "))
    if player_count < 1 or player_count > 4:
        print("Player count must be between 1 and 4.")
        return
    game = PrimeClimb(player_count)
    game.play_game()

if __name__ == "__main__":
    main()
