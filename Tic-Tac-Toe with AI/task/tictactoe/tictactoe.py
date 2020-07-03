import random
from abc import ABC, abstractmethod
from typing import List, Tuple


class TicTacToeField:
    """Game field"""

    def __init__(self):
        self.field = [[' ' for _ in range(3)] for _ in range(3)]
        self.turn = 'X'

    def print_game_field(self):
        """Prints game_field field to console"""
        print('---------')
        for row in self.field:
            print('|', end=' ')
            for element in row:
                print(element, end=' ')
            print('|', end='\n')
        print('---------')

    def get_empty_cells(self) -> List[Tuple]:
        """Finds all empty cells and returns it"""
        empty_cells = []
        for index_row, value_row in enumerate(self.field):
            for index_cell, value_cell in enumerate(value_row):
                if value_cell == ' ':
                    empty_cells.append((index_row, index_cell))
        return empty_cells

    def move(self, coordinates: Tuple[int, int]):
        """Makes a move"""
        x = coordinates[0]
        y = coordinates[1]
        self.field[x][y] = self.turn
        self.next_turn()

    def undo(self, coordinates: Tuple[int, int]):
        """Cancels the move"""
        x = coordinates[0]
        y = coordinates[1]
        self.field[x][y] = ' '
        self.next_turn()

    def next_turn(self):
        """Ends the current player’s turn and setups state for the next."""
        self.turn = 'X' if self.turn == 'O' else 'O'

    def check_winner(self) -> str:
        """Check who wins"""
        if self._win_condition('O'):
            return 'O'
        elif self._win_condition('X'):
            return 'X'
        elif not self.get_empty_cells():
            return 'Draw'

    def _win_condition(self, elem: str) -> bool:
        """Check wins conditions"""
        triple = [elem, elem, elem]

        row = self.field
        column = [[c[j] for c in self.field] for j in range(3)]
        diagonal = [row[i] for i, row in enumerate(self.field)]
        back_diagonal = [row[2 - i] for i, row in enumerate(self.field)]

        return any((triple in row, triple in column, diagonal == triple, back_diagonal == triple))


class AbstractPlayer(ABC):
    """Abstract player class for inheritance by other players"""

    def __init__(self, game_field: [TicTacToeField], mark: str):
        self.game_field = game_field
        self.coordinates = None
        self.mark = mark
        self.opponent_mark = 'X' if self.mark == 'O' else 'O'

    @abstractmethod
    def make_move(self):
        pass


class AI(AbstractPlayer):
    """AI player"""

    def __init__(self, game_field: [TicTacToeField], mark: str, difficult: str):
        super(AI, self).__init__(game_field, mark)
        self.difficult = difficult

    def make_move(self):
        """AI makes a move"""
        if self.difficult == 'easy':
            self.easy_move()

        elif self.difficult == 'medium':
            self.medium_move()

        elif self.difficult == 'hard':
            self.hard_move()
        print(f'Making move level "{self.difficult}"')

    def easy_move(self):
        """Makes a move of easy difficulty. Random move"""
        empty_cells = game_field.get_empty_cells()
        self.coordinates = random.choice(empty_cells)
        self.game_field.move(self.coordinates)

    def medium_move(self):
        """
        Makes a move of medium difficulty.
        If it can win in one move (if it has two in a row), it places a third to get three in a row and win.
        If the opponent can win in one move, it plays the third itself to block the opponent to win.
        Otherwise, it makes a easy (random) move.
        """
        for mark in (self.mark, self.opponent_mark):
            if self._get_priority_cell(mark):
                self.game_field.move(self.coordinates)
                return
        self.easy_move()

    def hard_move(self):
        """Finds the best move based on MiniMax Algorithm in Game Theory"""
        best_score = -2
        best_move = None
        for move in self.game_field.get_empty_cells():
            if len(self.game_field.get_empty_cells()) == 9:
                return self.easy_move()
            self.game_field.move(move)
            score = self.mini_max(False)
            self.game_field.undo(move)
            if score > best_score:
                best_score = score
                best_move = move
        self.game_field.move(best_move)

    def _get_priority_cell(self, mark: str) -> bool:
        """Get priority cell, return True if get it otherwise False"""

        # check for horizontal items in a row as two mark and empty one
        for row in range(len(self.game_field.field)):
            if self.game_field.field[row].count(mark) == 2 and self.game_field.field[row].count(
                    ' ') == 1:
                self.coordinates = [row, self.game_field.field[row].index(' ')]
                return True

        # check for vertical items in a row as two mark and empty one
        for col in range(len(self.game_field.field[0])):
            column = [self.game_field.field[row][col] for row in
                      range(len(self.game_field.field))]
            if column.count(mark) == 2 and column.count(' ') == 1:
                self.coordinates = [column.index(' '), col]
                return True

        # check the elements in a row diagonally from the upper left corner
        diagonal = [self.game_field.field[i][i] for i in range(len(self.game_field.field))]
        if diagonal.count(mark) == 2 and diagonal.count(' ') == 1:
            idx = diagonal.index(' ')
            self.coordinates = [idx, idx]
            return True

        # check the elements in a row diagonally from the lower left corner
        diagonal = [self.game_field.field[i][len(
            self.game_field.field) - 1 - i] for i in range(len(self.game_field.field))]
        if diagonal.count(mark) == 2 and diagonal.count(' ') == 1:
            idx = diagonal.index(' ')
            self.coordinates = [idx, len(self.game_field.field) - 1 - idx]
            return True

        return False

    def mini_max(self, is_max_turn: bool) -> int:
        """MiniMax Algorithm in Game Theory"""
        result = game_field.check_winner()

        if result == self.mark:
            return 1
        elif result == self.opponent_mark:
            return -1
        elif result == 'Draw':
            return 0

        scores = []
        for move in self.game_field.get_empty_cells():
            self.game_field.move(move)
            scores.append(self.mini_max(not is_max_turn))
            self.game_field.undo(move)

        return max(scores) if is_max_turn else min(scores)


