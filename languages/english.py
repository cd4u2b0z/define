"""
English language support.
"""

import re
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

from .base import Language


class English(Language):
    """English language dictionary using Free Dictionary API."""
    
    code = "en"
    name = "English"
    native_name = "English"
    
    API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"
    
    def __init__(self):
        self._idioms = None
        self._phrases = None
        self._variations = None
    
    def _load_json(self, path: Path) -> dict:
        """Load JSON file, return empty dict if not found."""
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (IOError, json.JSONDecodeError):
            return {}
    
    @property
    def idioms(self) -> dict:
        """Load idioms database lazily."""
        if self._idioms is None:
            idiom_file = Path(__file__).parent / "data" / "en_idioms.json"
            if idiom_file.exists():
                with open(idiom_file, 'r', encoding='utf-8') as f:
                    self._idioms = json.load(f)
            else:
                self._idioms = {}
        return self._idioms
    
    @property
    def phrases(self) -> dict:
        """Load phrases database lazily."""
        if self._phrases is None:
            phrase_file = Path(__file__).parent / "data" / "en_phrases.json"
            self._phrases = self._load_json(phrase_file)
            self._phrases.pop("_meta", None)
        return self._phrases
    
    @property
    def variations(self) -> dict:
        """Load variations (text speak, abbreviations, etc.) lazily."""
        if self._variations is None:
            var_file = Path(__file__).parent / "data" / "en_variations.json"
            self._variations = self._load_json(var_file)
            self._variations.pop("_meta", None)
        return self._variations
    
    def detect(self, text: str) -> bool:
        """
        Detect if text is English.
        
        Returns True only if text contains only ASCII letters and common punctuation.
        Russian/Cyrillic will return False.
        """
        # If it contains Cyrillic, it's not English
        if re.search(r'[\u0400-\u04FF]', text):
            return False
        
        # If it looks like Russian transliteration, let Russian handle it
        ru_patterns = r'(zh|kh|shch|sch|tch|chto|kto|ost$|stvo$|skiy$|skaya$|privet|spasibo|lyub|lub|noch|doch|zhizn|dusha|svobod|mechta|nadezh|krasot|schast|zdorov|pozhaluy|horosho|khorosho|harasho|plokho)'
        if re.search(ru_patterns, text.lower()):
            return False
        
        # Default to English for Latin script
        return bool(re.search(r'[a-zA-Z]', text))
    
    def normalize(self, text: str) -> str:
        """Normalize English input (lowercase, strip)."""
        return text.lower().strip()
    
    def lookup(self, word: str) -> Optional[dict]:
        """Look up an English word or phrase."""
        # Check phrases database first
        if word in self.phrases:
            return self._format_phrase(word, self.phrases[word])
        
        # Check if it's an abbreviation/text speak
        abbrev_result = self._lookup_abbreviation(word)
        if abbrev_result:
            return abbrev_result
        
        # Check for misspellings
        misspelling = self.variations.get("common_misspellings", {}).get(word)
        if misspelling:
            # Look up the correct spelling but note the misspelling
            result = self._lookup_api(misspelling)
            if result:
                result["misspelling_of"] = misspelling
                result["original_input"] = word
            return result
        
        # For multi-word phrases not in database, try API or breakdown
        if ' ' in word:
            # Try the phrase in API first
            result = self._lookup_api(word)
            if result:
                return result
            # Fall back to phrase lookup in database
            return self._lookup_phrase_breakdown(word)
        
        # Single word: use API
        return self._lookup_api(word)
    
    def _format_phrase(self, phrase: str, data: dict) -> dict:
        """Format phrase data to standard format."""
        return {
            "word": phrase,
            "phonetic": "",
            "audio": None,
            "is_phrase": True,
            "meanings": [{
                "partOfSpeech": "phrase",
                "definitions": [{
                    "definition": data.get("definition", ""),
                    "example": data.get("example"),
                    "synonyms": [],
                    "antonyms": []
                }],
                "synonyms": [],
                "antonyms": [],
                "register": data.get("register", "neutral")
            }],
            "usage": data.get("usage"),
            "variants": data.get("variants", []),
            "responses": data.get("responses", []),
            "origin": data.get("origin"),
            "note": data.get("note"),
            "source": "local phrase database"
        }
    
    def _lookup_abbreviation(self, word: str) -> Optional[dict]:
        """Look up text speak, abbreviations, etc."""
        word_lower = word.lower()
        
        # Check all variation categories
        for category in ["abbreviations", "text_speak", "british_american"]:
            if word_lower in self.variations.get(category, {}):
                expansion = self.variations[category][word_lower]
                return {
                    "word": word,
                    "phonetic": "",
                    "audio": None,
                    "is_abbreviation": True,
                    "meanings": [{
                        "partOfSpeech": category.replace("_", " "),
                        "definitions": [{
                            "definition": f"→ {expansion}",
                            "example": None,
                            "synonyms": [],
                            "antonyms": []
                        }],
                        "synonyms": [],
                        "antonyms": [],
                        "register": "informal" if category != "british_american" else "neutral"
                    }],
                    "expansion": expansion,
                    "category": category,
                    "source": "local variations database"
                }
        
        return None
    
    def _lookup_phrase_breakdown(self, phrase: str) -> Optional[dict]:
        """For unknown phrases, check if individual words are phrases/abbreviations."""
        words = phrase.split()
        found = []
        
        for w in words:
            if w in self.phrases:
                found.append({"word": w, "type": "phrase", "meaning": self.phrases[w].get("definition", "")})
            else:
                abbrev = self._lookup_abbreviation(w)
                if abbrev:
                    found.append({"word": w, "type": "abbreviation", "meaning": abbrev.get("expansion", "")})
        
        if not found:
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
                    "definition": f"Contains: {'; '.join(f'{f['word']} ({f['type']}): {f['meaning']}' for f in found)}",
                    "example": None,
                    "synonyms": [],
                    "antonyms": []
                }],
                "synonyms": [],
                "antonyms": []
            }],
            "word_breakdown": found,
            "source": "local dictionary (word breakdown)"
        }
    
    def _lookup_api(self, word: str) -> Optional[dict]:
        """Look up a word using the Free Dictionary API."""
        url = f"{self.API_URL}/{urllib.request.quote(word)}"
        
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "define/2.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
            return None
        
        if not data or not isinstance(data, list):
            return None
        
        entry = data[0]
        
        # Build result
        result = {
            "word": entry.get("word", word),
            "phonetic": self._extract_phonetic(entry),
            "audio": self._extract_audio(entry),
            "meanings": [],
            "etymology": self._extract_etymology(entry),
            "idioms": self._get_idioms(word),
            "source": "Free Dictionary API"
        }
        
        # Extract meanings
        for meaning in entry.get("meanings", []):
            pos = meaning.get("partOfSpeech", "")
            m = {
                "partOfSpeech": pos,
                "definitions": [],
                "register": self._detect_register(meaning)
            }
            
            for defn in meaning.get("definitions", []):
                d = {
                    "definition": defn.get("definition", ""),
                    "example": defn.get("example"),
                    "synonyms": defn.get("synonyms", []),
                    "antonyms": defn.get("antonyms", [])
                }
                m["definitions"].append(d)
            
            # Add top-level synonyms/antonyms
            m["synonyms"] = meaning.get("synonyms", [])
            m["antonyms"] = meaning.get("antonyms", [])
            
            result["meanings"].append(m)
        
        return result
    
    def _get_idioms(self, word: str) -> list:
        """Get idioms containing this word."""
        word_lower = word.lower()
        idiom_list = []
        
        # Direct match in idioms database
        if word_lower in self.idioms:
            idiom_list.extend(self.idioms[word_lower].get("idioms", []))
        
        # Also search for word in other idioms
        for key, data in self.idioms.items():
            if key != word_lower:
                for idiom in data.get("idioms", []):
                    if word_lower in idiom.get("phrase", "").lower():
                        if idiom not in idiom_list:
                            idiom_list.append(idiom)
        
        return idiom_list[:10]  # Limit to 10 idioms
    
    def _detect_register(self, meaning: dict) -> str:
        """Detect formality register from definition text."""
        definitions_text = " ".join(
            d.get("definition", "") for d in meaning.get("definitions", [])
        ).lower()
        
        if any(w in definitions_text for w in ["vulgar", "obscene", "taboo"]):
            return "vulgar"
        elif any(w in definitions_text for w in ["informal", "colloquial", "slang"]):
            return "informal"
        elif any(w in definitions_text for w in ["formal", "literary", "archaic"]):
            return "formal"
        return "neutral"
    
    def _extract_phonetic(self, entry: dict) -> str:
        """Extract phonetic transcription."""
        if entry.get("phonetic"):
            return entry["phonetic"]
        
        for p in entry.get("phonetics", []):
            if p.get("text"):
                return p["text"]
        
        return ""
    
    def _extract_audio(self, entry: dict) -> Optional[str]:
        """Extract audio URL."""
        for p in entry.get("phonetics", []):
            if p.get("audio"):
                return p["audio"]
        return None
    
    def _extract_etymology(self, entry: dict) -> Optional[str]:
        """Extract etymology if available."""
        # Free Dictionary API includes etymology in sourceUrls
        # but not directly. Return None for now.
        return entry.get("origin")
