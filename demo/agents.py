# -*-coding: utf-8 -*-

import json
from llm import call_openai_stream, call_openai
from abc import ABC
from data_model import AgentMessage, RspType
from functions import (
    Exit,
    JumpTo,
    CheckGeneExpressionData,
    CheckClinicalDataset,
    CleanClinicalDataset,
    CleanGeneExpressionData,
    PCAAnalysis,
    EnrichAnalysis,
)
from workspace import WorkSpace


class Agent(ABC):
    def __init__(self, functions):
        self.functions = functions
        self.name_to_func = {f.__class__.__name__: f for f in self.functions}

    def system(self, workspace: WorkSpace):
        raise NotImplementedError

    @property
    def function_schemas(self):
        return [f.schema for f in self.functions]

    def __call__(self, history, workspace):
        while True:
            break_flag = True
            content = ""
            for chunk in call_openai_stream([{"role": "system", "content": self.system(workspace)}] + history, self.function_schemas):
                if isinstance(chunk, str):
                    content += chunk
                    yield AgentMessage(type=RspType.CONTENT, content=chunk)
                else:  # function call
                    fname = chunk["name"]
                    arguments = json.loads(chunk["arguments"])
                    if fname == "Exit":
                        yield AgentMessage(type=RspType.EXIT)
                    elif fname == "JumpTo":
                        yield AgentMessage(type=RspType.JUMP_TO, target_agent=arguments["target_agent"])
                    else:
                        fc_output = self.name_to_func[fname](workspace, **arguments)
                        history += [
                            {"role": "assistant", "content": content, "function_call": chunk},
                            {"role": "function", "name": fname, "content": fc_output}
                        ]
                        break_flag = False
                    break
                history.append({"role": "assistant", "content": content})
            if break_flag:
                break


class MainAgent(Agent):
    def __init__(self):
        super().__init__([JumpTo()])

    def system(self, workspace: WorkSpace):
        return f"""你是一个辅助生物信息研究和分析的系统的中控agent，你的主要工作是与用户闲聊以及根据用户表达的意图跳转其他agent。你可以跳转到下面这些agent：
        1. 数据加载和处理 (DataAgent)，功能主要是帮助用户上传数据和进行数据预处理
        2. 分析数据 (AnalysisAgent)，功能主要是帮助用户进行数据分析，例如富集分析、绘制火山图等
        下面是用户目前的workspace信息，如果为空或者所有数据都是非标准化的话，那么请你直接跳转到DataAgent，因为没有标准化的数据系统是无法运作的。
        ```workspace
        {workspace}
        ```
        对于工作区所有数据都已经是标准化的情况，请你先和用户确认是需要增加或修改数据，还是要进行分析工作，以此来决定跳转哪个agent。
        """


class DataAgent(Agent):
    def __init__(self):
        super().__init__([
            CleanClinicalDataset(),
            CleanGeneExpressionData(),
            CheckClinicalDataset(),
            CheckGeneExpressionData(),
            Exit()
        ])

    def system(self, workspace: WorkSpace):
        return f"""你是一个辅助生物信息研究和分析的助手，你专门负责使用各种工具帮助用户进行数据清洗和标准化工作。
        这是用户目前的workspace:
        ```workspace
        {workspace}
        ```
        如果工作区是空的，请要求用户上传数据。
        你的目的是保证工作区所有数据都是标准格式的，如果满足此条件，请使用Exit函数退出当前任务。你可以使用下面这些函数来完成任务。
        1. 检查基因表达数据是否已经是标准格式(CheckGeneExpressionData)
        2. 检查临床实验数据是否已经是标准格式(CheckClinicalDataset)
        3. 清洗基因表达数据(CleanGeneExpressionData)
        4. 清洗临床实验数据(CleanClinicalDataset)
        注意！！：必须在调用Check函数之后才能调用Clean函数。
        """


class AnalysisAgent(Agent):
    def __init__(self):
        super().__init__([PCAAnalysis(), EnrichAnalysis()])

    def system(self, workspace: WorkSpace):
        return f"""你是一个辅助生物信息研究和分析的助手，你专门负责帮助用户进行数据分析工作，你可以执行的数据分析类型为以下几种：
            1. PCA分析
            2. 富集分析
            这是目前用户的workspace信息：
            ```workspace
            {workspace}
            ```
            注意：你只能调用上述三种函数和使用workspace中的文件来进行分析工作。并且确认你使用的数据是标准化的，如果不是请提醒用户对数据进行标准化后再进行分析。
            """

