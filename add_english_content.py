#!/usr/bin/env python3
"""Add comprehensive English → Russian dictionary content to en_phrases.json"""

import json
import os

os.chdir('/home/craig/projects/define/languages/data')

with open('en_phrases.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Loaded {len(d)} existing entries")
added = 0

# =============================================================================
# SECTION 1: ENGLISH SLANG → RUSSIAN
# =============================================================================

slang = {
    # General Slang
    "awesome": {"translation": "круто, офигенно, потрясающе", "transliteration": "kruto, ofigenno, potryasayushche", "type": "slang"},
    "cool": {"translation": "круто, классно, клёво", "transliteration": "kruto, klassno, klyovo", "type": "slang"},
    "sick": {"translation": "круто, офигенно (positive slang)", "transliteration": "kruto, ofigenno", "type": "slang"},
    "dope": {"translation": "крутой, клёвый", "transliteration": "krutoy, klyovyy", "type": "slang"},
    "lit": {"translation": "зажигательный, огонь", "transliteration": "zazhigatelnyy, ogon", "type": "slang"},
    "fire": {"translation": "огонь, круто", "transliteration": "ogon, kruto", "type": "slang"},
    "goat": {"translation": "лучший из лучших (greatest of all time)", "transliteration": "luchshiy iz luchshikh", "type": "slang"},
    "lowkey": {"translation": "типа, как бы, немного", "transliteration": "tipa, kak by, nemnogo", "type": "slang"},
    "highkey": {"translation": "реально, очень", "transliteration": "realno, ochen", "type": "slang"},
    "salty": {"translation": "обиженный, злой", "transliteration": "obizhennyy, zloy", "type": "slang"},
    "shady": {"translation": "подозрительный, мутный", "transliteration": "podozritelnyy, mutnyy", "type": "slang"},
    "sketchy": {"translation": "подозрительный, стрёмный", "transliteration": "podozritelnyy, stryomnyy", "type": "slang"},
    "sus": {"translation": "подозрительный, палевный (suspicious)", "transliteration": "podozritelnyy, palevnyy", "type": "slang"},
    "vibe": {"translation": "атмосфера, настроение", "transliteration": "atmosfera, nastroyeniye", "type": "slang"},
    "vibing": {"translation": "кайфую, чиллю", "transliteration": "kayfuyu, chillyu", "type": "slang"},
    "chill": {"translation": "расслабляться, чиллить", "transliteration": "rasslablyatsya, chillit", "type": "slang"},
    "hang out": {"translation": "тусоваться, зависать", "transliteration": "tusovatsya, zavisat", "type": "slang"},
    "crash": {"translation": "завалиться спать", "transliteration": "zavalitsya spat", "type": "slang"},
    "bail": {"translation": "свалить, слинять", "transliteration": "svalit, slinyat", "type": "slang"},
    "bounce": {"translation": "уходить, сваливать", "transliteration": "ukhodit, svalivat", "type": "slang"},
    "peace out": {"translation": "пока, бывай", "transliteration": "poka, byvay", "type": "slang"},
    "later": {"translation": "пока, до связи", "transliteration": "poka, do svyazi", "type": "slang"},
    "bro": {"translation": "брат, братан, бро", "transliteration": "brat, bratan, bro", "type": "slang"},
    "dude": {"translation": "чувак", "transliteration": "chuvak", "type": "slang"},
    "homie": {"translation": "кореш, друган", "transliteration": "koresh, drugan", "type": "slang"},
    "fam": {"translation": "семья, свои", "transliteration": "semya, svoi", "type": "slang"},
    "squad": {"translation": "компания, банда", "transliteration": "kompaniya, banda", "type": "slang"},
    "crew": {"translation": "команда, тусовка", "transliteration": "komanda, tusovka", "type": "slang"},
    "bestie": {"translation": "лучшая подруга / лучший друг", "transliteration": "luchshaya podruga / luchshiy drug", "type": "slang"},
    "bae": {"translation": "малыш, любимый/ая", "transliteration": "malysh, lyubimyy/aya", "type": "slang"},
    
    # Internet/Texting Slang
    "lol": {"translation": "лол, ржу", "transliteration": "lol, rzhu", "type": "internet slang"},
    "lmao": {"translation": "умираю со смеху", "transliteration": "umirayu so smekhu", "type": "internet slang"},
    "rofl": {"translation": "катаюсь по полу", "transliteration": "katayus po polu", "type": "internet slang"},
    "omg": {"translation": "о боже, офигеть", "transliteration": "o bozhe, ofiget", "type": "internet slang"},
    "wtf": {"translation": "какого хрена, что за фигня", "transliteration": "kakogo khrena, chto za fignya", "type": "internet slang"},
    "idk": {"translation": "не знаю, хз", "transliteration": "ne znayu, khz", "type": "internet slang"},
    "imo": {"translation": "по-моему, имхо", "transliteration": "po-moyemu, imkho", "type": "internet slang"},
    "tbh": {"translation": "честно говоря", "transliteration": "chestno govorya", "type": "internet slang"},
    "ngl": {"translation": "не буду врать", "transliteration": "ne budu vrat", "type": "internet slang"},
    "irl": {"translation": "в реальной жизни", "transliteration": "v realnoy zhizni", "type": "internet slang"},
    "dm": {"translation": "личное сообщение, личка", "transliteration": "lichnoye soobshcheniye, lichka", "type": "internet slang"},
    "afk": {"translation": "отошёл", "transliteration": "otoshyol", "type": "internet slang"},
    "brb": {"translation": "скоро вернусь", "transliteration": "skoro vernus", "type": "internet slang"},
    "gtg": {"translation": "мне пора", "transliteration": "mne pora", "type": "internet slang"},
    "ttyl": {"translation": "до связи", "transliteration": "do svyazi", "type": "internet slang"},
    "fyi": {"translation": "к сведению", "transliteration": "k svedeniyu", "type": "internet slang"},
    "asap": {"translation": "как можно скорее", "transliteration": "kak mozhno skoreye", "type": "internet slang"},
    "tldr": {"translation": "короче, вкратце", "transliteration": "koroche, vkrattse", "type": "internet slang"},
    "meme": {"translation": "мем", "transliteration": "mem", "type": "internet slang"},
    "viral": {"translation": "вирусный", "transliteration": "virusnyy", "type": "internet slang"},
    "trending": {"translation": "в тренде", "transliteration": "v trende", "type": "internet slang"},
    "ghosting": {"translation": "игнорирование, динамить", "transliteration": "ignorirovaniye, dinamit", "type": "internet slang"},
    "catfish": {"translation": "фейковый профиль", "transliteration": "feykovyy profil", "type": "internet slang"},
    "troll": {"translation": "тролль", "transliteration": "troll", "type": "internet slang"},
    "clickbait": {"translation": "кликбейт", "transliteration": "klikbeyt", "type": "internet slang"},
    "spam": {"translation": "спам", "transliteration": "spam", "type": "internet slang"},
    "noob": {"translation": "нуб, новичок", "transliteration": "nub, novichok", "type": "internet slang"},
    "pro": {"translation": "про, профи", "transliteration": "pro, profi", "type": "internet slang"},
    "hacker": {"translation": "хакер", "transliteration": "khaker", "type": "internet slang"},
    
    # Reaction Slang
    "no way": {"translation": "да ладно, не может быть", "transliteration": "da ladno, ne mozhet byt", "type": "slang"},
    "for real": {"translation": "реально, серьёзно", "transliteration": "realno, seryozno", "type": "slang"},
    "i can't even": {"translation": "я не могу, у меня нет слов", "transliteration": "ya ne mogu, u menya net slov", "type": "slang"},
    "dead": {"translation": "умираю (со смеху)", "transliteration": "umirayu so smekhu", "type": "slang"},
    "i'm dying": {"translation": "умираю", "transliteration": "umirayu", "type": "slang"},
    "that's crazy": {"translation": "это безумие, офигеть", "transliteration": "eto bezumiye, ofiget", "type": "slang"},
    "insane": {"translation": "безумный, дикий", "transliteration": "bezumnyy, dikiy", "type": "slang"},
    "wild": {"translation": "дикий, безумный", "transliteration": "dikiy, bezumnyy", "type": "slang"},
    "nuts": {"translation": "сумасшедший, чокнутый", "transliteration": "sumasshedshiy, choknutyy", "type": "slang"},
    "bruh": {"translation": "блин, чувак", "transliteration": "blin, chuvak", "type": "slang"},
    "damn": {"translation": "блин, чёрт", "transliteration": "blin, chyort", "type": "slang"},
    "yikes": {"translation": "ой, упс", "transliteration": "oy, ups", "type": "slang"},
    "oof": {"translation": "ой, блин", "transliteration": "oy, blin", "type": "slang"},
    "cringe": {"translation": "кринж, стыдно", "transliteration": "krinzh, stydno", "type": "slang"},
    "awkward": {"translation": "неловко", "transliteration": "nelovko", "type": "slang"},
    "relatable": {"translation": "жиза, знакомо", "transliteration": "zhiza, znakomo", "type": "slang"},
    "mood": {"translation": "настроение, жиза", "transliteration": "nastroyeniye, zhiza", "type": "slang"},
    "same": {"translation": "аналогично, так же", "transliteration": "analogichno, tak zhe", "type": "slang"},
    "facts": {"translation": "факт, правда", "transliteration": "fakt, pravda", "type": "slang"},
    "bet": {"translation": "договорились, замётано", "transliteration": "dogovorilis, zamyotano", "type": "slang"},
    "say less": {"translation": "понял, не продолжай", "transliteration": "ponyal, ne prodolzhay", "type": "slang"},
    
    # Negative Slang
    "lame": {"translation": "отстой, фигня", "transliteration": "otstoy, fignya", "type": "slang"},
    "bogus": {"translation": "липовый, фальшивый", "transliteration": "lipovyy, falshivyy", "type": "slang"},
    "wack": {"translation": "отстой, фигня", "transliteration": "otstoy, fignya", "type": "slang"},
    "trash": {"translation": "отстой, мусор", "transliteration": "otstoy, musor", "type": "slang"},
    "garbage": {"translation": "отстой, мусор", "transliteration": "otstoy, musor", "type": "slang"},
    "basic": {"translation": "банальный, простой", "transliteration": "banalnyy, prostoy", "type": "slang"},
    "corny": {"translation": "банальный, сопливый", "transliteration": "banalnyy, soplivyy", "type": "slang"},
    "cheesy": {"translation": "сопливый, пошлый", "transliteration": "soplivyy, poshlyy", "type": "slang"},
    "cringy": {"translation": "стрёмный, кринжовый", "transliteration": "stryomnyy, krinzhovyy", "type": "slang"},
    "toxic": {"translation": "токсичный", "transliteration": "toksichnyy", "type": "slang"},
    "fake": {"translation": "фейковый, ненастоящий", "transliteration": "feykovyy, nenastoyashchiy", "type": "slang"},
    "phony": {"translation": "липовый, фальшивый", "transliteration": "lipovyy, falshivyy", "type": "slang"},
    "shitty": {"translation": "хреновый, дерьмовый", "transliteration": "khrenovyy, dermovyy", "type": "slang"},
    "crappy": {"translation": "дерьмовый, паршивый", "transliteration": "dermovyy, parshivyy", "type": "slang"},
    "sucks": {"translation": "отстой", "transliteration": "otstoy", "type": "slang"},
    "blows": {"translation": "отстой", "transliteration": "otstoy", "type": "slang"},
    "bummer": {"translation": "облом", "transliteration": "oblom", "type": "slang"},
    "drag": {"translation": "тоска, облом", "transliteration": "toska, oblom", "type": "slang"},
    
    # Money Slang
    "cash": {"translation": "нал, бабки", "transliteration": "nal, babki", "type": "slang"},
    "dough": {"translation": "бабки, бабло", "transliteration": "babki, bablo", "type": "slang"},
    "bread": {"translation": "бабки", "transliteration": "babki", "type": "slang"},
    "bucks": {"translation": "баксы", "transliteration": "baksy", "type": "slang"},
    "grand": {"translation": "штука (тысяча)", "transliteration": "shtuka (tysyacha)", "type": "slang"},
    "broke": {"translation": "без денег, на мели", "transliteration": "bez deneg, na meli", "type": "slang"},
    "loaded": {"translation": "при деньгах, богатый", "transliteration": "pri dengakh, bogatyy", "type": "slang"},
    "ballin": {"translation": "богатый, при бабках", "transliteration": "bogatyy, pri babkakh", "type": "slang"},
    "rip-off": {"translation": "обдираловка, развод", "transliteration": "obdiralovka, razvod", "type": "slang"},
    "cheap": {"translation": "дешёвый, жадный", "transliteration": "deshyovyy, zhadnyy", "type": "slang"},
    "pricey": {"translation": "дорогой", "transliteration": "dorogoy", "type": "slang"},
}

for k, v in slang.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added} slang entries")
start = added

