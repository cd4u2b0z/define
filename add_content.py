#!/usr/bin/env python3
"""Script to add comprehensive dictionary content."""
import json
from pathlib import Path

data_dir = Path(__file__).parent / "languages/data"

def load_json(filename):
    path = data_dir / filename
    if path.exists():
        return json.load(open(path, 'r', encoding='utf-8'))
    return {}

def save_json(filename, data):
    path = data_dir / filename
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

ru_phrases = load_json("ru_phrases.json")
print(f"Loaded {len(ru_phrases)} existing entries")

added = 0

# =============================================================================
# MORE PROVERBS
# =============================================================================

proverbs = {
    "в гостях хорошо, а дома лучше": {"translation": "there's no place like home", "transliteration": "v gostyakh khorosho, a doma luchshe", "register": "proverb"},
    "любовь зла, полюбишь и козла": {"translation": "love is blind", "transliteration": "lyubov zla, polyubish i kozla", "literal": "love is cruel, you'll love even a goat", "register": "proverb"},
    "яблоко от яблони недалеко падает": {"translation": "the apple doesn't fall far from the tree", "transliteration": "yabloko ot yabloni nedaleko padayet", "register": "proverb"},
    "на вкус и цвет товарищей нет": {"translation": "there's no accounting for taste", "transliteration": "na vkus i tsvet tovarishchey net", "register": "proverb"},
    "старый друг лучше новых двух": {"translation": "old friends are the best friends", "transliteration": "staryy drug luchshe novykh dvukh", "register": "proverb"},
    "что посеешь, то и пожнёшь": {"translation": "you reap what you sow", "transliteration": "chto poseyesh, to i pozhnyosh", "register": "proverb"},
    "терпение и труд всё перетрут": {"translation": "patience and hard work overcome all", "transliteration": "terpeniye i trud vsyo peretrut", "register": "proverb"},
    "повторение - мать учения": {"translation": "practice makes perfect", "transliteration": "povtoreniye mat ucheniya", "literal": "repetition is the mother of learning", "register": "proverb"},
    "век живи, век учись": {"translation": "live and learn / you're never too old to learn", "transliteration": "vek zhivi, vek uchis", "register": "proverb"},
    "не буди лихо, пока оно тихо": {"translation": "let sleeping dogs lie", "transliteration": "ne budi likho, poka ono tikho", "register": "proverb"},
    "слово не воробей": {"translation": "a word once spoken cannot be taken back", "transliteration": "slovo ne vorobey", "literal": "a word is not a sparrow", "register": "proverb"},
    "не имей сто рублей, а имей сто друзей": {"translation": "friends are worth more than money", "transliteration": "ne imey sto rubley, a imey sto druzey", "register": "proverb"},
    "слезами горю не поможешь": {"translation": "crying won't help", "transliteration": "slezami goryu ne pomozhesh", "register": "proverb"},
    "с глаз долой, из сердца вон": {"translation": "out of sight, out of mind", "transliteration": "s glaz doloy, iz serdtsa von", "register": "proverb"},
    "друзья познаются в беде": {"translation": "a friend in need is a friend indeed", "transliteration": "druzya poznayutsya v bede", "register": "proverb"},
    "волков бояться - в лес не ходить": {"translation": "nothing ventured, nothing gained", "transliteration": "volkov boyatsya - v les ne khodit", "register": "proverb"},
    "у семи нянек дитя без глазу": {"translation": "too many cooks spoil the broth", "transliteration": "u semi nyanek ditya bez glazu", "register": "proverb"},
    "кто рано встаёт, тому бог даёт": {"translation": "the early bird gets the worm", "transliteration": "kto rano vstayot, tomu bog dayot", "register": "proverb"},
    "своя рубашка ближе к телу": {"translation": "charity begins at home", "transliteration": "svoya rubashka blizhe k telu", "register": "proverb"},
    "где тонко, там и рвётся": {"translation": "a chain is only as strong as its weakest link", "transliteration": "gde tonko, tam i rvyotsya", "register": "proverb"},
    "не рой другому яму": {"translation": "he who digs a pit for others falls in it himself", "transliteration": "ne roy drugomu yamu", "register": "proverb"},
    "аппетит приходит во время еды": {"translation": "appetite comes with eating", "transliteration": "appetit prikhodit vo vremya yedy", "register": "proverb"},
    "на безрыбье и рак - рыба": {"translation": "beggars can't be choosers", "transliteration": "na bezrybe i rak ryba", "register": "proverb"},
    "береженого бог бережёт": {"translation": "God helps those who help themselves", "transliteration": "berezhonogo bog berezhyot", "register": "proverb"},
    "куй железо, пока горячо": {"translation": "strike while the iron is hot", "transliteration": "kuy zhelezo, poka goryacho", "register": "proverb"},
    "с волками жить - по-волчьи выть": {"translation": "when in Rome, do as the Romans do", "transliteration": "s volkami zhit - po-volchi vyt", "register": "proverb"},
    "глаза боятся, а руки делают": {"translation": "it looks hard but it's doable", "transliteration": "glaza boyatsya, a ruki delayut", "register": "proverb"},
    "дарёному коню в зубы не смотрят": {"translation": "don't look a gift horse in the mouth", "transliteration": "daryonomu konyu v zuby ne smotryat", "register": "proverb"},
    "цыплят по осени считают": {"translation": "don't count your chickens before they hatch", "transliteration": "tsyplyat po oseni schitayut", "register": "proverb"},
    "за двумя зайцами погонишься": {"translation": "if you chase two rabbits, you won't catch either", "transliteration": "za dvumya zaytsami pogonishsya", "register": "proverb"},
    "мой дом - моя крепость": {"translation": "a man's home is his castle", "transliteration": "moy dom - moya krepost", "register": "proverb"},
    "любишь кататься - люби и саночки возить": {"translation": "you've made your bed, now lie in it", "transliteration": "lyubish katatsya - lyubi i sanochki vozit", "register": "proverb"},
    "всё хорошо, что хорошо кончается": {"translation": "all's well that ends well", "transliteration": "vsyo khorosho, chto khorosho konchaetsya", "register": "proverb"},
    "не откладывай на завтра то, что можно сделать сегодня": {"translation": "don't put off until tomorrow what you can do today", "transliteration": "ne otkladyvay na zavtra to, chto mozhno sdelat segodnya", "register": "proverb"},
}

