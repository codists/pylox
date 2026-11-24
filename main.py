# @Filename: main.py
# @Author: codists
# @Created: 2026-10-23 17:55:34
import os
import sys
from pathlib import Path

from ast_printer import print_ast
from lox import Lox
from parser import Parser
from scanner import Scanner


def main() -> None:
    """
    执行方式:
    1. python pylox.py [script.lox]; sys.argv的值不包含 python 这个参数
    2. REPEL;

    lox 解释器入口
    :return: None
    """
    print("python main.py [script.lox]")

    test_mode = True
    # test_file = "./test/comments/line_at_eof.lox"
    test_dir = False
    # test_file = "./test/identifier/identifier_temp.lox"
    # test_file = "./test/reserved_word/reserved_word_temp.lox"
    test_file = "./test/expressions/expression_temp.lox"
    if test_mode:
        if test_dir:
            test_path = Path(test_file)
            test_directory = test_path.parent

            for file in sorted(test_directory.iterdir()):
                if file.is_file():
                    print(f"\n========== Testing: {file} ==========")
                    run_file(str(file))
        else:
            run_file(test_file)

    # 参数过多，不符合要求
    if len(sys.argv) > 2:
        print("用法：python main.py [script.lox]")
        sys.exit(64)
    # 一个参数，运行的是文件
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])

    # 没有参数，REPL
    else:
        run_prompt()


def run_file(filename: str) -> None:
    """
    文件方式运行解释器：python pylox.py [script.lox]
    :param filename:
    :return:
    """

    print("当前工作目录：", os.getcwd())
    print("目标文件绝对路径：", os.path.abspath(filename))

    try:
        with open(filename, encoding="utf-8") as file:
            # read()得到的是 string
            source = file.read()
            print(f"文件内容：{source}")
            run(source)
    except FileNotFoundError:
        print(f"{filename} 找不到")


def run_prompt() -> None:
    """
    命令行方式运行
    :return: None
    """
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        run(line)


def run(source: str) -> None:
    """

    :param source: 代码
    :return:
    """
    # 源代码 > token
    scanner = Scanner(source)
    tokens: list = scanner.scan_tokens()

    for token in tokens:
        print(f"token 结构: {token.token_type}, {token.lexeme!r}, {token.literal!r}, {token.line}")

    ''' 
    tokens 示例：
    TokenType.LEFT_PAREN, '(', None, 5
    TokenType.NUMBER, '1', 1.0, 5
    TokenType.PLUS, '+', None, 5
    TokenType.NUMBER, '2', 2.0, 5
    TokenType.RIGHT_PAREN, ')', None, 5
    TokenType.STAR, '*', None, 5
    okenType.NUMBER, '3', 3.0, 5
    TokenType.EOF, '', None, 6
    '''
    parser = Parser(tokens)
    expression = parser.parse()

    if Lox.had_error:
        return
    if expression is None:
        return
    print(print_ast(expression))


if __name__ == "__main__":
    main()