# =============================================================================
# SECTION 2: ENGLISH IDIOMS → RUSSIAN
# =============================================================================

idioms = {
    # Difficulty/Ease
    "a piece of cake": {"translation": "проще пареной репы", "transliteration": "proshche parenoy repy", "type": "idiom"},
    "easy as pie": {"translation": "раз плюнуть", "transliteration": "raz plyunut", "type": "idiom"},
    "walk in the park": {"translation": "плёвое дело", "transliteration": "plyovoye delo", "type": "idiom"},
    "child's play": {"translation": "детские игрушки", "transliteration": "detskiye igrushki", "type": "idiom"},
    "not rocket science": {"translation": "не бином Ньютона", "transliteration": "ne binom Nyutona", "type": "idiom"},
    "when pigs fly": {"translation": "когда рак на горе свистнет", "transliteration": "kogda rak na gore svistnet", "type": "idiom"},
    "easier said than done": {"translation": "легче сказать, чем сделать", "transliteration": "legche skazat, chem sdelat", "type": "idiom"},
    "uphill battle": {"translation": "тяжёлая борьба", "transliteration": "tyazhyolaya borba", "type": "idiom"},
    
    # Luck/Fate
    "break a leg": {"translation": "ни пуха ни пера", "transliteration": "ni pukha ni pera", "type": "idiom"},
    "knock on wood": {"translation": "постучи по дереву", "transliteration": "postuchi po derevu", "type": "idiom"},
    "fingers crossed": {"translation": "держу кулаки", "transliteration": "derzhu kulaki", "type": "idiom"},
    "touch wood": {"translation": "тьфу-тьфу-тьфу", "transliteration": "tfu-tfu-tfu", "type": "idiom"},
    "lucky break": {"translation": "повезло", "transliteration": "povezlo", "type": "idiom"},
    "stroke of luck": {"translation": "везение", "transliteration": "vezeniye", "type": "idiom"},
    "blessing in disguise": {"translation": "нет худа без добра", "transliteration": "net khuda bez dobra", "type": "idiom"},
    "every cloud has a silver lining": {"translation": "нет худа без добра", "transliteration": "net khuda bez dobra", "type": "idiom"},
    
    # People/Character
    "couch potato": {"translation": "лежебока, диванный овощ", "transliteration": "lezheboka, divannyy ovoshch", "type": "idiom"},
    "party animal": {"translation": "тусовщик", "transliteration": "tusovshchik", "type": "idiom"},
    "bookworm": {"translation": "книжный червь", "transliteration": "knizhnyy cherv", "type": "idiom"},
    "early bird": {"translation": "ранняя пташка", "transliteration": "rannyaya ptashka", "type": "idiom"},
    "night owl": {"translation": "сова", "transliteration": "sova", "type": "idiom"},
    "busybody": {"translation": "любопытная Варвара", "transliteration": "lyubopytnaya Varvara", "type": "idiom"},
    "smart cookie": {"translation": "умник, смышлёный", "transliteration": "umnik, smyshlyonyy", "type": "idiom"},
    "tough cookie": {"translation": "крепкий орешек", "transliteration": "krepkiy oreshek", "type": "idiom"},
    "bad apple": {"translation": "паршивая овца", "transliteration": "parshivaya ovtsa", "type": "idiom"},
    "black sheep": {"translation": "белая ворона", "transliteration": "belaya vorona", "type": "idiom"},
    "big shot": {"translation": "большая шишка", "transliteration": "bolshaya shishka", "type": "idiom"},
    "big cheese": {"translation": "большая шишка", "transliteration": "bolshaya shishka", "type": "idiom"},
    "wet blanket": {"translation": "зануда", "transliteration": "zanuda", "type": "idiom"},
    "cheapskate": {"translation": "скряга, жмот", "transliteration": "skryaga, zhmot", "type": "idiom"},
    
    # Money
    "cost an arm and a leg": {"translation": "стоить бешеных денег", "transliteration": "stoit beshenykh deneg", "type": "idiom"},
    "break the bank": {"translation": "разорить", "transliteration": "razorit", "type": "idiom"},
    "make ends meet": {"translation": "сводить концы с концами", "transliteration": "svodit kontsy s kontsami", "type": "idiom"},
    "penny pincher": {"translation": "скряга", "transliteration": "skryaga", "type": "idiom"},
    "money doesn't grow on trees": {"translation": "деньги на дороге не валяются", "transliteration": "dengi na doroge ne valyayutsya", "type": "idiom"},
    "rags to riches": {"translation": "из грязи в князи", "transliteration": "iz gryazi v knyazi", "type": "idiom"},
    "filthy rich": {"translation": "купается в деньгах", "transliteration": "kupayetsya v dengakh", "type": "idiom"},
    "rolling in money": {"translation": "денег куры не клюют", "transliteration": "deneg kury ne klyuyut", "type": "idiom"},
    
    # Time
    "better late than never": {"translation": "лучше поздно, чем никогда", "transliteration": "luchshe pozdno, chem nikogda", "type": "idiom"},
    "time flies": {"translation": "время летит", "transliteration": "vremya letit", "type": "idiom"},
    "kill time": {"translation": "убивать время", "transliteration": "ubivat vremya", "type": "idiom"},
    "in the nick of time": {"translation": "в последний момент", "transliteration": "v posledniy moment", "type": "idiom"},
    "once in a blue moon": {"translation": "раз в сто лет", "transliteration": "raz v sto let", "type": "idiom"},
    "around the clock": {"translation": "круглосуточно", "transliteration": "kruglosutochno", "type": "idiom"},
    "at the eleventh hour": {"translation": "в последний момент", "transliteration": "v posledniy moment", "type": "idiom"},
    "time is money": {"translation": "время — деньги", "transliteration": "vremya — dengi", "type": "idiom"},
    
    # Communication
    "beat around the bush": {"translation": "ходить вокруг да около", "transliteration": "khodit vokrug da okolo", "type": "idiom"},
    "get to the point": {"translation": "переходить к делу", "transliteration": "perekhodit k delu", "type": "idiom"},
    "spill the beans": {"translation": "проболтаться", "transliteration": "proboltatsya", "type": "idiom"},
    "let the cat out of the bag": {"translation": "проговориться", "transliteration": "progovoritsya", "type": "idiom"},
    "break the ice": {"translation": "растопить лёд", "transliteration": "rastopit lyod", "type": "idiom"},
    "on the same page": {"translation": "на одной волне", "transliteration": "na odnoy volne", "type": "idiom"},
    "speak of the devil": {"translation": "лёгок на помине", "transliteration": "lyogok na pomine", "type": "idiom"},
    "word of mouth": {"translation": "сарафанное радио", "transliteration": "sarafannoye radio", "type": "idiom"},
    "get it off your chest": {"translation": "выговориться", "transliteration": "vygovoritsya", "type": "idiom"},
    
    # Actions/Behavior
    "bite off more than you can chew": {"translation": "откусить больше, чем можешь проглотить", "transliteration": "otkusit bolshe, chem mozhesh proglotit", "type": "idiom"},
    "burn the midnight oil": {"translation": "засиживаться допоздна", "transliteration": "zasizhivatsya dopozdna", "type": "idiom"},
    "hit the nail on the head": {"translation": "попасть в точку", "transliteration": "popast v tochku", "type": "idiom"},
    "miss the boat": {"translation": "упустить шанс", "transliteration": "upustit shans", "type": "idiom"},
    "jump the gun": {"translation": "поторопиться", "transliteration": "potoropitsya", "type": "idiom"},
    "cut corners": {"translation": "срезать углы, халтурить", "transliteration": "srezat ugly, khalturit", "type": "idiom"},
    "pull someone's leg": {"translation": "разыгрывать кого-то", "transliteration": "razygrivat kogo-to", "type": "idiom"},
    "give someone the cold shoulder": {"translation": "игнорировать", "transliteration": "ignorirovat", "type": "idiom"},
    "turn a blind eye": {"translation": "закрывать глаза на", "transliteration": "zakryvat glaza na", "type": "idiom"},
    "stab in the back": {"translation": "ударить в спину", "transliteration": "udarit v spinu", "type": "idiom"},
    "throw under the bus": {"translation": "подставить", "transliteration": "podstavit", "type": "idiom"},
    
    # Success/Failure
    "hit the jackpot": {"translation": "сорвать куш", "transliteration": "sorvat kush", "type": "idiom"},
    "strike gold": {"translation": "напасть на золотую жилу", "transliteration": "napast na zolotuyu zhilu", "type": "idiom"},
    "go down in flames": {"translation": "провалиться с треском", "transliteration": "provalitsya s treskom", "type": "idiom"},
    "fall flat on your face": {"translation": "сесть в лужу", "transliteration": "sest v luzhu", "type": "idiom"},
    "back to square one": {"translation": "вернуться к началу", "transliteration": "vernutsya k nachalu", "type": "idiom"},
    "the ball is in your court": {"translation": "ход за тобой", "transliteration": "khod za toboy", "type": "idiom"},
    "up in the air": {"translation": "ещё не решено", "transliteration": "yeshchyo ne resheno", "type": "idiom"},
    
    # Emotions
    "over the moon": {"translation": "на седьмом небе", "transliteration": "na sedmom nebe", "type": "idiom"},
    "on cloud nine": {"translation": "на седьмом небе", "transliteration": "na sedmom nebe", "type": "idiom"},
    "walking on air": {"translation": "летать от счастья", "transliteration": "letat ot schastya", "type": "idiom"},
    "down in the dumps": {"translation": "в подавленном настроении", "transliteration": "v podavlennom nastroenii", "type": "idiom"},
    "under the weather": {"translation": "неважно себя чувствовать", "transliteration": "nevazhno sebya chuvstvovat", "type": "idiom"},
    "blow off steam": {"translation": "выпустить пар", "transliteration": "vypustit par", "type": "idiom"},
    "lose your cool": {"translation": "выйти из себя", "transliteration": "vyyti iz sebya", "type": "idiom"},
    "keep your chin up": {"translation": "не вешай нос", "transliteration": "ne veshay nos", "type": "idiom"},
    "butterflies in stomach": {"translation": "бабочки в животе", "transliteration": "babochki v zhivote", "type": "idiom"},
    "get cold feet": {"translation": "струсить", "transliteration": "strusit", "type": "idiom"},
    
    # Work
    "call it a day": {"translation": "закончить на сегодня", "transliteration": "zakonchit na segodnya", "type": "idiom"},
    "burn the candle at both ends": {"translation": "работать на износ", "transliteration": "rabotat na iznos", "type": "idiom"},
    "work like a dog": {"translation": "работать как вол", "transliteration": "rabotat kak vol", "type": "idiom"},
    "the last straw": {"translation": "последняя капля", "transliteration": "poslednyaya kaplya", "type": "idiom"},
    "learn the ropes": {"translation": "освоиться", "transliteration": "osvoitsya", "type": "idiom"},
    "get the hang of it": {"translation": "освоиться, врубиться", "transliteration": "osvoitsya, vrubitsya", "type": "idiom"},
    
    # Knowledge/Truth
    "the tip of the iceberg": {"translation": "вершина айсберга", "transliteration": "vershina aysberga", "type": "idiom"},
    "see eye to eye": {"translation": "сходиться во мнении", "transliteration": "skhoditsya vo mnenii", "type": "idiom"},
    "actions speak louder than words": {"translation": "дела говорят громче слов", "transliteration": "dela govoryat gromche slov", "type": "idiom"},
    "don't judge a book by its cover": {"translation": "не суди по внешности", "transliteration": "ne sudi po vneshnosti", "type": "idiom"},
    "two wrongs don't make a right": {"translation": "злом зла не исправишь", "transliteration": "zlom zla ne ispravish", "type": "idiom"},
}

