"""
Terminal output formatting.
"""

import sys
from typing import Optional


class Colors:
    """ANSI color codes."""
    
    def __init__(self, no_color: bool = False):
        if no_color or not sys.stdout.isatty():
            self.RED = ""
            self.GREEN = ""
            self.BLUE = ""
            self.YELLOW = ""
            self.CYAN = ""
            self.MAGENTA = ""
            self.BOLD = ""
            self.DIM = ""
            self.ITALIC = ""
            self.UNDERLINE = ""
            self.NC = ""
        else:
            self.RED = "\033[0;31m"
            self.GREEN = "\033[0;32m"
            self.BLUE = "\033[0;34m"
            self.YELLOW = "\033[0;33m"
            self.CYAN = "\033[0;36m"
            self.MAGENTA = "\033[0;35m"
            self.BOLD = "\033[1m"
            self.DIM = "\033[2m"
            self.ITALIC = "\033[3m"
            self.UNDERLINE = "\033[4m"
            self.NC = "\033[0m"


class Formatter:
    """Format dictionary results for terminal output."""
    
    def __init__(self, no_color: bool = False):
        self.c = Colors(no_color)
    
    def error(self, msg: str) -> None:
        """Print error message."""
        print(f"{self.c.RED}{self.c.BOLD}Error:{self.c.NC} {msg}", file=sys.stderr)
    
    def info(self, msg: str) -> None:
        """Print info message."""
        print(f"{self.c.DIM}{msg}{self.c.NC}")
    
    def success(self, msg: str) -> None:
        """Print success message."""
        print(f"{self.c.GREEN}{msg}{self.c.NC}")
    
    def header(self, msg: str) -> None:
        """Print header."""
        print(f"\n{self.c.BLUE}{self.c.BOLD}━━━ {msg} ━━━{self.c.NC}\n")
    
    def random_word(self, word: str) -> None:
        """Print random word announcement."""
        print(f"{self.c.MAGENTA}Random word:{self.c.NC} {self.c.BOLD}{word}{self.c.NC}\n")
    
    def saved(self, word: str) -> None:
        """Print saved confirmation."""
        print(f"\n{self.c.GREEN}Saved '{word}' to vocabulary{self.c.NC}")
    
    def not_found(self, word: str) -> None:
        """Print not found message."""
        print(f"{self.c.YELLOW}No definition found for '{word}'{self.c.NC}")
    
    def display_result(
        self,
        result: dict,
        show_all: bool = False,
        show_examples: bool = False,
        show_synonyms: bool = False,
        show_etymology: bool = False,
        show_idioms: bool = False,
        short_mode: bool = False,
        show_grammar: bool = False
    ) -> None:
        """Display a dictionary result."""
        
        word = result.get("word", "")
        phonetic = result.get("phonetic", "")
        meanings = result.get("meanings", [])
        etymology = result.get("etymology")
        idioms = result.get("idioms", [])
        cases = result.get("cases")
        aspect = result.get("aspect")
        source = result.get("source", "")
        original = result.get("original_input", "")
        normalized = result.get("normalized", "")
        
        # Word header
        print(f"\n{self.c.BOLD}{self.c.UNDERLINE}{word}{self.c.NC}", end="")
        
        # Show original input if it was transliterated
        if normalized and normalized != original:
            print(f"  {self.c.DIM}({original}){self.c.NC}", end="")
        
        print()
        
        # Phonetic
        if phonetic and not short_mode:
            print(f"{self.c.DIM}{phonetic}{self.c.NC}")
        
        # Aspect (for Russian verbs)
        # Gender (for nouns)
        gender = result.get("gender")
        if gender and not short_mode:
            gender_ru = {"masculine": "м.р.", "feminine": "ж.р.", "neuter": "ср.р."}.get(gender, gender)
            print(f"{self.c.DIM}Gender: {gender} ({gender_ru}){self.c.NC}")
        
        # Aspect (for verbs)
        if aspect and not short_mode:
            aspect_ru = "несов." if "imperfective" in aspect else "сов."
            print(f"{self.c.DIM}Aspect: {aspect} ({aspect_ru}){self.c.NC}")
            pair = result.get("pair")
            if pair:
                print(f"{self.c.DIM}Aspectual pair: {pair}{self.c.NC}")
        
        print()
        
        # Meanings
        for meaning in meanings:
            pos = meaning.get("partOfSpeech", "")
            definitions = meaning.get("definitions", [])
            register = meaning.get("register", "")
            
            # Part of speech with register
            pos_line = f"{self.c.CYAN}{self.c.ITALIC}{pos}{self.c.NC}" if pos else ""
            if register and register != "neutral" and not short_mode:
                register_color = self.c.RED if register == "vulgar" else self.c.YELLOW
                pos_line += f"  {register_color}[{register}]{self.c.NC}"
            
            if pos_line:
                print(pos_line)
            
            # Limit definitions unless show_all
            defs_to_show = definitions if show_all else definitions[:3]
            
            for i, defn in enumerate(defs_to_show, 1):
                definition = defn.get("definition", "")
                example = defn.get("example")
                syns = defn.get("synonyms", [])
                ants = defn.get("antonyms", [])
                
                print(f"  {i}. {definition}")
                
                if show_examples and example:
                    print(f"     {self.c.DIM}\"{example}\"{self.c.NC}")
                
                if show_synonyms:
                    if syns:
                        syn_str = ", ".join(syns[:5])
                        print(f"     {self.c.GREEN}Synonyms: {syn_str}{self.c.NC}")
                    if ants:
                        ant_str = ", ".join(ants[:5])
                        print(f"     {self.c.RED}Antonyms: {ant_str}{self.c.NC}")
            
            # Top-level synonyms/antonyms for meaning
            if show_synonyms and not short_mode:
                top_syns = meaning.get("synonyms", [])
                top_ants = meaning.get("antonyms", [])
                
                if top_syns and not any(d.get("synonyms") for d in defs_to_show):
                    syn_str = ", ".join(top_syns[:8])
                    print(f"  {self.c.GREEN}Synonyms: {syn_str}{self.c.NC}")
                
                if top_ants and not any(d.get("antonyms") for d in defs_to_show):
                    ant_str = ", ".join(top_ants[:8])
                    print(f"  {self.c.RED}Antonyms: {ant_str}{self.c.NC}")
            
            # Show count of remaining definitions
            remaining = len(definitions) - len(defs_to_show)
            if remaining > 0 and not show_all:
                print(f"  {self.c.DIM}... and {remaining} more definition(s). Use -a to see all.{self.c.NC}")
            
            print()
        
        # Conjugation (for verbs)
        conjugation = result.get("conjugation")
        if conjugation and not short_mode:
            print(f"{self.c.MAGENTA}Conjugation (present):{self.c.NC}")
            for person, form in conjugation.items():
                print(f"  {person}: {form}")
            print()
        
        # Past tense (for Russian verbs with grammar data)
        past = result.get("past")
        if past and (show_grammar or not short_mode):
            print(f"{self.c.MAGENTA}Past tense (прошедшее время):{self.c.NC}")
            past_labels = {"masc": "он (m)", "fem": "она (f)", "neut": "оно (n)", "plural": "они (pl)"}
            for gender, form in past.items():
                label = past_labels.get(gender, gender)
                print(f"  {label}: {form}")
            print()
        
        # Future tense (for Russian verbs with grammar data)
        future = result.get("future")
        if future and (show_grammar or not short_mode):
            aspect_str = result.get("aspect", "")
            if "imperfective" in aspect_str.lower():
                print(f"{self.c.MAGENTA}Future tense (будущее время, compound):{self.c.NC}")
            else:
                print(f"{self.c.MAGENTA}Future tense (будущее время, simple):{self.c.NC}")
            for person, form in future.items():
                if person != "note":
                    print(f"  {person}: {form}")
            print()
        
        # Imperative mood (for Russian verbs with grammar data)
        imperative = result.get("imperative")
        if imperative and show_grammar:
            print(f"{self.c.MAGENTA}Imperative (повелительное наклонение):{self.c.NC}")
            sg = imperative.get("singular", "-")
            pl = imperative.get("plural", "-")
            note = imperative.get("note")
            print(f"  ты: {sg}")
            print(f"  вы: {pl}")
            if note:
                print(f"  {self.c.DIM}Note: {note}{self.c.NC}")
            print()
        
        # Participles (for Russian verbs with grammar data)
        participles = result.get("participles")
        if participles and show_grammar:
            print(f"{self.c.MAGENTA}Participles (причастия):{self.c.NC}")
            participle_labels = {
                "present_active": "present active (наст. действ.)",
                "past_active": "past active (прош. действ.)",
                "present_passive": "present passive (наст. страд.)",
                "past_passive": "past passive (прош. страд.)"
            }
            for ptype, form in participles.items():
                label = participle_labels.get(ptype, ptype)
                print(f"  {label}: {form}")
            print()
        
        # Cases (for Russian nouns - singular)
        if cases and not short_mode:
            print(f"{self.c.MAGENTA}Cases (singular):{self.c.NC}")
            case_labels = {
                "nom": "nominative (кто? что?)",
                "gen": "genitive (кого? чего?)",
                "dat": "dative (кому? чему?)",
                "acc": "accusative (кого? что?)",
                "ins": "instrumental (кем? чем?)",
                "prep": "prepositional (о ком? о чём?)",
                "nominative": "nominative (кто? что?)",
                "genitive": "genitive (кого? чего?)",
                "dative": "dative (кому? чему?)",
                "accusative": "accusative (кого? что?)",
                "instrumental": "instrumental (кем? чем?)",
                "prepositional": "prepositional (о ком? о чём?)"
            }
            for case_name, case_form in cases.items():
                label = case_labels.get(case_name, case_name)
                print(f"  {label}: {case_form}")
            print()
        
        # Singular cases from grammar data
        singular_cases = result.get("singular_cases")
        if singular_cases and not short_mode and not cases:
            print(f"{self.c.MAGENTA}Cases (singular / единственное):{self.c.NC}")
            case_labels = {
                "nominative": "им. (кто? что?)",
                "genitive": "род. (кого? чего?)",
                "dative": "дат. (кому? чему?)",
                "accusative": "вин. (кого? что?)",
                "instrumental": "тв. (кем? чем?)",
                "prepositional": "пр. (о ком? о чём?)"
            }
            for case_name, case_form in singular_cases.items():
                label = case_labels.get(case_name, case_name)
                print(f"  {label}: {case_form}")
            print()
        
        # Plural cases from grammar data
        plural_cases = result.get("plural_cases")
        if plural_cases and (show_grammar or not short_mode):
            print(f"{self.c.MAGENTA}Cases (plural / множественное):{self.c.NC}")
            case_labels = {
                "nominative": "им. (кто? что?)",
                "genitive": "род. (кого? чего?)",
                "dative": "дат. (кому? чему?)",
                "accusative": "вин. (кого? что?)",
                "instrumental": "тв. (кем? чем?)",
                "prepositional": "пр. (о ком? о чём?)"
            }
            for case_name, case_form in plural_cases.items():
                label = case_labels.get(case_name, case_name)
                print(f"  {label}: {case_form}")
            print()
        
        # Grammar note
        grammar_note = result.get("grammar_note")
        if grammar_note and show_grammar:
            print(f"{self.c.DIM}Grammar note: {grammar_note}{self.c.NC}")
            print()
        
        # Idioms
        if show_idioms and idioms:
            print(f"{self.c.MAGENTA}Idioms & Expressions:{self.c.NC}")
            for idiom in idioms[:7]:  # Limit to 7
                phrase = idiom.get("phrase", "")
                meaning = idiom.get("meaning", "")
                translit = idiom.get("translit", "")
                register = idiom.get("register", "")
                
                register_tag = ""
                if register and register != "neutral":
                    register_color = self.c.RED if register == "vulgar" else self.c.YELLOW
                    register_tag = f" {register_color}[{register}]{self.c.NC}"
                
                if translit:
                    print(f"  • {self.c.CYAN}{phrase}{self.c.NC} ({translit}){register_tag}")
                else:
                    print(f"  • {self.c.CYAN}{phrase}{self.c.NC}{register_tag}")
                print(f"    {meaning}")
            
            if len(idioms) > 7:
                print(f"  {self.c.DIM}... and {len(idioms) - 7} more idioms{self.c.NC}")
            print()
        
        # Etymology
        if show_etymology and etymology:
            print(f"{self.c.YELLOW}Etymology:{self.c.NC}")
            print(f"  {etymology}")
            print()
        
        # Source
        if not short_mode:
            print(f"{self.c.DIM}Source: {source}{self.c.NC}")
