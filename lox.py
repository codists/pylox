import sys


def main() -> None:
    """
    执行方式:
    1. python demo.lox;
    2. REPEL;

    lox 解释器入口
    :return: None
    """
    # 参数过多，不符合要求
    if len(sys.argv) > 1:
        print("用法：pylox script.lox")
        exit(0)
    # 一个参数，运行的是文件
    elif len(sys.argv) == 1:
        run_file(sys.argv[0])
    # 没有参数，REPL
    else:
        # run_prumpt()
        pass


def run_file(filename: str) -> None:
    try:
        with open(filename, encoding="utf-8") as file:
            source = file.read()
            current = 0
            while current < len(source):
                # 假设没有特殊字符
                char =



def run(filename: str) -> None:
    with open(filename, encoding="utf-8") as f:
        # f.read() 得到的是 string 或者 byte
        data = f.read().split(' ')
        print(data)


if __name__ == "__main__":
    main()
