# -*-coding: utf-8 -*-

import enum
from collections import defaultdict
from agents import MainAgent, DataAgent, AnalysisAgent
from workspace import WorkSpace
from data_model import RspType


class State(enum.Enum):
    Main = 1
    Data = 2
    Analysis = 3


class Bio(object):
    def __init__(self):
        self.state = State.Main
        self.state_to_agent = {
            State.Main: MainAgent(),
            State.Data: DataAgent(),
            State.Analysis: AnalysisAgent()
        }
        self.agent_history = defaultdict(list)
        self.workspace = WorkSpace()

    def message(self, msg):
        if msg.startswith("ADD"):
            path, desc = msg[3:].strip().split(" ")
            self.workspace.add(path, desc)
            yield "上传成功\n"
        else:
            while True:
                break_flag = True
                agent = self.state_to_agent[self.state]
                history = self.agent_history[self.state]
                history.append({"role": "user", "content": msg})
                for chunk in agent(history, self.workspace):
                    if chunk.type == RspType.CONTENT:
                        yield chunk.content
                    elif chunk.type == RspType.EXIT:
                        break_flag = False
                        self.state = State.Main
                        self.agent_history[self.state] = []
                        msg = "你好，请按system message的提示执行你的工作。"
                    elif chunk.type == RspType.JUMP_TO:
                        break_flag = False
                        if chunk.target_agent == "DataAgent":
                            msg = "你好，请按system message的提示执行你的工作。"
                            self.state = State.Data
                        elif chunk.target_agent == "AnalysisAgent":
                            self.state = State.Analysis
                        else:
                            raise RuntimeError(f"Error Jump agent: {chunk.target_agent}")
                if break_flag:
                    break

