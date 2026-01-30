#!/usr/bin/env python3
"""
Command-line interface for define.
"""

import argparse
import subprocess
import sys
from pathlib import Path

from core.dictionary import Dictionary
from core.vocabulary import Vocabulary
from core.cache import Cache
from core.audio import AudioPlayer
from languages import English, Russian
from ui.formatter import Formatter


def get_clipboard() -> str:
    """Get text from clipboard (cross-platform)."""
    commands = [
        ["xclip", "-o", "-selection", "primary"],
        ["xclip", "-o", "-selection", "clipboard"],
        ["xsel", "-p"],
        ["xsel", "-b"],
        ["wl-paste", "-p"],
        ["wl-paste"],
        ["pbpaste"],  # macOS
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    return ""


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="define",
        description="Terminal dictionary for English and Russian / "
                    "Терминальный словарь для английского и русского",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples / Примеры:
  define serendipity          Look up English word
  define привет               Look up Russian word (Cyrillic)
  define privet               Look up Russian word (transliteration)
  define -f love              Full info (etymology, examples, synonyms)
  define --save ephemeral     Save word to vocabulary
  define --quiz               Quiz yourself on saved words
  определить счастье          Use Russian command name
"""
    )
    
    parser.add_argument("word", nargs="*", help="Word to look up / Слово для поиска")
    
    # Display options
    display = parser.add_argument_group("Display options / Опции отображения")
    display.add_argument("-a", "--all", action="store_true",
                        help="Show all definitions / Показать все определения")
    display.add_argument("-s", "--short", action="store_true",
                        help="Short mode: definition only / Краткий режим")
    display.add_argument("-e", "--examples", action="store_true",
                        help="Show example sentences / Показать примеры")
    display.add_argument("-y", "--synonyms", action="store_true",
                        help="Show synonyms and antonyms / Показать синонимы")
    display.add_argument("-t", "--etymology", action="store_true",
                        help="Show word origin / Показать этимологию")
    display.add_argument("-i", "--idioms", action="store_true",
                        help="Show idioms and expressions / Показать идиомы")
    display.add_argument("-g", "--grammar", action="store_true",
                        help="Show full grammar (tenses, declensions, participles) / Полная грамматика")
    display.add_argument("-f", "--full", action="store_true",
                        help="Full mode: show everything / Полный режим")
    display.add_argument("-j", "--json", action="store_true",
                        help="Output raw JSON / Вывод в JSON")
    
    # Language options
    lang = parser.add_argument_group("Language options / Опции языка")
    lang.add_argument("-R", "--russian", action="store_true",
                     help="Force Russian lookup / Принудительно русский")
    lang.add_argument("-E", "--english", action="store_true",
                     help="Force English lookup / Принудительно английский")
    
    # Audio
    parser.add_argument("-p", "--pronounce", action="store_true",
                       help="Play pronunciation / Воспроизвести произношение")
    
    # Learning features
    learn = parser.add_argument_group("Learning features / Функции обучения")
    learn.add_argument("-r", "--random", action="store_true",
                      help="Look up a random word / Случайное слово")
    learn.add_argument("--save", action="store_true",
                      help="Save word to vocabulary / Сохранить в словарь")
    learn.add_argument("--review", action="store_true",
                      help="Review saved vocabulary / Повторить словарь")
    learn.add_argument("--quiz", action="store_true",
                      help="Quiz on saved words / Викторина")
    learn.add_argument("--study", action="store_true",
                      help="Spaced repetition study session / Интервальное повторение")
    learn.add_argument("--stats", action="store_true",
                      help="Show vocabulary statistics / Статистика словаря")
    learn.add_argument("--export-anki", nargs="?", const="vocabulary.csv",
                      metavar="FILE",
                      help="Export to Anki CSV / Экспорт в Anki")
    
    # Cache options
    cache = parser.add_argument_group("Cache options / Опции кэша")
    cache.add_argument("-o", "--offline", action="store_true",
                      help="Use cached results only / Только кэш")
    cache.add_argument("--clear-cache", action="store_true",
                      help="Clear the cache / Очистить кэш")
    
    # Other
    parser.add_argument("--no-color", action="store_true",
                       help="Disable colors / Отключить цвета")
    parser.add_argument("-v", "--version", action="version",
                       version="define 2.2.0")
    
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    # Initialize components
    cache = Cache()
    formatter = Formatter(no_color=args.no_color)
    vocabulary = Vocabulary()
    audio = AudioPlayer()
    
    # Initialize languages
    languages = [English(), Russian()]
    dictionary = Dictionary(languages, cache)
    
    # Handle special commands
    if args.clear_cache:
        count = cache.clear()
        formatter.info(f"Cleared {count} cached definitions / Очищено {count} определений")
        return 0
    
    if args.review:
        vocabulary.review(formatter)
        return 0
    
    if args.quiz:
        vocabulary.quiz(formatter)
        return 0
    
    if args.study:
        vocabulary.study(formatter)
        return 0
    
    if args.stats:
        stats = vocabulary.get_stats()
        formatter.header("Vocabulary Statistics / Статистика словаря")
        print(f"  Total words:    {stats['total']}")
        print(f"  Due for review: {stats['due']}")
        print(f"  Mastered:       {stats['mastered']} (21+ day interval)")
        print(f"  Learning:       {stats['learning']} (1-20 day interval)")
        print(f"  New:            {stats['new']} (never reviewed)")
        return 0
    
    if args.export_anki:
        count = vocabulary.export_anki(args.export_anki)
        formatter.info(f"Exported {count} words to {args.export_anki}")
        return 0
    
    # Get word to look up
    if args.random:
        word = dictionary.random_word()
        formatter.random_word(word)
    elif args.word:
        word = " ".join(args.word)
    else:
        word = get_clipboard()
    
    if not word:
        formatter.error("No word provided / Слово не указано")
        print("Usage: define [word] or highlight text and run 'define'")
        return 1
    
    # Determine language
    force_lang = None
    if args.russian:
        force_lang = "ru"
    elif args.english:
        force_lang = "en"
    
    # Look up word
    result = dictionary.lookup(
        word,
        force_lang=force_lang,
        offline=args.offline
    )
    
    if not result:
        formatter.not_found(word)
        return 1
    
    # Display result
    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Determine display options
        show_all = args.all
        show_examples = args.examples or args.full
        show_synonyms = args.synonyms or args.full
        show_etymology = args.etymology or args.full
        show_idioms = args.idioms or args.full
        show_grammar = args.grammar or args.full
        short_mode = args.short
        
        formatter.display_result(
            result,
            show_all=show_all,
            show_examples=show_examples,
            show_synonyms=show_synonyms,
            show_etymology=show_etymology,
            show_idioms=show_idioms,
            short_mode=short_mode,
            show_grammar=show_grammar
        )
    
    # Play audio if requested
    if args.pronounce and result.get("audio"):
        audio.play(result["audio"])
    
    # Save to vocabulary if requested
    if args.save:
        vocabulary.save(result)
        formatter.saved(result["word"])
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
