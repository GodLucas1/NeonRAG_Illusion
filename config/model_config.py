# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : model_config.py
# Time       : 2024/12/24 10:07
# Author     : Feiren Cheng
# Description: 
"""
from dataclasses import dataclass
from typing import Dict, Optional, Any


@dataclass
class ModelConfig:
    api_key: str
    api_base: Optional[str] = None
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    additional_params: Dict[str, Any] = None
