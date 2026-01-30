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
        
        # Phrases database
        self.phrases = self._load_json(data_dir / "ru_phrases.json")
        # Remove meta key if present
        self.phrases.pop("_meta", None)
        
        # Build reverse transliteration lookup for phrases
        self._phrase_translit_map = self._build_phrase_translit_map()
        
        # Idioms
        self._idioms = None
    
    def _build_phrase_translit_map(self) -> dict:
        """Build a map from transliterated phrases to Cyrillic."""
        mapping = {}
        for cyrillic, data in self.phrases.items():
            translit = data.get("transliteration", "").lower()
            if translit:
                # Store original transliteration
                mapping[translit] = cyrillic
                
                # Handle common variations for vowels
                variations = [translit]
                
                # yo/o variations (ё)
                if "yo" in translit:
                    variations.append(translit.replace("yo", "o"))
                if "o" in translit and "yo" not in translit:
                    variations.append(translit.replace("o", "yo"))
                
                # ye/e variations (е at start or after vowel)
                for v in list(variations):
                    if "ye" in v:
                        variations.append(v.replace("ye", "e"))
                    if "e" in v and "ye" not in v:
                        variations.append(v.replace("e", "ye"))
                
                # ya/ia variations (я)
                for v in list(variations):
                    if "ya" in v:
                        variations.append(v.replace("ya", "ia"))
                    if "ia" in v:
                        variations.append(v.replace("ia", "ya"))
                
                # yu/iu variations (ю)
                for v in list(variations):
                    if "yu" in v:
                        variations.append(v.replace("yu", "iu"))
                    if "iu" in v:
                        variations.append(v.replace("iu", "yu"))
                
                # vsyo/vse variation specifically
                for v in list(variations):
                    if "vsyo" in v:
                        variations.append(v.replace("vsyo", "vse"))
                    if "vse" in v and "vsyo" not in v:
                        variations.append(v.replace("vse", "vsyo"))
                
                # kh/h variations (х)
                for v in list(variations):
                    if "kh" in v:
                        variations.append(v.replace("kh", "h"))
                
                # Store all variations
                for var in set(variations):
                    mapping[var] = cyrillic
        
        return mapping
    
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
        
        # Check phrase lookup (transliterated phrases)
        if text in self._phrase_translit_map:
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
        
        # Check phrase lookup first (for multi-word input)
        if text in self._phrase_translit_map:
            return self._phrase_translit_map[text]
        
        # Check word lookup
        if text in self.word_lookup:
            return self.word_lookup[text]
        
        # For multi-word input, try to transliterate each word
        if ' ' in text:
            words = text.split()
            transliterated = []
            for word in words:
                if word in self.word_lookup:
                    transliterated.append(self.word_lookup[word])
                else:
                    # Apply transliteration rules
                    transliterated.append(self._transliterate_word(word))
            return ' '.join(transliterated)
        
        # Single word: apply transliteration rules
        return self._transliterate_word(text)
    
    def _transliterate_word(self, word: str) -> str:
        """Transliterate a single word from Latin to Cyrillic."""
        rules = self.translit_rules.get("rules", {})
        
        # Sort by length (longest first) to handle multi-char patterns
        sorted_rules = sorted(rules.items(), key=lambda x: -len(x[0]))
        
        result = word
        for latin, cyrillic in sorted_rules:
            result = result.replace(latin, cyrillic)
        
        return result
    
    def lookup(self, word: str) -> Optional[dict]:
        """Look up a Russian word or phrase."""
        # Check phrases database first (for translations)
        if word in self.phrases:
            return self._format_phrase(word, self.phrases[word])
        
        # Check local definitions
        if word in self.local_definitions:
            return self._format_local(word, self.local_definitions[word])
        
        # Fall back to Wiktionary for single words
        if ' ' not in word:
            return self._lookup_wiktionary(word)
        
        # For multi-word that's not in phrases, try to break down
        return self._lookup_phrase_words(word)
    
    def _format_phrase(self, phrase: str, data: dict) -> dict:
        """Format phrase data to standard format."""
        return {
            "word": phrase,
            "phonetic": data.get("transliteration", ""),
            "audio": None,
            "is_phrase": True,
            "meanings": [{
                "partOfSpeech": "phrase",
                "definitions": [{
                    "definition": data.get("translation", ""),
                    "example": None,
                    "synonyms": [],
                    "antonyms": []
                }],
                "synonyms": [],
                "antonyms": [],
                "register": data.get("register", "neutral")
            }],
            "literal": data.get("literal"),
            "usage": data.get("usage"),
            "source": "local phrase database"
        }
    
    def _lookup_phrase_words(self, phrase: str) -> Optional[dict]:
        """For unknown phrases, return definitions of individual words."""
        words = phrase.split()
        word_defs = []
        
        for w in words:
            if w in self.local_definitions:
                defn = self.local_definitions[w]
                word_defs.append({
                    "word": w,
                    "definition": defn.get("definition", ""),
                    "pos": defn.get("pos", "")
                })
        
        if not word_defs:
            return None
        
        return {
            "word": phrase,
            "phonetic": "",
            "audio": None,
            "is_phrase": True,
            "is_breakdown": True,
            "meanings": [{
                "partOfSpeech": "phrase (breakdown)",
                "definitions": [{
                    "definition": f"Individual words: {'; '.join(f'{w['word']} ({w['pos']}): {w['definition']}' for w in word_defs)}",
                    "example": None,
                    "synonyms": [],
                    "antonyms": []
                }],
                "synonyms": [],
                "antonyms": []
            }],
            "word_breakdown": word_defs,
            "source": "local dictionary (word breakdown)"
        }
    
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