for k, v in idioms.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added - start} idiom entries")
start = added

# =============================================================================
# SECTION 3: COMMON PHRASES
# =============================================================================

phrases = {
    # Greetings
    "hello": {"translation": "здравствуйте (formal) / привет (informal)", "transliteration": "zdravstvuyte / privet"},
    "hi": {"translation": "привет", "transliteration": "privet"},
    "hey": {"translation": "эй, привет", "transliteration": "ey, privet"},
    "good morning": {"translation": "доброе утро", "transliteration": "dobroye utro"},
    "good afternoon": {"translation": "добрый день", "transliteration": "dobryy den"},
    "good evening": {"translation": "добрый вечер", "transliteration": "dobryy vecher"},
    "how are you": {"translation": "как дела?", "transliteration": "kak dela?"},
    "how's it going": {"translation": "как жизнь?", "transliteration": "kak zhizn?"},
    "what's up": {"translation": "что нового?", "transliteration": "chto novogo?"},
    "long time no see": {"translation": "давно не виделись", "transliteration": "davno ne videlis"},
    "nice to meet you": {"translation": "приятно познакомиться", "transliteration": "priyatno poznakomitsya"},
    
    # Responses
    "i'm fine": {"translation": "у меня всё хорошо", "transliteration": "u menya vsyo khorosho"},
    "i'm good": {"translation": "хорошо", "transliteration": "khorosho"},
    "great": {"translation": "отлично", "transliteration": "otlichno"},
    "not bad": {"translation": "неплохо", "transliteration": "neploho"},
    "so-so": {"translation": "так себе", "transliteration": "tak sebe"},
    "could be better": {"translation": "бывало и лучше", "transliteration": "byvalo i luchshe"},
    "terrible": {"translation": "ужасно", "transliteration": "uzhasno"},
    "same old same old": {"translation": "всё по-старому", "transliteration": "vsyo po-staromu"},
    
    # Farewells
    "goodbye": {"translation": "до свидания", "transliteration": "do svidaniya"},
    "bye": {"translation": "пока", "transliteration": "poka"},
    "see you": {"translation": "увидимся", "transliteration": "uvidimsya"},
    "see you later": {"translation": "до встречи", "transliteration": "do vstrechi"},
    "see you tomorrow": {"translation": "до завтра", "transliteration": "do zavtra"},
    "take care": {"translation": "береги себя", "transliteration": "beregi sebya"},
    "have a nice day": {"translation": "хорошего дня", "transliteration": "khoroshego dnya"},
    "good night": {"translation": "спокойной ночи", "transliteration": "spokoynoy nochi"},
    "good luck": {"translation": "удачи", "transliteration": "udachi"},
    
    # Politeness
    "please": {"translation": "пожалуйста", "transliteration": "pozhaluysta"},
    "thank you": {"translation": "спасибо", "transliteration": "spasibo"},
    "thank you very much": {"translation": "большое спасибо", "transliteration": "bolshoye spasibo"},
    "you're welcome": {"translation": "пожалуйста / не за что", "transliteration": "pozhaluysta / ne za chto"},
    "excuse me": {"translation": "извините", "transliteration": "izvinite"},
    "sorry": {"translation": "простите / извините", "transliteration": "prostite / izvinite"},
    "no problem": {"translation": "без проблем", "transliteration": "bez problem"},
    "my pleasure": {"translation": "с удовольствием", "transliteration": "s udovolstviyem"},
    "don't mention it": {"translation": "не стоит", "transliteration": "ne stoit"},
    
    # Agreement/Disagreement
    "yes": {"translation": "да", "transliteration": "da"},
    "no": {"translation": "нет", "transliteration": "net"},
    "maybe": {"translation": "может быть", "transliteration": "mozhet byt"},
    "of course": {"translation": "конечно", "transliteration": "konechno"},
    "sure": {"translation": "конечно", "transliteration": "konechno"},
    "absolutely": {"translation": "абсолютно", "transliteration": "absolyutno"},
    "definitely": {"translation": "определённо", "transliteration": "opredelyonno"},
    "i agree": {"translation": "согласен / согласна", "transliteration": "soglasen / soglasna"},
    "i disagree": {"translation": "не согласен / не согласна", "transliteration": "ne soglasen / ne soglasna"},
    "i think so": {"translation": "думаю, да", "transliteration": "dumayu, da"},
    "i don't think so": {"translation": "думаю, нет", "transliteration": "dumayu, net"},
    "that's right": {"translation": "правильно", "transliteration": "pravilno"},
    "that's wrong": {"translation": "неправильно", "transliteration": "nepravilno"},
    "exactly": {"translation": "именно", "transliteration": "imenno"},
    "not exactly": {"translation": "не совсем", "transliteration": "ne sovsem"},
    
    # Questions
    "who": {"translation": "кто?", "transliteration": "kto?"},
    "what": {"translation": "что?", "transliteration": "chto?"},
    "where": {"translation": "где?", "transliteration": "gde?"},
    "where to": {"translation": "куда?", "transliteration": "kuda?"},
    "where from": {"translation": "откуда?", "transliteration": "otkuda?"},
    "when": {"translation": "когда?", "transliteration": "kogda?"},
    "why": {"translation": "почему?", "transliteration": "pochemu?"},
    "how": {"translation": "как?", "transliteration": "kak?"},
    "how much": {"translation": "сколько?", "transliteration": "skolko?"},
    "which": {"translation": "какой?", "transliteration": "kakoy?"},
    "what's your name": {"translation": "как вас зовут?", "transliteration": "kak vas zovut?"},
    "where are you from": {"translation": "откуда вы?", "transliteration": "otkuda vy?"},
    "do you speak english": {"translation": "вы говорите по-английски?", "transliteration": "vy govorite po-angliyski?"},
    "what time is it": {"translation": "который час?", "transliteration": "kotoryy chas?"},
    "how old are you": {"translation": "сколько вам лет?", "transliteration": "skolko vam let?"},
    
    # Understanding
    "i understand": {"translation": "я понимаю", "transliteration": "ya ponimayu"},
    "i don't understand": {"translation": "я не понимаю", "transliteration": "ya ne ponimayu"},
    "can you repeat that": {"translation": "можете повторить?", "transliteration": "mozhete povtorit?"},
    "speak slower please": {"translation": "говорите медленнее, пожалуйста", "transliteration": "govorite medlenneye, pozhaluysta"},
    "what does this mean": {"translation": "что это значит?", "transliteration": "chto eto znachit?"},
    "how do you say": {"translation": "как сказать...?", "transliteration": "kak skazat...?"},
    "i don't know": {"translation": "я не знаю", "transliteration": "ya ne znayu"},
    "i forgot": {"translation": "я забыл / забыла", "transliteration": "ya zabyl / zabyla"},
    "got it": {"translation": "понял / поняла", "transliteration": "ponyal / ponyala"},
    
    # Requests
    "can you help me": {"translation": "можете помочь?", "transliteration": "mozhete pomoch?"},
    "could you please": {"translation": "не могли бы вы...?", "transliteration": "ne mogli by vy...?"},
    "i need": {"translation": "мне нужно...", "transliteration": "mne nuzhno..."},
    "i would like": {"translation": "я хотел бы... / я хотела бы...", "transliteration": "ya khotel by... / ya khotela by..."},
    "may i": {"translation": "можно...?", "transliteration": "mozhno...?"},
    "do you have": {"translation": "у вас есть...?", "transliteration": "u vas yest...?"},
    "can i get": {"translation": "можно мне...?", "transliteration": "mozhno mne...?"},
    
    # Emotions/Reactions
    "wow": {"translation": "ого! / ничего себе!", "transliteration": "ogo! / nichego sebe!"},
    "really": {"translation": "правда? / серьёзно?", "transliteration": "pravda? / seryozno?"},
    "oh my god": {"translation": "о боже!", "transliteration": "o bozhe!"},
    "are you serious": {"translation": "ты серьёзно?", "transliteration": "ty seryozno?"},
    "that's amazing": {"translation": "это потрясающе!", "transliteration": "eto potryasayushche!"},
    "that's terrible": {"translation": "это ужасно!", "transliteration": "eto uzhasno!"},
    "i'm so happy": {"translation": "я так рад / рада!", "transliteration": "ya tak rad / rada!"},
    "i'm so sorry": {"translation": "мне очень жаль", "transliteration": "mne ochen zhal"},
    "congratulations": {"translation": "поздравляю!", "transliteration": "pozdravlyayu!"},
}

