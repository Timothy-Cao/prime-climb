from game import PrimeClimb
import random

class AutoPrimeClimb(PrimeClimb):
    def __init__(self):
        super().__init__(2)

    def play_game(self):
        import os

        while True:
            player = self.player_order[self.current_player_index]
            pawn = self.pawns[player]

            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            print("\nCurrent board positions")
            for p, pos in self.pawns.items():
                print(f"{p}: {pos[0]}, {pos[1]}")

            die1, die2 = self.roll_dice()
            print(f"Player {player}: Your dice rolls: {die1}, {die2}")

            # Get the valid moves
            valid_moves = self.get_valid_moves(pawn, die1, die2)

            # First player randomly picks a move, second player picks the move that maximizes total sum
            if self.current_player_index == 0:
                move_1 = random.choice(list(valid_moves.keys()))
            else:
                move_1 = max(valid_moves.keys(), key=lambda x: sum(self.apply_move(pawn, *valid_moves[x])))

            selected_pawn_index, _, operation, selected_die = random.choice(valid_moves[move_1])
            self.apply_move(pawn, selected_pawn_index, (operation, selected_die))

            # Determine the remaining die for the second move
            remaining_die = die1 if selected_die == die2 else die2

            # Continue the game with the second move
            # ... (repeat similar code for the second move)

            if pawn[0] == 101 and pawn[1] == 101:
                print(f"Player {player} wins!")
                break

            self.current_player_index = (self.current_player_index + 1) % len(self.player_order)


if __name__ == "__main__":
    game = AutoPrimeClimb()
    game.play_game()
