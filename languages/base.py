"""
Base language class for dictionary languages.
"""

from abc import ABC, abstractmethod
from typing import Optional


class Language(ABC):
    """Abstract base class for language implementations."""
    
    code: str           # ISO 639-1 code (e.g., "en", "ru")
    name: str           # English name
    native_name: str    # Native name
    
    @abstractmethod
    def detect(self, text: str) -> bool:
        """
        Detect if text appears to be this language.
        
        Args:
            text: Input text to check
            
        Returns:
            True if text appears to be this language
        """
        pass
    
    @abstractmethod
    def normalize(self, text: str) -> str:
        """
        Normalize input to canonical form.
        
        For example, transliterate Latin to Cyrillic for Russian.
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        pass
    
    @abstractmethod
    def lookup(self, word: str, translate: bool = False) -> Optional[dict]:
        """
        Look up a word in this language.
        
        Args:
            word: Word to look up (should be normalized)
            translate: If True, return translation instead of definition
            
        Returns:
            Dictionary result or None if not found
        """
        pass
