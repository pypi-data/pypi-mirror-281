from abc import ABC, abstractmethod

class TokenCounter(ABC):
    @abstractmethod
    def tokencount(self, text: str) -> int:
        """
        用于计算字符串中的词语数量。
        参数:
            text (str): 需要计算词语数量的字符串。
        返回:
            int: 字符串中的词语数量。
        """
        pass


import litellm
litellm.suppress_debug_info = True
litellm.set_verbose = False
class LLMTokenCounter(TokenCounter):
    def __init__(self, model_name: str):
        self.model_name = model_name
    def tokencount(self, text: str) -> int:
        tokens = litellm.encode(model=self.model_name, text=text)
        return len(tokens)
