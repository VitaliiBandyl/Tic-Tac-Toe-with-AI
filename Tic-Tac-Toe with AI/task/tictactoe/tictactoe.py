import random
from abc import ABC, abstractmethod
from typing import List, Sequence


class TicTacToeField:
    def __init__(self, string_desk: str = '_________'):
        self.string_field = string_desk
        self.nested_list_field = self._convert_field_to_nested_list()
        self._x = None
        self._y = None
        self.X = self.count_element('X')
        self.O = self.count_element('O')

    def _convert_field_to_nested_list(self) -> List[List]:
        """Replaces underscores to spaces and convert field to nested list"""
        cleaned_field = self.string_field.replace('_', ' ')
        nested_list = []
        index = 0
        for i in range(3):
            list_ = []
            for j in range(3):
                list_.append(cleaned_field[index])
                index += 1
            nested_list.append(list_)
        return nested_list

    def show_game_field(self):
        """Prints game_field field to console"""
        print('---------')
        for row in self.nested_list_field:
            print('|', end=' ')
            for element in row:
                print(element, end=' ')
            print('|', end='\n')
        print('---------')

    def validate_coordinates(self, coordinates: Sequence) -> str:
        """Input validation. Returns validation result"""
        try:
            x = int(coordinates[0])
            y = int(coordinates[1])
        except (ValueError, IndexError):
            return 'Not a Number'

        if not (1 <= x <= 3 and 1 <= y <= 3):
            return 'Incorrect coordinates'

        if self._is_empty_space(x, y):
            return 'Valid'
        return 'Cell is occupied'

    def _is_empty_space(self, x: int, y: int) -> bool:
        """Checks if selected cell is empty"""
        self._convert_coordinate(x, y)
        if self.nested_list_field[self._x][self._y] == ' ':
            return True
        return False

    def _convert_coordinate(self, x, y):
        """Convert enumeration to default in python, from left top to right bottom"""
        if x == 1 and y == 3:
            self._x, self._y = 0, 0
        elif x == 2 and y == 3:
            self._x, self._y = 0, 1
        elif x == 3 and y == 3:
            self._x, self._y = 0, 2
        elif x == 1 and y == 2:
            self._x, self._y = 1, 0
        elif x == 2 and y == 2:
            self._x, self._y = 1, 1
        elif x == 3 and y == 2:
            self._x, self._y = 1, 2
        elif x == 1 and y == 1:
            self._x, self._y = 2, 0
        elif x == 2 and y == 1:
            self._x, self._y = 2, 1
        elif x == 3 and y == 1:
            self._x, self._y = 2, 2

    def count_element(self, element: str) -> int:
        """Counts 'X' or 'O' or ' ' elements on desk to check whose turn"""
        count = 0
        for row in self.nested_list_field:
            for el in row:
                if el == element:
                    count += 1
        return count

    def move(self):
        """Make move"""
        if self.O < self.X:
            self.nested_list_field[self._x][self._y] = 'O'
            self.O = self.count_element('O')
        else:
            self.nested_list_field[self._x][self._y] = 'X'
            self.X = self.count_element('X')

    def check_winner(self):
        """Check who wins"""
        if self._win_condition('O'):
            return 'O wins'
        elif self._win_condition('X'):
            return 'X wins'
        elif not self.count_element(' '):
            return 'Draw'

    def _win_condition(self, elem: str):
        """Check wins conditions"""
        win_conditions = any([
            elem == self.nested_list_field[0][0] == self.nested_list_field[0][1] == self.nested_list_field[0][2],
            elem == self.nested_list_field[1][0] == self.nested_list_field[1][1] == self.nested_list_field[1][2],
            elem == self.nested_list_field[2][0] == self.nested_list_field[2][1] == self.nested_list_field[2][2],
            elem == self.nested_list_field[0][0] == self.nested_list_field[1][0] == self.nested_list_field[2][0],
            elem == self.nested_list_field[0][1] == self.nested_list_field[1][1] == self.nested_list_field[2][1],
            elem == self.nested_list_field[0][2] == self.nested_list_field[1][2] == self.nested_list_field[2][2],
            elem == self.nested_list_field[0][0] == self.nested_list_field[1][1] == self.nested_list_field[2][2],
            elem == self.nested_list_field[0][2] == self.nested_list_field[1][1] == self.nested_list_field[2][0],
        ])

        if win_conditions:
            return True
        return False

    @property
    def cursor_coordinates(self):
        return self._x, self._y

    @cursor_coordinates.setter
    def cursor_coordinates(self, coordinates: List[int]):
        self._x = coordinates[0]
        self._y = coordinates[1]