class User(AbstractPlayer):
    """Real player"""
    CONVERT_COORDINATES = {
        ('1', '3'): (0, 0), ('2', '3'): (0, 1), ('3', '3'): (0, 2),
        ('1', '2'): (1, 0), ('2', '2'): (1, 1), ('3', '2'): (1, 2),
        ('1', '1'): (2, 0), ('2', '1'): (2, 1), ('3', '1'): (2, 2),
    }

    def make_move(self):
        """User makes a move"""
        while True:
            self.coordinates = tuple(input('Enter the coordinates: ').split())
            validation_result = self.validate_coordinates(self.coordinates)
            if validation_result == 'Not a Number':
                print('You should enter numbers!')
                continue
            elif validation_result == 'Incorrect coordinates':
                print('Coordinates should be from 1 to 3!')
                continue
            elif validation_result == 'Cell is occupied':
                print('This cell is occupied! Choose another one!')
                continue
            else:
                return self.game_field.move(self.coordinates)

    def validate_coordinates(self, coordinates: Tuple) -> str:
        """Input validation. Returns validation result"""
        try:
            x = int(coordinates[0])
            y = int(coordinates[1])
        except (ValueError, IndexError):
            return 'Not a Number'

        if not (1 <= x <= 3 and 1 <= y <= 3):
            return 'Incorrect coordinates'

        self.coordinates = self.CONVERT_COORDINATES.get(coordinates)
        if self.coordinates not in self.game_field.get_empty_cells():
            return 'Cell is occupied'
        return 'Valid'


class GameFactory:
    """Creates setup game"""

    def __init__(self, player_1: [User, AI], player_2: [User, AI], game_field: [TicTacToeField]):
        self.player_1 = User(game_field, mark='X') if player_1 == 'user' else AI(game_field, 'X', player_1)
        self.player_2 = User(game_field, mark='O') if player_2 == 'user' else AI(game_field, 'O', player_2)
        self.turn = self.player_1

    def next_move(self):
        """Makes a move and passes the move to another player."""
        self.turn.make_move()
        self.turn = self.player_1 if self.turn == self.player_2 else self.player_2


class ParametersError(Exception):
    pass


def parse_command():
    """Parse user commands for setup game"""
    game_configuration = ('user', 'easy', 'medium', 'hard')
    while True:
        command = input('Input command: ').split(' ')
        try:
            if len(command) == 1 and command[0] == 'exit':
                return 'break'
            elif len(command) == 3 and command[0] == 'start':
                if command[1] in game_configuration and command[2] in game_configuration:
                    player_1 = command[1]
                    player_2 = command[2]
                    return player_1, player_2
            else:
                raise ParametersError
        except (IndexError, ParametersError):
            print('Bad parameters!')


if __name__ == '__main__':
    while True:
        command = parse_command()
        if command == 'break':
            break

        player_1 = command[0]
        player_2 = command[1]

        game_field = TicTacToeField()
        game = GameFactory(player_1, player_2, game_field)
        game_field.print_game_field()
        while True:
            game.next_move()
            game_field.print_game_field()
            winner = game_field.check_winner()
            if winner:
                print(winner if winner == 'Draw' else f'{winner} wins!')
                break