for k, v in phrases.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added - start} common phrases")
start = added

# =============================================================================
# SECTION 4: SYNONYMS (English words with Russian translations)
# =============================================================================

synonyms = {
    # Beautiful synonyms
    "beautiful": {"translation": "красивый", "transliteration": "krasivyy", "synonyms": ["pretty", "gorgeous", "stunning"]},
    "pretty": {"translation": "симпатичный, хорошенький", "transliteration": "simpatichnyy, khoroshenkiy"},
    "gorgeous": {"translation": "великолепный, шикарный", "transliteration": "velikolepnyy, shikarnyy"},
    "stunning": {"translation": "потрясающий, сногсшибательный", "transliteration": "potryasayushchiy, snogshibatelnyy"},
    "lovely": {"translation": "прелестный, милый", "transliteration": "prelestnyy, milyy"},
    "attractive": {"translation": "привлекательный", "transliteration": "privlekatelnyy"},
    "handsome": {"translation": "красивый (о мужчине)", "transliteration": "krasivyy (o muzhchine)"},
    "cute": {"translation": "милый, симпатичный", "transliteration": "milyy, simpatichnyy"},
    
    # Happy synonyms
    "happy": {"translation": "счастливый", "transliteration": "schastlivyy", "synonyms": ["glad", "pleased", "delighted"]},
    "glad": {"translation": "рад", "transliteration": "rad"},
    "pleased": {"translation": "доволен", "transliteration": "dovolen"},
    "delighted": {"translation": "в восторге", "transliteration": "v vostorge"},
    "thrilled": {"translation": "в восторге", "transliteration": "v vostorge"},
    "ecstatic": {"translation": "в экстазе", "transliteration": "v ekstaze"},
    "overjoyed": {"translation": "вне себя от радости", "transliteration": "vne sebya ot radosti"},
    "content": {"translation": "довольный", "transliteration": "dovolnyy"},
    "cheerful": {"translation": "весёлый", "transliteration": "vesyolyy"},
    "joyful": {"translation": "радостный", "transliteration": "radostnyy"},
    
    # Sad synonyms
    "sad": {"translation": "грустный", "transliteration": "grustnyy", "synonyms": ["unhappy", "depressed", "miserable"]},
    "unhappy": {"translation": "несчастный", "transliteration": "neschastnyy"},
    "depressed": {"translation": "подавленный", "transliteration": "podavlennyy"},
    "miserable": {"translation": "несчастный", "transliteration": "neschastnyy"},
    "gloomy": {"translation": "мрачный", "transliteration": "mrachnyy"},
    "melancholy": {"translation": "меланхоличный", "transliteration": "melankholichnyy"},
    "heartbroken": {"translation": "убитый горем", "transliteration": "ubityy gorem"},
    "devastated": {"translation": "опустошённый", "transliteration": "opustoshyonnyy"},
    "down": {"translation": "в плохом настроении", "transliteration": "v plokhom nastroenii"},
    "blue": {"translation": "в тоске", "transliteration": "v toske"},
    
    # Angry synonyms
    "angry": {"translation": "злой, сердитый", "transliteration": "zloy, serdityy", "synonyms": ["mad", "furious", "enraged"]},
    "mad": {"translation": "злой, бешеный", "transliteration": "zloy, beshenyy"},
    "furious": {"translation": "в ярости", "transliteration": "v yarosti"},
    "enraged": {"translation": "разъярённый", "transliteration": "razyaryonnyy"},
    "annoyed": {"translation": "раздражённый", "transliteration": "razdrazhyonnyy"},
    "irritated": {"translation": "раздражённый", "transliteration": "razdrazhyonnyy"},
    "upset": {"translation": "расстроенный", "transliteration": "rasstroyennyy"},
    "pissed off": {"translation": "взбешённый", "transliteration": "vzbeshyonnyy", "type": "colloquial"},
    
    # Big synonyms
    "big": {"translation": "большой", "transliteration": "bolshoy", "synonyms": ["large", "huge", "enormous"]},
    "large": {"translation": "большой, крупный", "transliteration": "bolshoy, krupnyy"},
    "huge": {"translation": "огромный", "transliteration": "ogromnyy"},
    "enormous": {"translation": "громадный", "transliteration": "gromadnyy"},
    "massive": {"translation": "массивный", "transliteration": "massivnyy"},
    "gigantic": {"translation": "гигантский", "transliteration": "gigantskiy"},
    "vast": {"translation": "обширный", "transliteration": "obshirnyy"},
    "immense": {"translation": "необъятный", "transliteration": "neobyatnyy"},
    
    # Small synonyms
    "small": {"translation": "маленький", "transliteration": "malenkiy", "synonyms": ["little", "tiny", "miniature"]},
    "little": {"translation": "маленький", "transliteration": "malenkiy"},
    "tiny": {"translation": "крошечный", "transliteration": "kroshechnyy"},
    "miniature": {"translation": "миниатюрный", "transliteration": "miniatyurnyy"},
    "petite": {"translation": "миниатюрный", "transliteration": "miniatyurnyy"},
    "compact": {"translation": "компактный", "transliteration": "kompaktnyy"},
    "minute": {"translation": "мельчайший", "transliteration": "melchayshiy"},
    
    # Good synonyms
    "good": {"translation": "хороший", "transliteration": "khoroshiy", "synonyms": ["great", "excellent", "wonderful"]},
    "excellent": {"translation": "превосходный", "transliteration": "prevoskhodnyy"},
    "wonderful": {"translation": "чудесный", "transliteration": "chudesnyy"},
    "fantastic": {"translation": "фантастический", "transliteration": "fantasticheskiy"},
    "amazing": {"translation": "удивительный", "transliteration": "udivitelnyy"},
    "outstanding": {"translation": "выдающийся", "transliteration": "vydayushchiysya"},
    "superb": {"translation": "великолепный", "transliteration": "velikolepnyy"},
    "terrific": {"translation": "потрясающий", "transliteration": "potryasayushchiy"},
    
    # Bad synonyms
    "bad": {"translation": "плохой", "transliteration": "plokhoy", "synonyms": ["terrible", "awful", "horrible"]},
    "awful": {"translation": "ужасный", "transliteration": "uzhasnyy"},
    "horrible": {"translation": "ужасный", "transliteration": "uzhasnyy"},
    "dreadful": {"translation": "ужасный", "transliteration": "uzhasnyy"},
    "poor": {"translation": "плохой", "transliteration": "plokhoy"},
    "lousy": {"translation": "паршивый", "transliteration": "parshivyy"},
    
    # Fast synonyms
    "fast": {"translation": "быстрый", "transliteration": "bystryy", "synonyms": ["quick", "rapid", "swift"]},
    "quick": {"translation": "быстрый", "transliteration": "bystryy"},
    "rapid": {"translation": "быстрый, стремительный", "transliteration": "bystryy, stremitelnyy"},
    "swift": {"translation": "быстрый", "transliteration": "bystryy"},
    "speedy": {"translation": "скоростной", "transliteration": "skorostnoy"},
    "hasty": {"translation": "поспешный", "transliteration": "pospeshnyy"},
    "prompt": {"translation": "оперативный", "transliteration": "operativnyy"},
    
    # Slow synonyms
    "slow": {"translation": "медленный", "transliteration": "medlennyy", "synonyms": ["sluggish", "gradual", "leisurely"]},
    "sluggish": {"translation": "вялый", "transliteration": "vyalyy"},
    "gradual": {"translation": "постепенный", "transliteration": "postepennyy"},
    "leisurely": {"translation": "неторопливый", "transliteration": "netoroplivyy"},
    "unhurried": {"translation": "неспешный", "transliteration": "nespeshnyy"},
    
    # Think synonyms
    "think": {"translation": "думать", "transliteration": "dumat", "synonyms": ["believe", "consider", "assume"]},
    "believe": {"translation": "верить, считать", "transliteration": "verit, schitat"},
    "consider": {"translation": "считать, рассматривать", "transliteration": "schitat, rassmatrivat"},
    "assume": {"translation": "предполагать", "transliteration": "predpolagat"},
    "suppose": {"translation": "полагать", "transliteration": "polagat"},
    "guess": {"translation": "догадываться", "transliteration": "dogadyvatsya"},
    "reckon": {"translation": "считать", "transliteration": "schitat"},
    "figure": {"translation": "думать, полагать", "transliteration": "dumat, polagat"},
    "ponder": {"translation": "обдумывать", "transliteration": "obdumyvat"},
    "contemplate": {"translation": "размышлять", "transliteration": "razmyshlyat"},
    
    # Say synonyms
    "say": {"translation": "говорить, сказать", "transliteration": "govorit, skazat", "synonyms": ["tell", "speak", "state"]},
    "tell": {"translation": "рассказывать", "transliteration": "rasskazyvat"},
    "speak": {"translation": "говорить", "transliteration": "govorit"},
    "state": {"translation": "заявлять", "transliteration": "zayavlyat"},
    "declare": {"translation": "объявлять", "transliteration": "obyavlyat"},
    "announce": {"translation": "объявлять", "transliteration": "obyavlyat"},
    "mention": {"translation": "упоминать", "transliteration": "upominat"},
    "remark": {"translation": "замечать", "transliteration": "zamechat"},
    "claim": {"translation": "утверждать", "transliteration": "utverzhdat"},
    "assert": {"translation": "утверждать", "transliteration": "utverzhdat"},
    
    # Walk synonyms
    "walk": {"translation": "идти, ходить", "transliteration": "idti, khodit", "synonyms": ["stroll", "wander", "march"]},
    "stroll": {"translation": "прогуливаться", "transliteration": "progulivatsya"},
    "wander": {"translation": "бродить", "transliteration": "brodit"},
    "march": {"translation": "маршировать", "transliteration": "marshirovat"},
    "stride": {"translation": "шагать", "transliteration": "shagat"},
    "pace": {"translation": "расхаживать", "transliteration": "raskhazhivat"},
    "trudge": {"translation": "тащиться", "transliteration": "tashchitsya"},
    "limp": {"translation": "хромать", "transliteration": "khromat"},
    "sneak": {"translation": "красться", "transliteration": "krastsya"},
    
    # Look synonyms
    "look": {"translation": "смотреть", "transliteration": "smotret", "synonyms": ["see", "watch", "observe"]},
    "see": {"translation": "видеть", "transliteration": "videt"},
    "watch": {"translation": "смотреть, наблюдать", "transliteration": "smotret, nablyudat"},
    "observe": {"translation": "наблюдать", "transliteration": "nablyudat"},
    "gaze": {"translation": "пристально смотреть", "transliteration": "pristalno smotret"},
    "stare": {"translation": "уставиться", "transliteration": "ustavitsya"},
    "glance": {"translation": "бросить взгляд", "transliteration": "brosit vzglyad"},
    "peek": {"translation": "подглядывать", "transliteration": "podglyadyvat"},
    "glimpse": {"translation": "мельком увидеть", "transliteration": "melkom uvidet"},
}

