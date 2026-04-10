from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt

class BaseProcessor(ABC):
    @abstractmethod
    def process(self, data): pass

# a. 采样数据集处理
class LimitChecker(BaseProcessor):
    def __init__(self, min_val, max_val):
        self.min, self.max = min_val, max_val
    def process(self, df: pd.DataFrame):
        df['pass'] = df['value'].between(self.min, self.max)
        return df

# b. 图片处理 (计算偏移示例)
class ImageCenterProcessor(BaseProcessor):
    def process(self, img_path):
        import cv2
        img = cv2.imread(img_path)
        # 这里实现具体的 OpenCv 找中心逻辑
        offset = (1.2, -0.5) # 示例值
        return offset