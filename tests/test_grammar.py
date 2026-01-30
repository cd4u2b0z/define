"""
Unit tests for Russian grammar features.

Tests verb conjugation (all tenses, imperative, participles)
and noun declension (singular and plural cases).
"""

import unittest
import json
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.grammar import (
    StressMarker, VerbConjugator, NounDecliner, GrammarEngine
)
from languages.russian import Russian


class TestStressMarker(unittest.TestCase):
    """Tests for stress marking utilities."""
    
    def test_mark_stress_first_vowel(self):
        """Marking stress on first vowel."""
        result = StressMarker.mark_stress("дома", 1)
        self.assertIn("о́", result)
    
    def test_mark_stress_second_vowel(self):
        """Marking stress on second vowel."""
        result = StressMarker.mark_stress("дома", 2)
        self.assertIn("а́", result)
    
    def test_remove_stress(self):
        """Removing stress marks."""
        # Pre-composed
        result = StressMarker.remove_stress("до́ма")
        self.assertEqual(result, "дома")
    
    def test_has_stress_true(self):
        """Detecting stress marks present."""
        self.assertTrue(StressMarker.has_stress("до́ма"))
        self.assertTrue(StressMarker.has_stress("зна́ю"))
    
    def test_has_stress_false(self):
        """Detecting no stress marks."""
        self.assertFalse(StressMarker.has_stress("дома"))
        self.assertFalse(StressMarker.has_stress("знаю"))
    
    def test_get_stress_position(self):
        """Getting stress position."""
        self.assertEqual(StressMarker.get_stress_position("до́ма"), 1)
        self.assertEqual(StressMarker.get_stress_position("дома́"), 2)
    
    def test_get_stress_position_none(self):
        """No stress mark returns None."""
        self.assertIsNone(StressMarker.get_stress_position("дома"))


class TestVerbConjugator(unittest.TestCase):
    """Tests for verb conjugation."""
    
    def test_past_tense_regular_first_conjugation(self):
        """Past tense of regular -ать verb."""
        past = VerbConjugator.get_past_tense("делать")
        self.assertEqual(past["masc"], "делал")
        self.assertEqual(past["fem"], "делала")
        self.assertEqual(past["neut"], "делало")
        self.assertEqual(past["plural"], "делали")
    
    def test_past_tense_regular_second_conjugation(self):
        """Past tense of regular -ить verb."""
        past = VerbConjugator.get_past_tense("говорить")
        self.assertEqual(past["masc"], "говорил")
        self.assertEqual(past["fem"], "говорила")
    
    def test_future_imperfective(self):
        """Compound future for imperfective verb."""
        future = VerbConjugator.get_future_tense("читать", "imperfective")
        self.assertIn("бу́ду читать", future["я"])
        self.assertIn("бу́дет читать", future["он/она"])
    
    def test_future_perfective(self):
        """Simple future for perfective verb (uses present conjugation)."""
        present = {
            "я": "прочита́ю",
            "ты": "прочита́ешь",
            "он/она": "прочита́ет"
        }
        future = VerbConjugator.get_future_tense("прочитать", "perfective", present)
        self.assertEqual(future, present)
    
    def test_imperative_vowel_stem(self):
        """Imperative for verbs with vowel stem (читать → читай)."""
        imp = VerbConjugator.get_imperative("чита́ешь", "чита́ют")
        self.assertIn("й", imp["singular"])
    
    def test_imperative_consonant_stem_stressed(self):
        """Imperative for verbs with consonant stem, stressed (говорить → говори)."""
        imp = VerbConjugator.get_imperative("говори́шь", "говоря́т")
        self.assertIn("и", imp["singular"])
    
    def test_participles_imperfective(self):
        """Present participles for imperfective verb."""
        present = {
            "они": "чита́ют",
            "мы": "чита́ем"
        }
        participles = VerbConjugator.get_participles(
            "читать", "imperfective", present
        )
        self.assertIn("past_active", participles)
        self.assertIn("present_active", participles)
    
    def test_participles_perfective(self):
        """Past participles for perfective verb."""
        participles = VerbConjugator.get_participles(
            "прочитать", "perfective", {}
        )
        self.assertIn("past_active", participles)
        self.assertIn("past_passive", participles)


