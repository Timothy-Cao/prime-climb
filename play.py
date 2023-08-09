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
            return self.play_near_20(pawn, valid_moves) # Change playstyle here
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
        # Separate valid moves for each pawn
        valid_moves_pawn1 = {k: v for k, v in valid_moves.items() if v[0][0] == 0}
        valid_moves_pawn2 = {k: v for k, v in valid_moves.items() if v[0][0] == 1}

        # Evaluate move to rush one pawn
        def evaluate_move(move, details_list):
            best_evaluation = float('-inf')
            for details in details_list:
                _, _, operation, selected_die = details
                temp_pawn = pawn.copy()
                self.apply_move(temp_pawn, 0, (operation, selected_die))
                best_evaluation = max(best_evaluation, temp_pawn[0])
            return best_evaluation

        # Evaluate move to keep pawn2 close to 10
        def evaluate_move_pawn2(move, details_list):
            best_evaluation = float('-inf')
            for details in details_list:
                _, _, operation, selected_die = details
                temp_pawn = pawn.copy()
                self.apply_move(temp_pawn, 1, (operation, selected_die))
                if temp_pawn[1] >= 80 and operation == '*': # Prefer moves that multiply and get above 80
                    return 1000
                best_evaluation = max(best_evaluation, -abs(temp_pawn[1] - 10)) # Maximize closeness to 10
            return best_evaluation

        if valid_moves_pawn1:
            max_move_pawn1 = max(valid_moves_pawn1.keys(), key=lambda m: evaluate_move(m, valid_moves_pawn1[m]))
        else:
            max_move_pawn1 = None

        if valid_moves_pawn2:
            max_move_pawn2 = max(valid_moves_pawn2.keys(), key=lambda m: evaluate_move_pawn2(m, valid_moves_pawn2[m]))
        else:
            max_move_pawn2 = None

        # If there is a valid move for pawn1, prioritize it, otherwise choose the move for pawn2
        if max_move_pawn1 is not None:
            return max_move_pawn1, random.choice(valid_moves_pawn1[max_move_pawn1])
        elif max_move_pawn2 is not None:
            return max_move_pawn2, random.choice(valid_moves_pawn2[max_move_pawn2])
        else:
            return None # Handle the case where there are no valid moves

    def play_near_20(self, pawn, valid_moves):
        def evaluate_move(move, details_list, original_pawn):
            best_evaluation = float('-inf')
            for details in details_list:
                selected_pawn_index, _, operation, selected_die = details
                temp_pawn = original_pawn.copy()
                self.apply_move(temp_pawn, selected_pawn_index, (operation, selected_die))
                # Priority 1: Reach 101 on any pawn
                if temp_pawn[0] == 101 or temp_pawn[1] == 101:
                    return 10000
                # Priority 2: Multiply a pawn that is under 50 to above 80 but below 101
                if 80 < temp_pawn[selected_pawn_index] * selected_die < 101:
                    return 5000
                # Priority 3: If there are any pawns above 50, prioritize maximizing the sum of the pawns that are above 50
                if any(x > 50 for x in temp_pawn):
                    return sum(temp_pawn)
                # Priority 4: Get pawns below 50 to be as near 20 as possible
                best_evaluation = max(best_evaluation, -abs(temp_pawn[selected_pawn_index] - 20))
            return best_evaluation

        valid_moves_by_pawn = [
            {k: v for k, v in valid_moves.items() if v[0][0] == i}
            for i in range(2)
        ]

        max_moves = [
            max(moves.keys(), key=lambda m: evaluate_move(m, moves[m], pawn)) if moves else None
            for moves in valid_moves_by_pawn
        ]

        if max_moves[0] is not None:
            return max_moves[0], random.choice(valid_moves_by_pawn[0][max_moves[0]])
        elif max_moves[1] is not None:
            return max_moves[1], random.choice(valid_moves_by_pawn[1][max_moves[1]])
        else:
            return None # Handle the case where there are no valid moves



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

#Tests the behavior in playstyle used by player A.
def test_strategy(player_positions, dice_rolls):
    print("")
    game = AutoPrimeClimb()
    game.pawns['A'] = player_positions

    die1, die2 = dice_rolls

    print("\nCurrent board positions")
    for p, pos in game.pawns.items():
        print(f"{p}: {pos[0]}, {pos[1]}")

    print(f"Player A: Your dice rolls: {die1}, {die2}")

    pawn = game.pawns['A']

    # First move
    move_1, details_1 = game.play_move(pawn, die1, die2)
    print(f"First move: {move_1}")
    selected_pawn_index, _, operation, selected_die = details_1
    game.apply_move(pawn, selected_pawn_index, (operation, selected_die))

    # Determine the remaining die for the second move
    remaining_die = die1 if selected_die == die2 else die2

    # Second move
    move_2, details_2 = game.play_move(pawn, remaining_die)
    print(f"Second move: {move_2}")
    selected_pawn_index, _, operation, selected_die = details_2
    game.apply_move(pawn, selected_pawn_index, (operation, selected_die))

    print(f"New board positions for player A: {pawn[0]}, {pawn[1]}")


import random

if __name__ == "__main__":
    for _ in range(100):
        player_positions = [random.randint(0, 100), random.randint(0, 100)] # Random player positions
        dice_rolls = [random.randint(1, 10), random.randint(1, 10)]          # Random dice rolls
        test_strategy(player_positions, dice_rolls)


# if __name__ == "__main__":
#     game = AutoPrimeClimb()
#     game.play_game()
    
