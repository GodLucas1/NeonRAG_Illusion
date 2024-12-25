# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : conversation.py
# Time       : 2024/12/24 10:15
# Author     : Feiren Cheng
# Description: 
"""
from typing import List, Dict
from datetime import datetime
import json


class ConversationManager:
    def __init__(self):
        self.conversation_history: List[Dict] = []

    def format_history(self) -> str:
        """Format conversation history for prompt"""
        formatted = []
        for msg in self.conversation_history[-5:]:
            formatted.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(formatted)

    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def save_conversation(self, filename: str):
        """Save conversation history to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2)

    def load_conversation(self, filename: str):
        """Load conversation history from file"""
        with open(filename, 'r', encoding='utf-8') as f:
            self.conversation_history = json.load(f)

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []