# @Filename: main.py
# @Author: codists
# @Created: 2026-10-23 17:55:34
import os
import sys

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
    test_file = "./test/comments/only_line_comment.lox"
    if test_mode:
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
    scanner = Scanner(source)
    tokens: list = scanner.scan_tokens()
    for token in tokens:
        print(f"token: {token}")


if __name__ == "__main__":
    main()
