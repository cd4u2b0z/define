#!/usr/bin/env python3
"""Add synonyms, antonyms, word families, and common verbs to ru_phrases.json"""

import json
import os

os.chdir('/home/craig/projects/define/languages/data')

with open('ru_phrases.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Loaded {len(d)} existing entries")
added = 0

# SYNONYMS & ANTONYMS
synonyms = {
    # Big/Large
    "большой": {"translation": "big, large", "transliteration": "bolshoy", "synonyms": ["огромный", "крупный", "великий"]},
    "огромный": {"translation": "huge, enormous", "transliteration": "ogromnyy", "synonyms": ["большой", "громадный"]},
    "крупный": {"translation": "large, big (scale)", "transliteration": "krupnyy"},
    "великий": {"translation": "great", "transliteration": "velikiy"},
    "громадный": {"translation": "gigantic, immense", "transliteration": "gromadnyy"},
    
    # Small
    "маленький": {"translation": "small, little", "transliteration": "malenkiy", "synonyms": ["небольшой", "крошечный", "мелкий"]},
    "небольшой": {"translation": "small, not big", "transliteration": "nebolshoy"},
    "крошечный": {"translation": "tiny", "transliteration": "kroshechnyy"},
    "мелкий": {"translation": "small, fine, petty", "transliteration": "melkiy"},
    
    # Good
    "хороший": {"translation": "good", "transliteration": "khoroshiy", "synonyms": ["отличный", "прекрасный", "замечательный"]},
    "отличный": {"translation": "excellent", "transliteration": "otlichnyy"},
    "прекрасный": {"translation": "wonderful, beautiful", "transliteration": "prekrasnyy"},
    "замечательный": {"translation": "remarkable, wonderful", "transliteration": "zamechatelnyy"},
    "великолепный": {"translation": "magnificent, splendid", "transliteration": "velikolepnyy"},
    
    # Bad
    "плохой": {"translation": "bad", "transliteration": "plokhoy", "antonyms": ["хороший"]},
    "ужасный": {"translation": "terrible, awful", "transliteration": "uzhasnyy"},
    "отвратительный": {"translation": "disgusting", "transliteration": "otvratitelnyy"},
    
    # Beautiful/Ugly
    "красивый": {"translation": "beautiful, handsome", "transliteration": "krasivyy", "synonyms": ["прекрасный", "симпатичный"]},
    "симпатичный": {"translation": "nice-looking, attractive", "transliteration": "simpatichnyy"},
    "милый": {"translation": "cute, sweet, nice", "transliteration": "milyy"},
    "некрасивый": {"translation": "ugly, unattractive", "transliteration": "nekrasivyy", "antonyms": ["красивый"]},
    "уродливый": {"translation": "ugly, deformed", "transliteration": "urodlivyy"},
    
    # Fast/Slow
    "быстрый": {"translation": "fast, quick", "transliteration": "bystryy", "antonyms": ["медленный"]},
    "медленный": {"translation": "slow", "transliteration": "medlennyy", "antonyms": ["быстрый"]},
    "скорый": {"translation": "rapid, quick", "transliteration": "skoryy"},
    
    # Happy/Sad
    "счастливый": {"translation": "happy", "transliteration": "schastlivyy", "antonyms": ["несчастный", "грустный"]},
    "радостный": {"translation": "joyful", "transliteration": "radostnyy"},
    "весёлый": {"translation": "cheerful, merry", "transliteration": "vesyolyy"},
    "грустный": {"translation": "sad", "transliteration": "grustnyy", "antonyms": ["весёлый"]},
    "печальный": {"translation": "sorrowful, sad", "transliteration": "pechalnyy"},
    "несчастный": {"translation": "unhappy, unfortunate", "transliteration": "neschastnyy"},
    
    # Hot/Cold
    "горячий": {"translation": "hot (to touch)", "transliteration": "goryachiy", "antonyms": ["холодный"]},
    "жаркий": {"translation": "hot (weather)", "transliteration": "zharkiy"},
    "тёплый": {"translation": "warm", "transliteration": "tyoplyy"},
    "холодный": {"translation": "cold", "transliteration": "kholodnyy", "antonyms": ["горячий", "тёплый"]},
    "прохладный": {"translation": "cool", "transliteration": "prokhladnyy"},
    
    # New/Old
    "новый": {"translation": "new", "transliteration": "novyy", "antonyms": ["старый"]},
    "старый": {"translation": "old", "transliteration": "staryy", "antonyms": ["новый", "молодой"]},
    "молодой": {"translation": "young", "transliteration": "molodoy", "antonyms": ["старый"]},
    "древний": {"translation": "ancient", "transliteration": "drevniy"},
    
    # Easy/Difficult
    "лёгкий": {"translation": "easy, light", "transliteration": "lyogkiy", "antonyms": ["трудный", "тяжёлый"]},
    "простой": {"translation": "simple", "transliteration": "prostoy"},
    "трудный": {"translation": "difficult", "transliteration": "trudnyy", "antonyms": ["лёгкий"]},
    "сложный": {"translation": "complex, complicated", "transliteration": "slozhnyy"},
    "тяжёлый": {"translation": "heavy, hard", "transliteration": "tyazhyolyy"},
    
    # Rich/Poor
    "богатый": {"translation": "rich", "transliteration": "bogatyy", "antonyms": ["бедный"]},
    "бедный": {"translation": "poor", "transliteration": "bednyy", "antonyms": ["богатый"]},
    
    # Smart/Stupid
    "умный": {"translation": "smart, clever", "transliteration": "umnyy", "antonyms": ["глупый"]},
    "глупый": {"translation": "stupid", "transliteration": "glupyy", "antonyms": ["умный"]},
    "мудрый": {"translation": "wise", "transliteration": "mudryy"},
    
    # Strong/Weak
    "сильный": {"translation": "strong", "transliteration": "silnyy", "antonyms": ["слабый"]},
    "слабый": {"translation": "weak", "transliteration": "slabyy", "antonyms": ["сильный"]},
    
    # Long/Short
    "длинный": {"translation": "long", "transliteration": "dlinnyy", "antonyms": ["короткий"]},
    "короткий": {"translation": "short", "transliteration": "korotkiy", "antonyms": ["длинный"]},
    
    # High/Low
    "высокий": {"translation": "high, tall", "transliteration": "vysokiy", "antonyms": ["низкий"]},
    "низкий": {"translation": "low, short", "transliteration": "nizkiy", "antonyms": ["высокий"]},
    
    # Wide/Narrow
    "широкий": {"translation": "wide", "transliteration": "shirokiy", "antonyms": ["узкий"]},
    "узкий": {"translation": "narrow", "transliteration": "uzkiy", "antonyms": ["широкий"]},
    
    # Full/Empty
    "полный": {"translation": "full", "transliteration": "polnyy", "antonyms": ["пустой"]},
    "пустой": {"translation": "empty", "transliteration": "pustoy", "antonyms": ["полный"]},
    
    # Clean/Dirty
    "чистый": {"translation": "clean", "transliteration": "chistyy", "antonyms": ["грязный"]},
    "грязный": {"translation": "dirty", "transliteration": "gryaznyy", "antonyms": ["чистый"]},
    
    # Light/Dark
    "светлый": {"translation": "light (color)", "transliteration": "svetlyy", "antonyms": ["тёмный"]},
    "тёмный": {"translation": "dark", "transliteration": "tyomnyy", "antonyms": ["светлый"]},
    
    # Cheap/Expensive
    "дешёвый": {"translation": "cheap", "transliteration": "deshyovyy", "antonyms": ["дорогой"]},
    "дорогой": {"translation": "expensive, dear", "transliteration": "dorogoy", "antonyms": ["дешёвый"]},
    
    # True/False
    "правда": {"translation": "truth", "transliteration": "pravda", "antonyms": ["ложь"]},
    "ложь": {"translation": "lie, falsehood", "transliteration": "lozh", "antonyms": ["правда"]},
    "истина": {"translation": "truth (philosophical)", "transliteration": "istina"},
    
    # Open/Closed
    "открытый": {"translation": "open", "transliteration": "otkrytyy", "antonyms": ["закрытый"]},
    "закрытый": {"translation": "closed", "transliteration": "zakrytyy", "antonyms": ["открытый"]},
    
    # Alive/Dead
    "живой": {"translation": "alive, living", "transliteration": "zhivoy", "antonyms": ["мёртвый"]},
    "мёртвый": {"translation": "dead", "transliteration": "myortvyy", "antonyms": ["живой"]},
    
    # Early/Late
    "ранний": {"translation": "early", "transliteration": "ranniy", "antonyms": ["поздний"]},
    "поздний": {"translation": "late", "transliteration": "pozdniy", "antonyms": ["ранний"]},
    
    # Near/Far
    "близкий": {"translation": "near, close", "transliteration": "blizkiy", "antonyms": ["далёкий"]},
    "далёкий": {"translation": "far, distant", "transliteration": "dalyokiy", "antonyms": ["близкий"]},
    
    # Sharp/Blunt
    "острый": {"translation": "sharp, spicy", "transliteration": "ostryy", "antonyms": ["тупой"]},
    "тупой": {"translation": "blunt, dull, stupid", "transliteration": "tupoy", "antonyms": ["острый"]},
    
    # Wet/Dry
    "мокрый": {"translation": "wet", "transliteration": "mokryy", "antonyms": ["сухой"]},
    "сухой": {"translation": "dry", "transliteration": "sukhoy", "antonyms": ["мокрый"]},
    
    # Soft/Hard
    "мягкий": {"translation": "soft", "transliteration": "myagkiy", "antonyms": ["твёрдый"]},
    "твёрдый": {"translation": "hard, solid, firm", "transliteration": "tvyordyy", "antonyms": ["мягкий"]},
    
    # Thick/Thin
    "толстый": {"translation": "thick, fat", "transliteration": "tolstyy", "antonyms": ["тонкий", "худой"]},
    "тонкий": {"translation": "thin", "transliteration": "tonkiy", "antonyms": ["толстый"]},
    "худой": {"translation": "thin, skinny", "transliteration": "khudoy", "antonyms": ["толстый"]},
    
    # Safe/Dangerous
    "безопасный": {"translation": "safe", "transliteration": "bezopasnyy", "antonyms": ["опасный"]},
    "опасный": {"translation": "dangerous", "transliteration": "opasnyy", "antonyms": ["безопасный"]},
    
    # Possible/Impossible
    "возможный": {"translation": "possible", "transliteration": "vozmozhnyy", "antonyms": ["невозможный"]},
    "невозможный": {"translation": "impossible", "transliteration": "nevozmozhnyy", "antonyms": ["возможный"]},
    
    # Necessary/Unnecessary
    "нужный": {"translation": "necessary, needed", "transliteration": "nuzhnyy", "antonyms": ["ненужный"]},
    "ненужный": {"translation": "unnecessary", "transliteration": "nenuzhnyy", "antonyms": ["нужный"]},
    
    # Same/Different
    "одинаковый": {"translation": "same, identical", "transliteration": "odinakovyy", "antonyms": ["разный"]},
    "разный": {"translation": "different, various", "transliteration": "raznyy", "antonyms": ["одинаковый"]},
}

for k, v in synonyms.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added} synonyms/antonyms")
start = added

