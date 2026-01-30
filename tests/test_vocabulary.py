"""
Tests for the Vocabulary and SM-2 Spaced Repetition system.
"""

import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.vocabulary import Vocabulary, SM2


class TestSM2Algorithm(unittest.TestCase):
    """Test the SM-2 spaced repetition algorithm."""
    
    def test_perfect_recall_increases_interval(self):
        """Test that perfect recall (5) increases interval."""
        # First review
        reps, ease, interval = SM2.calculate(5, 0, 2.5, 0)
        self.assertEqual(reps, 1)
        self.assertEqual(interval, 1)
        
        # Second review
        reps, ease, interval = SM2.calculate(5, 1, ease, 1)
        self.assertEqual(reps, 2)
        self.assertEqual(interval, 6)
        
        # Third review (interval grows)
        reps, ease, interval = SM2.calculate(5, 2, ease, 6)
        self.assertEqual(reps, 3)
        self.assertGreater(interval, 6)
    
    def test_failed_recall_resets(self):
        """Test that failed recall (0-2) resets repetitions."""
        # Start with some progress
        reps, ease, interval = 3, 2.5, 15
        
        # Fail (quality 0)
        new_reps, new_ease, new_interval = SM2.calculate(0, reps, ease, interval)
        self.assertEqual(new_reps, 0)
        self.assertEqual(new_interval, 1)
        
        # Fail (quality 2)
        new_reps, new_ease, new_interval = SM2.calculate(2, reps, ease, interval)
        self.assertEqual(new_reps, 0)
        self.assertEqual(new_interval, 1)
    
    def test_quality_3_is_passing(self):
        """Test that quality 3 (correct with difficulty) still passes."""
        reps, ease, interval = SM2.calculate(3, 0, 2.5, 0)
        self.assertEqual(reps, 1)  # Should increment
    
    def test_easiness_never_below_1_3(self):
        """Test that easiness factor never goes below 1.3."""
        # Repeatedly fail to drive down easiness
        ease = 2.5
        for _ in range(10):
            _, ease, _ = SM2.calculate(0, 0, ease, 1)
        
        self.assertGreaterEqual(ease, 1.3)
    
    def test_easiness_increases_with_perfect_recall(self):
        """Test that easiness increases with quality 5."""
        _, new_ease, _ = SM2.calculate(5, 0, 2.5, 0)
        self.assertGreater(new_ease, 2.5)
    
    def test_easiness_decreases_with_poor_recall(self):
        """Test that easiness decreases with low quality."""
        _, new_ease, _ = SM2.calculate(3, 0, 2.5, 0)
        self.assertLess(new_ease, 2.5)
    
    def test_quality_clamped_to_valid_range(self):
        """Test that quality values are clamped to 0-5."""
        # Quality below 0
        reps, ease, interval = SM2.calculate(-1, 0, 2.5, 0)
        self.assertIsNotNone(interval)  # Should not crash
        
        # Quality above 5
        reps, ease, interval = SM2.calculate(10, 0, 2.5, 0)
        self.assertIsNotNone(interval)


