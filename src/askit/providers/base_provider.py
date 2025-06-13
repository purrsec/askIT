from abc import ABC, abstractmethod

class AIBaseProvider(ABC):
    """
    Abstract base class for all AI providers.
    Each provider must implement these methods to ensure a consistent interface.
    """

    @abstractmethod
    def get_suggestion(self, prompt: str, context: str) -> str:
        """
        Takes a prompt and context, returns the AI's suggestion.

        Args:
            prompt: The user's prompt.
            context: The project context (files, history, etc.).

        Returns:
            A string containing the AI's command or suggestion.
        """
        pass

    def _prepare_prompt(self, prompt: str, context: str) -> str:
        """
        Base method for preparing the final prompt. Can be overridden if necessary.
        """
        return f"Context:\n{context}\n\nUser Prompt: {prompt}\n\nCommand:" 