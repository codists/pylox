"""
1.生成表达式 AST（按表达式类型划分）

expression → literal
           | unary
           | binary
           | grouping ;

literal    → NUMBER | STRING | "true" | "false" | "nil" ;
unary      → ( "-" | "!" ) expression ;
binary     → expression operator expression ;
grouping   → "(" expression ")" ;
operator   → "==" | "!=" | "<" | "<=" | ">" | ">=" | "+" | "-" | "*" | "/" ;

2.输入和输出
(1+2)*3
// expect: (* (group (+ 1.0 2.0)) 3.0)
"""
from dataclasses import dataclass
from functools import singledispatch

from tokens import Token


class Expr:
    def accept(self, visitor):
        return visitor(self)


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass(frozen=True)
class Grouping(Expr):
    expression: Expr


@dataclass(frozen=True)
class Literal(Expr):
    value: object


@dataclass(frozen=True)
class Unary(Expr):
    operator: Token
    right: Expr


@singledispatch
def visit(expr):
    raise NotImplementedError(f"No visit for {type(expr)}")


@visit.register
def _(expr: Binary):
    return f"({expr.operator.lexeme} {expr.left.accept(visit)} {expr.right.accept(visit)})"


@visit.register
def _(expr: Grouping):
    return f"(group {expr.expression.accept(visit)})"


@visit.register
def _(expr: Literal):
    return str(expr.value) if expr.value is not None else "nil"


@visit.register
def _(expr: Unary):
    return f"({expr.operator.lexeme} {expr.right.accept(visit)})"
