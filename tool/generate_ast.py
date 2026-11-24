#!/usr/bin/env python3
# @Filename: generate_ast.py
# @Author: codists
# @Created: 2026-11-20 20:35:30
"""
这里只是为了跟书中保持一致，实际未用到该模块生成的 expr.py。
"""

import re
import sys
from pathlib import Path
from typing import TextIO

SPACE_4 = "    "
SPACE_8 = "        "


def define_ast(output_dir: Path, base_name: str, types: list[str]) -> None:
    """

    :param output_dir:
    :param base_name:
    :param types: 类型，格式为：类名 | 属性
    :return:
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{base_name.lower()}.py"
    print(path)

    with open(path, "w", encoding="utf-8") as writer:
        writer.write("from abc import ABC, abstractmethod\n")
        writer.write("from typing import Generic, TypeVar\n\n")
        writer.write("from tokens import Token  # noqa: F401\n\n")
        writer.write("R = TypeVar('R')\n\n")

        # 1. 基类（只声明 accept）
        writer.write(f"class {base_name}(ABC, Generic[R]):\n")
        writer.write("    @abstractmethod\n")
        writer.write(
            f"    def accept(self, visitor: 'Visitor[R]') -> R:\n"
        )
        writer.write("        ...\n\n")

        # 访客模式
        define_visitor(writer, base_name, types)

        #
        for type_ in types:
            class_name, fields = type_.split("|", 1)
            define_type(writer, base_name, class_name.strip(), fields.strip())


def define_visitor(writer: TextIO, base_name: str, types: list[str]) -> None:
    """

    :param writer:
    :param base_name:
    :param types:
    :return:
    """
    writer.write("class Visitor(ABC, Generic[R]):\n")
    for type_ in types:
        type_name = type_.split("|", 1)[0].strip()
        method = f"visit_{type_name.lower()}_{base_name.lower()}"
        writer.write("    @abstractmethod\n")
        writer.write(
            f"    def {method}(self, {base_name.lower()}: '{type_name}') -> R:\n"
        )
        writer.write("        ...\n")
    writer.write("\n")


def define_type(
        writer: TextIO,
        base_name: str,
        class_name: str,
        field_list: str,
) -> None:
    """
    生成表达式 AST 类
    :param writer:
    :param base_name:
    :param class_name:
    :param field_list: 属性列表
    :return:
    """
    writer.write(f"class {class_name}({base_name}[R]):\n")
    writer.write(f"    def __init__(self, {field_list}):\n")

    field_names = []
    for part in field_list.split(", "):
        m = re.match(r"(\w+)", part.strip())
        if m:
            field_names.append(m.group(1))
    for name in field_names:
        writer.write(f"{SPACE_8}self.{name} = {name}\n")
    writer.write("\n")

    writer.write(f"{SPACE_4}def accept(self, visitor: 'Visitor[R]') -> R:\n")
    writer.write(
        f"{SPACE_8}return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n\n"
    )


def main() -> None:
    # 命令行输入参数
    if len(sys.argv) == 2:
        output_dir = Path(sys.argv[1])
    # 如果命令行没有输入参数，自动生成
    else:
        output_dir = Path(__file__).resolve().parent

    define_ast(output_dir, "Expr", [
        "Assign | name: Token, value: Expr",
        "Binary | left: Expr, operator: Token, right: Expr",
        "Call | callee: Expr, paren: Token, args: list[Expr]",
        "Grouping | expression: Expr",
        "Literal | value",
        "Logical | left: Expr, operator: Token, right: Expr",
        "Unary | operator: Token, right: Expr",
        "Variable | name: Token"
    ], )


if __name__ == "__main__":
    main()