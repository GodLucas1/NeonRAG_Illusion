# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : adapters.py
# Time       : 2024/12/24 10:07
# Author     : Feiren Cheng
# Description: 
"""

from langchain_openai import ChatOpenAI

from .base import ModelAdapter
from .base import EmbeddingAdapter
from .embedding.zhipuai_embedding import ZhipuAIEmbeddings


class OpenAIAdapter(ModelAdapter):
    """Adapter for OpenAI models"""

    def setup_llm(self):
        self.llm = ChatOpenAI(
            model_name=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            openai_api_key=self.config.api_key,
            **({"openai_api_base": self.config.api_base} if self.config.api_base else {}),
            **(self.config.additional_params or {})
        )


class ZhipuAIAdapter(ModelAdapter):
    """Adapter for ZhipuAI models"""

    def setup_llm(self):
        self.llm = ChatOpenAI(
            model_name=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            openai_api_key=self.config.api_key,
            openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
            **(self.config.additional_params or {})
        )


class ZhipuAIEmbeddingsAdapter(EmbeddingAdapter):
    """Adapter for ZhipuAI embeddings"""

    def setup_embeddings(self):
        self.embeddings = ZhipuAIEmbeddings(
            model="embedding-3",
            openai_api_key=self.config.api_key
        )


class XAIAdapter(ModelAdapter):
    """Adapter for ZhipuAI models"""

    def setup_llm(self):
        self.llm = ChatOpenAI(
            model_name=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            openai_api_key=self.config.api_key,
            openai_api_base="https://api.x.ai/v1",
            **(self.config.additional_params or {})
        )
