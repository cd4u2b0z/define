"""
Vocabulary management for learning features with SM-2 Spaced Repetition.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict
import os


class SM2:
    """
    SM-2 Spaced Repetition Algorithm.
    
    Based on the SuperMemo SM-2 algorithm by Piotr Wozniak.
    https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
    
    Quality ratings:
        0 - Complete blackout, no recall
        1 - Incorrect, but upon seeing the answer, remembered
        2 - Incorrect, but answer seemed easy to recall
        3 - Correct with serious difficulty
        4 - Correct after hesitation
        5 - Perfect response
    """
    
    @staticmethod
    def calculate(quality: int, repetitions: int, easiness: float, interval: int) -> tuple:
        """
        Calculate next review parameters based on quality of recall.
        
        Args:
            quality: Quality of recall (0-5)
            repetitions: Number of successful repetitions
            easiness: Easiness factor (starts at 2.5)
            interval: Current interval in days
            
        Returns:
            Tuple of (new_repetitions, new_easiness, new_interval)
        """
        # Clamp quality to valid range
        quality = max(0, min(5, quality))
        
        # Update easiness factor
        new_easiness = easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        
        # Easiness factor should never go below 1.3
        new_easiness = max(1.3, new_easiness)
        
        if quality < 3:
            # Failed recall - reset repetitions
            new_repetitions = 0
            new_interval = 1
        else:
            # Successful recall
            if repetitions == 0:
                new_interval = 1
            elif repetitions == 1:
                new_interval = 6
            else:
                new_interval = round(interval * new_easiness)
            
            new_repetitions = repetitions + 1
        
        return new_repetitions, new_easiness, new_interval


class Vocabulary:
    """Manage saved vocabulary for learning with spaced repetition."""
    
    def __init__(self, vocab_file: Optional[Path] = None):
        if vocab_file is None:
            xdg_data = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
            vocab_file = xdg_data / "define" / "vocabulary.json"
        
        self.vocab_file = Path(vocab_file)
        self.vocab_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.vocab_file.exists():
            self.vocab_file.write_text("[]", encoding="utf-8")
    
    def _load(self) -> list:
        """Load vocabulary from file."""
        try:
            return json.loads(self.vocab_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save_vocab(self, vocab: list) -> None:
        """Save vocabulary to file."""
        self.vocab_file.write_text(
            json.dumps(vocab, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def _migrate_entry(self, entry: dict) -> dict:
        """Migrate old entry format to SM-2 format."""
        if "sm2_easiness" not in entry:
            entry["sm2_easiness"] = 2.5
            entry["sm2_interval"] = 0
            entry["sm2_repetitions"] = 0
            entry["nextReview"] = datetime.now().isoformat()
        return entry
    
    def save(self, result: dict) -> None:
        """
        Save a word to vocabulary.
        
        Args:
            result: Dictionary lookup result
        """
        vocab = self._load()
        
        word = result.get("word", result.get("normalized", ""))
        
        # Check if already saved
        for entry in vocab:
            if entry.get("word") == word:
                return  # Already exists
        
        # Extract first definition
        definition = ""
        pos = ""
        if result.get("meanings"):
            meaning = result["meanings"][0]
            pos = meaning.get("partOfSpeech", "")
            if meaning.get("definitions"):
                definition = meaning["definitions"][0].get("definition", "")
        
        entry = {
            "word": word,
            "original": result.get("original_input", word),
            "definition": definition,
            "partOfSpeech": pos,
            "language": result.get("language", "en"),
            "phonetic": result.get("phonetic", ""),
            "dateAdded": datetime.now().isoformat(),
            "timesReviewed": 0,
            "correctCount": 0,
            # SM-2 fields
            "sm2_easiness": 2.5,
            "sm2_interval": 0,
            "sm2_repetitions": 0,
            "nextReview": datetime.now().isoformat()
        }
        
        vocab.append(entry)
        self._save_vocab(vocab)
    
    def get_due_words(self) -> List[Dict]:
        """Get words that are due for review."""
        vocab = self._load()
        now = datetime.now()
        due = []
        
        for entry in vocab:
            entry = self._migrate_entry(entry)
            next_review = datetime.fromisoformat(entry.get("nextReview", now.isoformat()))
            if next_review <= now:
                due.append(entry)
        
        # Sort by next review date (oldest first)
        due.sort(key=lambda x: x.get("nextReview", ""))
        return due
    
    def update_sm2(self, word: str, quality: int) -> None:
        """
        Update SM-2 parameters for a word after review.
        
        Args:
            word: The word that was reviewed
            quality: Quality of recall (0-5)
        """
        vocab = self._load()
        
        for entry in vocab:
            if entry.get("word") == word:
                entry = self._migrate_entry(entry)
                
                # Calculate new SM-2 values
                new_reps, new_ease, new_interval = SM2.calculate(
                    quality,
                    entry["sm2_repetitions"],
                    entry["sm2_easiness"],
                    entry["sm2_interval"]
                )
                
                entry["sm2_repetitions"] = new_reps
                entry["sm2_easiness"] = new_ease
                entry["sm2_interval"] = new_interval
                
                # Calculate next review date
                next_review = datetime.now() + timedelta(days=new_interval)
                entry["nextReview"] = next_review.isoformat()
                
                # Update legacy counters
                entry["timesReviewed"] = entry.get("timesReviewed", 0) + 1
                if quality >= 3:
                    entry["correctCount"] = entry.get("correctCount", 0) + 1
                
                break
        
        self._save_vocab(vocab)
    
    def get_stats(self) -> dict:
        """Get vocabulary learning statistics."""
        vocab = self._load()
        now = datetime.now()
        
        total = len(vocab)
        due = 0
        mastered = 0  # Words with interval >= 21 days
        learning = 0  # Words with 0 < interval < 21
        new = 0       # Words never reviewed
        
        for entry in vocab:
            entry = self._migrate_entry(entry)
            interval = entry.get("sm2_interval", 0)
            next_review = datetime.fromisoformat(entry.get("nextReview", now.isoformat()))
            
            if next_review <= now:
                due += 1
            
            if interval == 0:
                new += 1
            elif interval >= 21:
                mastered += 1
            else:
                learning += 1
        
        return {
            "total": total,
            "due": due,
            "mastered": mastered,
            "learning": learning,
            "new": new
        }
    
    def review(self, formatter) -> None:
        """Review saved vocabulary (simple list view)."""
        vocab = self._load()
        
        if not vocab:
            formatter.info("No saved vocabulary / Словарь пуст")
            return
        
        formatter.header("Vocabulary Review / Повторение словаря")
        
        stats = self.get_stats()
        formatter.info(f"Total: {stats['total']} | Due: {stats['due']} | "
                      f"Mastered: {stats['mastered']} | Learning: {stats['learning']} | "
                      f"New: {stats['new']}\n")
        
        for i, entry in enumerate(vocab, 1):
            entry = self._migrate_entry(entry)
            word = entry.get("word", "")
            definition = entry.get("definition", "")
            pos = entry.get("partOfSpeech", "")
            interval = entry.get("sm2_interval", 0)
            
            # Status indicator
            if interval == 0:
                status = "🆕"
            elif interval >= 21:
                status = "✅"
            else:
                status = "📚"
            
            print(f"{i}. {status} {word}")
            if pos:
                print(f"   [{pos}]")
            print(f"   {definition}")
            if interval > 0:
                print(f"   (next review in {interval} days)")
            print()
    
    def quiz(self, formatter) -> None:
        """Quiz on saved vocabulary (random selection)."""
        vocab = self._load()
        
        if len(vocab) < 4:
            formatter.info("Need at least 4 saved words for quiz / "
                          "Нужно минимум 4 слова для викторины")
            return
        
        formatter.header("Vocabulary Quiz / Викторина")
        
        # Pick a random word
        correct_entry = random.choice(vocab)
        word = correct_entry.get("word", "")
        correct_def = correct_entry.get("definition", "")
        
        # Get 3 wrong answers
        wrong_entries = [e for e in vocab if e.get("word") != word]
        random.shuffle(wrong_entries)
        wrong_defs = [e.get("definition", "") for e in wrong_entries[:3]]
        
        # Combine and shuffle options
        options = [correct_def] + wrong_defs
        random.shuffle(options)
        correct_index = options.index(correct_def)
        
        print(f"What does '{word}' mean?\n")
        print(f"Что означает '{word}'?\n")
        
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        
        print()
        
        try:
            answer = input("Your answer (1-4) / Ваш ответ (1-4): ").strip()
            
            if answer == str(correct_index + 1):
                formatter.success("Correct! / Правильно!")
                # SM-2: quality 4 (correct after hesitation)
                self.update_sm2(word, 4)
            else:
                formatter.error(f"Wrong. The answer was {correct_index + 1} / "
                               f"Неверно. Правильный ответ: {correct_index + 1}")
                # SM-2: quality 1 (incorrect but remembered upon seeing)
                self.update_sm2(word, 1)
            
        except (KeyboardInterrupt, EOFError):
            print("\nQuiz cancelled / Викторина отменена")
    
    def study(self, formatter) -> None:
        """
        Spaced repetition study session.
        Reviews words that are due, using SM-2 algorithm.
        """
        due_words = self.get_due_words()
        
        if not due_words:
            stats = self.get_stats()
            formatter.success("All caught up! No words due for review. / "
                            "Всё повторено! Нет слов для повторения.")
            formatter.info(f"\nStats: {stats['total']} total, {stats['mastered']} mastered, "
                          f"{stats['learning']} learning")
            return
        
        formatter.header(f"Study Session / Сессия обучения ({len(due_words)} words due)")
        
        print("Rate your recall quality after each card:")
        print("  0 - Complete blackout / Полный провал")
        print("  1 - Wrong, but recognized answer / Неверно, но узнал ответ")
        print("  2 - Wrong, but answer felt familiar / Неверно, но знакомо")
        print("  3 - Correct with difficulty / Верно с трудом")
        print("  4 - Correct after thinking / Верно после раздумий")
        print("  5 - Perfect, instant recall / Идеально, сразу вспомнил")
        print("\nPress Enter to reveal answer, 'q' to quit / "
              "Enter - показать ответ, 'q' - выйти\n")
        print("-" * 50)
        
        reviewed = 0
        
        for entry in due_words:
            word = entry.get("word", "")
            definition = entry.get("definition", "")
            pos = entry.get("partOfSpeech", "")
            phonetic = entry.get("phonetic", "")
            lang = entry.get("language", "en")
            
            # Show word
            print(f"\n{'🇷🇺' if lang == 'ru' else '🇬🇧'} {word}")
            if phonetic:
                print(f"   {phonetic}")
            
            try:
                response = input("\n[Press Enter to reveal / Enter для ответа] ")
                if response.lower() == 'q':
                    break
                
                # Show answer
                print(f"\n   → {definition}")
                if pos:
                    print(f"   [{pos}]")
                
                # Get quality rating
                while True:
                    rating = input("\nQuality (0-5) / Оценка (0-5): ").strip()
                    if rating.lower() == 'q':
                        break
                    try:
                        quality = int(rating)
                        if 0 <= quality <= 5:
                            self.update_sm2(word, quality)
                            reviewed += 1
                            
                            # Show feedback
                            if quality >= 3:
                                print("✓ Good! ", end="")
                            else:
                                print("✗ Keep practicing! ", end="")
                            
                            # Show next review
                            vocab = self._load()
                            for e in vocab:
                                if e.get("word") == word:
                                    interval = e.get("sm2_interval", 1)
                                    print(f"Next review in {interval} day(s)")
                                    break
                            break
                        else:
                            print("Please enter 0-5 / Введите 0-5")
                    except ValueError:
                        print("Please enter a number 0-5 / Введите число 0-5")
                
                if rating.lower() == 'q':
                    break
                    
                print("-" * 50)
                
            except (KeyboardInterrupt, EOFError):
                print("\n\nSession ended / Сессия завершена")
                break
        
        # Summary
        print(f"\n{'=' * 50}")
        formatter.success(f"Session complete! Reviewed {reviewed} word(s) / "
                         f"Сессия завершена! Повторено {reviewed} слов(а)")
        
        stats = self.get_stats()
        formatter.info(f"Remaining due: {stats['due']} | Mastered: {stats['mastered']}")
    
    def export_anki(self, filename: str) -> int:
        """
        Export vocabulary to Anki-compatible CSV.
        
        Args:
            filename: Output CSV filename
            
        Returns:
            Number of words exported
        """
        vocab = self._load()
        
        if not vocab:
            return 0
        
        with open(filename, "w", encoding="utf-8") as f:
            for entry in vocab:
                word = entry.get("word", "")
                definition = entry.get("definition", "")
                phonetic = entry.get("phonetic", "")
                pos = entry.get("partOfSpeech", "")
                
                # Anki format: front;back
                front = word
                if phonetic:
                    front += f" ({phonetic})"
                
                back = definition
                if pos:
                    back = f"[{pos}] {back}"
                
                # Escape semicolons
                front = front.replace(";", ",")
                back = back.replace(";", ",")
                
                f.write(f"{front};{back}\n")
        
        return len(vocab)
