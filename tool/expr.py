from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from tokens import Token  # noqa: F401

R = TypeVar('R')

class Expr(ABC, Generic[R]):
    @abstractmethod
    def accept(self, visitor: 'Visitor[R]') -> R:
        ...

class Visitor(ABC, Generic[R]):
    @abstractmethod
    def visit_assign_expr(self, expr: 'Assign') -> R:
        ...
    @abstractmethod
    def visit_binary_expr(self, expr: 'Binary') -> R:
        ...
    @abstractmethod
    def visit_call_expr(self, expr: 'Call') -> R:
        ...
    @abstractmethod
    def visit_grouping_expr(self, expr: 'Grouping') -> R:
        ...
    @abstractmethod
    def visit_literal_expr(self, expr: 'Literal') -> R:
        ...
    @abstractmethod
    def visit_logical_expr(self, expr: 'Logical') -> R:
        ...
    @abstractmethod
    def visit_unary_expr(self, expr: 'Unary') -> R:
        ...
    @abstractmethod
    def visit_variable_expr(self, expr: 'Variable') -> R:
        ...

class Assign(Expr[R]):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: 'Visitor[R]') -> R:
        return visitor.visit_assign_expr(self)

class Binary(Expr[R]):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: 'Visitor[R]') -> R:
        return visitor.visit_binary_expr(self)

class Call(Expr[R]):
    def __init__(self, callee: Expr, paren: Token, args: list[Expr]):
        self.callee = callee
        self.paren = paren
        self.args = args

    def accept(self, visitor: 'Visitor[R]') -> R:
        return visitor.visit_call_expr(self)

class Grouping(Expr[R]):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: 'Visitor[R]') -> R:
        return visitor.visit_grouping_expr(self)

class Literal(Expr[R]):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: 'Visitor[R]') -> R:
        return visitor.visit_literal_expr(self)

class Logical(Expr[R]):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: 'Visitor[R]') -> R:
        return visitor.visit_logical_expr(self)

class Unary(Expr[R]):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: 'Visitor[R]') -> R:
        return visitor.visit_unary_expr(self)

class Variable(Expr[R]):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: 'Visitor[R]') -> R:
        return visitor.visit_variable_expr(self)