for k, v in proverbs.items():
    if k not in ru_phrases:
        ru_phrases[k] = v
        added += 1

print(f"Added {added} proverbs")
proverb_count = added

# =============================================================================
# HOMONYMS, FALSE FRIENDS, TRUE COGNATES
# =============================================================================

linguistic = {
    # Homonyms
    "коса": {"translation": "1. braid (hair) 2. scythe 3. sandbar/spit", "transliteration": "kosa", "note": "homonym with three meanings"},
    "лук": {"translation": "1. onion 2. bow (weapon)", "transliteration": "luk", "note": "homonym"},
    "ключ": {"translation": "1. key 2. spring/source (water) 3. clef (music)", "transliteration": "klyuch", "note": "homonym"},
    "замок": {"translation": "1. lock (ZAmok) 2. castle (zamOK)", "transliteration": "zamok", "note": "homograph - different stress changes meaning"},
    "мука": {"translation": "1. flour (muKA) 2. torment (MUka)", "transliteration": "muka", "note": "homograph"},
    "пол": {"translation": "1. floor 2. sex/gender", "transliteration": "pol", "note": "homonym"},
    "мир": {"translation": "1. world 2. peace", "transliteration": "mir", "note": "homonym"},
    "свет": {"translation": "1. light 2. world/society", "transliteration": "svet", "note": "homonym"},
    "лист": {"translation": "1. leaf 2. sheet (of paper)", "transliteration": "list", "note": "homonym"},
    "среда": {"translation": "1. Wednesday 2. environment", "transliteration": "sreda", "note": "homonym"},
    "орган": {"translation": "1. organ (body) ORgan 2. organ (music) orGAN", "transliteration": "organ", "note": "homograph"},
    "атлас": {"translation": "1. atlas (maps) Atlas 2. satin (fabric) atLAS", "transliteration": "atlas", "note": "homograph"},
    
    # False friends
    "магазин": {"translation": "store/shop (NOT magazine)", "transliteration": "magazin", "note": "false friend - magazine = журнал"},
    "журнал": {"translation": "magazine, journal", "transliteration": "zhurnal"},
    "фабрика": {"translation": "factory (NOT fabric)", "transliteration": "fabrika", "note": "false friend - fabric = ткань"},
    "ткань": {"translation": "fabric, cloth", "transliteration": "tkan"},
    "симпатичный": {"translation": "attractive, good-looking (NOT sympathetic)", "transliteration": "simpatichnyy", "note": "false friend"},
    "сочувствующий": {"translation": "sympathetic", "transliteration": "sochuvstvuyushchiy"},
    "актуальный": {"translation": "current, relevant (NOT actual)", "transliteration": "aktualnyy", "note": "false friend - actual = настоящий"},
    "настоящий": {"translation": "real, actual, present", "transliteration": "nastoyashchiy"},
    "аккуратный": {"translation": "neat, tidy (NOT accurate)", "transliteration": "akkuratnyy", "note": "false friend - accurate = точный"},
    "точный": {"translation": "accurate, precise, exact", "transliteration": "tochnyy"},
    "ангина": {"translation": "tonsillitis (NOT angina)", "transliteration": "angina", "note": "false friend - angina (heart) = стенокардия"},
    "рецепт": {"translation": "recipe OR prescription", "transliteration": "retsept"},
    "бисквит": {"translation": "sponge cake (NOT biscuit)", "transliteration": "biskvit", "note": "false friend - biscuit = печенье"},
    "печенье": {"translation": "cookie, biscuit", "transliteration": "pechenye"},
    "кабинет": {"translation": "office, study room (NOT cabinet)", "transliteration": "kabinet", "note": "false friend"},
    "шкаф": {"translation": "cabinet, wardrobe", "transliteration": "shkaf"},
    "артист": {"translation": "performing artist, actor (NOT just any artist)", "transliteration": "artist", "note": "false friend - artist = художник"},
    "художник": {"translation": "artist (visual arts)", "transliteration": "khudozhnik"},
    "декада": {"translation": "period of 10 days (NOT decade)", "transliteration": "dekada", "note": "false friend - decade = десятилетие"},
    "десятилетие": {"translation": "decade (10 years)", "transliteration": "desyatiletiye"},
    
    # True cognates
    "такси": {"translation": "taxi", "transliteration": "taksi", "note": "true cognate"},
    "кофе": {"translation": "coffee", "transliteration": "kofe", "note": "true cognate - masculine gender!"},
    "телефон": {"translation": "telephone, phone", "transliteration": "telefon", "note": "true cognate"},
    "компьютер": {"translation": "computer", "transliteration": "kompyuter", "note": "true cognate"},
    "интернет": {"translation": "internet", "transliteration": "internet", "note": "true cognate"},
    "банк": {"translation": "bank", "transliteration": "bank", "note": "true cognate"},
    "ресторан": {"translation": "restaurant", "transliteration": "restoran", "note": "true cognate"},
    "музей": {"translation": "museum", "transliteration": "muzey", "note": "true cognate"},
    "театр": {"translation": "theater", "transliteration": "teatr", "note": "true cognate"},
    "проблема": {"translation": "problem", "transliteration": "problema", "note": "true cognate"},
    "система": {"translation": "system", "transliteration": "sistema"},
    "информация": {"translation": "information", "transliteration": "informatsiya"},
    "студент": {"translation": "student (university)", "transliteration": "student", "note": "true cognate - school student = ученик"},
    "ученик": {"translation": "pupil, student (school)", "transliteration": "uchenik"},
    "доктор": {"translation": "doctor", "transliteration": "doktor", "note": "true cognate"},
    "профессор": {"translation": "professor", "transliteration": "professor"},
}

