"""Configuration settings for the ReACT agent."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the ReACT agent."""

    # OpenAI API settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")

    # Agent settings
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))

    # Tool settings
    ENABLE_WEB_SEARCH: bool = os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true"
    ENABLE_FILE_OPERATIONS: bool = (
        os.getenv("ENABLE_FILE_OPERATIONS", "true").lower() == "true"
    )

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            print("Warning: OPENAI_API_KEY not found in environment variables.")
            print("Please set OPENAI_API_KEY in your .env file or environment.")
            return False
        return True


# Global config instance
config = Config()