for k, v in synonyms.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added - start} synonym entries")
start = added

# =============================================================================
# SECTION 5: ANTONYMS
# =============================================================================

antonyms = {
    # Adjective pairs
    "hot": {"translation": "горячий", "transliteration": "goryachiy", "antonyms": ["cold"]},
    "cold": {"translation": "холодный", "transliteration": "kholodnyy", "antonyms": ["hot"]},
    "new": {"translation": "новый", "transliteration": "novyy", "antonyms": ["old"]},
    "old": {"translation": "старый", "transliteration": "staryy", "antonyms": ["new", "young"]},
    "young": {"translation": "молодой", "transliteration": "molodoy", "antonyms": ["old"]},
    "high": {"translation": "высокий", "transliteration": "vysokiy", "antonyms": ["low"]},
    "low": {"translation": "низкий", "transliteration": "nizkiy", "antonyms": ["high"]},
    "long": {"translation": "длинный", "transliteration": "dlinnyy", "antonyms": ["short"]},
    "short": {"translation": "короткий", "transliteration": "korotkiy", "antonyms": ["long"]},
    "wide": {"translation": "широкий", "transliteration": "shirokiy", "antonyms": ["narrow"]},
    "narrow": {"translation": "узкий", "transliteration": "uzkiy", "antonyms": ["wide"]},
    "thick": {"translation": "толстый", "transliteration": "tolstyy", "antonyms": ["thin"]},
    "thin": {"translation": "тонкий", "transliteration": "tonkiy", "antonyms": ["thick"]},
    "heavy": {"translation": "тяжёлый", "transliteration": "tyazhyolyy", "antonyms": ["light"]},
    "light": {"translation": "лёгкий / светлый", "transliteration": "lyogkiy / svetlyy", "antonyms": ["heavy", "dark"]},
    "hard": {"translation": "твёрдый / трудный", "transliteration": "tvyordyy / trudnyy", "antonyms": ["soft", "easy"]},
    "soft": {"translation": "мягкий", "transliteration": "myagkiy", "antonyms": ["hard"]},
    "dry": {"translation": "сухой", "transliteration": "sukhoy", "antonyms": ["wet"]},
    "wet": {"translation": "мокрый", "transliteration": "mokryy", "antonyms": ["dry"]},
    "clean": {"translation": "чистый", "transliteration": "chistyy", "antonyms": ["dirty"]},
    "dirty": {"translation": "грязный", "transliteration": "gryaznyy", "antonyms": ["clean"]},
    "dark": {"translation": "тёмный", "transliteration": "tyomnyy", "antonyms": ["light"]},
    "loud": {"translation": "громкий", "transliteration": "gromkiy", "antonyms": ["quiet"]},
    "quiet": {"translation": "тихий", "transliteration": "tikhiy", "antonyms": ["loud"]},
    "strong": {"translation": "сильный", "transliteration": "silnyy", "antonyms": ["weak"]},
    "weak": {"translation": "слабый", "transliteration": "slabyy", "antonyms": ["strong"]},
    "rich": {"translation": "богатый", "transliteration": "bogatyy", "antonyms": ["poor"]},
    "expensive": {"translation": "дорогой", "transliteration": "dorogoy", "antonyms": ["cheap"]},
    "full": {"translation": "полный", "transliteration": "polnyy", "antonyms": ["empty"]},
    "empty": {"translation": "пустой", "transliteration": "pustoy", "antonyms": ["full"]},
    "alive": {"translation": "живой", "transliteration": "zhivoy", "antonyms": ["dead"]},
    "healthy": {"translation": "здоровый", "transliteration": "zdorovyy", "antonyms": ["sick"]},
    "easy": {"translation": "лёгкий", "transliteration": "lyogkiy", "antonyms": ["difficult"]},
    "difficult": {"translation": "трудный", "transliteration": "trudnyy", "antonyms": ["easy"]},
    "simple": {"translation": "простой", "transliteration": "prostoy", "antonyms": ["complex"]},
    "complex": {"translation": "сложный", "transliteration": "slozhnyy", "antonyms": ["simple"]},
    "right": {"translation": "правильный / правый", "transliteration": "pravilnyy / pravyy", "antonyms": ["wrong", "left"]},
    "wrong": {"translation": "неправильный", "transliteration": "nepravilnyy", "antonyms": ["right"]},
    "left": {"translation": "левый", "transliteration": "levyy", "antonyms": ["right"]},
    "true": {"translation": "истинный, правдивый", "transliteration": "istinnyy, pravdivyy", "antonyms": ["false"]},
    "false": {"translation": "ложный", "transliteration": "lozhnyy", "antonyms": ["true"]},
    "safe": {"translation": "безопасный", "transliteration": "bezopasnyy", "antonyms": ["dangerous"]},
    "dangerous": {"translation": "опасный", "transliteration": "opasnyy", "antonyms": ["safe"]},
    "ugly": {"translation": "уродливый", "transliteration": "urodlivyy", "antonyms": ["beautiful"]},
    "smart": {"translation": "умный", "transliteration": "umnyy", "antonyms": ["stupid"]},
    "stupid": {"translation": "глупый", "transliteration": "glupyy", "antonyms": ["smart"]},
    "brave": {"translation": "храбрый", "transliteration": "khrabryy", "antonyms": ["cowardly"]},
    "cowardly": {"translation": "трусливый", "transliteration": "truslivyy", "antonyms": ["brave"]},
    "polite": {"translation": "вежливый", "transliteration": "vezhlivyy", "antonyms": ["rude"]},
    "rude": {"translation": "грубый", "transliteration": "grubyy", "antonyms": ["polite"]},
    "honest": {"translation": "честный", "transliteration": "chestnyy", "antonyms": ["dishonest"]},
    "dishonest": {"translation": "нечестный", "transliteration": "nechestnyy", "antonyms": ["honest"]},
    
    # Verb pairs
    "come": {"translation": "приходить", "transliteration": "prikhodit", "antonyms": ["go"]},
    "go": {"translation": "идти, уходить", "transliteration": "idti, ukhodit", "antonyms": ["come"]},
    "enter": {"translation": "входить", "transliteration": "vkhodit", "antonyms": ["exit"]},
    "exit": {"translation": "выходить", "transliteration": "vykhodit", "antonyms": ["enter"]},
    "open": {"translation": "открывать", "transliteration": "otkryvat", "antonyms": ["close"]},
    "close": {"translation": "закрывать", "transliteration": "zakryvat", "antonyms": ["open"]},
    "start": {"translation": "начинать", "transliteration": "nachinat", "antonyms": ["finish"]},
    "finish": {"translation": "заканчивать", "transliteration": "zakanchivat", "antonyms": ["start"]},
    "love": {"translation": "любить", "transliteration": "lyubit", "antonyms": ["hate"]},
    "hate": {"translation": "ненавидеть", "transliteration": "nenavidet", "antonyms": ["love"]},
    "remember": {"translation": "помнить", "transliteration": "pomnit", "antonyms": ["forget"]},
    "forget": {"translation": "забывать", "transliteration": "zabyvat", "antonyms": ["remember"]},
    "give": {"translation": "давать", "transliteration": "davat", "antonyms": ["take"]},
    "take": {"translation": "брать", "transliteration": "brat", "antonyms": ["give"]},
    "buy": {"translation": "покупать", "transliteration": "pokupat", "antonyms": ["sell"]},
    "sell": {"translation": "продавать", "transliteration": "prodavat", "antonyms": ["buy"]},
    "ask": {"translation": "спрашивать", "transliteration": "sprashivat", "antonyms": ["answer"]},
    "answer": {"translation": "отвечать", "transliteration": "otvechat", "antonyms": ["ask"]},
    "win": {"translation": "выигрывать", "transliteration": "vyigryvat", "antonyms": ["lose"]},
    "lose": {"translation": "терять, проигрывать", "transliteration": "teryat, proigryvat", "antonyms": ["win", "find"]},
    "find": {"translation": "находить", "transliteration": "nakhodit", "antonyms": ["lose"]},
    "build": {"translation": "строить", "transliteration": "stroit", "antonyms": ["destroy"]},
    "destroy": {"translation": "разрушать", "transliteration": "razrushat", "antonyms": ["build"]},
    "accept": {"translation": "принимать", "transliteration": "prinimat", "antonyms": ["refuse"]},
    "refuse": {"translation": "отказываться", "transliteration": "otkazyvatsya", "antonyms": ["accept"]},
    "push": {"translation": "толкать", "transliteration": "tolkat", "antonyms": ["pull"]},
    "pull": {"translation": "тянуть", "transliteration": "tyanut", "antonyms": ["push"]},
    "rise": {"translation": "подниматься", "transliteration": "podnimatsya", "antonyms": ["fall"]},
    "fall": {"translation": "падать", "transliteration": "padat", "antonyms": ["rise"]},
    "laugh": {"translation": "смеяться", "transliteration": "smeyatsya", "antonyms": ["cry"]},
    "cry": {"translation": "плакать", "transliteration": "plakat", "antonyms": ["laugh"]},
    "wake": {"translation": "просыпаться", "transliteration": "prosypatsya", "antonyms": ["sleep"]},
    "sleep": {"translation": "спать", "transliteration": "spat", "antonyms": ["wake"]},
    "live": {"translation": "жить", "transliteration": "zhit", "antonyms": ["die"]},
    "die": {"translation": "умирать", "transliteration": "umirat", "antonyms": ["live"]},
    
    # Noun pairs
    "day": {"translation": "день", "transliteration": "den", "antonyms": ["night"]},
    "night": {"translation": "ночь", "transliteration": "noch", "antonyms": ["day"]},
    "morning": {"translation": "утро", "transliteration": "utro", "antonyms": ["evening"]},
    "evening": {"translation": "вечер", "transliteration": "vecher", "antonyms": ["morning"]},
    "summer": {"translation": "лето", "transliteration": "leto", "antonyms": ["winter"]},
    "winter": {"translation": "зима", "transliteration": "zima", "antonyms": ["summer"]},
    "north": {"translation": "север", "transliteration": "sever", "antonyms": ["south"]},
    "south": {"translation": "юг", "transliteration": "yug", "antonyms": ["north"]},
    "east": {"translation": "восток", "transliteration": "vostok", "antonyms": ["west"]},
    "west": {"translation": "запад", "transliteration": "zapad", "antonyms": ["east"]},
    "beginning": {"translation": "начало", "transliteration": "nachalo", "antonyms": ["end"]},
    "end": {"translation": "конец", "transliteration": "konets", "antonyms": ["beginning"]},
    "question": {"translation": "вопрос", "transliteration": "vopros", "antonyms": ["answer"]},
    "war": {"translation": "война", "transliteration": "voyna", "antonyms": ["peace"]},
    "peace": {"translation": "мир", "transliteration": "mir", "antonyms": ["war"]},
    "friend": {"translation": "друг", "transliteration": "drug", "antonyms": ["enemy"]},
    "enemy": {"translation": "враг", "transliteration": "vrag", "antonyms": ["friend"]},
    "success": {"translation": "успех", "transliteration": "uspekh", "antonyms": ["failure"]},
    "failure": {"translation": "неудача", "transliteration": "neudacha", "antonyms": ["success"]},
    "life": {"translation": "жизнь", "transliteration": "zhizn", "antonyms": ["death"]},
    "death": {"translation": "смерть", "transliteration": "smert", "antonyms": ["life"]},
    "joy": {"translation": "радость", "transliteration": "radost", "antonyms": ["sorrow"]},
    "sorrow": {"translation": "горе", "transliteration": "gore", "antonyms": ["joy"]},
    "truth": {"translation": "правда", "transliteration": "pravda", "antonyms": ["lie"]},
    "lie": {"translation": "ложь", "transliteration": "lozh", "antonyms": ["truth"]},
    "entrance": {"translation": "вход", "transliteration": "vkhod", "antonyms": ["exit"]},
    "heaven": {"translation": "рай", "transliteration": "ray", "antonyms": ["hell"]},
    "hell": {"translation": "ад", "transliteration": "ad", "antonyms": ["heaven"]},
    "man": {"translation": "мужчина", "transliteration": "muzhchina", "antonyms": ["woman"]},
    "woman": {"translation": "женщина", "transliteration": "zhenshchina", "antonyms": ["man"]},
    "boy": {"translation": "мальчик", "transliteration": "malchik", "antonyms": ["girl"]},
    "girl": {"translation": "девочка", "transliteration": "devochka", "antonyms": ["boy"]},
    "father": {"translation": "отец", "transliteration": "otets", "antonyms": ["mother"]},
    "mother": {"translation": "мать", "transliteration": "mat", "antonyms": ["father"]},
    "husband": {"translation": "муж", "transliteration": "muzh", "antonyms": ["wife"]},
    "wife": {"translation": "жена", "transliteration": "zhena", "antonyms": ["husband"]},
    "son": {"translation": "сын", "transliteration": "syn", "antonyms": ["daughter"]},
    "daughter": {"translation": "дочь", "transliteration": "doch", "antonyms": ["son"]},
    "brother": {"translation": "брат", "transliteration": "brat", "antonyms": ["sister"]},
    "sister": {"translation": "сестра", "transliteration": "sestra", "antonyms": ["brother"]},
    
    # Adverb pairs
    "here": {"translation": "здесь", "transliteration": "zdes", "antonyms": ["there"]},
    "there": {"translation": "там", "transliteration": "tam", "antonyms": ["here"]},
    "now": {"translation": "сейчас", "transliteration": "seychas", "antonyms": ["then"]},
    "then": {"translation": "тогда", "transliteration": "togda", "antonyms": ["now"]},
    "always": {"translation": "всегда", "transliteration": "vsegda", "antonyms": ["never"]},
    "never": {"translation": "никогда", "transliteration": "nikogda", "antonyms": ["always"]},
    "often": {"translation": "часто", "transliteration": "chasto", "antonyms": ["rarely"]},
    "rarely": {"translation": "редко", "transliteration": "redko", "antonyms": ["often"]},
    "everywhere": {"translation": "везде", "transliteration": "vezde", "antonyms": ["nowhere"]},
    "nowhere": {"translation": "нигде", "transliteration": "nigde", "antonyms": ["everywhere"]},
    "together": {"translation": "вместе", "transliteration": "vmeste", "antonyms": ["separately"]},
    "separately": {"translation": "отдельно", "transliteration": "otdelno", "antonyms": ["together"]},
    "inside": {"translation": "внутри", "transliteration": "vnutri", "antonyms": ["outside"]},
    "outside": {"translation": "снаружи", "transliteration": "snaruzhi", "antonyms": ["inside"]},
    "up": {"translation": "вверх", "transliteration": "vverkh", "antonyms": ["down"]},
    "forward": {"translation": "вперёд", "transliteration": "vperyod", "antonyms": ["backward"]},
    "backward": {"translation": "назад", "transliteration": "nazad", "antonyms": ["forward"]},
    "more": {"translation": "больше", "transliteration": "bolshe", "antonyms": ["less"]},
    "less": {"translation": "меньше", "transliteration": "menshe", "antonyms": ["more"]},
    "early": {"translation": "рано", "transliteration": "rano", "antonyms": ["late"]},
    "late": {"translation": "поздно", "transliteration": "pozdno", "antonyms": ["early"]},
    "quickly": {"translation": "быстро", "transliteration": "bystro", "antonyms": ["slowly"]},
    "slowly": {"translation": "медленно", "transliteration": "medlenno", "antonyms": ["quickly"]},
}

