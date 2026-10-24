# @Filename: scanner.py
# @Author: codists
# @Created: 2026-08-01 09:58:04

from lox import Lox
from token_type import TokenType
from tokens import Token


class Scanner:
    start: int = 0
    current: int = 0
    line: int = 1

    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        print(f"scan_tokens: {self.tokens}")
        print(f"self.current: {self.current}")

        # todo 创建一种 EOF 类型的 TokenType, 作用是：
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        print(f"self.tokens: {self.tokens}")
        return self.tokens

    def scan_token(self) -> None:
        c = self.advance()
        print(f"current={self.current}, 字符: {c}")
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICLON)
            case "*":
                self.add_token(TokenType.STAR)
            # 两个字符构成的符号：!=,==, <=, >=
            case "=":
                # 判断下一个字符
                if self.match("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            # /: 1.除号。//: 2.注释：Lox 语言只支持单行注释。
            case "/":
                # 判断下一个字符是否是 /,如果是 /,则是注释，否则是除号。
                # 注释的形式：// [xxx]
                if self.match("/"):
                    print(f"注释匹配成功：current={self.current}, 字符: {self.source[self.current]}")
                    # 判断注释结束的逻辑：遇到换行符 \n
                    # while not self.is_at_end() and  self.source[self.current] != "\n":
                    #     print(f"current:{self.current}, 字符：{self.source[self.current]}")
                    #     self.advance()

                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            # 异常字符处理, 如: @#^
            case _:
                Lox.error(f"Unexpected character '{c}'")

    def match(self, expected: str) -> bool:
        """
        判断是否是某个字符
        :param expected:
        :return: 如果匹配成功， 返回 True, 否则返回 False
        """
        # 已经到达字符串末尾
        if self.is_at_end():
            return False

        # advance() 里面 current 已经往前移动 1 位，所以这里的 self.current 判断的是下一位字符
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        """

        :return:
        """
        # todo 源代码中的这部分不知道什么场景会出现，先注释
        # if self.is_at_end():
        #     return "\0"

        return self.source[self.current]

    def is_at_end(self) -> bool:
        """
        判断扫描是否结束
        :return:
        """
        # 理论上 self.current = len(self.source) 就判断出扫描结束了。这里用 >= 是一种防御性写法
        return self.current >= len(self.source)

    def advance(self) -> str:
        """
        获取当前字符,current 索引 +1
        :return: character
        """
        char = self.source[self.current]
        # 取出后 current 往前移动 1 位
        self.current += 1
        return char

    def add_token(self, type: TokenType, literal: object | None) -> None:
        text: str = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
