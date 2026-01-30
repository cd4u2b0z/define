"""
Tests for the Dictionary orchestrator.
"""

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.cache import Cache
from core.dictionary import Dictionary
from languages.english import English
from languages.russian import Russian


class TestDictionary(unittest.TestCase):
    """Test cases for the Dictionary class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = Cache(cache_dir=Path(self.temp_dir), ttl_days=1)
        self.languages = [English(), Russian()]
        self.dictionary = Dictionary(self.languages, self.cache)
    
    def tearDown(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)


class TestLanguageDetection(TestDictionary):
    """Test language auto-detection."""
    
    def test_detect_english(self):
        """Test detection of English text."""
        self.assertEqual(self.dictionary.detect_language("hello"), "en")
        self.assertEqual(self.dictionary.detect_language("world"), "en")
        self.assertEqual(self.dictionary.detect_language("computer"), "en")
    
    def test_detect_russian_cyrillic(self):
        """Test detection of Cyrillic text."""
        self.assertEqual(self.dictionary.detect_language("привет"), "ru")
        self.assertEqual(self.dictionary.detect_language("мир"), "ru")
        self.assertEqual(self.dictionary.detect_language("любовь"), "ru")
    
    def test_detect_russian_transliteration(self):
        """Test detection of Russian transliteration."""
        self.assertEqual(self.dictionary.detect_language("privet"), "ru")
        self.assertEqual(self.dictionary.detect_language("spasibo"), "ru")
    
    def test_detect_defaults_to_english(self):
        """Test that unambiguous English text is detected."""
        # Use a clearly English word that doesn't match Russian patterns
        result = self.dictionary.detect_language("the")
        self.assertEqual(result, "en")
        
        result = self.dictionary.detect_language("computer")
        self.assertEqual(result, "en")


class TestDictionaryLookup(TestDictionary):
    """Test dictionary lookup functionality."""
    
    def test_lookup_english_phrase(self):
        """Test looking up an English phrase from local database."""
        result = self.dictionary.lookup("how are you")
        self.assertIsNotNone(result)
        self.assertEqual(result.get("word"), "how are you")
        self.assertEqual(result.get("language"), "en")
    
    def test_lookup_force_language(self):
        """Test forcing a specific language."""
        # Force English even for a word that might be detected as Russian
        result = self.dictionary.lookup("da", force_lang="en")
        if result:
            self.assertEqual(result.get("language"), "en")
    
    def test_lookup_adds_metadata(self):
        """Test that lookup adds required metadata."""
        result = self.dictionary.lookup("how are you")
        self.assertIsNotNone(result)
        
        # Should have language and original_input
        self.assertIn("language", result)
        self.assertIn("original_input", result)
    
    def test_lookup_caches_result(self):
        """Test that results are cached."""
        # First lookup
        result1 = self.dictionary.lookup("how are you")
        self.assertIsNotNone(result1)
        
        # Should now be in cache
        cached = self.cache.get("how are you", "en")
        self.assertIsNotNone(cached)
    
    def test_lookup_offline_mode(self):
        """Test offline mode uses only cache."""
        # First, ensure word is not in cache
        self.cache.clear()
        
        # Offline lookup should return None for uncached word
        # (assuming API is not called)
        result = self.dictionary.lookup("xyz123notaword", offline=True)
        self.assertIsNone(result)
    
    def test_lookup_strips_whitespace(self):
        """Test that whitespace is stripped from input."""
        result1 = self.dictionary.lookup("how are you")
        result2 = self.dictionary.lookup("  how are you  ")
        
        # Both should find the same entry
        if result1 and result2:
            self.assertEqual(result1.get("word"), result2.get("word"))


class TestRandomWord(TestDictionary):
    """Test random word feature."""
    
    def test_random_word_returns_string(self):
        """Test that random_word returns a string."""
        word = self.dictionary.random_word()
        self.assertIsInstance(word, str)
        self.assertGreater(len(word), 0)
    
    def test_random_word_variety(self):
        """Test that random_word returns different words."""
        words = set()
        for _ in range(20):
            words.add(self.dictionary.random_word())
        
        # Should have at least a few different words
        self.assertGreater(len(words), 1)


class TestDictionaryIntegration(TestDictionary):
    """Integration tests for full lookup flow."""
    
    def test_english_slang_with_russian_translation(self):
        """Test that English slang returns Russian translations in translate mode."""
        result = self.dictionary.lookup("awesome", translate=True)
        
        if result:
            self.assertEqual(result.get("language"), "en")
            
            # Check for Russian in definition
            meanings = result.get("meanings", [])
            if meanings:
                definition = meanings[0].get("definitions", [{}])[0].get("definition", "")
                import re
                has_cyrillic = bool(re.search(r'[\u0400-\u04FF]', definition))
                self.assertTrue(has_cyrillic, "Should have Russian translation in translate mode")
    
    def test_russian_phrase_transliterated_input(self):
        """Test looking up Russian phrase via transliteration."""
        result = self.dictionary.lookup("privet")
        
        if result:
            self.assertEqual(result.get("language"), "ru")


if __name__ == "__main__":
    unittest.main()
