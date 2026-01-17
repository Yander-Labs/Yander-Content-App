"""
Base Agent Class
All specialized agents inherit from this base class.
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseAgent:
    """Base class for all content creation agents."""

    def __init__(self, name: str, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize the base agent.

        Args:
            name: Name of the agent
            model: Claude model to use
        """
        self.name = name
        self.model = model
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.logger = self._setup_logger()
        self.conversation_history = []

    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the agent."""
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)

        # File handler
        fh = logging.FileHandler(f"logs/{self.name.lower().replace(' ', '_')}.log")
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def call_claude(self,
                   system_prompt: str,
                   user_message: str,
                   max_tokens: int = 4096,
                   temperature: float = 1.0) -> str:
        """
        Make a call to Claude API.

        Args:
            system_prompt: System instructions for Claude
            user_message: User message/query
            max_tokens: Maximum tokens in response
            temperature: Temperature for response generation

        Returns:
            Claude's response as string
        """
        try:
            self.logger.info(f"Calling Claude with message: {user_message[:100]}...")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )

            result = response.content[0].text
            self.logger.info(f"Received response ({len(result)} characters)")

            return result

        except Exception as e:
            self.logger.error(f"Error calling Claude: {str(e)}")
            raise

    def save_output(self, data: Any, filename: str, output_dir: str = "output"):
        """
        Save output data to a file.

        Args:
            data: Data to save
            filename: Name of the output file
            output_dir: Directory to save the file
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, filename)

            if filename.endswith('.json'):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(data))

            self.logger.info(f"Saved output to {filepath}")
            return filepath

        except Exception as e:
            self.logger.error(f"Error saving output: {str(e)}")
            raise

    def load_data(self, filename: str, data_dir: str = "data") -> Any:
        """
        Load data from a file.

        Args:
            filename: Name of the file to load
            data_dir: Directory containing the file

        Returns:
            Loaded data
        """
        try:
            filepath = os.path.join(data_dir, filename)

            if filename.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()

        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the agent's main task.
        Must be implemented by subclasses.

        Returns:
            Dictionary containing the results
        """
        raise NotImplementedError("Subclasses must implement execute()")