for k, v in linguistic.items():
    if k not in ru_phrases:
        ru_phrases[k] = v
        added += 1

print(f"Added {added - proverb_count} linguistic entries")
ling_count = added

# =============================================================================
# CULTURAL EXPRESSIONS
# =============================================================================

cultural = {
    # Restaurant
    "можно меню": {"translation": "may I have a menu", "transliteration": "mozhno menyu", "category": "restaurant"},
    "счёт, пожалуйста": {"translation": "the check, please", "transliteration": "schyot, pozhaluysta", "category": "restaurant"},
    "что вы рекомендуете": {"translation": "what do you recommend", "transliteration": "chto vy rekomenduete", "category": "restaurant"},
    "мне это, пожалуйста": {"translation": "I'll have this, please", "transliteration": "mne eto, pozhaluysta", "category": "restaurant"},
    "приятного аппетита": {"translation": "bon appetit / enjoy your meal", "transliteration": "priyatnogo appetita"},
    "за ваше здоровье": {"translation": "to your health (toast)", "transliteration": "za vashe zdorovye", "category": "dining"},
    "на здоровье": {"translation": "you're welcome (response to thanks)", "transliteration": "na zdorovye"},
    
    # Shopping
    "сколько это стоит": {"translation": "how much does this cost", "transliteration": "skolko eto stoit", "category": "shopping"},
    "где касса": {"translation": "where is the checkout/register", "transliteration": "gde kassa", "category": "shopping"},
    "можно примерить": {"translation": "can I try this on", "transliteration": "mozhno primerit", "category": "shopping"},
    "есть другой размер": {"translation": "do you have another size", "transliteration": "yest drugoy razmer", "category": "shopping"},
    "есть скидки": {"translation": "are there any discounts", "transliteration": "yest skidki", "category": "shopping"},
    
    # Transport
    "остановите здесь": {"translation": "stop here, please", "transliteration": "ostanovite zdes", "category": "transport"},
    "как добраться до": {"translation": "how do I get to", "transliteration": "kak dobratsya do", "category": "transport"},
    "какая следующая остановка": {"translation": "what's the next stop", "transliteration": "kakaya sleduyushchaya ostanovka", "category": "transport"},
    "где ближайшая станция метро": {"translation": "where is the nearest metro station", "transliteration": "gde blizhayshaya stantsiya metro", "category": "transport"},
    
    # Emergency
    "помогите": {"translation": "help!", "transliteration": "pomogite", "register": "urgent", "category": "emergency"},
    "вызовите скорую": {"translation": "call an ambulance", "transliteration": "vyzovite skoruyu", "register": "urgent", "category": "emergency"},
    "вызовите полицию": {"translation": "call the police", "transliteration": "vyzovite politsiyu", "register": "urgent", "category": "emergency"},
    "где больница": {"translation": "where is the hospital", "transliteration": "gde bolnitsa", "category": "emergency"},
    "мне плохо": {"translation": "I feel sick / I'm not well", "transliteration": "mne plokho", "category": "health"},
    "где туалет": {"translation": "where is the toilet/bathroom", "transliteration": "gde tualet", "category": "essential"},
    "где аптека": {"translation": "where is the pharmacy", "transliteration": "gde apteka", "category": "health"},
    
    # Social
    "очень приятно": {"translation": "nice to meet you", "transliteration": "ochen priyatno"},
    "как вас зовут": {"translation": "what is your name (formal)", "transliteration": "kak vas zovut"},
    "как тебя зовут": {"translation": "what is your name (informal)", "transliteration": "kak tebya zovut"},
    "меня зовут": {"translation": "my name is", "transliteration": "menya zovut"},
    "откуда вы": {"translation": "where are you from (formal)", "transliteration": "otkuda vy"},
    "откуда ты": {"translation": "where are you from (informal)", "transliteration": "otkuda ty"},
    "я из": {"translation": "I am from", "transliteration": "ya iz"},
    "я не понимаю": {"translation": "I don't understand", "transliteration": "ya ne ponimayu"},
    "повторите, пожалуйста": {"translation": "please repeat", "transliteration": "povtorite, pozhaluysta"},
    "говорите медленнее": {"translation": "speak slower, please", "transliteration": "govorite medlenneye"},
    "вы говорите по-английски": {"translation": "do you speak English (formal)", "transliteration": "vy govorite po-angliyski"},
    "я немного говорю по-русски": {"translation": "I speak a little Russian", "transliteration": "ya nemnogo govoryu po-russki"},
}

