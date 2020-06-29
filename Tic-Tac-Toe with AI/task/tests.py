from hstest.stage_test import *
from hstest.test_case import TestCase
from enum import Enum
from typing import List, Optional
from copy import deepcopy

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class FieldState(Enum):
    X = 'X'
    O = 'O'
    FREE = ' '


def get_state(symbol):
    if symbol == 'X':
        return FieldState.X
    elif symbol == 'O':
        return FieldState.O
    elif symbol == ' ' or symbol == '_':
        return FieldState.FREE
    else:
        return None


class TicTacToeField:

    def __init__(self, *, field: str = '', constructed=None):

        if constructed is not None:
            self.field = deepcopy(constructed)

        else:
            self.field: List[List[Optional[FieldState]]] = [
                [None for _ in range(3)] for _ in range(3)
            ]

            for row in range(3):
                for col in range(3):
                    index = (2 - row) * 3 + col
                    self.field[row][col] = get_state(field[index])

    def equal_to(self, other) -> bool:
        for i in range(3):
            for j in range(3):
                if self.field[i][j] != other.field[i][j]:
                    return False
        return True

    def has_next_as(self, other) -> bool:
        improved: bool = False
        for i in range(3):
            for j in range(3):
                if self.field[i][j] != other.field[i][j]:
                    if self.field[i][j] == FieldState.FREE and not improved:
                        improved = True
                    else:
                        return False
        return improved

    def differ_by_one(self, other) -> bool:
        have_single_difference = False
        for i in range(3):
            for j in range(3):
                if self.field[i][j] != other.field[i][j]:
                    if have_single_difference:
                        return False
                    have_single_difference = True
        return have_single_difference

    def is_close_to(self, other) -> bool:
        return (
            self.equal_to(other)
            or self.has_next_as(other)
            or other.has_next_as(self)
        )

    @staticmethod
    def parse(field_str: str):

        lines = field_str.splitlines()
        lines = [i.strip() for i in lines]
        lines = [i for i in lines if
                 i.startswith('|') and i.endswith('|')]

        for line in lines:
            if len(line) != 9:
                raise WrongAnswerException(
                    f"Line of Tic-Tac-Toe field should be 9 characters long\n"
                    f"found {len(line)} characters in \"{line}\"")
            for c in line:
                if c not in 'XO|_ ':
                    return None

        field: List[List[Optional[FieldState]]] = [
            [None for _ in range(3)] for _ in range(3)
        ]

        y: int = 2

        for line in lines:
            cols = line[2], line[4], line[6]
            x: int = 0
            for c in cols:
                state = get_state(c)
                if state is None:
                    return None
                field[y][x] = state
                x += 1
            y -= 1

        return TicTacToeField(constructed=field)

    @staticmethod
    def parse_all(output: str):
        fields = []

        lines = output.splitlines()
        lines = [i.strip() for i in lines]
        lines = [i for i in lines if len(i) > 0]

        candidate_field = ''
        inside_field = False
        for line in lines:
            if '----' in line and not inside_field:
                inside_field = True
                candidate_field = ''
            elif '----' in line and inside_field:
                field = TicTacToeField.parse(candidate_field)
                if field is not None:
                    fields += [field]
                inside_field = False

            if inside_field and line.startswith('|'):
                candidate_field += line + '\n'

        return fields


inputs = [
    "1 1", "1 2", "1 3",
    "2 1", "2 2", "2 3",
    "3 1", "3 2", "3 3"
]


def iterate_cells(initial: str) -> str:
    index: int = -1
    for i in range(len(inputs)):
        if initial == inputs[i]:
            index = i
            break

    if index == -1:
        return ''

    full_input: str = ''
    for i in range(index, index + 9):
        full_input += inputs[i % len(inputs)] + '\n'

    return full_input


