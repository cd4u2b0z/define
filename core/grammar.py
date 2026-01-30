"""
Russian Grammar Engine

Handles verb conjugation (past, future, imperative, participles)
and noun/adjective declensions (singular and plural).

Russian verb tenses:
- Present (only imperfective verbs)
- Past (both aspects, changes by gender)
- Future (imperfective = буду + infinitive, perfective = conjugated)
- Imperative (commands)
- Participles (verbal adjectives)

Russian noun/adjective cases:
- Nominative (кто? что?)
- Genitive (кого? чего?)
- Dative (кому? чему?)
- Accusative (кого? что?)
- Instrumental (кем? чем?)
- Prepositional (о ком? о чём?)
"""

import re
from typing import Optional, Dict, List, Tuple


class StressMarker:
    """
    Handles stress marking for Russian words.
    
    Russian stress is unpredictable and must be learned per word.
    We mark stress with acute accent (á, é, etc.) on the vowel.
    """
    
    VOWELS = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
    STRESSED_MAP = {
        'а': 'а́', 'е': 'е́', 'ё': 'ё', 'и': 'и́', 'о': 'о́',
        'у': 'у́', 'ы': 'ы́', 'э': 'э́', 'ю': 'ю́', 'я': 'я́',
        'А': 'А́', 'Е': 'Е́', 'Ё': 'Ё', 'И': 'И́', 'О': 'О́',
        'У': 'У́', 'Ы': 'Ы́', 'Э': 'Э́', 'Ю': 'Ю́', 'Я': 'Я́'
    }
    UNSTRESSED_MAP = {v: k for k, v in STRESSED_MAP.items() if k != v}
    
    @classmethod
    def mark_stress(cls, word: str, stress_position: int) -> str:
        """
        Mark stress on a word at the given vowel position (1-indexed).
        
        Args:
            word: The word to mark
            stress_position: Which vowel to stress (1 = first vowel)
        
        Returns:
            Word with stress mark on the specified vowel
        """
        if stress_position < 1:
            return word
        
        vowel_count = 0
        result = []
        
        for char in word:
            if char in cls.VOWELS:
                vowel_count += 1
                if vowel_count == stress_position and char in cls.STRESSED_MAP:
                    result.append(cls.STRESSED_MAP[char])
                else:
                    result.append(char)
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def remove_stress(cls, word: str) -> str:
        """Remove all stress marks from a word."""
        result = []
        for char in word:
            # Remove combining acute accent
            if char == '\u0301':
                continue
            # Check for pre-composed stressed characters
            result.append(cls.UNSTRESSED_MAP.get(char, char))
        return ''.join(result)
    
    @classmethod
    def has_stress(cls, word: str) -> bool:
        """Check if word has stress marks."""
        return '\u0301' in word or any(c in word for c in cls.UNSTRESSED_MAP)
    
    @classmethod
    def get_stress_position(cls, word: str) -> Optional[int]:
        """Get the vowel position of stress (1-indexed), or None if unmarked."""
        vowel_count = 0
        i = 0
        while i < len(word):
            char = word[i]
            if char in cls.VOWELS:
                vowel_count += 1
                # Check for combining accent after this vowel
                if i + 1 < len(word) and word[i + 1] == '\u0301':
                    return vowel_count
                # Check for pre-composed stressed vowel
                if char in cls.UNSTRESSED_MAP:
                    return vowel_count
            i += 1
        return None


