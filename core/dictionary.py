"""
Core dictionary functionality.
"""

import urllib.request
import urllib.error
import json
from typing import Optional

from .cache import Cache


class Dictionary:
    """Multi-language dictionary with caching."""
    
    def __init__(self, languages: list, cache: Cache):
        self.languages = {lang.code: lang for lang in languages}
        self.language_list = languages
        self.cache = cache
    
    def detect_language(self, text: str) -> str:
        """Auto-detect language of input text."""
        # Check Russian first since it has specific patterns
        # and a word lookup table
        ru = self.languages.get("ru")
        if ru and ru.detect(text):
            return "ru"
        
        # Then check other languages
        for lang in self.language_list:
            if lang.code != "ru" and lang.detect(text):
                return lang.code
        
        return "en"  # Default to English
    
    def lookup(self, word: str, force_lang: Optional[str] = None,
               offline: bool = False, translate: bool = False) -> Optional[dict]:
        """
        Look up a word in the dictionary.
        
        Args:
            word: The word to look up
            force_lang: Force a specific language code
            offline: Only use cached results
            translate: Use translation mode (show translation, not definition)
            
        Returns:
            Dictionary result or None if not found
        """
        word = word.strip()
        
        # Detect or use forced language
        lang_code = force_lang or self.detect_language(word)
        lang = self.languages.get(lang_code)
        
        if not lang:
            lang = self.languages["en"]
            lang_code = "en"
        
        # Normalize word (e.g., transliterate Russian)
        normalized = lang.normalize(word)
        
        # Check cache first (different cache key for translate mode)
        cache_key = f"{normalized}:translate" if translate else normalized
        cached = self.cache.get(cache_key, lang_code)
        if cached:
            return cached
        
        if offline:
            return None
        
        # Look up in language module
        result = lang.lookup(normalized, translate=translate)
        
        if result:
            # Add metadata
            result["language"] = lang_code
            result["original_input"] = word
            if normalized != word:
                result["normalized"] = normalized
            
            # Cache the result
            self.cache.set(cache_key, lang_code, result)
        
        return result
    
    def random_word(self) -> str:
        """Get a random interesting word for learning."""
        interesting_words = [
            "serendipity", "ephemeral", "eloquent", "ineffable",
            "mellifluous", "petrichor", "luminous", "ethereal",
            "sonder", "vellichor", "hiraeth", "fernweh",
            "apricity", "phosphenes", "eunoia", "kairos",
            "meraki", "komorebi", "ubuntu", "hygge",
            "любовь", "счастье", "душа", "свобода",
            "мечта", "надежда", "красота", "истина"
        ]
        import random
        return random.choice(interesting_words)