for k, v in antonyms.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added - start} antonym entries")
start = added

# =============================================================================
# SECTION 6: PROVERBS
# =============================================================================

proverbs = {
    "the early bird catches the worm": {"translation": "кто рано встаёт, тому Бог подаёт", "transliteration": "kto rano vstayot, tomu Bog podayot", "type": "proverb"},
    "practice makes perfect": {"translation": "повторение — мать учения", "transliteration": "povtoreniye — mat ucheniya", "type": "proverb"},
    "all that glitters is not gold": {"translation": "не всё то золото, что блестит", "transliteration": "ne vsyo to zoloto, chto blestit", "type": "proverb"},
    "where there's a will there's a way": {"translation": "было бы желание", "transliteration": "bylo by zhelaniye", "type": "proverb"},
    "a friend in need is a friend indeed": {"translation": "друг познаётся в беде", "transliteration": "drug poznayotsya v bede", "type": "proverb"},
    "when in rome do as the romans do": {"translation": "в чужой монастырь со своим уставом не ходят", "transliteration": "v chuzhoy monastyr so svoim ustavom ne khodyat", "type": "proverb"},
    "there's no place like home": {"translation": "в гостях хорошо, а дома лучше", "transliteration": "v gostyakh khorosho, a doma luchshe", "type": "proverb"},
    "the apple doesn't fall far from the tree": {"translation": "яблоко от яблони недалеко падает", "transliteration": "yabloko ot yabloni nedaleko padayet", "type": "proverb"},
    "don't count your chickens before they hatch": {"translation": "цыплят по осени считают", "transliteration": "tsyplyat po oseni schitayut", "type": "proverb"},
    "a penny saved is a penny earned": {"translation": "копейка рубль бережёт", "transliteration": "kopeyka rubl berezhyot", "type": "proverb"},
    "the grass is always greener on the other side": {"translation": "хорошо там, где нас нет", "transliteration": "khorosho tam, gde nas net", "type": "proverb"},
    "you can't have your cake and eat it too": {"translation": "и волки сыты, и овцы целы", "transliteration": "i volki syty, i ovtsy tsely", "type": "proverb"},
    "two heads are better than one": {"translation": "ум хорошо, а два лучше", "transliteration": "um khorosho, a dva luchshe", "type": "proverb"},
    "rome wasn't built in a day": {"translation": "Москва не сразу строилась", "transliteration": "Moskva ne srazu stroilas", "type": "proverb"},
    "once bitten twice shy": {"translation": "обжёгшись на молоке, дуешь на воду", "transliteration": "obzhyogshis na moloke, duyesh na vodu", "type": "proverb"},
    "what goes around comes around": {"translation": "как аукнется, так и откликнется", "transliteration": "kak auknetsya, tak i otkliknetsya", "type": "proverb"},
    "when the cat's away the mice will play": {"translation": "без кота мышам раздолье", "transliteration": "bez kota mysham razdolye", "type": "proverb"},
    "too many cooks spoil the broth": {"translation": "у семи нянек дитя без глаза", "transliteration": "u semi nyanek ditya bez glaza", "type": "proverb"},
    "look before you leap": {"translation": "семь раз отмерь, один раз отрежь", "transliteration": "sem raz otmer, odin raz otrezh", "type": "proverb"},
    "a rolling stone gathers no moss": {"translation": "под лежачий камень вода не течёт", "transliteration": "pod lezhachiy kamen voda ne techyot", "type": "proverb"},
    "an eye for an eye": {"translation": "око за око", "transliteration": "oko za oko", "type": "proverb"},
    "curiosity killed the cat": {"translation": "любопытство сгубило кошку", "transliteration": "lyubopytstvo sgubilo koshku", "type": "proverb"},
    "you can lead a horse to water but you can't make it drink": {"translation": "силой мил не будешь", "transliteration": "siloy mil ne budesh", "type": "proverb"},
    "time heals all wounds": {"translation": "время лечит", "transliteration": "vremya lechit", "type": "proverb"},
    "if you chase two rabbits you will catch neither": {"translation": "за двумя зайцами погонишься — ни одного не поймаешь", "transliteration": "za dvumya zaytsami pogonishsya — ni odnogo ne poymayesh", "type": "proverb"},
}

