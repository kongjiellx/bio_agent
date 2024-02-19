# -*-coding: utf-8 -*-

import os
from const import WORKSPACE

class WorkSpace(object):
    def __init__(self):
        self.files = {}

    def __str__(self):
        ret = ""
        for k, v in self.files.items():
            ret += f"文件名: {k}, 类型: {v[0]}, 是否标准格式: {v[1]}\n"
        return ret

    def add(self, path, desc):
        os.system(f"cp {path} {WORKSPACE}")
        self.files[path.split("/")[-1]] = [desc, False]