"""
Russian language support with transliteration.
"""

import re
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

from .base import Language


class Russian(Language):
    """Russian language with transliteration and Wiktionary support."""
    
    code = "ru"
    name = "Russian"
    native_name = "Русский"
    
    WIKTIONARY_URL = "https://en.wiktionary.org/api/rest_v1/page/definition"
    
    # Patterns that indicate Russian (even in Latin script)
    DETECTION_PATTERNS = re.compile(
        r'(zh|kh|shch|sch|tch|'
        r'chto|kto|gde|kogda|pochemu|kak|'
        r'privet|privyet|spasibo|poka|'
        r'khorosho|horosho|harasho|'
        r'da|net|niet|'
        r'ost$|stvo$|stvo$|nie$|tie$|'
        r'skiy$|skaya$|skoe$|skie$|'
        r'ova$|eva$|enko$|'
        r'yat$|vat$|nut$)',
        re.IGNORECASE
    )
    
    def __init__(self):
        # Load data files
        data_dir = Path(__file__).parent / "data"
        
        # Transliteration rules
        self.translit_rules = self._load_json(data_dir / "ru_translit.json")
        
        # Word lookup (common words with special handling)
        self.word_lookup = self.translit_rules.get("word_lookup", {})
        
        # Local definitions
        self.local_definitions = self._load_json(data_dir / "ru_definitions.json")
        
        # Idioms
        self._idioms = None
    
    @property
    def idioms(self) -> dict:
        """Load idioms database lazily."""
        if self._idioms is None:
            idiom_file = Path(__file__).parent / "data" / "ru_idioms.json"
            if idiom_file.exists():
                with open(idiom_file, 'r', encoding='utf-8') as f:
                    self._idioms = json.load(f)
            else:
                self._idioms = {}
        return self._idioms
    
    def _load_json(self, path: Path) -> dict:
        """Load JSON file, return empty dict if not found."""
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (IOError, json.JSONDecodeError):
            return {}
    
    def detect(self, text: str) -> bool:
        """Detect if text is Russian."""
        text = text.lower().strip()
        
        # Already Cyrillic?
        if re.search(r'[\u0400-\u04FF]', text):
            return True
        
        # Check word lookup
        if text in self.word_lookup:
            return True
        
        # Check patterns
        if self.DETECTION_PATTERNS.search(text):
            return True
        
        return False
    
    def normalize(self, text: str) -> str:
        """Transliterate Latin to Cyrillic if needed."""
        # If already Cyrillic, just lowercase
        if re.search(r'[\u0400-\u04FF]', text):
            return text.lower().strip()
        
        text = text.lower().strip()
        
        # Check word lookup first
        if text in self.word_lookup:
            return self.word_lookup[text]
        
        # Apply transliteration rules
        rules = self.translit_rules.get("rules", {})
        
        # Sort by length (longest first) to handle multi-char patterns
        sorted_rules = sorted(rules.items(), key=lambda x: -len(x[0]))
        
        result = text
        for latin, cyrillic in sorted_rules:
            result = result.replace(latin, cyrillic)
        
        return result
    
    def lookup(self, word: str) -> Optional[dict]:
        """Look up a Russian word."""
        # Check local definitions first
        if word in self.local_definitions:
            return self._format_local(word, self.local_definitions[word])
        
        # Fall back to Wiktionary
        return self._lookup_wiktionary(word)
    
    def _format_local(self, word: str, data: dict) -> dict:
        """Format local definition to standard format."""
        return {
            "word": word,
            "phonetic": data.get("phonetic", ""),
            "audio": None,
            "meanings": [{
                "partOfSpeech": data.get("pos", ""),
                "definitions": [{
                    "definition": data.get("definition", ""),
                    "example": data.get("example"),
                    "synonyms": data.get("synonyms", []),
                    "antonyms": data.get("antonyms", [])
                }],
                "synonyms": data.get("synonyms", []),
                "antonyms": data.get("antonyms", []),
                "register": data.get("register", self._detect_register(data))
            }],
            "etymology": data.get("etymology"),
            "cases": data.get("cases"),
            "aspect": data.get("aspect"),
            "pair": data.get("pair"),
            "conjugation": data.get("conjugation"),
            "gender": data.get("gender"),
            "idioms": self._get_idioms(word),
            "source": "local dictionary"
        }
    
    def _detect_register(self, data: dict) -> str:
        """Detect formality register from definition."""
        definition = data.get("definition", "").lower()
        pos = data.get("pos", "").lower()
        
        if any(w in definition or w in pos for w in ["vulgar", "obscene", "мат"]):
            return "vulgar"
        elif any(w in definition for w in ["informal", "colloquial", "slang", "разг"]):
            return "informal"
        elif any(w in definition for w in ["formal", "literary", "книжн"]):
            return "formal"
        return "neutral"
    
    def _get_idioms(self, word: str) -> list:
        """Get idioms containing this word."""
        idiom_list = []
        
        # Direct match only for short words (< 3 chars)
        if word in self.idioms:
            idiom_list.extend(self.idioms[word].get("idioms", []))
        
        # For longer words, also search in other entries
        if len(word) >= 3:
            for key, data in self.idioms.items():
                if key != word:
                    for idiom in data.get("idioms", []):
                        phrase = idiom.get("phrase", "")
                        # Match word boundary
                        if f" {word}" in phrase or f"{word} " in phrase or phrase.startswith(word) or phrase.endswith(word):
                            if idiom not in idiom_list:
                                idiom_list.append(idiom)
        
        return idiom_list[:10]
    
    def _lookup_wiktionary(self, word: str) -> Optional[dict]:
        """Look up word on Wiktionary."""
        url = f"{self.WIKTIONARY_URL}/{urllib.request.quote(word)}"
        
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "define/2.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
            return None
        
        # Parse Wiktionary response
        russian_data = data.get("ru") or data.get("en", [])
        
        if not russian_data:
            return None
        
        result = {
            "word": word,
            "phonetic": "",
            "audio": None,
            "meanings": [],
            "etymology": None,
            "idioms": self._get_idioms(word),  # Add idioms from local database
            "source": "Wiktionary"
        }
        
        for entry in russian_data:
            pos = entry.get("partOfSpeech", "")
            
            m = {
                "partOfSpeech": pos,
                "definitions": [],
                "synonyms": [],
                "antonyms": []
            }
            
            for defn in entry.get("definitions", []):
                definition_text = defn.get("definition", "")
                # Clean up HTML
                definition_text = re.sub(r'<[^>]+>', '', definition_text)
                
                d = {
                    "definition": definition_text,
                    "example": None,
                    "synonyms": [],
                    "antonyms": []
                }
                
                # Extract examples
                examples = defn.get("examples", [])
                if examples:
                    d["example"] = examples[0]
                
                m["definitions"].append(d)
            
            if m["definitions"]:
                result["meanings"].append(m)
        
        return result if result["meanings"] else None
