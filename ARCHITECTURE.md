# 󰙵 Architecture / Архитектура

Technical documentation for the define dictionary tool.

Техническая документация для словаря define.

English | [Русский](#русский-1)

---

## 󰉋 Project Structure / Структура проекта

```
define/
├── 󰡯 define                    # Main entry point (shebang script)
├── 󰌠 cli.py                    # Command-line interface & argument parsing
│
├── 󰉋 core/                     # Core functionality
│   ├── 󰌠 __init__.py
│   ├── 󰌠 dictionary.py         # Multi-language dictionary orchestrator
│   ├── 󰌠 cache.py              # XDG-compliant caching system
│   ├── 󰌠 vocabulary.py         # Learning features (save, review, quiz)
│   └── 󰌠 audio.py              # Pronunciation playback
│
├── 󰉋 languages/                # Language handlers (plugin architecture)
│   ├── 󰌠 __init__.py           # Language registry
│   ├── 󰌠 base.py               # Abstract Language base class
│   ├── 󰌠 english.py            # English: Free Dictionary API + idioms
│   ├── 󰌠 russian.py            # Russian: Wiktionary API + transliteration
│   └── 󰉋 data/                 # Static data files
│       ├── 󰘦 ru_translit.json      # 643 transliteration mappings
│       ├── 󰘦 ru_definitions.json   # 177+ local definitions + grammar
│       ├── 󰘦 en_idioms.json        # 180+ English idioms
│       └── 󰘦 ru_idioms.json        # 25+ Russian idioms (including mat)
│
├── 󰉋 ui/                       # User interface
│   ├── 󰌠 __init__.py
│   └── 󰌠 formatter.py          # Terminal output formatting & colors
│
├── 󰡯 определить                # Russian command wrapper → define
├── 󰡯 словарь                   # Russian command wrapper → define
└── 󰡯 слово                     # Russian command wrapper → define
```

---

## 󰙵 System Architecture / Системная архитектура

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Input                                │
│                   define -f привет                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CLI (cli.py)                                │
│  ├─ Argument parsing (argparse)                                  │
│  ├─ Mode detection (full, short, examples, etc.)                 │
│  └─ Output routing (terminal, JSON, Anki)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                Dictionary (core/dictionary.py)                   │
│  ├─ Language detection (Cyrillic vs Latin)                       │
│  ├─ Language handler dispatch                                    │
│  └─ Result aggregation                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│   English Handler        │     │   Russian Handler        │
│   (languages/english.py) │     │   (languages/russian.py) │
│                          │     │                          │
│  ├─ Free Dictionary API  │     │  ├─ Transliteration      │
│  ├─ Idioms database      │     │  │   (privet → привет)   │
│  ├─ Register detection   │     │  ├─ Local definitions    │
│  └─ Synonyms/Antonyms    │     │  ├─ Wiktionary API       │
│                          │     │  ├─ Grammar (gender,     │
│                          │     │  │   cases, conjugation) │
│                          │     │  └─ Idioms database      │
└─────────────────────────┘     └─────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Cache (core/cache.py)                         │
│  ├─ XDG Base Directory compliance                                │
│  │   └─ ~/.cache/define/                                         │
│  ├─ JSON file per word lookup                                    │
│  ├─ TTL-based expiration (7 days default)                        │
│  └─ Offline fallback support                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Formatter (ui/formatter.py)                     │
│  ├─ ANSI color codes (256-color support)                         │
│  ├─ Part-of-speech styling                                       │
│  ├─ Grammar tables (cases, conjugation)                          │
│  ├─ Idiom formatting                                             │
│  └─ Terminal width detection                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Terminal Output                             │
│                                                                  │
│  дом                                                             │
│  Gender: masculine (м.р.)                                        │
│                                                                  │
│  noun                                                            │
│    1. house, home                                                │
│                                                                  │
│  Cases:                                                          │
│    nominative (кто? что?): дом                                   │
│    genitive (кого? чего?): до́ма                                  │
│    ...                                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 󰌠 Module Details / Детали модулей

### 󰌌 CLI Module (`cli.py`)

The command-line interface handles:

| Function | Description |
|----------|-------------|
| `parse_args()` | Argument parsing with argparse |
| `main()` | Entry point, mode routing |
| `output_json()` | JSON format output |
| `output_terminal()` | Formatted terminal output |

**Key Features:**
- Mutually exclusive mode groups (short vs full)
- Russian command detection via `sys.argv[0]`
- XDG directory initialization

### 󰗊 Language Base Class (`languages/base.py`)

Abstract interface for language handlers:

```python
class Language(ABC):
    code: str           # ISO 639-1 code ("en", "ru")
    name: str           # English name
    native_name: str    # Native name (Русский)
    
    @abstractmethod
    def detect(self, text: str) -> bool:
        """Detect if text is in this language"""
        
    @abstractmethod
    def normalize(self, text: str) -> str:
        """Normalize input (transliteration, case)"""
        
    @abstractmethod
    def lookup(self, word: str) -> dict | None:
        """Look up word, return definition dict"""
```

### 󰗃 Russian Handler (`languages/russian.py`)

**Transliteration System:**

```python
# Example mappings (643 total)
{
    "privet": "привет",
    "spasibo": "спасибо",
    "lyubov": "любовь",
    "khorosho": "хорошо",
    ...
}
```

**Grammar Data Structure:**

```python
# Noun with cases
{
    "дом": {
        "pos": "noun",
        "definition": "house, home",
        "gender": "masculine",
        "cases": {
            "nominative": "дом",
            "genitive": "до́ма",
            "dative": "до́му",
            "accusative": "дом",
            "instrumental": "до́мом",
            "prepositional": "до́ме"
        }
    }
}

# Verb with conjugation
{
    "писать": {
        "pos": "verb",
        "definition": "to write",
        "aspect": "imperfective",
        "pair": "написать",
        "conjugation": {
            "я": "пишу́",
            "ты": "пи́шешь",
            "он/она": "пи́шет",
            "мы": "пи́шем",
            "вы": "пи́шете",
            "они": "пи́шут"
        }
    }
}
```

### 󰎁 English Handler (`languages/english.py`)

**API Integration:**

```python
# Free Dictionary API
url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

# Response structure
{
    "word": "serendipity",
    "phonetic": "/ˌsɛɹ.ənˈdɪp.ə.ti/",
    "meanings": [
        {
            "partOfSpeech": "noun",
            "definitions": [...],
            "synonyms": [...],
            "antonyms": [...]
        }
    ]
}
```

**Idiom Matching:**

```python
# Only match words 3+ characters to avoid noise
if len(word) >= 3 and word in self._idioms:
    return self._idioms[word]
```

### 󰆸 Cache System (`core/cache.py`)

**XDG Compliance:**

| Directory | Path | Purpose |
|-----------|------|---------|
| Cache | `~/.cache/define/` | API response cache |
| Data | `~/.local/share/define/` | Vocabulary, history |
| Config | `~/.config/define/` | User settings |

**Cache Key Format:**

```python
# Hash-based filename to handle special characters
cache_key = hashlib.md5(f"{lang}:{word}".encode()).hexdigest()
cache_file = cache_dir / f"{cache_key}.json"
```

### 󰗅 Formatter (`ui/formatter.py`)

**Color Scheme:**

| Element | Color Code | Use |
|---------|------------|-----|
| Word | Bold + Cyan | Main headword |
| POS | Yellow | Part of speech |
| Definition | Default | Definition text |
| Example | Dim | Usage examples |
| Register | Red | Vulgar markers |
| Idiom | Magenta | Idiom headers |

**Grammar Display:**

```python
# Case labels with Russian questions
CASE_LABELS = {
    "nominative": "nominative (кто? что?)",
    "genitive": "genitive (кого? чего?)",
    "dative": "dative (кому? чему?)",
    "accusative": "accusative (кого? что?)",
    "instrumental": "instrumental (кем? чем?)",
    "prepositional": "prepositional (о ком? о чём?)"
}

# Gender abbreviations
GENDER_LABELS = {
    "masculine": "masculine (м.р.)",
    "feminine": "feminine (ж.р.)",
    "neuter": "neuter (ср.р.)"
}
```

---

## 󰓾 Data Flow / Поток данных

### Lookup Flow

```
1. User input: "privet"
   │
2. CLI parses arguments
   │
3. Dictionary.lookup("privet")
   │
4. Language detection: Latin chars → could be English or transliterated Russian
   │
5. Try Russian first (transliteration check)
   │  ├─ Found in ru_translit.json: "privet" → "привет"
   │  └─ Lookup "привет" in local definitions
   │
6. Return result with grammar
   │
7. Formatter renders to terminal
```

### Caching Flow

```
1. Lookup request for "serendipity"
   │
2. Check cache: ~/.cache/define/{hash}.json
   │  ├─ Cache hit + not expired → Return cached
   │  └─ Cache miss or expired → Continue
   │
3. API request to Free Dictionary API
   │
4. Store response in cache with timestamp
   │
5. Return result
```

---

## 󰏗 Adding a New Language / Добавление нового языка

1. **Create language handler:**

```python
# languages/german.py
from .base import Language

class German(Language):
    code = "de"
    name = "German"
    native_name = "Deutsch"
    
    def detect(self, text: str) -> bool:
        # Check for German-specific characters or patterns
        german_chars = set("äöüßÄÖÜ")
        return bool(set(text) & german_chars)
    
    def normalize(self, text: str) -> str:
        return text.lower()
    
    def lookup(self, word: str) -> dict | None:
        # Implement API lookup
        pass
```

2. **Register in `languages/__init__.py`:**

```python
from .german import German
LANGUAGES = [English, Russian, German]
```

3. **Add data files if needed:**

```
languages/data/
├── de_definitions.json
└── de_idioms.json
```

---

## 󰏖 Dependencies / Зависимости

**Zero external dependencies** — uses Python standard library only:

| Module | Use |
|--------|-----|
| `urllib.request` | HTTP requests |
| `json` | Data serialization |
| `hashlib` | Cache key generation |
| `pathlib` | Path handling |
| `argparse` | CLI argument parsing |
| `subprocess` | Audio playback |
| `re` | Regular expressions |

---

# Русский

## 󰉋 Структура проекта

Проект организован по модульному принципу:

- **cli.py** — интерфейс командной строки
- **core/** — основная функциональность (кэш, словарь, обучение)
- **languages/** — обработчики языков (плагинная архитектура)
- **ui/** — форматирование вывода

## 󰗊 Особенности русского модуля

### Транслитерация

643 отображения латиница → кириллица для ввода без русской раскладки.

### Грамматика

- **Существительные**: род + все 6 падежей с вопросами
- **Глаголы**: вид + видовая пара + спряжение
- **Идиомы**: включая мат с транслитерацией

### Локальный словарь

177+ слов с полной грамматикой для офлайн-режима.

---

"Архитектура — это замороженная музыка." — Гёте 🏛️
