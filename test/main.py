# @Filename: main.py
# @Author: codists
# @Created: 2026-10-23 08:24:12
with open('other/temp.txt',newline='',encoding='utf-8') as f:
    data = f.read()
    print(repr(data))