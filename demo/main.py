# -*-coding: utf-8 -*-

from bio import Bio


if __name__ == "__main__":
    b = Bio()
    while True:
        msg = input("USER: ")
        print("ASSISTANT: ", end="")
        for ch in b.message(msg):
            print(ch, end="")
        print()
