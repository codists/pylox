# @Filename: token.py
# @Author: 95232
# @Created: 2026-08-01 07:52:40
from typing import Any

from token_type import TokenType

class Token:
    # 这里的 literal Java 里面用的类型是 Object, Python 里面类型注解暂时用 Any
    def __init__(self, token_type: TokenType, lexeme: str, literal: Any, line: int) -> None:
        self.token_type = token_type
        self.lexeme  = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f'{self.token_type} {self.lexeme} {self.literal} {self.line}'