for k, v in cultural.items():
    if k not in ru_phrases:
        ru_phrases[k] = v
        added += 1

print(f"Added {added - ling_count} cultural expressions")
cultural_count = added

# =============================================================================
# DIMINUTIVES & AUGMENTATIVES
# =============================================================================

diminutives = {
    "домик": {"translation": "little house", "transliteration": "domik", "base": "дом", "note": "diminutive"},
    "столик": {"translation": "little table", "transliteration": "stolik", "base": "стол", "note": "diminutive"},
    "котик": {"translation": "kitty", "transliteration": "kotik", "base": "кот", "note": "diminutive, affectionate"},
    "собачка": {"translation": "doggy", "transliteration": "sobachka", "base": "собака", "note": "diminutive"},
    "мамочка": {"translation": "mommy", "transliteration": "mamochka", "base": "мама", "note": "diminutive, affectionate"},
    "папочка": {"translation": "daddy", "transliteration": "papochka", "base": "папа", "note": "diminutive, affectionate"},
    "бабушка": {"translation": "grandma", "transliteration": "babushka", "note": "already diminutive form"},
    "дедушка": {"translation": "grandpa", "transliteration": "dedushka", "note": "already diminutive form"},
    "сынок": {"translation": "sonny, little son", "transliteration": "synok", "base": "сын", "note": "diminutive"},
    "дочка": {"translation": "daughter (affectionate)", "transliteration": "dochka", "base": "дочь", "note": "diminutive"},
    "девочка": {"translation": "little girl", "transliteration": "devochka", "note": "diminutive"},
    "мальчик": {"translation": "little boy", "transliteration": "malchik", "note": "diminutive"},
    "водичка": {"translation": "water (affectionate/baby talk)", "transliteration": "vodichka", "base": "вода", "note": "diminutive"},
    "хлебушек": {"translation": "bread (affectionate)", "transliteration": "khlebushek", "base": "хлеб", "note": "diminutive"},
    "солнышко": {"translation": "little sun, sweetheart", "transliteration": "solnyshko", "base": "солнце", "note": "diminutive, term of endearment"},
    "зайчик": {"translation": "bunny, darling", "transliteration": "zaychik", "base": "заяц", "note": "diminutive, term of endearment"},
    "звёздочка": {"translation": "little star, darling", "transliteration": "zvyozdochka", "base": "звезда", "note": "diminutive, term of endearment"},
    "минуточка": {"translation": "just a moment", "transliteration": "minutochka", "base": "минута", "note": "diminutive, softener"},
    "секундочка": {"translation": "just a second", "transliteration": "sekundochka", "base": "секунда", "note": "diminutive, softener"},
    
    # Augmentatives
    "домище": {"translation": "huge house", "transliteration": "domishche", "base": "дом", "note": "augmentative"},
    "ручища": {"translation": "huge hand", "transliteration": "ruchishcha", "base": "рука", "note": "augmentative"},
    "волчище": {"translation": "huge wolf", "transliteration": "volchishche", "base": "волк", "note": "augmentative"},
}