class VerbConjugator:
    """
    Russian verb conjugation engine.
    
    Handles:
    - Past tense (all aspects, by gender)
    - Future tense (imperfective compound, perfective simple)
    - Imperative mood
    - Present/Active/Passive participles
    """
    
    # Infinitive endings
    INF_ENDINGS = ('ть', 'ти', 'чь')
    
    # Past tense endings
    PAST_ENDINGS = {
        'masc': 'л',
        'fem': 'ла',
        'neut': 'ло',
        'plural': 'ли'
    }
    
    # Future auxiliary forms (буду, будешь, etc.)
    FUTURE_AUXILIARY = {
        'я': 'бу́ду',
        'ты': 'бу́дешь',
        'он/она': 'бу́дет',
        'мы': 'бу́дем',
        'вы': 'бу́дете',
        'они': 'бу́дут'
    }
    
    # Conjugation patterns (1st and 2nd conjugation)
    CONJ_1_ENDINGS = {
        'я': 'ю', 'ты': 'ешь', 'он/она': 'ет',
        'мы': 'ем', 'вы': 'ете', 'они': 'ют'
    }
    
    CONJ_2_ENDINGS = {
        'я': 'ю', 'ты': 'ишь', 'он/она': 'ит',
        'мы': 'им', 'вы': 'ите', 'они': 'ят'
    }
    
    @classmethod
    def get_past_tense(cls, infinitive: str, stem: str = None) -> Dict[str, str]:
        """
        Generate past tense forms from infinitive.
        
        Past tense in Russian doesn't conjugate by person,
        only by gender and number.
        
        Args:
            infinitive: The verb infinitive (e.g., делать)
            stem: Optional custom stem (for irregular verbs)
        
        Returns:
            Dict with masc, fem, neut, plural forms
        """
        if stem is None:
            stem = cls._get_past_stem(infinitive)
        
        return {
            'masc': stem + cls.PAST_ENDINGS['masc'],
            'fem': stem + cls.PAST_ENDINGS['fem'],
            'neut': stem + cls.PAST_ENDINGS['neut'],
            'plural': stem + cls.PAST_ENDINGS['plural']
        }
    
    @classmethod
    def _get_past_stem(cls, infinitive: str) -> str:
        """Get the past tense stem from infinitive."""
        # Remove stress marks for processing
        clean = StressMarker.remove_stress(infinitive)
        
        # Handle -ть verbs (most common)
        if clean.endswith('ть'):
            return infinitive[:-2]
        
        # Handle -ти verbs (идти → шёл is irregular, handled separately)
        if clean.endswith('ти'):
            return infinitive[:-2]
        
        # Handle -чь verbs (мочь → мог)
        if clean.endswith('чь'):
            stem = infinitive[:-2]
            # чь → г or к depending on verb
            if StressMarker.remove_stress(infinitive) in ('мочь', 'смочь', 'помочь'):
                return stem + 'г'
            elif StressMarker.remove_stress(infinitive) in ('печь', 'испечь'):
                return stem + 'к'
            return stem + 'г'  # Default to г
        
        return infinitive
    
    @classmethod
    def get_future_tense(cls, infinitive: str, aspect: str, 
                         present_conjugation: Dict[str, str] = None) -> Dict[str, str]:
        """
        Generate future tense forms.
        
        Imperfective: буду + infinitive (compound future)
        Perfective: Same endings as present tense (simple future)
        
        Args:
            infinitive: The verb infinitive
            aspect: 'imperfective' or 'perfective'
            present_conjugation: Present tense forms (for perfective)
        
        Returns:
            Dict with future forms for each person
        """
        if 'imperfective' in aspect.lower():
            # Compound future: буду + infinitive
            return {
                person: f"{aux} {infinitive}"
                for person, aux in cls.FUTURE_AUXILIARY.items()
            }
        else:
            # Perfective verbs use present conjugation for future
            if present_conjugation:
                return present_conjugation
            return {}
    
    @classmethod
    def get_imperative(cls, present_2sg: str, present_3pl: str) -> Dict[str, str]:
        """
        Generate imperative forms from present tense.
        
        Formation rules:
        - If stem ends in vowel: add -й (читай, делай)
        - If stem ends in consonant + stressed ending: add -и (говори, пиши)
        - If stem ends in consonant + unstressed ending: add -ь (готовь)
        
        Args:
            present_2sg: "ты" form (e.g., читаешь)
            present_3pl: "они" form (e.g., читают)
        
        Returns:
            Dict with singular and plural imperative forms
        """
        clean_3pl = StressMarker.remove_stress(present_3pl)
        clean_2sg = StressMarker.remove_stress(present_2sg)
        
        # Check if this is 2nd conjugation (ending in -ишь/-ят or -ишь/-ат)
        is_second_conj = clean_2sg.endswith('ишь') or clean_3pl.endswith(('ят', 'ат'))
        
        # For 2nd conjugation verbs, the stem is from 2sg minus -ишь
        # For 1st conjugation verbs, stem is from 3pl minus ending
        if is_second_conj:
            # 2nd conjugation: говоришь → говор, пишешь → пиш
            if clean_2sg.endswith('ишь'):
                stem = present_2sg[:-3]  # Remove -ишь (with stress marks)
            else:
                stem = present_2sg[:-3]  # Just in case
            clean_stem = StressMarker.remove_stress(stem)
        else:
            # 1st conjugation: читают → чита, делают → дела
            if clean_3pl.endswith(('ут', 'ют', 'ат', 'ят')):
                stem = present_3pl[:-2]
            else:
                stem = present_3pl
            clean_stem = StressMarker.remove_stress(stem)
        
        # Determine imperative ending
        if clean_stem and clean_stem[-1] in 'аеёиоуыэюя' and not is_second_conj:
            # Vowel stem (1st conj only): add -й
            imp_sg = stem + 'й'
            imp_pl = stem + 'йте'
        elif is_second_conj or StressMarker.has_stress(present_2sg) or present_2sg.endswith('ёшь'):
            # Second conjugation or stressed ending: add -и
            imp_sg = stem + 'и́'
            imp_pl = stem + 'и́те'
        else:
            # Unstressed ending: add soft sign
            imp_sg = stem + 'ь'
            imp_pl = stem + 'ьте'
        
        return {
            'singular': imp_sg,
            'plural': imp_pl
        }
    
    @classmethod
    def get_participles(cls, infinitive: str, aspect: str,
                        present_conjugation: Dict[str, str] = None,
                        past_stem: str = None) -> Dict[str, str]:
        """
        Generate participle forms.
        
        Types:
        - Present Active: читающий (one who reads)
        - Present Passive: читаемый (being read) - only imperfective
        - Past Active: читавший (one who read)
        - Past Passive: прочитанный (having been read) - mainly perfective
        
        Args:
            infinitive: The verb infinitive
            aspect: 'imperfective' or 'perfective'
            present_conjugation: Present tense forms
            past_stem: Past tense stem
        
        Returns:
            Dict with available participle forms
        """
        participles = {}
        
        if past_stem is None:
            past_stem = cls._get_past_stem(infinitive)
        
        clean_inf = StressMarker.remove_stress(infinitive)
        clean_stem = StressMarker.remove_stress(past_stem)
        
        # Past Active Participle (both aspects)
        # читать → читавший
        participles['past_active'] = clean_stem + 'вший'
        
        # Present Active Participle (imperfective only)
        if 'imperfective' in aspect.lower() and present_conjugation:
            # From 3rd person plural: читают → читающий
            form_3pl = present_conjugation.get('они', '')
            clean_3pl = StressMarker.remove_stress(form_3pl)
            if clean_3pl.endswith(('ут', 'ют')):
                participles['present_active'] = clean_3pl[:-2] + 'ущий' if clean_3pl.endswith('ут') else clean_3pl[:-2] + 'ющий'
            elif clean_3pl.endswith(('ат', 'ят')):
                participles['present_active'] = clean_3pl[:-2] + 'ащий' if clean_3pl.endswith('ат') else clean_3pl[:-2] + 'ящий'
        
        # Present Passive Participle (imperfective only, 1st conjugation mainly)
        if 'imperfective' in aspect.lower() and present_conjugation:
            # From 1st person plural: читаем → читаемый
            form_1pl = present_conjugation.get('мы', '')
            clean_1pl = StressMarker.remove_stress(form_1pl)
            if clean_1pl.endswith(('ем', 'ём')):
                participles['present_passive'] = clean_1pl + 'ый'
            elif clean_1pl.endswith('им'):
                participles['present_passive'] = clean_1pl + 'ый'
        
        # Past Passive Participle (mainly perfective)
        if 'perfective' in aspect.lower():
            # Formation depends on infinitive ending
            if clean_inf.endswith('ать'):
                participles['past_passive'] = clean_stem + 'нный'
            elif clean_inf.endswith('ить'):
                # Often with consonant mutation
                participles['past_passive'] = clean_stem[:-1] + 'енный' if clean_stem.endswith('и') else clean_stem + 'енный'
            elif clean_inf.endswith('еть'):
                participles['past_passive'] = clean_stem + 'нный'
        
        return participles


