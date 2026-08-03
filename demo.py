# @Filename: demo.py
# @Author: 95232
# @Created: 2026-08-01 00:39:40

# string = 'the beautiful white moon'
# white_space = ' '
#
# lexeme = ''
# for i, char in enumerate(string):
#     lexeme += char
#     # if i + 1 < len(string):
#     if string[i + 1] == white_space:
#         print(lexeme)
#         lexeme = ''

from enum import Enum


class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


print(Weekday(3))
