# @Filename: parser.py
# @Author: codists
# @Created: 2026-11-21 16:56:44
"""
运算符优先级（从低到高）

1. equality()     ==  !=
2. comparison()  >   >=  <   <=
3. term()        -   +
4. factor()      /   *
5. unary()       !   -
6. primary()     string, number, ()


解析调用关系：

expression()
    └── equality()
          └── comparison()
                └── term()
                      └── factor()
                            └── unary()
                                  └── primary()

'''
    (1+2)*3 构成的 token 示例：
    TokenType.LEFT_PAREN, '(', None, 5
    TokenType.NUMBER, '1', 1.0, 5
    TokenType.PLUS, '+', None, 5
    TokenType.NUMBER, '2', 2.0, 5
    TokenType.RIGHT_PAREN, ')', None, 5
    TokenType.STAR, '*', None, 5
    okenType.NUMBER, '3', 3.0, 5
    TokenType.EOF, '', None, 6
    '''
"""

from expr import Binary, Grouping, Literal, Unary
from expr import Expr
from lox import Lox
from token_type import TokenType
from tokens import Token


class Parser:
    class ParseError(RuntimeError):
        """
        解析错误
        """
        pass

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def expression(self) -> Expr | None:
        """

        :return:
        """
        return self.equality()

    def equality(self) -> Expr:
        """
        处理:
        equality → comparison ( ( "!=" | "==" ) comparison )* ;
        :return:
        """
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def match(self, *types):
        """

        :param types:
        :return:
        """
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True

        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        """

        :param token_type:
        :param message:
        :return:
        """
        if self.check(token_type):
            return self.advance()

        raise self.error(self.peek(), message)

    def check(self, type_: TokenType) -> bool:
        """

        """
        if self.is_at_end():
            return False
        return self.peek().token_type == type_

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        """
        判断是否到达 token 末尾
        :return:
        """
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        """

        :return:
        """
        return self.tokens[self.current]

    def previous(self) -> Token:
        """
        获取上一个 token
        :return:
        """
        return self.tokens[self.current - 1]

    def error(self, token: Token, message: str) -> "Parser.ParseError":
        Lox.error(token, message)
        return Parser.ParseError()

    def synchronize(self) -> None:
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            match self.peek().token_type:
                case (
                TokenType.CLASS
                | TokenType.FUN
                | TokenType.VAR
                | TokenType.FOR
                | TokenType.IF
                | TokenType.WHILE
                | TokenType.PRINT
                | TokenType.RETURN
                ):
                    return
            self.advance()

    def comparison(self) -> Expr:
        """
        处理:
        comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        :return:
        """
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        """
        处理：
        term → factor ( ( "-" | "+" ) factor )* ;
        :return:
        """
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        """
        处理：
        factor → unary ( ( "/" | "*" ) unary )* ;
        :return:
        """
        expr = self.unary()

        while (self.match(TokenType.SLASH, TokenType.STAR)):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        """
        处理前缀运算符：!, -。
        unary → ( "!" | "-" ) unary | primary ;
        :return:
        """
        # !, -
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        """
        处理：
        primary → NUMBER | STRING | "true" | "false" | "nil"| "(" expression ")" ;
        :return:
        """
        # False
        if self.match(TokenType.FALSE):
            return Literal(False)
        # True
        if self.match(TokenType.TRUE):
            return Literal(True)

        # NIL
        if self.match(TokenType.NIL):
            return Literal(None)

        # NUMBER, STRING
        if self.match(TokenType.NUMBER, TokenType.STRING):
            # 匹配到数字的时候，移动，所以找上一个
            literal = Literal(self.previous().literal)
            return literal
            # return Literal(self.previous().literal)

        # (
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def parse(self) -> Expr | None:
        try:
            return self.expression()
        except Parser.ParseError:
            return None