class NounDecliner:
    """
    Russian noun declension engine.
    
    Handles all 6 cases in both singular and plural.
    
    Declension patterns depend on:
    - Gender (masculine, feminine, neuter)
    - Ending (-а/-я, -о/-е, consonant, -ь, etc.)
    - Animacy (affects accusative)
    """
    
    # Case names with Russian equivalents
    CASE_NAMES = {
        'nominative': 'именительный (кто? что?)',
        'genitive': 'родительный (кого? чего?)',
        'dative': 'дательный (кому? чему?)',
        'accusative': 'винительный (кого? что?)',
        'instrumental': 'творительный (кем? чем?)',
        'prepositional': 'предложный (о ком? о чём?)'
    }
    
    # Hard consonants
    HARD_CONSONANTS = 'бвгдзклмнпрстфхцш'
    
    # Soft consonants and hushers
    SOFT_CONSONANTS = 'йчщь'
    HUSHERS = 'жчшщ'
    VELARS = 'гкх'
    
    @classmethod
    def _ends_with_any(cls, word: str, chars: str) -> bool:
        """Check if word ends with any of the given characters."""
        return word and word[-1] in chars
    
    @classmethod
    def get_plural_declension(cls, singular_cases: Dict[str, str], 
                               gender: str, 
                               animate: bool = False) -> Dict[str, str]:
        """
        Generate plural declension from singular nominative.
        
        Args:
            singular_cases: Singular case forms
            gender: 'masculine', 'feminine', or 'neuter'
            animate: Whether the noun is animate
        
        Returns:
            Dict with all 6 plural case forms
        """
        nom_sg = singular_cases.get('nominative', '')
        if not nom_sg:
            return {}
        
        clean_nom = StressMarker.remove_stress(nom_sg)
        
        # Determine stem and declension pattern
        stem = cls._get_stem(clean_nom, gender)
        
        plural = {}
        
        # Nominative plural
        if gender == 'masculine':
            if clean_nom.endswith('ь'):
                plural['nominative'] = stem + 'и'
            elif cls._ends_with_any(clean_nom, cls.HUSHERS + cls.VELARS):
                plural['nominative'] = clean_nom + 'и'
            elif clean_nom.endswith('й'):
                plural['nominative'] = stem + 'и'
            else:
                plural['nominative'] = clean_nom + 'ы'
        elif gender == 'feminine':
            if clean_nom.endswith('а'):
                if cls._ends_with_any(stem, cls.HUSHERS + cls.VELARS) or stem.endswith('ц'):
                    plural['nominative'] = stem + 'и'
                else:
                    plural['nominative'] = stem + 'ы'
            elif clean_nom.endswith('я'):
                plural['nominative'] = stem + 'и'
            elif clean_nom.endswith('ь'):
                plural['nominative'] = stem + 'и'
            else:
                plural['nominative'] = clean_nom + 'ы'
        elif gender == 'neuter':
            if clean_nom.endswith('о'):
                plural['nominative'] = stem + 'а'
            elif clean_nom.endswith('е'):
                plural['nominative'] = stem + 'я'
            elif clean_nom.endswith('мя'):
                plural['nominative'] = stem + 'мена'
            else:
                plural['nominative'] = clean_nom + 'а'
        
        nom_pl = plural.get('nominative', '')
        stem_pl = cls._get_stem(nom_pl, gender)
        
        # Genitive plural (complex rules)
        plural['genitive'] = cls._get_genitive_plural(clean_nom, stem, gender)
        
        # Dative plural
        if nom_pl.endswith(('и', 'ы')):
            plural['dative'] = stem_pl + 'ам'
        elif nom_pl.endswith('я'):
            plural['dative'] = stem_pl + 'ям'
        else:
            plural['dative'] = stem_pl + 'ам'
        
        # Accusative plural (depends on animacy)
        if animate:
            plural['accusative'] = plural['genitive']
        else:
            plural['accusative'] = plural['nominative']
        
        # Instrumental plural
        if nom_pl.endswith(('и', 'ы', 'а')):
            plural['instrumental'] = stem_pl + 'ами'
        elif nom_pl.endswith('я'):
            plural['instrumental'] = stem_pl + 'ями'
        else:
            plural['instrumental'] = stem_pl + 'ами'
        
        # Prepositional plural
        if nom_pl.endswith(('и', 'ы', 'а')):
            plural['prepositional'] = stem_pl + 'ах'
        elif nom_pl.endswith('я'):
            plural['prepositional'] = stem_pl + 'ях'
        else:
            plural['prepositional'] = stem_pl + 'ах'
        
        return plural
    
    @classmethod
    def _get_stem(cls, word: str, gender: str) -> str:
        """Extract the stem from a noun."""
        if not word:
            return ''
        
        # Remove typical endings
        if gender == 'feminine':
            if word.endswith(('а', 'я', 'ь')):
                return word[:-1]
        elif gender == 'neuter':
            if word.endswith(('о', 'е')):
                return word[:-1]
            if word.endswith('мя'):
                return word[:-2]
        elif gender == 'masculine':
            if word.endswith(('й', 'ь')):
                return word[:-1]
        
        return word
    
    @classmethod
    def _get_genitive_plural(cls, nom_sg: str, stem: str, gender: str) -> str:
        """
        Get genitive plural form.
        
        This is the most complex case with many patterns:
        - Zero ending (книг from книга)
        - -ов/-ев (столов from стол)
        - -ей (морей from море)
        - Fleeting vowels (окно → окон)
        """
        if gender == 'masculine':
            if nom_sg.endswith('й'):
                return stem + 'ев'
            elif nom_sg.endswith('ь'):
                return stem + 'ей'
            elif cls._ends_with_any(nom_sg, cls.HUSHERS):
                return nom_sg + 'ей'
            elif nom_sg.endswith('ц'):
                return nom_sg + 'ев'
            else:
                return nom_sg + 'ов'
        
        elif gender == 'feminine':
            if nom_sg.endswith('а'):
                # Check for fleeting vowel or cluster
                if len(stem) > 1 and stem[-1] in 'кг' and stem[-2] not in 'аеёиоуыэюя':
                    # Insert fleeting о/е
                    return stem[:-1] + 'о' + stem[-1]
                elif cls._ends_with_any(stem, cls.HUSHERS):
                    return stem + 'ей'
                else:
                    return stem
            elif nom_sg.endswith('я'):
                if stem.endswith('и'):
                    return stem + 'й'
                else:
                    return stem + 'ь'
            elif nom_sg.endswith('ь'):
                return stem + 'ей'
            else:
                return stem
        
        elif gender == 'neuter':
            if nom_sg.endswith('о'):
                return stem
            elif nom_sg.endswith('е'):
                if stem.endswith('и'):
                    return stem + 'й'
                else:
                    return stem + 'ей'
            elif nom_sg.endswith('мя'):
                return stem + 'мён'
            else:
                return stem
        
        return stem