# WORD FAMILIES
word_families = {
    # писать family (to write)
    "писать": {"translation": "to write", "transliteration": "pisat", "family": "пис-"},
    "написать": {"translation": "to write (perfective)", "transliteration": "napisat"},
    "писатель": {"translation": "writer", "transliteration": "pisatel"},
    "писательница": {"translation": "writer (female)", "transliteration": "pisatelnitsa"},
    "письмо": {"translation": "letter", "transliteration": "pismo"},
    "подписать": {"translation": "to sign", "transliteration": "podpisat"},
    "подпись": {"translation": "signature", "transliteration": "podpis"},
    "записать": {"translation": "to write down, record", "transliteration": "zapisat"},
    "записка": {"translation": "note", "transliteration": "zapiska"},
    "описать": {"translation": "to describe", "transliteration": "opisat"},
    "описание": {"translation": "description", "transliteration": "opisaniye"},
    "переписать": {"translation": "to rewrite, copy", "transliteration": "perepisat"},
    
    # читать family (to read)
    "читать": {"translation": "to read", "transliteration": "chitat", "family": "чит-"},
    "прочитать": {"translation": "to read (perfective)", "transliteration": "prochitat"},
    "читатель": {"translation": "reader", "transliteration": "chitatel"},
    "чтение": {"translation": "reading", "transliteration": "chteniye"},
    "перечитать": {"translation": "to reread", "transliteration": "perechitat"},
    
    # говорить family (to speak)
    "говорить": {"translation": "to speak, talk", "transliteration": "govorit", "family": "говор-"},
    "сказать": {"translation": "to say (perfective)", "transliteration": "skazat"},
    "разговор": {"translation": "conversation", "transliteration": "razgovor"},
    "разговаривать": {"translation": "to converse", "transliteration": "razgovarivat"},
    "говорящий": {"translation": "speaking, speaker", "transliteration": "govoryashchiy"},
    "выговор": {"translation": "reprimand, pronunciation", "transliteration": "vygovor"},
    "заговор": {"translation": "conspiracy, spell", "transliteration": "zagovor"},
    
    # работать family (to work)
    "работать": {"translation": "to work", "transliteration": "rabotat", "family": "работ-"},
    "работа": {"translation": "work, job", "transliteration": "rabota"},
    "работник": {"translation": "worker", "transliteration": "rabotnik"},
    "работница": {"translation": "worker (female)", "transliteration": "rabotnitsa"},
    "безработный": {"translation": "unemployed", "transliteration": "bezrabotnyy"},
    "безработица": {"translation": "unemployment", "transliteration": "bezrabotitsa"},
    "заработать": {"translation": "to earn", "transliteration": "zarabotat"},
    "заработок": {"translation": "earnings", "transliteration": "zarabotok"},
    "обработать": {"translation": "to process, work on", "transliteration": "obrabotat"},
    "разработать": {"translation": "to develop", "transliteration": "razrabotat"},
    
    # учить family (to teach/learn)
    "учить": {"translation": "to teach, to learn", "transliteration": "uchit", "family": "уч-"},
    "учиться": {"translation": "to study, learn", "transliteration": "uchitsya"},
    "научить": {"translation": "to teach (perfective)", "transliteration": "nauchit"},
    "научиться": {"translation": "to learn (perfective)", "transliteration": "nauchitsya"},
    "учитель": {"translation": "teacher (male)", "transliteration": "uchitel"},
    "учительница": {"translation": "teacher (female)", "transliteration": "uchitelnitsa"},
    "ученик": {"translation": "student, pupil", "transliteration": "uchenik"},
    "ученица": {"translation": "student (female)", "transliteration": "uchenitsa"},
    "учёный": {"translation": "scientist, scholar", "transliteration": "uchyonyy"},
    "учебник": {"translation": "textbook", "transliteration": "uchebnik"},
    "учёба": {"translation": "studies", "transliteration": "uchyoba"},
    "наука": {"translation": "science", "transliteration": "nauka"},
    "научный": {"translation": "scientific", "transliteration": "nauchnyy"},
    "изучать": {"translation": "to study (subject)", "transliteration": "izuchat"},
    "изучение": {"translation": "study, learning", "transliteration": "izucheniye"},
    
    # жить family (to live)
    "жить": {"translation": "to live", "transliteration": "zhit", "family": "жи-/жив-"},
    "жизнь": {"translation": "life", "transliteration": "zhizn"},
    "животное": {"translation": "animal", "transliteration": "zhivotnoye"},
    "жилой": {"translation": "residential", "transliteration": "zhiloy"},
    "жильё": {"translation": "housing, dwelling", "transliteration": "zhilyo"},
    "пережить": {"translation": "to survive, experience", "transliteration": "perezhit"},
    "выжить": {"translation": "to survive", "transliteration": "vyzhit"},
    "прожить": {"translation": "to live through", "transliteration": "prozhit"},
    
    # любить family (to love)
    "любить": {"translation": "to love", "transliteration": "lyubit", "family": "люб-"},
    "любовь": {"translation": "love", "transliteration": "lyubov"},
    "любимый": {"translation": "beloved, favorite", "transliteration": "lyubimyy"},
    "любовник": {"translation": "lover (male)", "transliteration": "lyubovnik"},
    "любовница": {"translation": "lover (female)", "transliteration": "lyubovnitsa"},
    "влюбиться": {"translation": "to fall in love", "transliteration": "vlyubitsya"},
    "влюблённый": {"translation": "in love", "transliteration": "vlyublyonnyy"},
    "полюбить": {"translation": "to come to love", "transliteration": "polyubit"},
    "любопытный": {"translation": "curious", "transliteration": "lyubopytnyy"},
    "любезный": {"translation": "kind, courteous", "transliteration": "lyubeznyy"},
    
    # видеть family (to see)
    "видеть": {"translation": "to see", "transliteration": "videt", "family": "вид-"},
    "увидеть": {"translation": "to see (perfective)", "transliteration": "uvidet"},
    "вид": {"translation": "view, appearance, type", "transliteration": "vid"},
    "видимый": {"translation": "visible", "transliteration": "vidimyy"},
    "невидимый": {"translation": "invisible", "transliteration": "nevidimyy"},
    "видео": {"translation": "video", "transliteration": "video"},
    "очевидный": {"translation": "obvious", "transliteration": "ochevidnyy"},
    "свидетель": {"translation": "witness", "transliteration": "svidetel"},
    "завидовать": {"translation": "to envy", "transliteration": "zavidovat"},
    "зависть": {"translation": "envy", "transliteration": "zavist"},
    
    # ходить family (to walk/go)
    "ходить": {"translation": "to walk, go (regularly)", "transliteration": "khodit", "family": "ход-"},
    "идти": {"translation": "to go, walk (once)", "transliteration": "idti"},
    "выходить": {"translation": "to exit, go out", "transliteration": "vykhodit"},
    "выход": {"translation": "exit", "transliteration": "vykhod"},
    "вход": {"translation": "entrance", "transliteration": "vkhod"},
    "входить": {"translation": "to enter", "transliteration": "vkhodit"},
    "уходить": {"translation": "to leave", "transliteration": "ukhodit"},
    "приходить": {"translation": "to arrive, come", "transliteration": "prikhodit"},
    "переходить": {"translation": "to cross", "transliteration": "perekhodit"},
    "переход": {"translation": "crossing, passage", "transliteration": "perekhod"},
    "находить": {"translation": "to find", "transliteration": "nakhodit"},
    "поход": {"translation": "hike, campaign", "transliteration": "pokhod"},
    "доход": {"translation": "income", "transliteration": "dokhod"},
    "расход": {"translation": "expense", "transliteration": "raskhod"},
    
    # делать family (to do/make)
    "делать": {"translation": "to do, make", "transliteration": "delat", "family": "дел-"},
    "сделать": {"translation": "to do, make (perfective)", "transliteration": "sdelat"},
    "дело": {"translation": "matter, business, affair", "transliteration": "delo"},
    "деловой": {"translation": "business (adj)", "transliteration": "delovoy"},
    "переделать": {"translation": "to redo", "transliteration": "peredelat"},
    "отделать": {"translation": "to finish, decorate", "transliteration": "otdelat"},
    
    # думать family (to think)
    "думать": {"translation": "to think", "transliteration": "dumat", "family": "дум-"},
    "подумать": {"translation": "to think (perfective)", "transliteration": "podumat"},
    "дума": {"translation": "thought, Duma (parliament)", "transliteration": "duma"},
    "задуматься": {"translation": "to ponder", "transliteration": "zadumatsya"},
    "обдумать": {"translation": "to think over", "transliteration": "obdumat"},
    "передумать": {"translation": "to change one's mind", "transliteration": "peredumat"},
    
    # строить family (to build)
    "строить": {"translation": "to build", "transliteration": "stroit", "family": "строй-"},
    "построить": {"translation": "to build (perfective)", "transliteration": "postroit"},
    "строительство": {"translation": "construction", "transliteration": "stroitelstvo"},
    "строитель": {"translation": "builder", "transliteration": "stroitel"},
    "здание": {"translation": "building", "transliteration": "zdaniye"},
    "постройка": {"translation": "building, structure", "transliteration": "postroyka"},
    "перестроить": {"translation": "to rebuild", "transliteration": "perestroit"},
    
    # готовить family (to prepare/cook)
    "готовить": {"translation": "to prepare, cook", "transliteration": "gotovit", "family": "готов-"},
    "приготовить": {"translation": "to prepare (perfective)", "transliteration": "prigotovit"},
    "готовый": {"translation": "ready", "transliteration": "gotovyy"},
    "готовка": {"translation": "cooking", "transliteration": "gotovka"},
    "подготовить": {"translation": "to prepare (thoroughly)", "transliteration": "podgotovit"},
    "подготовка": {"translation": "preparation, training", "transliteration": "podgotovka"},
}

