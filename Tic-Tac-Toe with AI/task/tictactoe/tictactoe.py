import random
from typing import List, Sequence


class TicTacToe:
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
        """Counts 'X' or 'O' or ' ' elements on desk"""
        count = 0
        for row in self.nested_list_field:
            for el in row:
                if el == element:
                    count += 1
        return count

    def make_move(self):
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


class AI:
    def __init__(self, game_field, difficult):
        self.field = game_field
        self.difficult = difficult

    def AI_move(self):
        """AI makes move"""
        if not self.field.count_element(' '):
            return
        elif self.difficult == 'easy':
            self.easy_move()

        elif self.difficult == 'medium':
            pass

        elif self.difficult == 'hard':
            pass

    def easy_move(self):
        """Make easy move"""
        while True:
            coordinates = (random.randint(1, 3), random.randint(1, 3))
            validation_result = self.field.validate_coordinates(coordinates)
            if validation_result == 'Valid':
                print('Making move level "easy"')
                self.field.make_move()
                return


if __name__ == '__main__':
    game_field = TicTacToe()
    game_field.show_game_field()
    enemy = AI(game_field, 'easy')
    while True:
        coordinates = input('Enter the coordinates: ').split()
        validation_result = game_field.validate_coordinates(coordinates)
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
            game_field.make_move()
            game_field.show_game_field()
            enemy.AI_move()
            game_field.show_game_field()
            winner = game_field.check_winner()
            if winner:
                print(winner)
                break
