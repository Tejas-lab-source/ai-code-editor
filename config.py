# config.py

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


@dataclass
class Config:
    """
    Central configuration for the entire application.

    The provider is decided by base_url, not by a hard-coded vendor. Groq is
    OpenAI-compatible, so the same client speaks to either one.
    """

    api_key: str
    base_url: str
    model: str
    temperature: float
    workspace: str
    max_iterations: int
    debug: bool

    @classmethod
    def load(cls) -> "Config":
        """
        Load configuration from environment variables.
        """

        api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please check your .env file. "
                "Get a key at https://console.groq.com/keys"
            )

        return cls(
            api_key=api_key,
            base_url=os.getenv("BASE_URL", GROQ_BASE_URL),
            model=os.getenv("MODEL", "openai/gpt-oss-120b"),
            temperature=float(os.getenv("TEMPERATURE", "0.2")),
            workspace=os.getenv("WORKSPACE", "./workspace"),
            max_iterations=int(os.getenv("MAX_ITERATIONS", "10")),
            debug=os.getenv("DEBUG", "False").lower() == "true",
        )