for k, v in word_families.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added - start} word family entries")
start = added

# COMMON VERBS
verbs = {
    "быть": {"translation": "to be", "transliteration": "byt"},
    "есть": {"translation": "1. to eat 2. there is/are", "transliteration": "yest"},
    "иметь": {"translation": "to have", "transliteration": "imet"},
    "мочь": {"translation": "can, to be able", "transliteration": "moch"},
    "хотеть": {"translation": "to want", "transliteration": "khotet"},
    "знать": {"translation": "to know", "transliteration": "znat"},
    "понимать": {"translation": "to understand", "transliteration": "ponimat"},
    "понять": {"translation": "to understand (perfective)", "transliteration": "ponyat"},
    "давать": {"translation": "to give", "transliteration": "davat"},
    "дать": {"translation": "to give (perfective)", "transliteration": "dat"},
    "брать": {"translation": "to take", "transliteration": "brat"},
    "взять": {"translation": "to take (perfective)", "transliteration": "vzyat"},
    "стоять": {"translation": "to stand", "transliteration": "stoyat"},
    "сидеть": {"translation": "to sit", "transliteration": "sidet"},
    "лежать": {"translation": "to lie down", "transliteration": "lezhat"},
    "спать": {"translation": "to sleep", "transliteration": "spat"},
    "бежать": {"translation": "to run", "transliteration": "bezhat"},
    "летать": {"translation": "to fly", "transliteration": "letat"},
    "плавать": {"translation": "to swim", "transliteration": "plavat"},
    "играть": {"translation": "to play", "transliteration": "igrat"},
    "пить": {"translation": "to drink", "transliteration": "pit"},
    "купить": {"translation": "to buy", "transliteration": "kupit"},
    "покупать": {"translation": "to buy (imperfective)", "transliteration": "pokupat"},
    "продавать": {"translation": "to sell", "transliteration": "prodavat"},
    "открывать": {"translation": "to open", "transliteration": "otkryvat"},
    "закрывать": {"translation": "to close", "transliteration": "zakryvat"},
    "начинать": {"translation": "to begin", "transliteration": "nachinat"},
    "кончать": {"translation": "to finish", "transliteration": "konchat"},
    "помогать": {"translation": "to help", "transliteration": "pomogat"},
    "помочь": {"translation": "to help (perfective)", "transliteration": "pomoch"},
    "ждать": {"translation": "to wait", "transliteration": "zhdat"},
    "искать": {"translation": "to search, look for", "transliteration": "iskat"},
    "найти": {"translation": "to find", "transliteration": "nayti"},
    "терять": {"translation": "to lose", "transliteration": "teryat"},
    "потерять": {"translation": "to lose (perfective)", "transliteration": "poteryat"},
    "отвечать": {"translation": "to answer", "transliteration": "otvechat"},
    "спрашивать": {"translation": "to ask", "transliteration": "sprashivat"},
    "спросить": {"translation": "to ask (perfective)", "transliteration": "sprosit"},
    "слушать": {"translation": "to listen", "transliteration": "slushat"},
    "слышать": {"translation": "to hear", "transliteration": "slyshat"},
    "смотреть": {"translation": "to look, watch", "transliteration": "smotret"},
    "показывать": {"translation": "to show", "transliteration": "pokazyvat"},
    "отдыхать": {"translation": "to rest, relax", "transliteration": "otdykhat"},
    "болеть": {"translation": "to be sick, to hurt", "transliteration": "bolet"},
    "лечить": {"translation": "to treat, heal", "transliteration": "lechit"},
    "умереть": {"translation": "to die", "transliteration": "umeret"},
    "родиться": {"translation": "to be born", "transliteration": "roditsya"},
    "вставать": {"translation": "to get up", "transliteration": "vstavat"},
    "встать": {"translation": "to get up (perfective)", "transliteration": "vstat"},
    "ложиться": {"translation": "to lie down", "transliteration": "lozhitsya"},
    "лечь": {"translation": "to lie down (perfective)", "transliteration": "lech"},
    "одеваться": {"translation": "to get dressed", "transliteration": "odevatsya"},
    "раздеваться": {"translation": "to undress", "transliteration": "razdevatsya"},
    "мыться": {"translation": "to wash oneself", "transliteration": "mytsya"},
    "умываться": {"translation": "to wash face/hands", "transliteration": "umyvatsya"},
    "бриться": {"translation": "to shave", "transliteration": "britsya"},
    "причёсываться": {"translation": "to comb one's hair", "transliteration": "prichyosyvatsya"},
    "есть": {"translation": "to eat", "transliteration": "yest"},
    "завтракать": {"translation": "to have breakfast", "transliteration": "zavtrakat"},
    "обедать": {"translation": "to have lunch", "transliteration": "obedat"},
    "ужинать": {"translation": "to have dinner", "transliteration": "uzhinat"},
    "варить": {"translation": "to boil, cook", "transliteration": "varit"},
    "жарить": {"translation": "to fry", "transliteration": "zharit"},
    "печь": {"translation": "to bake", "transliteration": "pech"},
    "резать": {"translation": "to cut", "transliteration": "rezat"},
    "мешать": {"translation": "to stir, to bother", "transliteration": "meshat"},
    "звонить": {"translation": "to call, ring", "transliteration": "zvonit"},
    "позвонить": {"translation": "to call (perfective)", "transliteration": "pozvonit"},
    "посылать": {"translation": "to send", "transliteration": "posylat"},
    "послать": {"translation": "to send (perfective)", "transliteration": "poslat"},
    "получать": {"translation": "to receive", "transliteration": "poluchat"},
    "получить": {"translation": "to receive (perfective)", "transliteration": "poluchit"},
    "платить": {"translation": "to pay", "transliteration": "platit"},
    "заплатить": {"translation": "to pay (perfective)", "transliteration": "zaplatit"},
    "стоить": {"translation": "to cost", "transliteration": "stoit"},
    "менять": {"translation": "to change, exchange", "transliteration": "menyat"},
    "поменять": {"translation": "to change (perfective)", "transliteration": "pomenyat"},
    "обменять": {"translation": "to exchange", "transliteration": "obmenyat"},
    "возвращать": {"translation": "to return (something)", "transliteration": "vozvrashchat"},
    "возвращаться": {"translation": "to return (come back)", "transliteration": "vozvrashchatsya"},
    "вернуть": {"translation": "to return (perfective)", "transliteration": "vernut"},
    "вернуться": {"translation": "to return (perfective)", "transliteration": "vernutsya"},
}