for k, v in proverbs.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added - start} proverb entries")
start = added

# =============================================================================
# SECTION 7: PROFANITY (English → Russian)
# =============================================================================

profanity = {
    # Exclamations
    "damn it": {"translation": "чёрт возьми", "transliteration": "chyort vozmi", "type": "profanity"},
    "holy shit": {"translation": "охуеть, ни фига себе", "transliteration": "okhuyet, ni figa sebe", "type": "profanity"},
    "what the fuck": {"translation": "какого хера, какого хуя", "transliteration": "kakogo khera, kakogo khuya", "type": "profanity"},
    "what the hell": {"translation": "какого чёрта", "transliteration": "kakogo chyorta", "type": "profanity"},
    "for fuck's sake": {"translation": "ёб твою мать, да блядь", "transliteration": "yob tvoyu mat, da blyad", "type": "profanity"},
    "goddamn": {"translation": "чёрт побери", "transliteration": "chyort poberi", "type": "profanity"},
    "fuck": {"translation": "блядь", "transliteration": "blyad", "type": "profanity"},
    "shit": {"translation": "блядь, дерьмо", "transliteration": "blyad, dermo", "type": "profanity"},
    
    # Insults
    "asshole": {"translation": "мудак", "transliteration": "mudak", "type": "profanity"},
    "bitch": {"translation": "сука", "transliteration": "suka", "type": "profanity"},
    "bastard": {"translation": "ублюдок", "transliteration": "ublyudok", "type": "profanity"},
    "idiot": {"translation": "идиот, дурак", "transliteration": "idiot, durak", "type": "profanity"},
    "moron": {"translation": "дебил", "transliteration": "debil", "type": "profanity"},
    "fucking idiot": {"translation": "долбоёб", "transliteration": "dolboyob", "type": "profanity"},
    "dumbass": {"translation": "еблан, тупица", "transliteration": "yeblan, tupitsa", "type": "profanity"},
    "piece of shit": {"translation": "кусок дерьма, уёбок", "transliteration": "kusok derma, uyobok", "type": "profanity"},
    "scumbag": {"translation": "мразь", "transliteration": "mraz", "type": "profanity"},
    "jerk": {"translation": "козёл", "transliteration": "kozyol", "type": "profanity"},
    "dick": {"translation": "хер, член", "transliteration": "kher, chlen", "type": "profanity"},
    "prick": {"translation": "хуй, мудак", "transliteration": "khuy, mudak", "type": "profanity"},
    "loser": {"translation": "неудачник, лузер", "transliteration": "neudachnik, luzer", "type": "profanity"},
    
    # Commands
    "fuck off": {"translation": "пошёл нахуй", "transliteration": "poshyol nakhuy", "type": "profanity"},
    "go fuck yourself": {"translation": "иди нахуй", "transliteration": "idi nakhuy", "type": "profanity"},
    "shut up": {"translation": "заткнись", "transliteration": "zatknis", "type": "profanity"},
    "shut the fuck up": {"translation": "закрой ебало", "transliteration": "zakroy yebalo", "type": "profanity"},
    "leave me alone": {"translation": "отстань", "transliteration": "otstan", "type": "profanity"},
    "leave me the fuck alone": {"translation": "отъебись", "transliteration": "otyebis", "type": "profanity"},
    "get out": {"translation": "убирайся", "transliteration": "ubiraisa", "type": "profanity"},
    "get lost": {"translation": "проваливай", "transliteration": "provalivay", "type": "profanity"},
    "don't bullshit me": {"translation": "не пизди", "transliteration": "ne pizdi", "type": "profanity"},
    "stop talking shit": {"translation": "не неси хуйню", "transliteration": "ne nesi khuynu", "type": "profanity"},
    
    # Reactions
    "fuck yeah": {"translation": "ахуенно", "transliteration": "akhuyenno", "type": "profanity"},
    "no fucking way": {"translation": "ну нахуй", "transliteration": "nu nakhuy", "type": "profanity"},
    "i don't give a fuck": {"translation": "мне похуй, мне поебать", "transliteration": "mne pokhuy, mne poyebat", "type": "profanity"},
    "i don't give a shit": {"translation": "мне насрать", "transliteration": "mne nasrat", "type": "profanity"},
    "this is bullshit": {"translation": "это хуйня", "transliteration": "eto khuynya", "type": "profanity"},
    "total disaster": {"translation": "полный пиздец", "transliteration": "polnyy pizdets", "type": "profanity"},
    "i feel like shit": {"translation": "мне хуёво", "transliteration": "mne khuyovo", "type": "profanity"},
    
    # Verbs
    "to fuck up": {"translation": "облажаться, запороть", "transliteration": "oblazhat'sya, zaporot", "type": "profanity"},
    "to screw up": {"translation": "облажаться", "transliteration": "oblazhat'sya", "type": "profanity"},
    "to bullshit": {"translation": "пиздеть", "transliteration": "pizdet", "type": "profanity"},
    "to talk shit": {"translation": "хуйню нести", "transliteration": "khuynu nesti", "type": "profanity"},
    "to be fucked": {"translation": "попасть", "transliteration": "popast", "type": "profanity"},
    "to work hard": {"translation": "ебашить, хуярить", "transliteration": "yebashit, khuyarit", "type": "profanity"},
    
    # Adjectives
    "fucked up": {"translation": "запоротый", "transliteration": "zaporotyy", "type": "profanity"},
    "ass-backwards": {"translation": "через жопу", "transliteration": "cherez zhopu", "type": "profanity"},
}

