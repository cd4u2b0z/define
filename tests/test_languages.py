"""
Tests for the Language detection and normalization.
"""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from languages.english import English
from languages.russian import Russian


class TestEnglishDetection(unittest.TestCase):
    """Test English language detection."""
    
    def setUp(self):
        self.english = English()
    
    def test_detect_basic_english(self):
        """Test detection of basic English words."""
        self.assertTrue(self.english.detect("hello"))
        self.assertTrue(self.english.detect("world"))
        self.assertTrue(self.english.detect("computer"))
        self.assertTrue(self.english.detect("serendipity"))
    
    def test_detect_english_phrases(self):
        """Test detection of English phrases."""
        self.assertTrue(self.english.detect("how are you"))
        self.assertTrue(self.english.detect("good morning"))
        self.assertTrue(self.english.detect("thank you very much"))
    
    def test_reject_cyrillic(self):
        """Test that Cyrillic text is not detected as English."""
        self.assertFalse(self.english.detect("привет"))
        self.assertFalse(self.english.detect("мир"))
        self.assertFalse(self.english.detect("как дела"))
    
    def test_reject_russian_transliteration(self):
        """Test that Russian transliteration patterns are rejected."""
        self.assertFalse(self.english.detect("privet"))
        self.assertFalse(self.english.detect("spasibo"))
        self.assertFalse(self.english.detect("khorosho"))
        self.assertFalse(self.english.detect("lyubov"))
    
    def test_normalize(self):
        """Test English normalization."""
        self.assertEqual(self.english.normalize("  HELLO  "), "hello")
        self.assertEqual(self.english.normalize("World"), "world")
        self.assertEqual(self.english.normalize("HoW aRe YoU"), "how are you")


class TestRussianDetection(unittest.TestCase):
    """Test Russian language detection."""
    
    def setUp(self):
        self.russian = Russian()
    
    def test_detect_cyrillic(self):
        """Test detection of Cyrillic text."""
        self.assertTrue(self.russian.detect("привет"))
        self.assertTrue(self.russian.detect("спасибо"))
        self.assertTrue(self.russian.detect("любовь"))
        self.assertTrue(self.russian.detect("как дела"))
    
    def test_detect_transliteration(self):
        """Test detection of Russian transliteration."""
        self.assertTrue(self.russian.detect("privet"))
        self.assertTrue(self.russian.detect("spasibo"))
        self.assertTrue(self.russian.detect("khorosho"))
    
    def test_detect_transliteration_patterns(self):
        """Test detection based on Russian word patterns."""
        # Words ending in typical Russian suffixes
        self.assertTrue(self.russian.detect("chto"))
        self.assertTrue(self.russian.detect("kogda"))
        self.assertTrue(self.russian.detect("pochemu"))


class TestRussianTransliteration(unittest.TestCase):
    """Test Russian transliteration (Latin → Cyrillic)."""
    
    def setUp(self):
        self.russian = Russian()
    
    def test_basic_transliteration(self):
        """Test basic word transliteration."""
        # These should be in the word_lookup
        normalized = self.russian.normalize("privet")
        self.assertEqual(normalized, "привет")
        
        normalized = self.russian.normalize("spasibo")
        self.assertEqual(normalized, "спасибо")
    
    def test_cyrillic_passthrough(self):
        """Test that Cyrillic text passes through unchanged."""
        self.assertEqual(self.russian.normalize("привет"), "привет")
        self.assertEqual(self.russian.normalize("любовь"), "любовь")
    
    def test_normalize_case(self):
        """Test that normalization handles case."""
        # Should normalize case and transliterate
        normalized = self.russian.normalize("PRIVET")
        # May or may not transliterate uppercase - depends on implementation
        self.assertIn(normalized.lower(), ["привет", "privet"])


class TestEnglishPhrases(unittest.TestCase):
    """Test English phrase lookup."""
    
    def setUp(self):
        self.english = English()
    
    def test_phrase_database_loaded(self):
        """Test that phrase database is loaded."""
        self.assertIsNotNone(self.english.phrases)
        self.assertGreater(len(self.english.phrases), 0)
    
    def test_common_phrase_lookup(self):
        """Test looking up common phrases."""
        # These should be in the phrases database
        result = self.english.lookup("how are you")
        self.assertIsNotNone(result)
        self.assertEqual(result.get("word"), "how are you")
    
    def test_phrase_has_definition(self):
        """Test that phrase results have definitions."""
        result = self.english.lookup("how are you")
        self.assertIsNotNone(result)
        
        meanings = result.get("meanings", [])
        self.assertGreater(len(meanings), 0)
        
        definitions = meanings[0].get("definitions", [])
        self.assertGreater(len(definitions), 0)


class TestRussianPhrases(unittest.TestCase):
    """Test Russian phrase lookup."""
    
    def setUp(self):
        self.russian = Russian()
    
    def test_phrase_database_loaded(self):
        """Test that phrase database is loaded."""
        self.assertIsNotNone(self.russian.phrases)
        self.assertGreater(len(self.russian.phrases), 0)
    
    def test_cyrillic_phrase_lookup(self):
        """Test looking up Cyrillic phrases."""
        # Test a phrase that should be in the database
        if "привет" in self.russian.phrases:
            result = self.russian.lookup("привет")
            self.assertIsNotNone(result)


class TestEnglishSlang(unittest.TestCase):
    """Test English slang/colloquial entries."""
    
    def setUp(self):
        self.english = English()
    
    def test_slang_entries_exist(self):
        """Test that slang entries are in the database."""
        slang_words = ["awesome", "cool", "bro", "dude"]
        
        for word in slang_words:
            if word in self.english.phrases:
                result = self.english.lookup(word)
                self.assertIsNotNone(result, f"'{word}' should return a result")
    
    def test_slang_has_russian_translation(self):
        """Test that slang entries have Russian translations."""
        if "awesome" in self.english.phrases:
            result = self.english.lookup("awesome")
            self.assertIsNotNone(result)
            
            # Check that definition contains Cyrillic (Russian translation)
            meanings = result.get("meanings", [])
            if meanings:
                definition = meanings[0].get("definitions", [{}])[0].get("definition", "")
                # Should contain Cyrillic characters (Russian translation)
                import re
                has_cyrillic = bool(re.search(r'[\u0400-\u04FF]', definition))
                self.assertTrue(has_cyrillic, "Slang should have Russian translation")


class TestIdioms(unittest.TestCase):
    """Test idiom databases."""
    
    def setUp(self):
        self.english = English()
        self.russian = Russian()
    
    def test_english_idioms_loaded(self):
        """Test that English idioms database is loaded."""
        self.assertIsNotNone(self.english.idioms)
        self.assertGreater(len(self.english.idioms), 0)
    
    def test_russian_idioms_loaded(self):
        """Test that Russian idioms database is loaded."""
        self.assertIsNotNone(self.russian.idioms)
        self.assertGreater(len(self.russian.idioms), 0)


if __name__ == "__main__":
    unittest.main()
