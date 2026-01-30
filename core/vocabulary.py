"""
Vocabulary management for learning features.
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Optional
import os


class Vocabulary:
    """Manage saved vocabulary for learning."""
    
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
            "correctCount": 0
        }
        
        vocab.append(entry)
        self._save_vocab(vocab)
    
    def review(self, formatter) -> None:
        """Review saved vocabulary."""
        vocab = self._load()
        
        if not vocab:
            formatter.info("No saved vocabulary / Словарь пуст")
            return
        
        formatter.header("Vocabulary Review / Повторение словаря")
        formatter.info(f"Total words: {len(vocab)} / Всего слов: {len(vocab)}\n")
        
        for i, entry in enumerate(vocab, 1):
            word = entry.get("word", "")
            definition = entry.get("definition", "")
            pos = entry.get("partOfSpeech", "")
            lang = entry.get("language", "en")
            
            lang_flag = "🇷🇺" if lang == "ru" else "🇬🇧"
            
            print(f"{i}. {word}")
            if pos:
                print(f"   [{pos}]")
            print(f"   {definition}")
            print()
    
    def quiz(self, formatter) -> None:
        """Quiz on saved vocabulary."""
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
                correct_entry["correctCount"] = correct_entry.get("correctCount", 0) + 1
            else:
                formatter.error(f"Wrong. The answer was {correct_index + 1} / "
                               f"Неверно. Правильный ответ: {correct_index + 1}")
            
            correct_entry["timesReviewed"] = correct_entry.get("timesReviewed", 0) + 1
            self._save_vocab(vocab)
            
        except (KeyboardInterrupt, EOFError):
            print("\nQuiz cancelled / Викторина отменена")
    
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