for k, v in profanity.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added - start} profanity entries")
start = added

# =============================================================================
# SECTION 8: NUMBERS & TIME
# =============================================================================

numbers_time = {
    # Numbers
    "zero": {"translation": "ноль", "transliteration": "nol"},
    "one": {"translation": "один", "transliteration": "odin"},
    "two": {"translation": "два", "transliteration": "dva"},
    "three": {"translation": "три", "transliteration": "tri"},
    "four": {"translation": "четыре", "transliteration": "chetyre"},
    "five": {"translation": "пять", "transliteration": "pyat"},
    "six": {"translation": "шесть", "transliteration": "shest"},
    "seven": {"translation": "семь", "transliteration": "sem"},
    "eight": {"translation": "восемь", "transliteration": "vosem"},
    "nine": {"translation": "девять", "transliteration": "devyat"},
    "ten": {"translation": "десять", "transliteration": "desyat"},
    "eleven": {"translation": "одиннадцать", "transliteration": "odinnadtsat"},
    "twelve": {"translation": "двенадцать", "transliteration": "dvenadtsat"},
    "twenty": {"translation": "двадцать", "transliteration": "dvadtsat"},
    "thirty": {"translation": "тридцать", "transliteration": "tridtsat"},
    "forty": {"translation": "сорок", "transliteration": "sorok"},
    "fifty": {"translation": "пятьдесят", "transliteration": "pyatdesyat"},
    "hundred": {"translation": "сто", "transliteration": "sto"},
    "thousand": {"translation": "тысяча", "transliteration": "tysyacha"},
    "million": {"translation": "миллион", "transliteration": "million"},
    
    # Ordinals
    "first": {"translation": "первый", "transliteration": "pervyy"},
    "second": {"translation": "второй", "transliteration": "vtoroy"},
    "third": {"translation": "третий", "transliteration": "tretiy"},
    "fourth": {"translation": "четвёртый", "transliteration": "chetvyortyy"},
    "fifth": {"translation": "пятый", "transliteration": "pyatyy"},
    "last": {"translation": "последний", "transliteration": "posledniy"},
    
    # Days
    "monday": {"translation": "понедельник", "transliteration": "ponedelnik"},
    "tuesday": {"translation": "вторник", "transliteration": "vtornik"},
    "wednesday": {"translation": "среда", "transliteration": "sreda"},
    "thursday": {"translation": "четверг", "transliteration": "chetverg"},
    "friday": {"translation": "пятница", "transliteration": "pyatnitsa"},
    "saturday": {"translation": "суббота", "transliteration": "subbota"},
    "sunday": {"translation": "воскресенье", "transliteration": "voskresenye"},
    
    # Months
    "january": {"translation": "январь", "transliteration": "yanvar"},
    "february": {"translation": "февраль", "transliteration": "fevral"},
    "march": {"translation": "март", "transliteration": "mart"},
    "april": {"translation": "апрель", "transliteration": "aprel"},
    "may": {"translation": "май", "transliteration": "may"},
    "june": {"translation": "июнь", "transliteration": "iyun"},
    "july": {"translation": "июль", "transliteration": "iyul"},
    "august": {"translation": "август", "transliteration": "avgust"},
    "september": {"translation": "сентябрь", "transliteration": "sentyabr"},
    "october": {"translation": "октябрь", "transliteration": "oktyabr"},
    "november": {"translation": "ноябрь", "transliteration": "noyabr"},
    "december": {"translation": "декабрь", "transliteration": "dekabr"},
    
    # Seasons
    "spring": {"translation": "весна", "transliteration": "vesna"},
    "autumn": {"translation": "осень", "transliteration": "osen"},
    
    # Time expressions
    "today": {"translation": "сегодня", "transliteration": "segodnya"},
    "tomorrow": {"translation": "завтра", "transliteration": "zavtra"},
    "yesterday": {"translation": "вчера", "transliteration": "vchera"},
    "this week": {"translation": "на этой неделе", "transliteration": "na etoy nedele"},
    "next week": {"translation": "на следующей неделе", "transliteration": "na sleduyushchey nedele"},
    "last week": {"translation": "на прошлой неделе", "transliteration": "na proshloy nedele"},
    "in the morning": {"translation": "утром", "transliteration": "utrom"},
    "in the afternoon": {"translation": "днём", "transliteration": "dnyom"},
    "in the evening": {"translation": "вечером", "transliteration": "vecherom"},
    "at night": {"translation": "ночью", "transliteration": "nochyu"},
    "hour": {"translation": "час", "transliteration": "chas"},
    "week": {"translation": "неделя", "transliteration": "nedelya"},
    "month": {"translation": "месяц", "transliteration": "mesyats"},
    "year": {"translation": "год", "transliteration": "god"},
}

for k, v in numbers_time.items():
    if k not in d:
        d[k] = v
        added += 1

print(f"Added {added - start} numbers/time entries")

# Save
with open('en_phrases.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"\n=== SUMMARY ===")
print(f"Total new entries added: {added}")
print(f"Total entries in file: {len(d)}")
