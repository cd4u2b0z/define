# 󰗊 определить / define

Terminal dictionary for English and Russian with deep grammatical support.

Терминальный словарь для английского и русского языков с полной грамматической поддержкой.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white) ![Bash](https://img.shields.io/badge/Bash-4.0+-4EAA25?style=flat&logo=gnu-bash&logoColor=white) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-blue)

> **Two versions available:** [Python](#-installation--установка) (recommended, with grammar) | [Bash](bash/) (lightweight, single-file)

English | [Русский](#русский)

---

## 󰐕 Features / Возможности

### 󰗊 Core Features

| Feature | Description | Функция |
|---------|-------------|---------|
| 󰗊 Bilingual | English + Russian support | Английский + русский |
| 󰌌 Transliteration | Type Russian in Latin (`privet` → `привет`) | Транслитерация |
| 󰎈 Offline Mode | 1,780+ words cached locally (936 RU + 845 EN) | Офлайн режим |
| 󰕾 Audio | Pronunciation playback | Произношение |
| 󰃀 Learning | Save, review, quiz, Anki export | Обучение |
| 󰇦 SM-2 | Spaced repetition for optimal review | Интервальное повторение |

### 󱗊 Grammar Features (v2.0)

| Feature | Example | Описание |
|---------|---------|----------|
| 󰚹 Noun Gender | `дом` → м.р. (masculine) | Род существительных |
| 󰆥 Noun Cases | All 6 cases with question prompts | Падежи с вопросами |
| 󱗃 Verb Aspects | `писать` (impf) ↔ `написать` (pf) | Вид глагола |
| 󰛺 Conjugation | Full present tense tables | Спряжение |
| 󰏪 Idioms | 50+ English, 25+ Russian idioms | Идиомы |
| 󰖚 Register | Formal/informal/colloquial markers | Регистр |

### 󰗊 Vocabulary Database (v2.1)

| Database | Entries | Content |
|----------|---------|----------|
| 󰗃 Russian Phrases | 936 entries | Idioms, proverbs, common phrases, expressions |
| 󰗊 English Phrases | 845 entries | Idioms, synonyms, antonyms, numbers/time |
| 󰌌 Transliteration | 640+ mappings | Latin → Cyrillic conversion |
| 󰏪 English Idioms | 50+ expressions | Break a leg, piece of cake, etc. |
| 󰏪 Russian Idioms | 25+ expressions | Common Russian expressions |

### 󰇦 Spaced Repetition (v2.1)

Built-in SM-2 algorithm for optimal vocabulary learning:

```bash
# Start a study session with due words
./define --study

# Check your learning statistics
./define --stats
```

| Status | Meaning | Icon |
|--------|---------|------|
| New | Never reviewed |  󰎔 |
| Learning | 1-20 day interval |  󱓷 |
| Mastered | 21+ day interval |  󰘽 |

**Quality Ratings (0-5):**
- 0-2: Failed recall → Reset to 1 day
- 3-5: Successful recall → Interval grows

### 󰗃 Russian Grammar Display

```
дом
Gender: masculine (м.р.)

noun
  1. house, home

Cases:
  nominative (кто? что?): дом
  genitive (кого? чего?): до́ма
  dative (кому? чему?): до́му
  accusative (кого? что?): дом
  instrumental (кем? чем?): до́мом
  prepositional (о ком? о чём?): до́ме
```

```
писать
Aspect: imperfective (несов.)
Aspectual pair: написать

verb
  1. to write

Conjugation (present):
  я: пишу́
  ты: пи́шешь
  он/она: пи́шет
  мы: пи́шем
  вы: пи́шете
  они: пи́шут
```

---

## 󰏗 Installation / Установка

### 󰈈 Quick Start (Linux/macOS)

```bash
# Clone the repository / Клонируйте репозиторий
git clone https://github.com/cd4u2b0z/define.git ~/projects/define
cd ~/projects/define

# Add to PATH (add to ~/.zshrc or ~/.bashrc)
# Добавьте в PATH (добавьте в ~/.zshrc или ~/.bashrc)
export PATH="$HOME/projects/define:$PATH"

# Reload shell / Перезапустите оболочку
source ~/.zshrc  # or ~/.bashrc
```

### 󰀵 macOS Specific

```bash
# No additional dependencies required!
# Python 3.8+ comes with macOS

# Optional: for audio pronunciation / Для произношения (опционально):
# macOS uses built-in afplay - no installation needed
# macOS использует встроенный afplay - установка не требуется

# Verify installation / Проверьте установку:
define hello
определить привет
```

### 󰣇 Linux (Ubuntu/Debian)

```bash
# Python 3.8+ usually pre-installed
# Обычно Python 3.8+ уже установлен

# Optional: for audio pronunciation / Для произношения (опционально):
sudo apt install mpv  # or vlc, ffplay
```

### 󰣇 Linux (Arch)

```bash
# Optional: for audio pronunciation
sudo pacman -S mpv
```

### 󰆍 Alternative: Symlinks

```bash
# Create symlinks to ~/.local/bin
# Создайте символические ссылки в ~/.local/bin
mkdir -p ~/.local/bin
ln -sf ~/projects/define/define ~/.local/bin/define
ln -sf ~/projects/define/определить ~/.local/bin/определить
ln -sf ~/projects/define/словарь ~/.local/bin/словарь
ln -sf ~/projects/define/слово ~/.local/bin/слово

# Ensure ~/.local/bin is in PATH
export PATH="$HOME/.local/bin:$PATH"
```

### 󰏖 Requirements / Требования

- **Python 3.8+** (stdlib only, no pip install needed)
- **Terminal with UTF-8** (for Cyrillic display)
- **Internet** (for API lookups, offline cache available)

---

## 󰙨 Usage / Использование

### 󰌌 Basic Commands / Базовые команды

```bash
# English words / Английские слова
define serendipity          # Basic lookup
define -f love              # Full info (examples, synonyms, etymology)
define -e run               # With examples
define -y happy             # With synonyms
define -t word              # With etymology
define -i break             # With idioms

# Russian (Cyrillic) / Русский (кириллица)
define привет
define -f любовь
определить счастье
словарь друг
слово мир

# Russian (Transliteration) / Русский (транслитерация)
define privet               # → привет
define lyubov               # → любовь
define spasibo              # → спасибо
```

### 󰘳 All Options / Все опции

| Option | Description | Описание |
|--------|-------------|----------|
| `-a` | All definitions | Все определения |
| `-s` | Short mode | Краткий режим |
| `-e` | Show examples | С примерами |
| `-y` | Show synonyms | С синонимами |
| `-t` | Show etymology | С этимологией |
| `-i` | Show idioms | С идиомами |
| `-f` | Full mode (all above) | Полный режим |
| `-p` | Play pronunciation | Произношение |
| `-R` | Force Russian | Принудительно русский |
| `-E` | Force English | Принудительно английский |
| `-r` | Random word | Случайное слово |
| `-j` | JSON output | Вывод JSON |
| `-o` | Offline only | Только офлайн |
| `--save` | Save to vocabulary | Сохранить в словарь |
| `--review` | Review vocabulary | Повторение |
| `--quiz` | Quiz mode | Викторина |
| `--export-anki FILE` | Export to Anki CSV | Экспорт в Anki |
| `--clear-cache` | Clear cache | Очистить кэш |

### 󰗊 Russian Commands / Русские команды

| Command | Translation | Description |
|---------|-------------|-------------|
| `define` | — | Main command |
| `определить` | "to define" | Найти определение |
| `словарь` | "dictionary" | Словарь |
| `слово` | "word" | Слово |

All commands accept the same options / Все команды принимают одинаковые опции.

---

## 󰏪 Idioms / Идиомы

### English Idioms (50+)

```bash
$ define -i break

Idioms & Expressions:
  • break a leg [informal]
    good luck (theatrical)
  • break the ice
    make people feel more comfortable
  • break the bank [informal]
    cost too much money
  • break even
    neither profit nor lose
  ...
```

### Russian Idioms (25+)

```bash
$ define -f душа

Idioms & Expressions:
  • душа в душу (dusha v dushu)
    in perfect harmony; like two peas in a pod
  • от души (ot dushi)
    from the heart; sincerely
  • душа болит (dusha bolit)
    the soul aches; feeling deep sorrow
  ...
```

---

## 󰉋 Data Files / Файлы данных

| File | Location | Description |
|------|----------|-------------|
| Vocabulary | `~/.local/share/define/vocabulary.json` | Saved words |
| History | `~/.local/share/define/history.txt` | Lookup history |
| Cache | `~/.cache/define/` | API response cache |

---

## 󰙅 Documentation / Документация

- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture / Техническая архитектура
- [ROADMAP.md](ROADMAP.md) - Future plans / Планы развития

---

## 󰋗 Troubleshooting / Устранение неполадок

| Issue | Solution |
|-------|----------|
| Command not found | Add project to PATH or create symlinks |
| No audio | Install mpv/vlc (Linux) or use macOS built-in afplay |
| Russian text garbled | Ensure terminal supports UTF-8 (`echo $LANG`) |
| API timeout | Use `-o` for offline mode with cached data |

---

## 󱗗 Credits / Благодарности

Based on the original [define script](https://github.com/BreadOnPenguins/scripts/blob/master/shortcuts-menus/define) by [BreadOnPenguins](https://github.com/BreadOnPenguins)

### APIs

- [Free Dictionary API](https://dictionaryapi.dev/) - English definitions
- [Wiktionary REST API](https://en.wiktionary.org/api/rest_v1/) - Russian definitions

---

## 󰿃 License

MIT License - See [LICENSE](LICENSE) for details.

---

Original work by Dr. Baklava • [github.com/cd4u2b0z](https://github.com/cd4u2b0z) • 2026

---

# Русский

## 󰐕 Возможности

### Основные функции

- **Двуязычный словарь** — английский и русский
- **Транслитерация** — вводите русские слова латиницей (`privet` → `привет`)
- **Офлайн режим** — 1,780+ слов в локальном кэше (936 RU + 845 EN)
- **Произношение** — аудио для английских слов
- **Обучение** — сохранение, повторение, викторина, экспорт в Anki

### Грамматика (v2.0)

- **Род существительных** — м.р., ж.р., ср.р.
- **Падежи** — все 6 падежей с вопросами (кто? что? кого? чего? и т.д.)
- **Вид глагола** — совершенный/несовершенный с видовыми парами
- **Спряжение** — полные таблицы настоящего времени
- **Идиомы** — 25+ русских идиом и выражений
- **Фразы** — 936 русских и 845 английских фраз с переводами
- **Регистр** — формальный/неформальный/разговорный

## 󰏗 Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/cd4u2b0z/define.git ~/projects/define

# Добавьте в PATH (~/.zshrc или ~/.bashrc)
export PATH="$HOME/projects/define:$PATH"

# Перезапустите оболочку
source ~/.zshrc
```

## 󰙨 Использование

```bash
# Кириллица
определить любовь
словарь -f дом
слово привет

# Транслитерация
define lyubov
define -f dom
define privet

# Полная информация
define -f писать    # спряжение, вид, пара
define -f книга     # род, падежи
define -i время     # идиомы и выражения
```

---

## 󰙨 Testing / Тестирование

Run the test suite to verify dictionary health after making changes:

```bash
# Run all tests (115 tests)
python3 tests/run_tests.py

# Run specific test modules
python3 tests/test_grammar.py -v     # Grammar tests (38)
python3 tests/test_data.py -v        # Data integrity tests (18)
python3 tests/test_languages.py -v   # Language detection tests (20)
python3 tests/test_vocabulary.py -v  # SM-2 & vocabulary tests (17)
python3 tests/test_dictionary.py -v  # Dictionary tests (14)
python3 tests/test_cache.py -v       # Cache tests (8)

# Quick sanity check
./define привет && ./define hello && ./define знать --grammar
```

**When adding new data:**
- After adding words to `ru_definitions.json`, run `test_data.py`
- After adding phrases to `ru_phrases.json` or `en_phrases.json`, run `test_data.py`
- After modifying grammar in `ru_grammar.json`, run `test_grammar.py`
- After changing language detection, run `test_languages.py`

---

"Слово — серебро, молчание — золото." 󰗋