class GrammarEngine:
    """
    Main grammar engine combining all components.
    """
    
    def __init__(self):
        self.stress = StressMarker
        self.verbs = VerbConjugator
        self.nouns = NounDecliner
    
    def get_full_verb_conjugation(self, verb_data: dict) -> dict:
        """
        Get complete conjugation for a verb including all tenses.
        
        Args:
            verb_data: Dictionary with verb info (infinitive, aspect, 
                      present conjugation, etc.)
        
        Returns:
            Dictionary with all conjugation forms
        """
        infinitive = verb_data.get('word', '')
        aspect = verb_data.get('aspect', 'imperfective')
        present = verb_data.get('conjugation', {})
        
        result = {
            'infinitive': infinitive,
            'aspect': aspect
        }
        
        # Present tense (only for imperfective)
        if 'imperfective' in aspect.lower() and present:
            result['present'] = present
        
        # Past tense
        result['past'] = self.verbs.get_past_tense(infinitive)
        
        # Future tense
        result['future'] = self.verbs.get_future_tense(infinitive, aspect, present)
        
        # Imperative
        if present:
            present_2sg = present.get('ты', '')
            present_3pl = present.get('они', '')
            if present_2sg and present_3pl:
                result['imperative'] = self.verbs.get_imperative(present_2sg, present_3pl)
        
        # Participles
        result['participles'] = self.verbs.get_participles(
            infinitive, aspect, present
        )
        
        return result
    
    def get_full_noun_declension(self, noun_data: dict) -> dict:
        """
        Get complete declension for a noun including plural.
        
        Args:
            noun_data: Dictionary with noun info (word, gender, cases, animate)
        
        Returns:
            Dictionary with singular and plural declensions
        """
        singular = noun_data.get('cases', {})
        gender = noun_data.get('gender', '')
        animate = noun_data.get('animate', False)
        
        if not singular or not gender:
            return {}
        
        result = {
            'singular': singular
        }
        
        # Generate plural
        plural = self.nouns.get_plural_declension(singular, gender, animate)
        if plural:
            result['plural'] = plural
        
        return result