class TestNounDecliner(unittest.TestCase):
    """Tests for noun declension."""
    
    def test_masculine_plural_regular(self):
        """Plural of regular masculine noun."""
        singular = {"nominative": "стол"}
        plural = NounDecliner.get_plural_declension(singular, "masculine")
        self.assertEqual(plural["nominative"], "столы")
    
    def test_masculine_plural_after_velar(self):
        """Plural of masculine noun ending in velar (requires -и)."""
        singular = {"nominative": "друг"}
        plural = NounDecliner.get_plural_declension(singular, "masculine")
        self.assertEqual(plural["nominative"], "други")
    
    def test_feminine_plural_a_ending(self):
        """Plural of feminine noun ending in -а."""
        singular = {"nominative": "книга"}
        plural = NounDecliner.get_plural_declension(singular, "feminine")
        self.assertIn("и", plural["nominative"])  # книги
    
    def test_neuter_plural_o_ending(self):
        """Plural of neuter noun ending in -о."""
        singular = {"nominative": "слово"}
        plural = NounDecliner.get_plural_declension(singular, "neuter")
        self.assertEqual(plural["nominative"], "слова")
    
    def test_plural_dative(self):
        """Dative plural ending -ам."""
        singular = {"nominative": "дом"}
        plural = NounDecliner.get_plural_declension(singular, "masculine")
        self.assertIn("ам", plural["dative"])
    
    def test_plural_instrumental(self):
        """Instrumental plural ending -ами."""
        singular = {"nominative": "книга"}
        plural = NounDecliner.get_plural_declension(singular, "feminine")
        self.assertIn("ами", plural["instrumental"])
    
    def test_accusative_animate(self):
        """Accusative plural = genitive for animate nouns."""
        singular = {"nominative": "друг"}
        plural = NounDecliner.get_plural_declension(singular, "masculine", animate=True)
        self.assertEqual(plural["accusative"], plural["genitive"])
    
    def test_accusative_inanimate(self):
        """Accusative plural = nominative for inanimate nouns."""
        singular = {"nominative": "стол"}
        plural = NounDecliner.get_plural_declension(singular, "masculine", animate=False)
        self.assertEqual(plural["accusative"], plural["nominative"])


class TestGrammarDataIntegrity(unittest.TestCase):
    """Tests for grammar data file integrity."""
    
    @classmethod
    def setUpClass(cls):
        """Load grammar data once for all tests."""
        grammar_file = Path(__file__).parent.parent / "languages" / "data" / "ru_grammar.json"
        with open(grammar_file, 'r', encoding='utf-8') as f:
            cls.grammar_data = json.load(f)
    
    def test_verbs_have_required_fields(self):
        """All verbs have infinitive and aspect."""
        verbs = self.grammar_data.get("verbs", {})
        for verb, data in verbs.items():
            self.assertIn("infinitive", data, f"{verb} missing infinitive")
            self.assertIn("aspect", data, f"{verb} missing aspect")
    
    def test_imperfective_verbs_have_present(self):
        """Imperfective verbs have present tense."""
        verbs = self.grammar_data.get("verbs", {})
        for verb, data in verbs.items():
            if "imperfective" in data.get("aspect", "").lower():
                # быть is a special case
                if verb != "быть":
                    self.assertIn("present", data, 
                                  f"Imperfective verb {verb} missing present tense")
    
    def test_verbs_have_past_tense(self):
        """All verbs have past tense."""
        verbs = self.grammar_data.get("verbs", {})
        for verb, data in verbs.items():
            self.assertIn("past", data, f"{verb} missing past tense")
            past = data["past"]
            self.assertIn("masc", past, f"{verb} past missing masculine")
            self.assertIn("fem", past, f"{verb} past missing feminine")
            self.assertIn("plural", past, f"{verb} past missing plural")
    
    def test_verbs_have_future_tense(self):
        """All verbs have future tense."""
        verbs = self.grammar_data.get("verbs", {})
        for verb, data in verbs.items():
            self.assertIn("future", data, f"{verb} missing future tense")
    
    def test_nouns_have_required_fields(self):
        """All nouns have gender and cases."""
        nouns = self.grammar_data.get("nouns", {})
        for noun, data in nouns.items():
            self.assertIn("gender", data, f"{noun} missing gender")
            self.assertIn("singular", data, f"{noun} missing singular cases")
            self.assertIn("plural", data, f"{noun} missing plural cases")
    
    def test_noun_cases_complete(self):
        """All nouns have all 6 cases in singular and plural."""
        required_cases = ["nominative", "genitive", "dative", 
                         "accusative", "instrumental", "prepositional"]
        nouns = self.grammar_data.get("nouns", {})
        for noun, data in nouns.items():
            for case in required_cases:
                self.assertIn(case, data["singular"], 
                              f"{noun} singular missing {case}")
                self.assertIn(case, data["plural"], 
                              f"{noun} plural missing {case}")


