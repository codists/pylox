from token_type import TokenType
from tokens import Token


class Lox:
    # @staticmethod
    # def error(line: int, message: str) -> None:
    #     Lox.report(line, "", message)
    had_error = False

    @staticmethod
    def error(token: Token, message: str) -> None:
        if token.token_type == TokenType.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        Lox.had_error = True
