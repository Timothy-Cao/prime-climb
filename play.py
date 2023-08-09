from game import PrimeClimb
import random

class AutoPrimeClimb(PrimeClimb):
    def __init__(self):
        super().__init__(2)

    def play_game(self):
        import os
        
        turn_count = 0  # Add a variable to keep track of the turn count

        while True:

            player = self.player_order[self.current_player_index]
            pawn = self.pawns[player]

            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
            turn_count += 1
            print(f"Turn {turn_count}") 

            print("\nCurrent board positions")
            for p, pos in self.pawns.items():
                print(f"{p}: {pos[0]}, {pos[1]}")

            die1, die2 = self.roll_dice()
            print(f"Player {player}: Your dice rolls: {die1}, {die2}")

            # Get the valid moves
            valid_moves_1 = {**self.get_valid_moves(pawn, die1), **self.get_valid_moves(pawn, die2)}

            if self.current_player_index == 0:
                move_1 = random.choice(list(valid_moves_1.keys()))
            else:
                def evaluate_move(move):
                    # Clone the pawn's positions to test the move without altering the real pawn
                    temp_pawn = pawn.copy()
                    selected_pawn_index, _, operation, selected_die = random.choice(valid_moves_1[move])
                    self.apply_move(temp_pawn, selected_pawn_index, (operation, selected_die))
                    return sum(temp_pawn)
                move_1 = max(valid_moves_1.keys(), key=evaluate_move)

            selected_pawn_index, _, operation, selected_die = random.choice(valid_moves_1[move_1])
            self.apply_move(pawn, selected_pawn_index, (operation, selected_die))


            # Determine the remaining die for the second move
            remaining_die = die1 if selected_die == die2 else die2

            # Get the valid moves for the second move
            valid_moves_2 = self.get_valid_moves(pawn, remaining_die)

            if self.current_player_index == 0:
                move_2 = random.choice(list(valid_moves_2.keys()))
            else:
                def evaluate_move(move):
                    # Clone the pawn's positions to test the move without altering the real pawn
                    temp_pawn = pawn.copy()
                    selected_pawn_index, _, operation, selected_die = random.choice(valid_moves_2[move])
                    self.apply_move(temp_pawn, selected_pawn_index, (operation, selected_die))
                    return sum(temp_pawn)
                move_2 = max(valid_moves_2.keys(), key=evaluate_move)

            selected_pawn_index, _, operation, selected_die = random.choice(valid_moves_2[move_2])
            self.apply_move(pawn, selected_pawn_index, (operation, selected_die))


            if pawn[0] == 101 and pawn[1] == 101:
                print(f"Player {player} wins!")
                break

            self.current_player_index = (self.current_player_index + 1) % len(self.player_order)



if __name__ == "__main__":
    game = AutoPrimeClimb()
    game.play_game()
