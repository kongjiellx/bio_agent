# -*-coding: utf-8 -*-

from abc import ABC
import matplotlib
import pandas as pd
from sklearn.decomposition import PCA

matplotlib.use('Qt5Agg')  # 指定后端
import matplotlib.pyplot as plt
import seaborn as sns
from workspace import WORKSPACE


class BaseFunction(ABC):
    @property
    def schema(self):
        raise NotImplementedError

    def __call__(self, workspace, **kwargs):
        raise NotImplementedError


class Exit(BaseFunction):
    @property
    def schema(self):
        return {
            "name": "Exit",
            "description": "退出当前任务",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }

    def __call__(self, workspace, **kwargs):
        # 并不会call
        pass


class JumpTo(BaseFunction):
    @property
    def schema(self):
        return {
            "name": "JumpTo",
            "description": "跳转到其他的agent",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_agent": {"type": "string", "enum": ["DataAgent", "AnalysisAgent"]}
                },
                "required": ["target_agent"],
            },
        }

    def __call__(self, workspace, **kwargs):
        # 并不会call
        pass


class CheckGeneExpressionData(BaseFunction):
    @property
    def schema(self):
        return {
            "name": "CheckGeneExpressionData",
            "description": "检查基因表达数据是否标准格式",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {"type": "string"}
                },
                "required": ["file_name"],
            },
        }

    def __call__(self, workspace, **kwargs):
        print(f"检查基因表达数据{kwargs['file_name']}是否标准化格式，结果 \"{workspace.files[kwargs['file_name']][1]}\"")
        return str(workspace.files[kwargs["file_name"]][1])


class CheckClinicalDataset(BaseFunction):
    @property
    def schema(self):
        return {
            "name": "CheckClinicalDataset",
            "description": "检查临床数据是否标准格式",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {"type": "string"}
                },
                "required": ["file_name"],
            },
        }

    def __call__(self, workspace, **kwargs):
        print(f"检查临床实验数据{kwargs['file_name']}是否标准化格式，结果 \"{workspace.files[kwargs['file_name']][1]}\"")
        return str(workspace.files[kwargs["file_name"]][1])


class CleanGeneExpressionData(BaseFunction):
    @property
    def schema(self):
        return {
            "name": "CleanGeneExpressionData",
            "description": "清洗基因表达数据",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {"type": "string"}
                },
                "required": ["file_name"],
            },
        }

    def __call__(self, workspace, **kwargs):
        print(f"清洗基因表达数据{kwargs['file_name']}")
        workspace.files[kwargs["file_name"]][1] = True
        return "数据清洗完成"


class CleanClinicalDataset(BaseFunction):
    @property
    def schema(self):
        return {
            "name": "CleanClinicalDataset",
            "description": "清洗临床实验数据",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {"type": "string"}
                },
                "required": ["file_name"],
            },
        }

    def __call__(self, workspace, **kwargs):
        print(f"清洗临床实验数据{kwargs['file_name']}")
        workspace.files[kwargs["file_name"]][1] = True
        return "数据清洗完成"


class PCAAnalysis(BaseFunction):
    @property
    def schema(self):
        return {
            "name": "PCAAnalysis",
            "description": "PCA分析",
            "parameters": {
                "type": "object",
                "properties": {
                    "exp_file": {"type": "string", "description": "基因表达数据文件"},
                    "clin_file": {"type": "string", "description": "临床实验数据文件"},
                },
                "required": ["exp_file", "clin_file"],
            },
        }

    def __call__(self, workspace, **kwargs):
        exp = pd.read_csv(WORKSPACE + kwargs["exp_file"], index_col=0)
        clin = pd.read_csv(WORKSPACE + kwargs["clin_file"])

        pca = PCA(n_components=2)
        exp_pca = pca.fit_transform(exp.T)
        exp_pca_df = pd.DataFrame(exp_pca, columns=['PC1', 'PC2'], index=exp.columns)
        exp_pca_df = exp_pca_df.merge(clin[['ID', 'Tissue']], left_index=True, right_on='ID')

        sns.scatterplot(x='PC1', y='PC2', hue='Tissue', data=exp_pca_df)
        plt.title('PCA of Gene Expression Data')
        plt.show()
        return "PCA已完成"


class EnrichAnalysis(BaseFunction):
    @property
    def schema(self):
        return {
            "name": "EnrichAnalysis",
            "description": "富集分析",
            "parameters": {
                "type": "object",
                "properties": {
                    "exp_file": {"type": "string", "description": "基因表达数据文件"},
                    "clin_file": {"type": "string", "description": "临床实验数据文件"},
                },
                "required": ["exp_file", "clin_file"],
            },
        }

    def __call__(self, workspace, **kwargs):
        return "富集分析已完成"