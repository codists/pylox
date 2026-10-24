# @Filename: token_type.py
# @Author: codists
# @Created: 2026-08-03 08:16:00
from enum import Enum, auto


class TokenType(Enum):

    # 单个 character
    # (
    LEFT_PAREN = auto()
    # )
    RIGHT_PAREN = auto()
    # {
    LEFT_BRACE = auto()
    # }
    RIGHT_BRACE = auto()
    # ,
    COMMA = auto()
    # .
    DOT = auto()
    # -
    MINUS = auto()
    # +
    PLUS = auto()
    # ;
    SEMICOLON = auto()
    # /
    SLASH = auto()
    # *
    STAR = auto()

    # 单个或者两个连在一起的 character
    # !
    BANG = auto()
    # !=
    BANG_EQUAL = auto()
    # =
    EQUAL = auto()
    # ==
    EQUAL_EQUAL = auto()
    # >
    GREATER = auto()
    # >=
    GREATER_EQUAL = auto()
    # <
    LESS = auto()
    # <=
    LESS_EQUAL = auto()

    # 关键字
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()