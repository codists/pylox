# @Filename: scanner.py
# @Author: codists
# @Created: 2026-08-01 09:58:04

from lox import Lox
from token_type import TokenType
from tokens import Token


class Scanner:
    keywords: dict[str, TokenType] = {
        "add": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "return": TokenType.RETURN,
        "print": TokenType.PRINT,
        "super": TokenType.SUPER,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> list[Token]:
        """
        处理所有的 lexeme
        :return:
        """
        while not self.is_at_end():
            # 每处理完一个 lexeme, self.start 更新为下一个 lexeme 的开始索引
            self.start = self.current
            self.scan_token()

        # todo 创建一种 EOF 类型的 TokenType, 作用是：
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        """
        处理单个 lexeme
        :return:
        """
        c = self.advance()
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
                self.add_token(TokenType.SEMICOLON)
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
                    # 判断注释结束的逻辑：遇到换行符 \n
                    # while not self.is_at_end() and  self.source[self.current] != "\n":
                    #     print(f"current:{self.current}, 字符：{self.source[self.current]}")
                    #     self.advance()

                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            # ' ': 按键盘的空格键(space bar, 最长的那个按键)会出现这种情况
            # '\r': 这里其实是换行符的一部分，一般来说，在 Window 系统的软件上按 Enter 键会出现这种情况，按 Enter 键时，
            # 行尾会追加 \r\n
            # '\t': 按键盘的 Tab 键会出现这种情况。
            case " " | "\r" | "\t":
                pass
            # \n: 一般来说, 在 Linux 系统输入时, 按 Enter 键的时候会出现这种情况.按 Enter 键时，行尾会追加 \n。
            case "\n":
                self.line += 1

            # 字符串(STRING)
            # '"' 也可以写成 "\""
            case '"':
                # 判断是否是右引号？
                literal_string = ""
                while self.peek() != '"' and not self.is_at_end():
                    data = self.advance()

                    # 字符串中包含换行符
                    if data == "\n":
                        self.line += 1

                    literal_string += data

                # 缺失右双引号
                if self.is_at_end():
                    Lox.error(self.line, f"右双引号缺失(Unexpected character) {c}")
                    # 这里要返回，以免不完整的字符串(如："123 )被添加到 Token
                    return

                # 如果没有到达代码末尾，消耗掉右双引号
                if not self.is_at_end():
                    self.advance()

                self.add_token(TokenType.STRING, literal_string)

            # 数字(NUMBER)
            # case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
            case _ if self.is_digit(c):
                # 遍历，如果是数字，则继续往下
                while self.is_digit(self.peek()):
                    self.advance()
                # 遍历的时候如果遇到点，则判断下一个字符是数字还是点，是数字表明是小数，继续，如果不是则结束
                if self.peek() == "." and self.is_digit(self.source[self.current + 1]):
                    self.advance()
                    while self.is_digit(self.peek()):
                        self.advance()

                self.add_token(TokenType.NUMBER, float(self.source[self.start: self.current]))
            # 异常字符处理, 如: @#^
            case _:
                if (self.is_alpha(c)):
                    self.identifier()
                else:
                    Lox.error(self.line, f"Unexpected character {c}")

    def identifier(self) -> None:
        while (self.is_alpha_numeric(self.peek())):
            self.advance()
        text = self.source[self.start: self.current]
        token_type = Scanner.keywords.get(text)

        # 如果text不在 keywords 里，那就是标识符
        if token_type is None:
            token_type = TokenType.IDENTIFIER

        self.add_token(token_type)

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
        获取当前字符

        :return:
        """
        # todo 源代码中的这部分不知道什么场景会出现，先注释
        if self.is_at_end():
            return "\0"

        return self.source[self.current]

    def peek_next(self) -> str:
        """
        获取下一个字符

        :return:
        """
        return self.source[self.current + 1]

    def is_alpha(self, c: str) -> bool:
        """
        判断是否是字母(alphabet)
        :param c: 字符
        :return: 如果字符 c 是字母， 返回 True, 否则返回 False
        """
        return "a" <= c <= "z" or "A" <= c <= "Z" or c == "_"

    def is_alpha_numeric(self, c: str) -> bool:
        """
        判断是否是字母(alphabet)或者数字
        :param c: 字符
        :return: 如果字符 c 是字母或数字， 返回 True, 否则返回 False
        """
        return self.is_alpha(c) or self.is_digit(c)

    def is_digit(self, c: str) -> bool:
        """
        判断字符是否是 "0123456789" 中的一个。虽然 Python 内置库有 str.isdigit(),但是范围太广(如上标数字：²也被认为是数字)，所以自定义。
        :param c: 字符
        :return: True: 如果字符不是数字；False：字符不是数字。
        """
        return c in "0123456789"

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

    def add_token(self, type: TokenType, literal: object | None = None) -> None:
        """
        将每个 token 添加到 tokens 列表中，数据来源于 scan_token()。
        :param type: token 类型
        :param literal: token 字面量
        :return: None
        """
        text: str = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def is_number(self, string) -> bool:
        """
        判断是否是数字
        :param string:
        :return:
        """
        if string in "0123456789":
            return True
        return False
