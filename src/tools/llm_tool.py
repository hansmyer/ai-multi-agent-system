"""OpenAI LLM Tool for text generation and analysis"""

from typing import Dict, Any, Optional, List

import openai

from src.tools.base_tool import BaseTool
from src.config.settings import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LLMTool(BaseTool):
    """Tool for interacting with OpenAI LLM models"""

    def __init__(self):
        """Initialize LLM tool"""
        super().__init__(
            name="LLMTool",
            description="Generate text, analyze content, and solve problems using OpenAI models",
        )

        settings = get_settings()
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens

        openai.api_key = self.api_key

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute LLM operation"""
        operation = kwargs.get("operation", "generate")

        if operation == "generate":
            return await self.generate_text(**kwargs)
        elif operation == "analyze":
            return await self.analyze_text(**kwargs)
        elif operation == "chat":
            return await self.chat(**kwargs)
        else:
            return {"success": False, "error": f"Unknown operation: {operation}"}

    async def validate_input(self, **kwargs) -> bool:
        """Validate input parameters"""
        operation = kwargs.get("operation", "generate")

        if operation == "generate":
            return "prompt" in kwargs and len(kwargs["prompt"]) > 0
        elif operation == "analyze":
            return "content" in kwargs and len(kwargs["content"]) > 0
        elif operation == "chat":
            return "messages" in kwargs and len(kwargs["messages"]) > 0

        return False

    async def generate_text(self, **kwargs) -> Dict[str, Any]:
        """Generate text using LLM"""
        prompt = kwargs.get("prompt", "")
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)

        try:
            logger.debug(f"Generating text with prompt: {prompt[:50]}...")

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            generated_text = response.choices[0].message.content

            logger.debug(f"Text generated successfully")

            return {
                "success": True,
                "data": {
                    "generated_content": generated_text,
                    "tokens_used": response.usage.total_tokens,
                    "model": self.model,
                },
            }

        except Exception as e:
            logger.error(f"Text generation failed: {str(e)}")
            return {"success": False, "error": str(e)}

    async def analyze_text(self, **kwargs) -> Dict[str, Any]:
        """Analyze text content"""
        content = kwargs.get("content", "")
        analysis_type = kwargs.get("analysis_type", "general")

        try:
            prompt = f"Analyze the following {analysis_type} content and provide insights:\n\n{content}"

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert analyst."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=self.max_tokens,
            )

            analysis = response.choices[0].message.content

            logger.debug(f"Content analyzed successfully")

            return {
                "success": True,
                "data": {
                    "analysis": analysis,
                    "tokens_used": response.usage.total_tokens,
                },
            }

        except Exception as e:
            logger.error(f"Text analysis failed: {str(e)}")
            return {"success": False, "error": str(e)}

    async def chat(self, **kwargs) -> Dict[str, Any]:
        """Chat with LLM"""
        messages = kwargs.get("messages", [])
        system_message = kwargs.get("system_message", "You are a helpful AI assistant.")

        try:
            # Add system message
            full_messages = [{"role": "system", "content": system_message}]
            full_messages.extend(messages)

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=full_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            reply = response.choices[0].message.content

            logger.debug(f"Chat completed successfully")

            return {
                "success": True,
                "data": {
                    "reply": reply,
                    "tokens_used": response.usage.total_tokens,
                },
            }

        except Exception as e:
            logger.error(f"Chat failed: {str(e)}")
            return {"success": False, "error": str(e)}

    async def code_generation(self, **kwargs) -> Dict[str, Any]:
        """Generate code"""
        language = kwargs.get("language", "python")
        description = kwargs.get("description", "")

        try:
            prompt = f"Generate {language} code for the following requirement:\n{description}"

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert programmer."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=self.max_tokens,
            )

            code = response.choices[0].message.content

            logger.debug(f"Code generated for {language}")

            return {
                "success": True,
                "data": {
                    "generated_code": code,
                    "language": language,
                    "tokens_used": response.usage.total_tokens,
                },
            }

        except Exception as e:
            logger.error(f"Code generation failed: {str(e)}")
            return {"success": False, "error": str(e)}
