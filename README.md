# define

A terminal dictionary with deep grammatical support. Currently supports **English** and **Russian**, with more languages planned.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white) ![Bash](https://img.shields.io/badge/Bash-4.0+-4EAA25?style=flat&logo=gnu-bash&logoColor=white) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-blue)

> **Two versions available:** [Python](#installation) (recommended, with grammar) | [Bash](bash/) (lightweight, single-file)

---

## Features

### Core Features

| Feature | Description |
|---------|-------------|
| Multi-language | English + Russian (more planned) |
| Transliteration | Type Russian in Latin (`privet` → `привет`) |
| Offline Mode | 1,780+ words cached locally |
| Audio | Pronunciation playback |
| Learning | Save, review, quiz, Anki export |
| SM-2 | Spaced repetition for optimal review |

### Grammar Features (v2.0+)

| Feature | Example |
|---------|---------|
| Noun Gender | `дом` → masculine |
| Noun Cases | All 6 Russian cases with prompts |
| Verb Aspects | `писать` (impf) ↔ `написать` (pf) |
| Conjugation | Full tense tables (present, past, future) |
| Idioms | 50+ English, 25+ Russian idioms |
| Register | Formal/informal/colloquial markers |

### Enhanced Grammar (v2.2)

| Feature | Description |
|---------|-------------|
| Past/Future Tense | Full verb conjugation across all tenses |
| Imperative | Command forms (`пиши!`, `напишите!`) |
| Participles | Active, passive, present, past forms |
| Plural Cases | All 6 cases in singular and plural |
| Stress Marks | Automatic stress placement |

### Vocabulary Database

| Database | Entries |
|----------|---------|
| Russian Phrases | 936 entries (idioms, proverbs, expressions) |
| English Phrases | 845 entries (idioms, synonyms, antonyms) |
| Transliteration | 640+ Latin → Cyrillic mappings |
| Local Definitions | 212+ words with full grammar |

---

## Installation

### Quick Start (Linux/macOS)

```bash
# Clone the repository (anywhere you like)
git clone https://github.com/cd4u2b0z/define.git
cd define

# Run the installer (recommended)
./install.sh
```

The installer will:
- Let you choose **Python** (recommended) or **Bash** version
- Install commands to `~/.local/bin`
- Optionally add to your PATH automatically

### Manual Installation (Alternative)

```bash
# Add to PATH (add to ~/.zshrc or ~/.bashrc)
# Replace with wherever you cloned the repo
export PATH="$HOME/define:$PATH"

# Reload shell
source ~/.zshrc  # or ~/.bashrc

# Verify installation
define hello
```

### macOS

Just run `./install.sh` and choose **[1] Python** - no dependencies needed!

> **Note:** If you want the Bash version instead, you'll need `brew install bash curl jq` (macOS ships with Bash 3.2, but the script requires 4.0+).

### Linux (Ubuntu/Debian)

```bash
# Python version: no dependencies needed

# Bash version requires:
sudo apt install curl jq

# Optional for audio (both versions):
sudo apt install mpv  # or vlc, ffplay
```

### Linux (Arch)

```bash
# Bash version requires:
sudo pacman -S curl jq

# Optional for audio:
sudo pacman -S mpv
```

### Alternative: Symlinks

```bash
mkdir -p ~/.local/bin
ln -sf ~/projects/define/define ~/.local/bin/define

# Ensure ~/.local/bin is in PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Requirements

- **Python 3.8+** (stdlib only, no pip install needed)
- **Terminal with UTF-8** (for non-Latin display)
- **Internet** (for API lookups, offline cache available)

---

## Usage

### Basic Commands

```bash
# English words
define serendipity          # Basic lookup
define -f love              # Full info (examples, synonyms, etymology)
define -e run               # With examples
define -y happy             # With synonyms
define -t word              # With etymology
define -i break             # With idioms

# Russian (Cyrillic)
define привет
define -f любовь

# Russian (Transliteration - type without switching keyboard)
define privet               # → привет
define lyubov               # → любовь
define spasibo              # → спасибо

# Grammar mode (v2.2+)
define -g знать             # Full conjugation tables
define --grammar дом        # Singular and plural declensions
```

### All Options

| Option | Description |
|--------|-------------|
| `-a` | All definitions |
| `-s` | Short mode |
| `-e` | Show examples |
| `-y` | Show synonyms |
| `-t` | Show etymology |
| `-i` | Show idioms |
| `-f` | Full mode (all above) |
| `-g` | Grammar mode (tenses, cases, plurals) |
| `-p` | Play pronunciation |
| `-R` | Force Russian |
| `-E` | Force English |
| `-r` | Random word |
| `-j` | JSON output |
| `-o` | Offline only |
| `--save` | Save to vocabulary |
| `--review` | Review vocabulary |
| `--quiz` | Quiz mode |
| `--study` | SM-2 spaced repetition session |
| `--stats` | Learning statistics |
| `--export-anki FILE` | Export to Anki CSV |
| `--clear-cache` | Clear cache |

### Spaced Repetition (SM-2)

Built-in algorithm for optimal vocabulary learning:

```bash
# Start a study session with due words
./define --study

# Check your learning statistics
./define --stats
```

| Status | Meaning | Icon |
|--------|---------|------|
| New | Never reviewed | 🆕 |
| Learning | 1-20 day interval | 📚 |
| Mastered | 21+ day interval | ✅ |

---

## Example Output

### English Word

```bash
$ define serendipity

serendipity  /ˌsɛɹ.ənˈdɪp.ə.ti/

noun
  1. The occurrence of events by chance in a happy way
  2. Good luck in making unexpected discoveries

Synonyms: luck, fortune, chance, fate
```

### Russian Word with Grammar

```bash
$ define -g дом

дом
Gender: masculine (м.р.)

noun
  1. house, home

Singular:
  nominative: дом
  genitive: до́ма
  dative: до́му
  accusative: дом
  instrumental: до́мом
  prepositional: до́ме

Plural:
  nominative: дома́
  genitive: домо́в
  dative: дома́м
  accusative: дома́
  instrumental: дома́ми
  prepositional: дома́х
```

### Verb with Full Conjugation

```bash
$ define -g писать

писать
Aspect: imperfective (несов.)
Pair: написать

verb
  1. to write

Present:
  я: пишу́       мы: пи́шем
  ты: пи́шешь    вы: пи́шете
  он/она: пи́шет они: пи́шут

Past:
  м: писа́л   ж: писа́ла   ср: писа́ло   мн: писа́ли

Future:
  я: бу́ду писа́ть    мы: бу́дем писа́ть
  ты: бу́дешь писа́ть  вы: бу́дете писа́ть
  он: бу́дет писа́ть   они: бу́дут писа́ть

Imperative: пиши́! / пиши́те!
```

---

## Data Files

| File | Location |
|------|----------|
| Vocabulary | `~/.local/share/define/vocabulary.json` |
| History | `~/.local/share/define/history.txt` |
| Cache | `~/.cache/define/` |

---

## Testing

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
./define hello && ./define привет
```

**When adding new data:**
- After modifying `ru_definitions.json` → run `test_data.py`
- After modifying `ru_phrases.json` or `en_phrases.json` → run `test_data.py`
- After modifying `ru_grammar.json` → run `test_grammar.py`
- After changing language detection → run `test_languages.py`

---

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — Technical architecture
- [ROADMAP.md](ROADMAP.md) — Future plans
- [CHANGELOG.md](CHANGELOG.md) — Version history

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found | Add project to PATH or create symlinks |
| No audio | Install mpv/vlc (Linux) or use macOS built-in afplay |
| Text garbled | Ensure terminal supports UTF-8 (`echo $LANG`) |
| API timeout | Use `-o` for offline mode with cached data |

---

## Credits

Based on the original [define script](https://github.com/BreadOnPenguins/scripts/blob/master/shortcuts-menus/define) by [BreadOnPenguins](https://github.com/BreadOnPenguins)

### APIs

- [Free Dictionary API](https://dictionaryapi.dev/) — English definitions
- [Wiktionary REST API](https://en.wiktionary.org/api/rest_v1/) — Russian definitions

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

Original work by Dr. Baklava • [github.com/cd4u2b0z](https://github.com/cd4u2b0z) • 2026
