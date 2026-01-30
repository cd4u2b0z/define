"""
Tests for data file integrity.

These tests verify that the JSON data files are valid and contain expected data.
"""

import json
import re
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

DATA_DIR = Path(__file__).parent.parent / "languages" / "data"


class TestDataFileIntegrity(unittest.TestCase):
    """Test that all data files are valid JSON."""
    
    def test_en_phrases_valid_json(self):
        """Test en_phrases.json is valid JSON."""
        path = DATA_DIR / "en_phrases.json"
        self.assertTrue(path.exists(), "en_phrases.json should exist")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, dict)
    
    def test_ru_phrases_valid_json(self):
        """Test ru_phrases.json is valid JSON."""
        path = DATA_DIR / "ru_phrases.json"
        self.assertTrue(path.exists(), "ru_phrases.json should exist")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, dict)
    
    def test_en_idioms_valid_json(self):
        """Test en_idioms.json is valid JSON."""
        path = DATA_DIR / "en_idioms.json"
        self.assertTrue(path.exists(), "en_idioms.json should exist")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, dict)
    
    def test_ru_idioms_valid_json(self):
        """Test ru_idioms.json is valid JSON."""
        path = DATA_DIR / "ru_idioms.json"
        self.assertTrue(path.exists(), "ru_idioms.json should exist")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, dict)
    
    def test_ru_translit_valid_json(self):
        """Test ru_translit.json is valid JSON."""
        path = DATA_DIR / "ru_translit.json"
        self.assertTrue(path.exists(), "ru_translit.json should exist")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, dict)
    
    def test_ru_definitions_valid_json(self):
        """Test ru_definitions.json is valid JSON."""
        path = DATA_DIR / "ru_definitions.json"
        self.assertTrue(path.exists(), "ru_definitions.json should exist")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, dict)


class TestEnglishPhrasesContent(unittest.TestCase):
    """Test English phrases database content."""
    
    @classmethod
    def setUpClass(cls):
        with open(DATA_DIR / "en_phrases.json", 'r', encoding='utf-8') as f:
            cls.data = json.load(f)
            cls.data.pop("_meta", None)
    
    def test_minimum_entries(self):
        """Test that we have a minimum number of entries."""
        self.assertGreaterEqual(len(self.data), 800, "Should have at least 800 entries")
    
    def test_entries_have_definition(self):
        """Test that entries have definition field."""
        missing_definition = []
        
        for word, entry in self.data.items():
            if isinstance(entry, dict) and "definition" not in entry:
                missing_definition.append(word)
        
        self.assertEqual(
            len(missing_definition), 0,
            f"Entries missing definition: {missing_definition[:10]}..."
        )
    
    def test_slang_entries_have_russian(self):
        """Test that new slang entries have Russian translations."""
        # These are entries we added with Russian translations
        slang_words = ["awesome", "cool", "dope", "bro", "dude"]
        
        found_any = False
        for word in slang_words:
            if word in self.data:
                found_any = True
                definition = self.data[word].get("definition", "")
                has_cyrillic = bool(re.search(r'[\u0400-\u04FF]', definition))
                self.assertTrue(
                    has_cyrillic,
                    f"'{word}' should have Russian translation, got: {definition}"
                )
        
        self.assertTrue(found_any, "Should find at least one slang word")


class TestRussianPhrasesContent(unittest.TestCase):
    """Test Russian phrases database content."""
    
    @classmethod
    def setUpClass(cls):
        with open(DATA_DIR / "ru_phrases.json", 'r', encoding='utf-8') as f:
            cls.data = json.load(f)
            cls.data.pop("_meta", None)
    
    def test_minimum_entries(self):
        """Test that we have a minimum number of entries."""
        self.assertGreaterEqual(len(self.data), 900, "Should have at least 900 entries")
    
    def test_entries_have_translation(self):
        """Test that entries have translation/definition field."""
        missing = []
        
        for word, entry in self.data.items():
            if isinstance(entry, dict):
                has_translation = "translation" in entry or "definition" in entry
                if not has_translation:
                    missing.append(word)
        
        # Allow some entries to be missing (might have different structure)
        self.assertLess(
            len(missing), 50,
            f"Too many entries missing translation: {missing[:10]}..."
        )
    
    def test_entries_have_transliteration(self):
        """Test that Russian entries have transliteration."""
        missing = []
        
        for word, entry in self.data.items():
            if isinstance(entry, dict) and "transliteration" not in entry:
                missing.append(word)
        
        # Most entries should have transliteration
        missing_pct = len(missing) / len(self.data) * 100
        self.assertLess(
            missing_pct, 10,
            f"{missing_pct:.1f}% entries missing transliteration"
        )
    
    def test_cyrillic_keys(self):
        """Test that most keys are Cyrillic."""
        cyrillic_count = 0
        
        for word in self.data.keys():
            if re.search(r'[\u0400-\u04FF]', word):
                cyrillic_count += 1
        
        cyrillic_pct = cyrillic_count / len(self.data) * 100
        self.assertGreater(
            cyrillic_pct, 90,
            f"Only {cyrillic_pct:.1f}% of keys are Cyrillic"
        )


class TestTransliterationData(unittest.TestCase):
    """Test transliteration database."""
    
    @classmethod
    def setUpClass(cls):
        with open(DATA_DIR / "ru_translit.json", 'r', encoding='utf-8') as f:
            cls.data = json.load(f)
    
    def test_has_word_lookup(self):
        """Test that word_lookup section exists."""
        self.assertIn("word_lookup", self.data)
    
    def test_common_words_present(self):
        """Test that common Russian words are in lookup."""
        lookup = self.data.get("word_lookup", {})
        
        common_words = ["privet", "spasibo", "da", "net", "khorosho"]
        
        for word in common_words:
            self.assertIn(
                word, lookup,
                f"Common word '{word}' should be in transliteration lookup"
            )
    
    def test_transliteration_produces_cyrillic(self):
        """Test that transliterations produce Cyrillic text."""
        lookup = self.data.get("word_lookup", {})
        
        for latin, cyrillic in list(lookup.items())[:50]:
            has_cyrillic = bool(re.search(r'[\u0400-\u04FF]', cyrillic))
            self.assertTrue(
                has_cyrillic,
                f"'{latin}' -> '{cyrillic}' should produce Cyrillic"
            )


class TestIdiomsData(unittest.TestCase):
    """Test idioms databases."""
    
    def test_english_idioms_structure(self):
        """Test English idioms have expected structure."""
        with open(DATA_DIR / "en_idioms.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Should have root words with idiom data
        for word, entry in data.items():
            if word.startswith("_"):
                continue
            # Entry can be a dict with 'idioms' key or a list directly
            if isinstance(entry, dict):
                self.assertIn("idioms", entry, f"'{word}' entry should have 'idioms' key")
                self.assertIsInstance(entry["idioms"], list)
            else:
                self.assertIsInstance(
                    entry, list,
                    f"Idioms for '{word}' should be a list or dict with 'idioms'"
                )
    
    def test_russian_idioms_structure(self):
        """Test Russian idioms have expected structure."""
        with open(DATA_DIR / "ru_idioms.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for word, entry in data.items():
            if word.startswith("_"):
                continue
            # Entry can be a dict with 'idioms' key or a list directly
            if isinstance(entry, dict):
                self.assertIn("idioms", entry, f"'{word}' entry should have 'idioms' key")
                self.assertIsInstance(entry["idioms"], list)
            else:
                self.assertIsInstance(
                    entry, list,
                    f"Idioms for '{word}' should be a list or dict with 'idioms'"
                )


if __name__ == "__main__":
    unittest.main()