for k, v in diminutives.items():
    if k not in ru_phrases:
        ru_phrases[k] = v
        added += 1

print(f"Added {added - cultural_count} diminutives/augmentatives")
dim_count = added

# =============================================================================
# PARTICLES & INTERJECTIONS
# =============================================================================

particles = {
    "ну": {"translation": "well, so, come on", "transliteration": "nu", "note": "particle - various contextual meanings"},
    "же": {"translation": "emphasis particle (after all, really)", "transliteration": "zhe", "note": "adds emphasis to previous word"},
    "ведь": {"translation": "after all, you know", "transliteration": "ved", "note": "explanatory particle"},
    "вот": {"translation": "here is, there is, that's it", "transliteration": "vot", "note": "demonstrative particle"},
    "вон": {"translation": "there (pointing)", "transliteration": "von", "note": "demonstrative particle"},
    "так": {"translation": "so, thus, like this", "transliteration": "tak", "note": "particle/adverb"},
    "уже": {"translation": "already", "transliteration": "uzhe"},
    "ещё": {"translation": "still, yet, more", "transliteration": "yeshchyo"},
    "даже": {"translation": "even", "transliteration": "dazhe"},
    "только": {"translation": "only, just", "transliteration": "tolko"},
    "именно": {"translation": "exactly, precisely", "transliteration": "imenno"},
    "как раз": {"translation": "exactly, just right", "transliteration": "kak raz"},
    
    # Interjections
    "ах": {"translation": "ah!", "transliteration": "akh", "note": "interjection - surprise, delight, disappointment"},
    "ох": {"translation": "oh!", "transliteration": "okh", "note": "interjection - pain, fatigue, disappointment"},
    "ух": {"translation": "whew! phew!", "transliteration": "ukh", "note": "interjection - relief, amazement"},
    "эх": {"translation": "oh well, alas", "transliteration": "ekh", "note": "interjection - regret, resignation"},
    "ой": {"translation": "oops! oh!", "transliteration": "oy", "note": "interjection - surprise, pain"},
    "ай": {"translation": "ouch! oh!", "transliteration": "ay", "note": "interjection - pain, surprise"},
    "увы": {"translation": "alas", "transliteration": "uvy", "note": "interjection - regret"},
    "ура": {"translation": "hooray!", "transliteration": "ura", "note": "interjection - joy, celebration"},
    "тьфу": {"translation": "ugh! yuck!", "transliteration": "tfu", "note": "interjection - disgust"},
    "фу": {"translation": "yuck! ew!", "transliteration": "fu", "note": "interjection - disgust"},
    "брр": {"translation": "brrr!", "transliteration": "brr", "note": "interjection - cold"},
    "тс": {"translation": "shh!", "transliteration": "ts", "note": "interjection - calling for silence"},
    "эй": {"translation": "hey!", "transliteration": "ey", "note": "interjection - getting attention"},
    "алло": {"translation": "hello (on phone)", "transliteration": "allo", "note": "phone greeting only"},
}

