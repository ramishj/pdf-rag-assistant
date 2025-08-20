"""
Configuration file for PDF Knowledge Assistant
Contains all the necessary API keys and settings for different LLM providers
"""

import os
from typing import Dict, List

# LLM Provider Configuration
LLM_PROVIDERS = {
    "OpenAI": {
        "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
        "default_model": "gpt-3.5-turbo",
        "api_key_env": "OPENAI_API_KEY",
        "description": "OpenAI's GPT models for text generation and analysis"
    },
    "Claude": {
        "models": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"],
        "default_model": "claude-3-sonnet-20240229",
        "api_key_env": "ANTHROPIC_API_KEY",
        "description": "Anthropic's Claude models for safe and helpful AI assistance"
    },
    "Azure": {
        "models": ["gpt-4o", "gpt-35-turbo", "gpt-4", "gpt-4-32k"],
        "default_model": "gpt-4o",
        "api_key_env": "AZURE_OPENAI_API_KEY",
        "endpoint_env": "AZURE_OPENAI_ENDPOINT",
        "description": "Azure OpenAI service for enterprise-grade AI solutions"
    },
    "Grok": {
        "models": ["gemini-pro", "gemini-pro-vision"],
        "default_model": "gemini-pro",
        "api_key_env": "GOOGLE_API_KEY",
        "description": "Google's Gemini models for advanced AI capabilities"
    }
}

# Vector Database Configuration
VECTOR_DB_CONFIG = {
    "default_collection": "pdf_knowledge_base",
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "embedding_model": "all-MiniLM-L6-v2",
    "max_results": 5
}

# PDF Processing Configuration
PDF_CONFIG = {
    "supported_formats": [".pdf"],
    "max_file_size_mb": 50,
    "text_extraction_method": "PyPDF2"
}

# Chat Configuration
CHAT_CONFIG = {
    "max_history": 100,
    "temperature": 0.7,
    "max_tokens": 2000
}

def get_api_key(provider: str) -> str:
    """Get API key for the specified provider from environment variables"""
    if provider in LLM_PROVIDERS:
        env_var = LLM_PROVIDERS[provider]["api_key_env"]
        return os.getenv(env_var, "")
    return ""

def get_azure_endpoint() -> str:
    """Get Azure OpenAI endpoint from environment variables"""
    return os.getenv("AZURE_OPENAI_ENDPOINT", "")

def get_available_models(provider: str) -> List[str]:
    """Get available models for the specified provider"""
    if provider in LLM_PROVIDERS:
        return LLM_PROVIDERS[provider]["models"]
    return []

def get_default_model(provider: str) -> str:
    """Get default model for the specified provider"""
    if provider in LLM_PROVIDERS:
        return LLM_PROVIDERS[provider]["default_model"]
    return ""

def get_provider_description(provider: str) -> str:
    """Get description for the specified provider"""
    if provider in LLM_PROVIDERS:
        return LLM_PROVIDERS[provider]["description"]
    return ""
