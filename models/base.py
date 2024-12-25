# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base.py
# Time       : 2024/12/24 10:08
# Author     : Feiren Cheng
# Description: 
"""
from abc import ABC, abstractmethod

from config.model_config import ModelConfig


class ModelAdapter(ABC):
    """Base adapter class for different models"""

    def __init__(self, config: ModelConfig):
        self.config = config
        self.llm = None
        self.setup_llm()

    @abstractmethod
    def setup_llm(self):
        """Setup the language model"""
        raise NotImplementedError("Subclasses must implement setup_llm")


class EmbeddingAdapter(ABC):
    """Base adapter class for different embedding models"""

    def __init__(self, config: ModelConfig):
        self.config = config
        self.embeddings = None
        self.setup_embeddings()

    @abstractmethod
    def setup_embeddings(self):
        raise NotImplementedError("Subclasses must implement setup_embeddings")