for k, v in particles.items():
    if k not in ru_phrases:
        ru_phrases[k] = v
        added += 1

print(f"Added {added - dim_count} particles/interjections")
particle_count = added

# =============================================================================
# FORMAL VS INFORMAL PAIRS
# =============================================================================

formal_informal = {
    "здравствуйте": {"translation": "hello (formal/plural)", "transliteration": "zdravstvuyte", "register": "formal", "informal": "привет"},
    "до свидания": {"translation": "goodbye (formal)", "transliteration": "do svidaniya", "register": "formal", "informal": "пока"},
    "пока": {"translation": "bye (informal)", "transliteration": "poka", "register": "informal"},
    "извините": {"translation": "excuse me / sorry (formal)", "transliteration": "izvinite", "register": "formal"},
    "извини": {"translation": "sorry (informal)", "transliteration": "izvini", "register": "informal"},
    "простите": {"translation": "forgive me / pardon (formal)", "transliteration": "prostite", "register": "formal"},
    "прости": {"translation": "forgive me (informal)", "transliteration": "prosti", "register": "informal"},
    "благодарю": {"translation": "thank you (formal)", "transliteration": "blagodaryu", "register": "formal"},
    "спасибо": {"translation": "thank you (standard)", "transliteration": "spasibo"},
    "пожалуйста": {"translation": "please / you're welcome", "transliteration": "pozhaluysta"},
    "будьте добры": {"translation": "would you be so kind (very formal)", "transliteration": "budte dobry", "register": "formal"},
    "не за что": {"translation": "you're welcome / don't mention it", "transliteration": "ne za chto"},
}

for k, v in formal_informal.items():
    if k not in ru_phrases:
        ru_phrases[k] = v
        added += 1

print(f"Added {added - particle_count} formal/informal pairs")
formal_count = added

# =============================================================================
# NUMBERS & TIME EXPRESSIONS
# =============================================================================

numbers_time = {
    "ноль": {"translation": "zero", "transliteration": "nol"},
    "один": {"translation": "one", "transliteration": "odin"},
    "два": {"translation": "two", "transliteration": "dva"},
    "три": {"translation": "three", "transliteration": "tri"},
    "четыре": {"translation": "four", "transliteration": "chetyre"},
    "пять": {"translation": "five", "transliteration": "pyat"},
    "шесть": {"translation": "six", "transliteration": "shest"},
    "семь": {"translation": "seven", "transliteration": "sem"},
    "восемь": {"translation": "eight", "transliteration": "vosem"},
    "девять": {"translation": "nine", "transliteration": "devyat"},
    "десять": {"translation": "ten", "transliteration": "desyat"},
    "сто": {"translation": "hundred", "transliteration": "sto"},
    "тысяча": {"translation": "thousand", "transliteration": "tysyacha"},
    "миллион": {"translation": "million", "transliteration": "million"},
    
    # Time
    "сейчас": {"translation": "now", "transliteration": "seychas"},
    "сегодня": {"translation": "today", "transliteration": "segodnya"},
    "вчера": {"translation": "yesterday", "transliteration": "vchera"},
    "завтра": {"translation": "tomorrow", "transliteration": "zavtra"},
    "позавчера": {"translation": "day before yesterday", "transliteration": "pozavchera"},
    "послезавтра": {"translation": "day after tomorrow", "transliteration": "poslezavtra"},
    "утром": {"translation": "in the morning", "transliteration": "utrom"},
    "днём": {"translation": "in the afternoon", "transliteration": "dnyom"},
    "вечером": {"translation": "in the evening", "transliteration": "vecherom"},
    "ночью": {"translation": "at night", "transliteration": "nochyu"},
    "который час": {"translation": "what time is it", "transliteration": "kotoryy chas"},
    "полчаса": {"translation": "half an hour", "transliteration": "polchasa"},
    
    # Days
    "понедельник": {"translation": "Monday", "transliteration": "ponedelnik"},
    "вторник": {"translation": "Tuesday", "transliteration": "vtornik"},
    "среда": {"translation": "Wednesday", "transliteration": "sreda"},
    "четверг": {"translation": "Thursday", "transliteration": "chetverg"},
    "пятница": {"translation": "Friday", "transliteration": "pyatnitsa"},
    "суббота": {"translation": "Saturday", "transliteration": "subbota"},
    "воскресенье": {"translation": "Sunday", "transliteration": "voskresenye"},
}

