from game import PrimeClimb
import random

class AutoPrimeClimb(PrimeClimb):
    def __init__(self):
        super().__init__(2)

    def play_move(self, pawn, die1, die2=None):
        valid_moves = {**self.get_valid_moves(pawn, die1)}
        if die2:
            valid_moves.update(self.get_valid_moves(pawn, die2))

        if self.current_player_index == 0:
            return self.play_rush_one(pawn, valid_moves) # Change playstyle here
        else:
            return self.play_maximize_sum(pawn, valid_moves) # Change playstyle here

# -----------------------------------------------------PLAY STYLES -----------------------------------------------------
# -----------------------------------------------------PLAY STYLES -----------------------------------------------------
    def play_random(self, pawn, valid_moves):
        move = random.choice(list(valid_moves.keys()))
        return move, random.choice(valid_moves[move])

    def play_maximize_sum(self, pawn, valid_moves):
        def evaluate_move(move):
            temp_pawn = pawn.copy()
            selected_pawn_index, _, operation, selected_die = random.choice(valid_moves[move])
            self.apply_move(temp_pawn, selected_pawn_index, (operation, selected_die))
            return sum(temp_pawn)
            
        move = max(valid_moves.keys(), key=evaluate_move)
        return move, random.choice(valid_moves[move])

    def play_rush_one(self, pawn, valid_moves):
        # Separate moves for each pawn
        valid_moves_pawn0 = {key: value for key, value in valid_moves.items() if value[0][0] == 0}
        valid_moves_pawn1 = {key: value for key, value in valid_moves.items() if value[0][0] == 1}

        # If one pawn is on 10, try to roll a 10 to multiply by 10
        if pawn[1] == 10:
            for move, options in valid_moves_pawn1.items():
                for option in options:
                    if option[2] == "*" and option[3] == 10:
                        return move, option

        # Select the move that maximizes the sum of pawns but prioritizes the first pawn
        def evaluate_move(move, options):
            temp_pawn = pawn.copy()
            selected_pawn_index, _, operation, selected_die = random.choice(options)
            self.apply_move(temp_pawn, selected_pawn_index, (operation, selected_die))
            if selected_pawn_index == 0:
                return temp_pawn[0] * 100 + sum(temp_pawn)
            else:
                return sum(temp_pawn) - (temp_pawn[1] - 10)**2

        max_move_pawn0 = max(valid_moves_pawn0.keys(), key=lambda m: evaluate_move(m, valid_moves_pawn0[m]))
        max_move_pawn1 = max(valid_moves_pawn1.keys(), key=lambda m: evaluate_move(m, valid_moves_pawn1[m]))

        if evaluate_move(max_move_pawn0, valid_moves_pawn0[max_move_pawn0]) > evaluate_move(max_move_pawn1, valid_moves_pawn1[max_move_pawn1]):
            return max_move_pawn0, random.choice(valid_moves_pawn0[max_move_pawn0])
        else:
            return max_move_pawn1, random.choice(valid_moves_pawn1[max_move_pawn1])

# -----------------------------------------------------PLAY STYLES -----------------------------------------------------
# -----------------------------------------------------PLAY STYLES -----------------------------------------------------




        

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

            # First move
            move_1, (selected_pawn_index, _, operation, selected_die) = self.play_move(pawn, die1, die2)
            self.apply_move(pawn, selected_pawn_index, (operation, selected_die))

            # Determine the remaining die for the second move
            remaining_die = die1 if selected_die == die2 else die2

            # Second move
            move_2, (selected_pawn_index, _, operation, selected_die) = self.play_move(pawn, remaining_die)
            self.apply_move(pawn, selected_pawn_index, (operation, selected_die))

            if pawn[0] == 101 and pawn[1] == 101:
                print(f"Player {player} wins!")
                break

            self.current_player_index = (self.current_player_index + 1) % len(self.player_order)


if __name__ == "__main__":
    game = AutoPrimeClimb()
    game.play_game()