class TestRussianGrammarIntegration(unittest.TestCase):
    """Integration tests for Russian language grammar."""
    
    @classmethod
    def setUpClass(cls):
        """Initialize Russian language handler."""
        cls.russian = Russian()
    
    def test_verb_lookup_has_past(self):
        """Verb lookup includes past tense."""
        result = self.russian.lookup("знать")
        self.assertIsNotNone(result)
        self.assertIn("past", result)
        self.assertEqual(result["past"]["masc"], "зна́л")
    
    def test_verb_lookup_has_future(self):
        """Verb lookup includes future tense."""
        result = self.russian.lookup("знать")
        self.assertIn("future", result)
        self.assertIn("бу́ду знать", result["future"]["я"])
    
    def test_verb_lookup_has_imperative(self):
        """Verb lookup includes imperative."""
        result = self.russian.lookup("знать")
        self.assertIn("imperative", result)
        self.assertEqual(result["imperative"]["singular"], "зна́й")
    
    def test_verb_lookup_has_participles(self):
        """Verb lookup includes participles."""
        result = self.russian.lookup("знать")
        self.assertIn("participles", result)
        self.assertIn("present_active", result["participles"])
    
    def test_noun_lookup_has_plural_cases(self):
        """Noun lookup includes plural cases."""
        result = self.russian.lookup("дом")
        self.assertIsNotNone(result)
        self.assertIn("plural_cases", result)
        self.assertEqual(result["plural_cases"]["nominative"], "дома́")
    
    def test_irregular_verb_past(self):
        """Irregular verb идти has correct past (шёл)."""
        result = self.russian.lookup("идти")
        self.assertIn("past", result)
        self.assertEqual(result["past"]["masc"], "шёл")
    
    def test_irregular_noun_plural(self):
        """Irregular noun человек has correct plural (люди)."""
        result = self.russian.lookup("человек")
        self.assertIn("plural_cases", result)
        self.assertEqual(result["plural_cases"]["nominative"], "лю́ди")


class TestGrammarEngine(unittest.TestCase):
    """Tests for GrammarEngine class."""
    
    def setUp(self):
        """Initialize grammar engine."""
        self.engine = GrammarEngine()
    
    def test_full_verb_conjugation(self):
        """Get complete verb conjugation."""
        verb_data = {
            "word": "читать",
            "aspect": "imperfective",
            "conjugation": {
                "они": "читают",
                "ты": "читаешь",
                "мы": "читаем"
            }
        }
        result = self.engine.get_full_verb_conjugation(verb_data)
        self.assertIn("past", result)
        self.assertIn("future", result)
        self.assertIn("infinitive", result)
    
    def test_full_noun_declension(self):
        """Get complete noun declension."""
        noun_data = {
            "gender": "masculine",
            "cases": {
                "nominative": "стол",
                "genitive": "стола"
            }
        }
        result = self.engine.get_full_noun_declension(noun_data)
        self.assertIn("singular", result)
        self.assertIn("plural", result)


if __name__ == "__main__":
    unittest.main()
