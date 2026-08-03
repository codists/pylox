# @Filename: scanner.py
# @Author: codists
# @Created: 2026-08-01 09:58:04
from token import Token


class Scanner:
    current = 0
    def __init__(self, source: str) -> None:
        self.source = source

    def scan_tokens(self) -> list[Token]:
        while (!is_at_end()):
            start = current
            scan_token()

    def is_at_end(self) -> bool:
        """
        判断扫描代码是否已经到末尾
        :return:
        """
        return current >= len(self.source)