class AbstractPlayer(ABC):
    """Abstract player class for inheritance by other players"""
    def __init__(self, game_field, mark):
        self.game_field = game_field
        self.mark = mark
        self.opponent_mark = 'X' if self.mark == 'O' else 'O'

    @abstractmethod
    def make_move(self):
        pass


class AI(AbstractPlayer):
    def __init__(self, game_field, mark, difficult):
        super(AI, self).__init__(game_field, mark)
        self.difficult = difficult
        self.coordinates = None

    def make_move(self):
        """AI makes move"""
        if not self.game_field.count_element(' '):
            return

        elif self.difficult == 'easy':
            self._easy_move()

        elif self.difficult == 'medium':
            self._medium_move()

        elif self.difficult == 'hard':
            pass

    def _easy_move(self):
        """Make easy move. Random move"""
        while True:
            self.coordinates = (random.randint(1, 3), random.randint(1, 3))
            validation_result = self.game_field.validate_coordinates(self.coordinates)
            if validation_result == 'Valid':
                print(f'Making move level "{self.difficult}"')
                self.game_field.move()
                return

    def _medium_move(self):
        """Make medium move"""
        for mark in (self.mark, self.opponent_mark):
            if self._get_priority_cell(mark):
                self.game_field.cursor_coordinates = self.coordinates
                print(f'Making move level "{self.difficult}"')
                self.game_field.move()
                return
        self._easy_move()

    def _get_priority_cell(self, mark):
        """Get priority cell, return True if get it otherwise False"""

        # check for horizontal items in a row as two mark and empty one
        for row in range(len(self.game_field.nested_list_field)):
            if self.game_field.nested_list_field[row].count(mark) == 2 and self.game_field.nested_list_field[row].count(' ') == 1:
                self.coordinates = [row, self.game_field.nested_list_field[row].index(' ')]
                return True

        # check for vertical items in a row as two mark and empty one
        for col in range(len(self.game_field.nested_list_field[0])):
            column = [self.game_field.nested_list_field[row][col] for row in range(len(self.game_field.nested_list_field))]
            if column.count(mark) == 2 and column.count(' ') == 1:
                self.coordinates = [column.index(' '), col]
                return True

        # check the elements in a row diagonally from the upper left corner
        diag = [self.game_field.nested_list_field[i][i] for i in range(len(self.game_field.nested_list_field))]
        if diag.count(mark) == 2 and diag.count(' ') == 1:
            idx = diag.index(' ')
            self.coordinates = [idx, idx]
            return True

        # check the elements in a row diagonally from the lower left corner
        diag = [self.game_field.nested_list_field[i][len(
            self.game_field.nested_list_field) - 1 - i] for i in range(len(self.game_field.nested_list_field))]
        if diag.count(mark) == 2 and diag.count(' ') == 1:
            idx = diag.index(' ')
            self.coordinates = [idx, len(self.game_field.nested_list_field) - 1 - idx]
            return True

        return False


class User(AbstractPlayer):
    """Real player"""
    def make_move(self):
        """User makes move"""
        while True:
            coordinates = input('Enter the coordinates: ').split()
            validation_result = self.game_field.validate_coordinates(coordinates)
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
                return self.game_field.move()


class GameFactory:
    """Creates setup game"""
    def __init__(self, player_1, player_2, game_field):
        self.player_1 = User(game_field, mark='X') if player_1 == 'user' else AI(game_field, 'X', player_1)
        self.player_2 = User(game_field, mark='O') if player_2 == 'user' else AI(game_field, 'O', player_2)


class ParametersError(Exception):
    pass


def parse_command():
    """Parse user commands for setup game"""
    game_configuration = ('user', 'easy', 'medium')
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
        game_field.show_game_field()
        while True:
            game.player_1.make_move()
            game_field.show_game_field()
            winner = game_field.check_winner()
            if winner:
                print(winner)
                break

            game.player_2.make_move()
            game_field.show_game_field()
            winner = game_field.check_winner()
            if winner:
                print(winner)
                break
