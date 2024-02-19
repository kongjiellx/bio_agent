# -*-coding: utf-8 -*-

from bio import Bio


if __name__ == "__main__":
    b = Bio()
    for msg in [
        "ADD /Users/admin/fish/code/bio/exp.csv 基因表达数据",
        "ADD /Users/admin/fish/code/bio/clin.csv 临床实验数据",
        "你好",
        "帮我把数据标准化",
        "我要进行PCA分析"
    ]:
        print(f"USER: {msg}")
        print("ASSISTANT: ", end="")
        for ch in b.message(msg):
            print(ch, end="", flush=True)
        print()
