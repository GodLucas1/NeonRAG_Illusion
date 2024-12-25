from importlib import import_module
from typing import Dict, Any
from common.constants.model_constants import ModelProvider
from common.constants.enums import ModelRole, SubscriptionTier
from neonrag_illusion.config.model_config import ModelConfig
from neonrag_illusion.models.base import ModelAdapter, EmbeddingAdapter


class ModelMappings:
    """Mappings related to models"""

    # Map model names to their providers
    MODEL_PROVIDER_MAP = {
        "gpt-3.5-turbo": ModelProvider.OPENAI,
        "gpt-4": ModelProvider.OPENAI,
        "glm-4": ModelProvider.ZHIPUAI,
        "glm-3-flash": ModelProvider.ZHIPUAI
    }

    # Map subscription tiers to allowed models
    SUBSCRIPTION_MODEL_MAP = {
        SubscriptionTier.FREE: ["glm-3-flash", "grok-2-1212"],
        SubscriptionTier.BASIC: ["gpt-3.5-turbo", "glm-3-turbo", "claude-3-sonnet-20240229"],
        SubscriptionTier.PREMIUM: ["gpt-4", "claude-3-sonnet-20240229", "glm-4"],
        SubscriptionTier.ENTERPRISE: ["gpt-4", "claude-3-opus-20240229", "glm-4"]
    }

    # Map models to their roles
    MODEL_ROLE_MAP = {
        "gpt-4": ModelRole.PRIMARY,
        "claude-3-opus-20240229": ModelRole.PRIMARY,
        "gpt-3.5-turbo": ModelRole.FALLBACK,
        "claude-3-sonnet-20240229": ModelRole.FALLBACK,
        "glm-4": ModelRole.SPECIALIZED,
        "glm-4-flash": ModelRole.EXPERIMENTAL
    }

    # Map models to their default parameters
    MODEL_PARAMS_MAP: Dict[str, Dict[str, Any]] = {
        "gpt-3.5-turbo": {
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 1.0
        },
        "glm-4-flash": {
            "temperature": 0.95,
            "max_tokens": 4096,
            "top_p": 0.9
        }
    }

    MODEL_ADAPTER_MAP = {
        ModelProvider.OPENAI.value: "neonrag_illusion.models.adapters.OpenAIAdapter",
        ModelProvider.ZHIPUAI.value: "neonrag_illusion.models.adapters.ZhipuAIAdapter",
        ModelProvider.XAI: "neonrag_illusion.models.adapters.XAIAdapter"
    }

    EMBEDDING_ADAPTER_MAP = {
        ModelProvider.OPENAI.value: "OpenAIEmbeddingsAdapter",
        ModelProvider.ZHIPUAI.value: "ZhipuAIEmbeddingsAdapter"
    }

    @classmethod
    def get_provider(cls, model_name: str) -> ModelProvider:
        """Get provider for a model"""
        return cls.MODEL_PROVIDER_MAP.get(model_name)

    @classmethod
    def get_allowed_models(cls, tier: SubscriptionTier) -> list:
        """Get allowed models for a subscription tier"""
        return cls.SUBSCRIPTION_MODEL_MAP.get(tier, [])

    @classmethod
    def get_model_role(cls, model_name: str) -> ModelRole:
        """Get role for a model"""
        return cls.MODEL_ROLE_MAP.get(model_name)

    @classmethod
    def get_model_params(cls, model_name: str) -> Dict[str, Any]:
        """Get default parameters for a model"""
        return cls.MODEL_PARAMS_MAP.get(model_name, {})

    @classmethod
    def get_model_adapter(cls, model_provider: ModelProvider, model_config: ModelConfig) -> ModelAdapter:
        """Get model adapter for a model provider"""
        module_name, classname = cls.MODEL_ADAPTER_MAP.get(model_provider).rsplit(".", 1)
        module = import_module(module_name)
        return getattr(module, classname)(model_config)

    @classmethod
    def get_embedding_adapter(cls, model_provider: ModelProvider, model_config: ModelConfig) -> EmbeddingAdapter:
        """Get embedding adapter for a model provider"""
        module_name, classname = cls.EMBEDDING_ADAPTER_MAP.get(model_provider).rsplit(".", 1)
        module = import_module(module_name)
        return getattr(module, classname)(model_config)
