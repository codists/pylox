# @Filename: ast_printer.py
# @Author: codists
# @Created: 2026-11-22 18:11:19
from functools import singledispatch

from expr import Binary, Expr, Unary, Literal, Grouping
from token_type import TokenType
from tokens import Token


@singledispatch
def print_ast(expr):
    raise NotImplementedError(f"No printer for {type(expr)}")


@print_ast.register
def _(expr: Binary) -> str:
    return _parenthesize(expr.operator.lexeme, expr.left, expr.right)


@print_ast.register
def _(expr: Grouping) -> str:
    return _parenthesize("group", expr.expression)


@print_ast.register
def _(expr: Literal) -> str:
    return "nil" if expr.value is None else str(expr.value)


@print_ast.register
def _(expr: Unary) -> str:
    return _parenthesize(expr.operator.lexeme, expr.right)


def _parenthesize(name: str, *exprs: Expr) -> str:
    return f"({name} {' '.join(expr.accept(print_ast) for expr in exprs)})"


def main():
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )

    print(expression.accept(print_ast))


if __name__ == "__main__":
    main()