for k, v in numbers_time.items():
    if k not in ru_phrases:
        ru_phrases[k] = v
        added += 1

print(f"Added {added - formal_count} numbers/time expressions")
numbers_count = added

# =============================================================================
# MAT (PROFANITY) - COMPREHENSIVE SECTION
# =============================================================================

mat = {
    # Core mat words
    "блядь": {"translation": "whore, slut", "transliteration": "blyad", "register": "vulgar/mat", "note": "one of the core mat words"},
    "блять": {"translation": "fuck! damn!", "transliteration": "blyat", "register": "vulgar/mat", "note": "exclamation form, extremely common"},
    "хуй": {"translation": "dick, cock", "transliteration": "khuy", "register": "vulgar/mat", "note": "one of the core mat words"},
    "пизда": {"translation": "cunt", "transliteration": "pizda", "register": "vulgar/mat", "note": "one of the core mat words"},
    "ебать": {"translation": "to fuck", "transliteration": "yebat", "register": "vulgar/mat", "note": "core mat verb"},
    "сука": {"translation": "bitch", "transliteration": "suka", "register": "vulgar", "note": "literally: female dog"},
    "мудак": {"translation": "asshole, dickhead", "transliteration": "mudak", "register": "vulgar"},
    "пиздец": {"translation": "fucked up, total mess, holy shit", "transliteration": "pizdets", "register": "vulgar/mat", "usage": "expresses something extreme (good or bad)"},
    "хуёво": {"translation": "shitty, terrible", "transliteration": "khuyovo", "register": "vulgar/mat"},
    "заебись": {"translation": "fucking great, awesome", "transliteration": "zayebis", "register": "vulgar/mat", "usage": "positive despite etymology"},
    "охуенно": {"translation": "fucking amazing", "transliteration": "okhuyenno", "register": "vulgar/mat", "usage": "emphatic positive"},
    "охуеть": {"translation": "to be fucking amazed", "transliteration": "okhuyet", "register": "vulgar/mat"},
    
    # Common mat expressions
    "иди на хуй": {"translation": "fuck off, go to hell", "transliteration": "idi na khuy", "register": "vulgar/mat"},
    "иди в пизду": {"translation": "fuck off (stronger)", "transliteration": "idi v pizdu", "register": "vulgar/mat"},
    "ёб твою мать": {"translation": "motherfucker (as exclamation)", "transliteration": "yob tvoyu mat", "register": "vulgar/mat"},
    "ёбаный в рот": {"translation": "fucking hell", "transliteration": "yobanyy v rot", "register": "vulgar/mat"},
    "до хуя": {"translation": "a shitload, a lot", "transliteration": "do khuya", "register": "vulgar/mat"},
    "ни хуя": {"translation": "nothing at all, jack shit", "transliteration": "ni khuya", "register": "vulgar/mat"},
    "ни хуя себе": {"translation": "holy shit! (surprise)", "transliteration": "ni khuya sebe", "register": "vulgar/mat"},
    "хуй знает": {"translation": "who the fuck knows", "transliteration": "khuy znayet", "register": "vulgar/mat"},
    "на хуй": {"translation": "what the fuck for, why bother", "transliteration": "na khuy", "register": "vulgar/mat"},
    "какого хуя": {"translation": "what the fuck", "transliteration": "kakogo khuya", "register": "vulgar/mat"},
    "хуйня": {"translation": "bullshit, crap, nonsense", "transliteration": "khuynya", "register": "vulgar/mat"},
    "пиздёж": {"translation": "bullshit, lies", "transliteration": "pizdyozh", "register": "vulgar/mat"},
    "пиздеть": {"translation": "to bullshit, to lie", "transliteration": "pizdet", "register": "vulgar/mat"},
    "ебало": {"translation": "face, mug (vulgar)", "transliteration": "yebalo", "register": "vulgar/mat"},
    "ебальник": {"translation": "face, mug (vulgar)", "transliteration": "yebalnik", "register": "vulgar/mat"},
    "долбоёб": {"translation": "fucking idiot", "transliteration": "dolboyob", "register": "vulgar/mat"},
    "ёбнутый": {"translation": "crazy, fucked up (person)", "transliteration": "yobnutyy", "register": "vulgar/mat"},
    "заёбанный": {"translation": "exhausted, fed up", "transliteration": "zayobannyy", "register": "vulgar/mat"},
    "выёбываться": {"translation": "to show off, to be a smartass", "transliteration": "vyyobyvatsya", "register": "vulgar/mat"},
    "отъебись": {"translation": "fuck off, leave me alone", "transliteration": "otyebis", "register": "vulgar/mat"},
    "уёбок": {"translation": "piece of shit, scumbag", "transliteration": "uyobok", "register": "vulgar/mat"},
    "уёбище": {"translation": "ugly freak, monster", "transliteration": "uyobishche", "register": "vulgar/mat"},
    
    # Softer variants / euphemisms
    "блин": {"translation": "damn! (euphemism for блядь)", "transliteration": "blin", "literal": "pancake", "register": "mild euphemism"},
    "ёлки-палки": {"translation": "darn it! (mild euphemism)", "transliteration": "yolki-palki", "register": "euphemism"},
    "ёшкин кот": {"translation": "for crying out loud", "transliteration": "yoshkin kot", "register": "euphemism"},
    "ёпрст": {"translation": "shoot! (euphemism)", "transliteration": "yoprst", "register": "euphemism"},
    "фиг": {"translation": "euphemism for хуй", "transliteration": "fig", "register": "mild"},
    "на фиг": {"translation": "to hell with it (mild)", "transliteration": "na fig", "register": "mild"},
    "иди на фиг": {"translation": "go away (mild)", "transliteration": "idi na fig", "register": "mild euphemism"},
    "офигеть": {"translation": "wow, to be amazed (euphemism for охуеть)", "transliteration": "ofiget", "register": "mild"},
    "фигня": {"translation": "crap, nonsense (mild)", "transliteration": "fignya", "register": "mild euphemism for хуйня"},
    
    # Other vulgar (non-mat) words
    "жопа": {"translation": "ass, butt", "transliteration": "zhopa", "register": "vulgar"},
    "говно": {"translation": "shit", "transliteration": "govno", "register": "vulgar"},
    "срать": {"translation": "to shit", "transliteration": "srat", "register": "vulgar"},
    "ссать": {"translation": "to piss", "transliteration": "ssat", "register": "vulgar"},
    "хер": {"translation": "dick (milder than хуй)", "transliteration": "kher", "register": "vulgar"},
    "хрен": {"translation": "1. horseradish 2. dick (euphemism)", "transliteration": "khren", "register": "mild vulgar"},
    "дерьмо": {"translation": "crap, shit", "transliteration": "derymo", "register": "vulgar"},
    "засранец": {"translation": "little shit", "transliteration": "zasranets", "register": "vulgar"},
    "придурок": {"translation": "idiot, moron", "transliteration": "pridurok", "register": "informal/rude"},
    "дебил": {"translation": "moron, idiot", "transliteration": "debil", "register": "rude"},
    "идиот": {"translation": "idiot", "transliteration": "idiot", "register": "rude"},
    "дурак": {"translation": "fool, idiot", "transliteration": "durak", "register": "informal"},
    "дура": {"translation": "fool, idiot (female)", "transliteration": "dura", "register": "informal"},
    "козёл": {"translation": "bastard, jerk", "transliteration": "kozyol", "literal": "goat", "register": "rude"},
    "урод": {"translation": "freak, ugly person", "transliteration": "urod", "register": "rude"},
}

for k, v in mat.items():
    if k not in ru_phrases:
        ru_phrases[k] = v
        added += 1

print(f"Added {added - numbers_count} mat/profanity entries")

# =============================================================================
# SAVE
# =============================================================================

save_json("ru_phrases.json", ru_phrases)
print(f"\n=== SUMMARY ===")
print(f"Total new entries added: {added}")
print(f"Total entries in file: {len(ru_phrases)}")