class TicTacToeTest(StageTest):
    def generate(self) -> List[TestCase]:
        tests: List[TestCase] = [
            TestCase(
                stdin="_XXOO_OX_\n1 3",
                attach=("_XXOO_OX_", "XXXOO_OX_", "X wins")
            ),
            TestCase(
                stdin="_XXOO_OX_\n1 1\n1 3",
                attach=("_XXOO_OX_", "XXXOO_OX_", "X wins",
                        "This cell is occupied! Choose another one!")
            ),
            TestCase(
                stdin="_XXOO_OX_\n1 4\n1 3",
                attach=("_XXOO_OX_", "XXXOO_OX_", "X wins",
                        "Coordinates should be from 1 to 3!")
            ),
            TestCase(
                stdin="_XXOO_OX_\none\n1 3",
                attach=("_XXOO_OX_", "XXXOO_OX_", "X wins",
                        "You should enter numbers!")
            ),
            TestCase(
                stdin="_XXOO_OX_\none three\n1 3",
                attach=("_XXOO_OX_", "XXXOO_OX_", "X wins",
                        "You should enter numbers!")
            ),
            TestCase(
                stdin="_XXOO_OX_\n3 2",
                attach=("_XXOO_OX_", "_XXOOXOX_", "Game not finished")
            ),
            TestCase(
                stdin="_XXOO_OX_\n3 1",
                attach=("_XXOO_OX_", "_XXOO_OXX", "Game not finished")
            ),


            TestCase(
                stdin="OXXXOOOX_\n3 1",
                attach=("OXXXOOOX_", "OXXXOOOXX", "Draw")
            ),


            TestCase(
                stdin="XX_XOXOO_\n3 3",
                attach=("XX_XOXOO_", "XXOXOXOO_", "O wins")
            ),
            TestCase(
                stdin="XX_XOXOO_\n3 1",
                attach=("XX_XOXOO_", "XX_XOXOOO", "O wins")
            ),


            TestCase(
                stdin="_XO_OX___\n1 3",
                attach=("_XO_OX___", "XXO_OX___", "Game not finished")
            ),
            TestCase(
                stdin="_XO_OX___\n1 2",
                attach=("_XO_OX___", "_XOXOX___", "Game not finished")
            ),
            TestCase(
                stdin="_XO_OX___\n1 1",
                attach=("_XO_OX___", "_XO_OXX__", "Game not finished")
            ),
            TestCase(
                stdin="_XO_OX___\n2 1",
                attach=("_XO_OX___", "_XO_OX_X_", "Game not finished")
            ),
            TestCase(
                stdin="_XO_OX___\n3 1",
                attach=("_XO_OX___", "_XO_OX__X", "Game not finished")
            ),


            TestCase(
                stdin="_XO_OX__X\n1 3",
                attach=("_XO_OX__X", "OXO_OX__X", "Game not finished")
            ),
            TestCase(
                stdin="_XO_OX__X\n1 2",
                attach=("_XO_OX__X", "_XOOOX__X", "Game not finished")
            ),
            TestCase(
                stdin="_XO_OX__X\n1 1",
                attach=("_XO_OX__X", "_XO_OXO_X", "O wins")
            ),
            TestCase(
                stdin="_XO_OX__X\n2 1",
                attach=("_XO_OX__X", "_XO_OX_OX", "Game not finished")
            ),


            TestCase(
                stdin="XO_OXOX__\n3 3",
                attach=("XO_OXOX__", "XOXOXOX__", "X wins")
            ),
            TestCase(
                stdin="XO_OXOX__\n2 1",
                attach=("XO_OXOX__", "XO_OXOXX_", "Game not finished")
            ),
            TestCase(
                stdin="XO_OXOX__\n3 1",
                attach=("XO_OXOX__", "XO_OXOX_X", "X wins")
            ),
        ]

        return tests

    def check(self, reply: str, attach: str) -> CheckResult:

        if len(attach) == 4:
            stdin, result, state, additional = attach
        else:
            stdin, result, state = attach
            additional = None

        fields = TicTacToeField.parse_all(reply)

        if len(fields) != 2:
            return CheckResult.wrong(
                f"You should output exactly 2 fields, found: {len(fields)}"
            )

        curr: TicTacToeField = fields[0]
        next: TicTacToeField = fields[1]

        correct_curr = TicTacToeField(field=stdin)
        correct_next = TicTacToeField(field=result)

        reply = [line.strip() for line in reply.splitlines()
                 if len(line.strip()) != 0]

        last_line = reply[-1]

        if last_line != state:
            return CheckResult.wrong(
                "The final result is wrong. Should be \""
                + state + "\", found: \"" + last_line + "\""
            )

        if additional is not None:

            if len([line for line in reply if additional in line]) == 0:
                return CheckResult.wrong(
                    "Output should contain a line \""
                    + additional + "\", but this line wasn't found."
                )

        if not curr.equal_to(correct_curr):
            return CheckResult.wrong(
                "The first field is not equal to the input field " + stdin
            )

        if curr.equal_to(next):
            return CheckResult.wrong(
                "The first field is equals to the second, " +
                "but should be different"
            )

        if not next.equal_to(correct_next):
            return CheckResult.wrong(
                "The first field is correct, but the second is not"
            )

        return CheckResult.correct()


if __name__ == '__main__':
    TicTacToeTest('tictactoe.tictactoe').run_tests()