for k, v in verbs.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added - start} common verbs")
start = added

# COMMON NOUNS
nouns = {
    # Family
    "семья": {"translation": "family", "transliteration": "semya"},
    "родители": {"translation": "parents", "transliteration": "roditeli"},
    "отец": {"translation": "father", "transliteration": "otets"},
    "мать": {"translation": "mother", "transliteration": "mat"},
    "папа": {"translation": "dad", "transliteration": "papa"},
    "мама": {"translation": "mom", "transliteration": "mama"},
    "сын": {"translation": "son", "transliteration": "syn"},
    "дочь": {"translation": "daughter", "transliteration": "doch"},
    "брат": {"translation": "brother", "transliteration": "brat"},
    "сестра": {"translation": "sister", "transliteration": "sestra"},
    "дедушка": {"translation": "grandfather", "transliteration": "dedushka"},
    "бабушка": {"translation": "grandmother", "transliteration": "babushka"},
    "внук": {"translation": "grandson", "transliteration": "vnuk"},
    "внучка": {"translation": "granddaughter", "transliteration": "vnuchka"},
    "дядя": {"translation": "uncle", "transliteration": "dyadya"},
    "тётя": {"translation": "aunt", "transliteration": "tyotya"},
    "муж": {"translation": "husband", "transliteration": "muzh"},
    "жена": {"translation": "wife", "transliteration": "zhena"},
    "ребёнок": {"translation": "child", "transliteration": "rebyonok"},
    "дети": {"translation": "children", "transliteration": "deti"},
    
    # Body parts
    "голова": {"translation": "head", "transliteration": "golova"},
    "лицо": {"translation": "face", "transliteration": "litso"},
    "глаз": {"translation": "eye", "transliteration": "glaz"},
    "нос": {"translation": "nose", "transliteration": "nos"},
    "рот": {"translation": "mouth", "transliteration": "rot"},
    "ухо": {"translation": "ear", "transliteration": "ukho"},
    "волосы": {"translation": "hair", "transliteration": "volosy"},
    "рука": {"translation": "hand, arm", "transliteration": "ruka"},
    "нога": {"translation": "leg, foot", "transliteration": "noga"},
    "палец": {"translation": "finger, toe", "transliteration": "palets"},
    "сердце": {"translation": "heart", "transliteration": "serdtse"},
    "живот": {"translation": "stomach, belly", "transliteration": "zhivot"},
    "спина": {"translation": "back", "transliteration": "spina"},
    "кожа": {"translation": "skin", "transliteration": "kozha"},
    "кровь": {"translation": "blood", "transliteration": "krov"},
    
    # Food & Drinks
    "еда": {"translation": "food", "transliteration": "yeda"},
    "хлеб": {"translation": "bread", "transliteration": "khleb"},
    "мясо": {"translation": "meat", "transliteration": "myaso"},
    "рыба": {"translation": "fish", "transliteration": "ryba"},
    "курица": {"translation": "chicken", "transliteration": "kuritsa"},
    "овощи": {"translation": "vegetables", "transliteration": "ovoshchi"},
    "фрукты": {"translation": "fruits", "transliteration": "frukty"},
    "яйцо": {"translation": "egg", "transliteration": "yaytso"},
    "сыр": {"translation": "cheese", "transliteration": "syr"},
    "молоко": {"translation": "milk", "transliteration": "moloko"},
    "масло": {"translation": "butter, oil", "transliteration": "maslo"},
    "соль": {"translation": "salt", "transliteration": "sol"},
    "сахар": {"translation": "sugar", "transliteration": "sakhar"},
    "вода": {"translation": "water", "transliteration": "voda"},
    "чай": {"translation": "tea", "transliteration": "chay"},
    "кофе": {"translation": "coffee", "transliteration": "kofe"},
    "сок": {"translation": "juice", "transliteration": "sok"},
    "пиво": {"translation": "beer", "transliteration": "pivo"},
    "вино": {"translation": "wine", "transliteration": "vino"},
    "водка": {"translation": "vodka", "transliteration": "vodka"},
    
    # Places
    "дом": {"translation": "house, home", "transliteration": "dom"},
    "квартира": {"translation": "apartment", "transliteration": "kvartira"},
    "комната": {"translation": "room", "transliteration": "komnata"},
    "кухня": {"translation": "kitchen", "transliteration": "kukhnya"},
    "ванная": {"translation": "bathroom", "transliteration": "vannaya"},
    "спальня": {"translation": "bedroom", "transliteration": "spalnya"},
    "гостиная": {"translation": "living room", "transliteration": "gostinaya"},
    "улица": {"translation": "street", "transliteration": "ulitsa"},
    "город": {"translation": "city", "transliteration": "gorod"},
    "деревня": {"translation": "village", "transliteration": "derevnya"},
    "страна": {"translation": "country", "transliteration": "strana"},
    "мир": {"translation": "world, peace", "transliteration": "mir"},
    "магазин": {"translation": "store, shop", "transliteration": "magazin"},
    "рынок": {"translation": "market", "transliteration": "rynok"},
    "ресторан": {"translation": "restaurant", "transliteration": "restoran"},
    "кафе": {"translation": "cafe", "transliteration": "kafe"},
    "банк": {"translation": "bank", "transliteration": "bank"},
    "больница": {"translation": "hospital", "transliteration": "bolnitsa"},
    "аптека": {"translation": "pharmacy", "transliteration": "apteka"},
    "школа": {"translation": "school", "transliteration": "shkola"},
    "университет": {"translation": "university", "transliteration": "universitet"},
    "библиотека": {"translation": "library", "transliteration": "biblioteka"},
    "музей": {"translation": "museum", "transliteration": "muzey"},
    "театр": {"translation": "theater", "transliteration": "teatr"},
    "кино": {"translation": "cinema, movie", "transliteration": "kino"},
    "парк": {"translation": "park", "transliteration": "park"},
    "вокзал": {"translation": "train station", "transliteration": "vokzal"},
    "аэропорт": {"translation": "airport", "transliteration": "aeroport"},
    "станция": {"translation": "station", "transliteration": "stantsiya"},
    "остановка": {"translation": "stop (bus/tram)", "transliteration": "ostanovka"},
    
    # Time
    "время": {"translation": "time", "transliteration": "vremya"},
    "год": {"translation": "year", "transliteration": "god"},
    "месяц": {"translation": "month", "transliteration": "mesyats"},
    "неделя": {"translation": "week", "transliteration": "nedelya"},
    "день": {"translation": "day", "transliteration": "den"},
    "час": {"translation": "hour", "transliteration": "chas"},
    "минута": {"translation": "minute", "transliteration": "minuta"},
    "секунда": {"translation": "second", "transliteration": "sekunda"},
    "утро": {"translation": "morning", "transliteration": "utro"},
    "вечер": {"translation": "evening", "transliteration": "vecher"},
    "ночь": {"translation": "night", "transliteration": "noch"},
    
    # Nature
    "природа": {"translation": "nature", "transliteration": "priroda"},
    "погода": {"translation": "weather", "transliteration": "pogoda"},
    "солнце": {"translation": "sun", "transliteration": "solntse"},
    "луна": {"translation": "moon", "transliteration": "luna"},
    "звезда": {"translation": "star", "transliteration": "zvezda"},
    "небо": {"translation": "sky", "transliteration": "nebo"},
    "земля": {"translation": "earth, land, ground", "transliteration": "zemlya"},
    "море": {"translation": "sea", "transliteration": "more"},
    "река": {"translation": "river", "transliteration": "reka"},
    "озеро": {"translation": "lake", "transliteration": "ozero"},
    "гора": {"translation": "mountain", "transliteration": "gora"},
    "лес": {"translation": "forest", "transliteration": "les"},
    "дерево": {"translation": "tree", "transliteration": "derevo"},
    "цветок": {"translation": "flower", "transliteration": "tsvetok"},
    "трава": {"translation": "grass", "transliteration": "trava"},
    "дождь": {"translation": "rain", "transliteration": "dozhd"},
    "снег": {"translation": "snow", "transliteration": "sneg"},
    "ветер": {"translation": "wind", "transliteration": "veter"},
    
    # Animals
    "собака": {"translation": "dog", "transliteration": "sobaka"},
    "кошка": {"translation": "cat", "transliteration": "koshka"},
    "кот": {"translation": "cat (male)", "transliteration": "kot"},
    "птица": {"translation": "bird", "transliteration": "ptitsa"},
    "лошадь": {"translation": "horse", "transliteration": "loshad"},
    "корова": {"translation": "cow", "transliteration": "korova"},
    "свинья": {"translation": "pig", "transliteration": "svinya"},
    "медведь": {"translation": "bear", "transliteration": "medved"},
    "волк": {"translation": "wolf", "transliteration": "volk"},
    "лиса": {"translation": "fox", "transliteration": "lisa"},
    "заяц": {"translation": "hare", "transliteration": "zayats"},
    
    # Things
    "вещь": {"translation": "thing", "transliteration": "veshch"},
    "книга": {"translation": "book", "transliteration": "kniga"},
    "газета": {"translation": "newspaper", "transliteration": "gazeta"},
    "журнал": {"translation": "magazine", "transliteration": "zhurnal"},
    "телефон": {"translation": "telephone", "transliteration": "telefon"},
    "компьютер": {"translation": "computer", "transliteration": "kompyuter"},
    "машина": {"translation": "car, machine", "transliteration": "mashina"},
    "автобус": {"translation": "bus", "transliteration": "avtobus"},
    "поезд": {"translation": "train", "transliteration": "poyezd"},
    "самолёт": {"translation": "airplane", "transliteration": "samolyot"},
    "деньги": {"translation": "money", "transliteration": "dengi"},
    "ключ": {"translation": "key", "transliteration": "klyuch"},
    "дверь": {"translation": "door", "transliteration": "dver"},
    "окно": {"translation": "window", "transliteration": "okno"},
    "стол": {"translation": "table", "transliteration": "stol"},
    "стул": {"translation": "chair", "transliteration": "stul"},
    "кровать": {"translation": "bed", "transliteration": "krovat"},
    "одежда": {"translation": "clothes", "transliteration": "odezhda"},
}

for k, v in nouns.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added - start} common nouns")

# Save
with open('ru_phrases.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"\n=== SUMMARY ===")
print(f"Total new entries added: {added}")
print(f"Total entries in file: {len(d)}")
