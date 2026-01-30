"""
Tests for the Cache module.
"""

import json
import os
import tempfile
import time
import unittest
from pathlib import Path

# Add parent to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.cache import Cache


class TestCache(unittest.TestCase):
    """Test cases for the Cache class."""
    
    def setUp(self):
        """Create a temporary cache directory for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = Cache(cache_dir=Path(self.temp_dir), ttl_days=1)
    
    def tearDown(self):
        """Clean up temporary directory."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_cache_miss(self):
        """Test that getting a non-existent key returns None."""
        result = self.cache.get("nonexistent", "en")
        self.assertIsNone(result)
    
    def test_cache_set_and_get(self):
        """Test basic set and get operations."""
        test_data = {
            "word": "hello",
            "definition": "a greeting"
        }
        
        self.cache.set("hello", "en", test_data)
        result = self.cache.get("hello", "en")
        
        self.assertEqual(result, test_data)
    
    def test_cache_different_languages(self):
        """Test that same word in different languages are cached separately."""
        en_data = {"word": "да", "definition": "yes (English context)"}
        ru_data = {"word": "да", "definition": "да (Russian context)"}
        
        self.cache.set("да", "en", en_data)
        self.cache.set("да", "ru", ru_data)
        
        self.assertEqual(self.cache.get("да", "en"), en_data)
        self.assertEqual(self.cache.get("да", "ru"), ru_data)
    
    def test_cache_unicode(self):
        """Test caching words with Cyrillic and special characters."""
        test_data = {
            "word": "привет",
            "definition": "hello, hi",
            "transliteration": "privet"
        }
        
        self.cache.set("привет", "ru", test_data)
        result = self.cache.get("привет", "ru")
        
        self.assertEqual(result, test_data)
        self.assertEqual(result["word"], "привет")
    
    def test_cache_clear(self):
        """Test clearing all cached entries."""
        # Add some entries
        self.cache.set("word1", "en", {"definition": "test1"})
        self.cache.set("word2", "en", {"definition": "test2"})
        self.cache.set("слово", "ru", {"definition": "test3"})
        
        # Verify they exist
        self.assertIsNotNone(self.cache.get("word1", "en"))
        self.assertIsNotNone(self.cache.get("word2", "en"))
        
        # Clear and verify
        count = self.cache.clear()
        self.assertEqual(count, 3)
        
        self.assertIsNone(self.cache.get("word1", "en"))
        self.assertIsNone(self.cache.get("word2", "en"))
        self.assertIsNone(self.cache.get("слово", "ru"))
    
    def test_cache_hash_consistency(self):
        """Test that hash generation is consistent."""
        hash1 = self.cache._hash("test", "en")
        hash2 = self.cache._hash("test", "en")
        hash3 = self.cache._hash("test", "ru")
        
        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)
    
    def test_cache_complex_data(self):
        """Test caching complex nested data structures."""
        complex_data = {
            "word": "run",
            "meanings": [
                {
                    "partOfSpeech": "verb",
                    "definitions": [
                        {"definition": "to move quickly", "example": "He runs fast"},
                        {"definition": "to operate", "example": "Run the program"}
                    ]
                },
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {"definition": "an act of running"}
                    ]
                }
            ],
            "synonyms": ["sprint", "jog", "dash"],
            "nested": {"deep": {"value": True}}
        }
        
        self.cache.set("run", "en", complex_data)
        result = self.cache.get("run", "en")
        
        self.assertEqual(result, complex_data)
        self.assertEqual(len(result["meanings"]), 2)
        self.assertEqual(result["nested"]["deep"]["value"], True)


class TestCacheExpiration(unittest.TestCase):
    """Test cache TTL expiration (requires time manipulation)."""
    
    def test_cache_ttl_parameter(self):
        """Test that TTL is properly set."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(cache_dir=Path(temp_dir), ttl_days=7)
            self.assertEqual(cache.ttl_seconds, 7 * 86400)
            
            cache2 = Cache(cache_dir=Path(temp_dir), ttl_days=30)
            self.assertEqual(cache2.ttl_seconds, 30 * 86400)


if __name__ == "__main__":
    unittest.main()
