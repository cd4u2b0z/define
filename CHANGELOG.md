# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-01-30

### Added
- **Enhanced Grammar System** with comprehensive Russian verb and noun support
- `--grammar` / `-g` flag to display extended grammatical information
- **Past Tense Conjugation** for all verbs (я писал, ты писал, etc.)
- **Future Tense Conjugation** for perfective and imperfective verbs
- **Imperative Mood** for commands (пиши!, напиши!, идите!)
- **Participles** — active, passive, present, past forms
- **Plural Declensions** — all 6 cases in plural form
- **Stress Marks** — automatic stress placement for Russian words
- New `core/grammar.py` module with:
  - StressMarker class for stress mark utilities
  - VerbConjugator class for tense generation
  - NounDecliner class for case/number declension
  - GrammarEngine class orchestrating all grammar features
- `languages/data/ru_grammar.json` with:
  - 30+ verbs with full conjugation (all tenses, imperative, participles)
  - 20+ nouns with singular and plural declensions
  - Irregular forms (идти→шёл, человек→люди, ребёнок→дети)
- **38 new unit tests** for grammar features (115 total tests)

### Changed
- Formatter now displays extended grammar when `--grammar` flag is used
- Russian handler prioritizes definitions over phrase lookups
- Version bumped to 2.2.0

### Technical
- Added `tests/test_grammar.py` with comprehensive grammar tests
- Grammar data loaded lazily from JSON files
- Velar consonant handling for genitive plural (-ов → -ей)

## [2.1.0] - 2026-01-30

### Added
- **SM-2 Spaced Repetition Algorithm** for optimal vocabulary review scheduling
- `--study` command for interactive spaced repetition study sessions
- `--stats` command for vocabulary learning statistics
- Quality ratings (0-5) for self-assessment during study
- Automatic interval calculation based on recall quality
- Migration support for existing vocabulary entries to SM-2 format
- **Comprehensive test suite** with 77 tests covering:
  - Cache operations (8 tests)
  - Language detection and transliteration (20 tests)
  - Dictionary orchestration (14 tests)
  - Data file integrity (18 tests)
  - SM-2 algorithm and vocabulary (17 tests)

### Changed
- Vocabulary entries now include SM-2 fields (easiness, interval, repetitions, nextReview)
- `--review` now shows learning status icons (🆕 New, 📚 Learning, ✅ Mastered)
- `--quiz` now integrates with SM-2 (updates intervals based on answers)

### Technical
- Added `tests/` directory with unittest-based test suite
- SM2 class in `core/vocabulary.py` implements the algorithm
- Vocabulary class extended with `get_due_words()`, `update_sm2()`, `get_stats()`, `study()`

## [2.1.0-vocab] - 2026-01-30

### Added
- **936 Russian→English phrase entries** covering:
  - Slang and colloquial expressions
  - Idioms and proverbs
  - Common phrases and greetings
  - Emotions and feelings
  - Time and numbers
  - Body parts
- **845 English→Russian phrase entries** covering:
  - Slang (awesome, cool, dope, bro, etc.)
  - Idioms (break a leg, piece of cake, etc.)
  - Synonyms and antonyms
  - Numbers and time expressions
  - Common phrases
- Transliterations for all Russian translations
- Category tagging (type field: slang, idiom, proverb, etc.)

## [2.0.0] - 2026-01-30

### Added
- **Russian Grammar Support**
  - Noun gender display (м.р., ж.р., ср.р.)
  - All 6 Russian cases with question prompts
  - Verb aspects (perfective/imperfective) with pairs
  - Verb conjugation tables (present tense)
- **Idiom Databases**
  - 50+ English idioms
  - 25+ Russian idioms
- Register markers (formal/informal/colloquial)

## [1.0.0] - 2026-01-30

### Added
- Initial Python rewrite from Bash
- Modular architecture with language plugins
- 640+ Russian transliteration mappings
- 212 local Russian definitions with grammar
- XDG-compliant data directories
- Free Dictionary API integration
- Wiktionary API integration
- Learning features (save, review, quiz, Anki export)
- Russian command aliases (определить, словарь, слово)

---

## Version Numbering

- **Major** (X.0.0): Breaking changes or major feature additions
- **Minor** (0.X.0): New features, backwards compatible
- **Patch** (0.0.X): Bug fixes, minor improvements