class TestVocabulary(unittest.TestCase):
    """Test the Vocabulary class."""
    
    def setUp(self):
        """Create a temporary vocabulary file."""
        self.temp_dir = tempfile.mkdtemp()
        self.vocab_file = Path(self.temp_dir) / "vocabulary.json"
        self.vocabulary = Vocabulary(vocab_file=self.vocab_file)
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_save_word(self):
        """Test saving a word to vocabulary."""
        result = {
            "word": "test",
            "meanings": [{
                "partOfSpeech": "noun",
                "definitions": [{"definition": "a procedure"}]
            }],
            "language": "en"
        }
        
        self.vocabulary.save(result)
        
        vocab = self.vocabulary._load()
        self.assertEqual(len(vocab), 1)
        self.assertEqual(vocab[0]["word"], "test")
    
    def test_save_word_has_sm2_fields(self):
        """Test that saved words have SM-2 fields."""
        result = {
            "word": "test",
            "meanings": [{"partOfSpeech": "noun", "definitions": [{"definition": "a test"}]}],
            "language": "en"
        }
        
        self.vocabulary.save(result)
        vocab = self.vocabulary._load()
        
        self.assertIn("sm2_easiness", vocab[0])
        self.assertIn("sm2_interval", vocab[0])
        self.assertIn("sm2_repetitions", vocab[0])
        self.assertIn("nextReview", vocab[0])
        
        self.assertEqual(vocab[0]["sm2_easiness"], 2.5)
        self.assertEqual(vocab[0]["sm2_interval"], 0)
        self.assertEqual(vocab[0]["sm2_repetitions"], 0)
    
    def test_no_duplicate_saves(self):
        """Test that the same word is not saved twice."""
        result = {"word": "duplicate", "meanings": [], "language": "en"}
        
        self.vocabulary.save(result)
        self.vocabulary.save(result)
        
        vocab = self.vocabulary._load()
        self.assertEqual(len(vocab), 1)
    
    def test_get_due_words_new_words_are_due(self):
        """Test that new words are immediately due for review."""
        result = {"word": "newword", "meanings": [], "language": "en"}
        self.vocabulary.save(result)
        
        due = self.vocabulary.get_due_words()
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0]["word"], "newword")
    
    def test_update_sm2(self):
        """Test updating SM-2 parameters after review."""
        result = {"word": "reviewed", "meanings": [], "language": "en"}
        self.vocabulary.save(result)
        
        # Review with quality 5 (perfect)
        self.vocabulary.update_sm2("reviewed", 5)
        
        vocab = self.vocabulary._load()
        entry = vocab[0]
        
        self.assertEqual(entry["sm2_repetitions"], 1)
        self.assertEqual(entry["sm2_interval"], 1)
        self.assertEqual(entry["timesReviewed"], 1)
        self.assertEqual(entry["correctCount"], 1)
    
    def test_update_sm2_failed_review(self):
        """Test SM-2 update after failed review."""
        result = {"word": "failed", "meanings": [], "language": "en"}
        self.vocabulary.save(result)
        
        # Review with quality 1 (failed)
        self.vocabulary.update_sm2("failed", 1)
        
        vocab = self.vocabulary._load()
        entry = vocab[0]
        
        self.assertEqual(entry["sm2_repetitions"], 0)  # Reset
        self.assertEqual(entry["sm2_interval"], 1)
        self.assertEqual(entry["timesReviewed"], 1)
        self.assertEqual(entry["correctCount"], 0)  # Not incremented for failure
    
    def test_get_stats(self):
        """Test vocabulary statistics."""
        # Add some words
        for i in range(5):
            result = {"word": f"word{i}", "meanings": [], "language": "en"}
            self.vocabulary.save(result)
        
        stats = self.vocabulary.get_stats()
        
        self.assertEqual(stats["total"], 5)
        self.assertEqual(stats["new"], 5)
        self.assertEqual(stats["due"], 5)
        self.assertEqual(stats["learning"], 0)
        self.assertEqual(stats["mastered"], 0)
    
    def test_migrate_entry(self):
        """Test that old entries are migrated to SM-2 format."""
        # Create an old-format entry (missing SM-2 fields)
        old_entry = {
            "word": "old",
            "definition": "ancient",
            "language": "en",
            "dateAdded": datetime.now().isoformat(),
            "timesReviewed": 0,
            "correctCount": 0
        }
        
        # Save directly to file (bypassing save method)
        self.vocab_file.write_text(json.dumps([old_entry]), encoding="utf-8")
        
        # Load and migrate
        vocab = self.vocabulary._load()
        migrated = self.vocabulary._migrate_entry(vocab[0])
        
        # Check SM-2 fields were added
        self.assertIn("sm2_easiness", migrated)
        self.assertEqual(migrated["sm2_easiness"], 2.5)
        self.assertIn("sm2_interval", migrated)
        self.assertIn("sm2_repetitions", migrated)
        self.assertIn("nextReview", migrated)


class TestVocabularyExport(unittest.TestCase):
    """Test vocabulary export functionality."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.vocab_file = Path(self.temp_dir) / "vocabulary.json"
        self.vocabulary = Vocabulary(vocab_file=self.vocab_file)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_export_anki_empty(self):
        """Test exporting empty vocabulary."""
        export_file = Path(self.temp_dir) / "export.csv"
        count = self.vocabulary.export_anki(str(export_file))
        self.assertEqual(count, 0)
    
    def test_export_anki_with_words(self):
        """Test exporting vocabulary to Anki format."""
        result = {
            "word": "hello",
            "phonetic": "/həˈloʊ/",
            "meanings": [{
                "partOfSpeech": "interjection",
                "definitions": [{"definition": "a greeting"}]
            }],
            "language": "en"
        }
        self.vocabulary.save(result)
        
        export_file = Path(self.temp_dir) / "export.csv"
        count = self.vocabulary.export_anki(str(export_file))
        
        self.assertEqual(count, 1)
        self.assertTrue(export_file.exists())
        
        content = export_file.read_text(encoding="utf-8")
        self.assertIn("hello", content)
        self.assertIn("greeting", content)


if __name__ == "__main__":
    unittest.main()
