# Előre is elnézést de semmiféle tervezés nem előzte meg ennek a kódnak a megírását
# mivel 1. szerintem nem tudok tervezni 2. ha véletlenül terveznék 2 lépést előre
# folyton bennem van hogy mi van ha az úgy mégsem működik ezért azonnal meg kell írni
# és kipróbálni. Szóval ennek a kódnak a nagyobb része balesetek utáni kárelhárításként született 
# nehány függvény neve kicsit csalóka például a check_letters még akkor született mikor még
# nem tudtam hogy szavakat is akarok majd vizsgálni nem csak betűket. 

#  Itt beimportálok dolgokat amik később szükségesek lesznek
import os
import random
import time
import regex
from playsound import playsound
import threading


#  Létrehozok globális változókat amiket később használni fogok, lehet van rá jobb ötlet nekem ez jutott eszembe :)
specWords = ["mute", "hint", "quit", "unmute"]
lang = ""
lives = 0
difficulty = 0
word = ""
usedLetters = set()
message = ""
stage = []
hint = 0
muted = False
pics = ['''
  +---+
      |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']
introPics = [
    """ /$$   /$$
| $$  | $$
| $$  | $$
| $$$$$$$$
| $$__  $$
| $$  | $$
| $$  | $$
|__/  |__/
          
          
          """,
    """ /$$   /$$  /$$$$$$ 
| $$  | $$ /$$__  $$
| $$  | $$| $$  \ $$
| $$$$$$$$| $$$$$$$$
| $$__  $$| $$__  $$
| $$  | $$| $$  | $$
| $$  | $$| $$  | $$
|__/  |__/|__/  |__/
                    
                    
                    """,
    """ /$$   /$$  /$$$$$$  /$$   /$$
| $$  | $$ /$$__  $$| $$$ | $$
| $$  | $$| $$  \ $$| $$$$| $$
| $$$$$$$$| $$$$$$$$| $$ $$ $$
| $$__  $$| $$__  $$| $$  $$$$
| $$  | $$| $$  | $$| $$\  $$$
| $$  | $$| $$  | $$| $$ \  $$
|__/  |__/|__/  |__/|__/  \__/
                              
                              
                              """,
    """ /$$   /$$  /$$$$$$  /$$   /$$  /$$$$$$ 
| $$  | $$ /$$__  $$| $$$ | $$ /$$__  $$
| $$  | $$| $$  \ $$| $$$$| $$| $$  \__/
| $$$$$$$$| $$$$$$$$| $$ $$ $$| $$ /$$$$
| $$__  $$| $$__  $$| $$  $$$$| $$|_  $$
| $$  | $$| $$  | $$| $$\  $$$| $$  \ $$
| $$  | $$| $$  | $$| $$ \  $$|  $$$$$$/
|__/  |__/|__/  |__/|__/  \__/ \______/ 
                                        
                                        
                                        """,
    """ /$$   /$$  /$$$$$$  /$$   /$$  /$$$$$$  /$$      /$$
| $$  | $$ /$$__  $$| $$$ | $$ /$$__  $$| $$$    /$$$
| $$  | $$| $$  \ $$| $$$$| $$| $$  \__/| $$$$  /$$$$
| $$$$$$$$| $$$$$$$$| $$ $$ $$| $$ /$$$$| $$ $$/$$ $$
| $$__  $$| $$__  $$| $$  $$$$| $$|_  $$| $$  $$$| $$
| $$  | $$| $$  | $$| $$\  $$$| $$  \ $$| $$\  $ | $$
| $$  | $$| $$  | $$| $$ \  $$|  $$$$$$/| $$ \/  | $$
|__/  |__/|__/  |__/|__/  \__/ \______/ |__/     |__/
                                                     
                                                     
                                                     """,
    """ /$$   /$$  /$$$$$$  /$$   /$$  /$$$$$$  /$$      /$$  /$$$$$$ 
| $$  | $$ /$$__  $$| $$$ | $$ /$$__  $$| $$$    /$$$ /$$__  $$
| $$  | $$| $$  \ $$| $$$$| $$| $$  \__/| $$$$  /$$$$| $$  \ $$
| $$$$$$$$| $$$$$$$$| $$ $$ $$| $$ /$$$$| $$ $$/$$ $$| $$$$$$$$
| $$__  $$| $$__  $$| $$  $$$$| $$|_  $$| $$  $$$| $$| $$__  $$
| $$  | $$| $$  | $$| $$\  $$$| $$  \ $$| $$\  $ | $$| $$  | $$
| $$  | $$| $$  | $$| $$ \  $$|  $$$$$$/| $$ \/  | $$| $$  | $$
|__/  |__/|__/  |__/|__/  \__/ \______/ |__/     |__/|__/  |__/
                                                               
                                                               
 """,
    """ /$$   /$$  /$$$$$$  /$$   /$$  /$$$$$$  /$$      /$$  /$$$$$$  /$$   /$$
| $$  | $$ /$$__  $$| $$$ | $$ /$$__  $$| $$$    /$$$ /$$__  $$| $$$ | $$
| $$  | $$| $$  \ $$| $$$$| $$| $$  \__/| $$$$  /$$$$| $$  \ $$| $$$$| $$
| $$$$$$$$| $$$$$$$$| $$ $$ $$| $$ /$$$$| $$ $$/$$ $$| $$$$$$$$| $$ $$ $$
| $$__  $$| $$__  $$| $$  $$$$| $$|_  $$| $$  $$$| $$| $$__  $$| $$  $$$$
| $$  | $$| $$  | $$| $$\  $$$| $$  \ $$| $$\  $ | $$| $$  | $$| $$\  $$$
| $$  | $$| $$  | $$| $$ \  $$|  $$$$$$/| $$ \/  | $$| $$  | $$| $$ \  $$
|__/  |__/|__/  |__/|__/  \__/ \______/ |__/     |__/|__/  |__/|__/  \__/
                                                                         
                                                                         
                                                                         """]

#  Fontos az ablakpucolás


def screen_clear():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')


"""
Több nyelvből vannak szó listák így nem akartam 
hogy ha olyan betűt üt le ami abban a nyelvben nem is létezik hibának számítson
így csakk akkor hiba ha benne van a betűkészletben de nincs a szóban ehhez én 
regex-et használok talán erre is van jobb ötlet
"""


def regex_choose(argument):
    switch = {
        "en": "^[a-z]$",
        "fr": "^[a-zàâçéèêëîïôûùüÿñæœ]$",
        "es": "^[a-zÑ]$",
        "it": "^(?![KWXYJ])[a-z]$",
        "hu": "^[a-zíüóőéöúáű]$"
    }
    return switch.get(argument, "")

#  kilépés


def quit(arg):
    if arg.lower() == "quit":
        goodBye()


"""
maga a játék. erre a függvényre önmagában semmi szükség nem lenne csak nem tetszett hogy olyan hosszú lett
ezért beletettem egy game_play nevű függvénybe és itt csak meghívom.
"""


def play(word, lives):
    game_play(word, lives)

# vizsgálom hogy a beírt dolog némítással kapcsolatos-e


def mute(arg, lives):
    if arg.lower() == "mute" or arg.lower() == "unmute":

        mute_question(arg, lives)


"""
Megkérdezzük hogy némítani vagy hangosítani szeretne-e tényleg
ha igen akkor átállítjuk a kapcsolót megfelelően
ha nem akkor megkérdezzük hogy megfejteni szeretné-e
mindezt addig míg értelmes választ nem kapunk (y/n yes/no)
"""


def mute_question(arg, lives):
    screen_clear()
    print(f"""Would you like to {arg}? Yes/No""")
    answer = input()
    mute(answer, lives)
    if answer.lower() == "yes" or answer.lower() == 'y':
        globals()['muted'] = (arg < "n")

    elif answer.lower() == 'no' or answer.lower() == 'n':
        guess_question(globals()['word'], arg, lives)

    else:
        mute_question(arg, lives)


"""
Erre azért volt szükségem mert addig nem tudtam külön kezelni hogy ha
egy olyan szót írt be amit másra is használok pl.: 'hint' akkor ne rögtön
adjon segítséget hanem kérdezze meg hogy ez tipp vagy segítség kérés
"""


def check_spec_words(word, char, lives):
    if char.casefold() == "hint":
        hint_question(word, char, lives)
    elif char.lower() == "quit":
        quit_question(word, char, lives)
    elif char.lower() == "mute" or char.lower() == "unmute":
        mute(char, lives)
        game_play(word, lives)
    else:
        game_play(word, lives)


def guess_question(word, char, lives):
    screen_clear()
# ez a rész arra vonatkozik hogy ha nincsbenne mondjuk a szókészletbe amit beírt
# attól még vizsgáljuk meg hogy esetleg segítséget kért vagy egyéb dolgot pl.: némítás
    if char not in globals()['words']:         
        check_spec_words(word, char, lives)
# itt meg továbbmegyünk ha benne van a szókészletben eldöntjük hogy
# tippelni akar vagy mi folyik itt
    print(f"""Do you think '{char}' is the answer? Yes/No""")
    answer = input()
    mute(answer, lives)
    if answer.lower() == "yes" or answer.lower() == 'y':
        check_letters(word, char, lives)
    elif answer.lower() == 'no' or answer.lower() == 'n':
        check_spec_words(word, char, lives)

    else:
        guess_question(word, char, lives)



def hint_question(word, char, lives):
    screen_clear()
    print("Would you like a hint? Yes/No")
    answer = input()
    mute(answer, lives)
 # az érdekes rész itt jön ha segítséget kér akkor létrehozok egy objektumot? vagy azt hiszem itt 
 # dictonary-nek hívják nem tudom. végigjárom a szót és azokat a betűket amik nincsnek az aktuális 
 # állapotban magyarul a megtalált betűk között azokat az indexnek megfelelő nevű kulcsra teszem
 # a karakter pedig az érték lesz. ha ezzel megvagyok már csak kisorsolok egy számot 0 és a 
 # kulcsok listájának a hossza között. aztán a kulcs változónak átadom a kulcsok listáját mert valamiért
 # nem tudtam rögtön listaként kezelni és ez jutott eszembe hirtelen. Aztán elkérem a kisorsolt kulcs nevét
 # aztán pedig a megfelelő értéket (karaktert/betűt) aztán már csak megnézem benne van-e a szóban és 
 # ha benne van akkor beteszem a megfelelő helyre. Mivel onnan vettem ki ezért benne kell lennie ha nincs
 # az baj és szomorú helyzet 
  
    if answer.lower() == "yes" or answer.lower() == 'y':
        hat = {}
        for index, letter in enumerate(word):
            if letter.casefold() not in globals()['stage']:
                hat[index] = letter

        randNum = random.randint(0, len(hat.keys())-1)
        key = list(hat.keys())
        key = key[randNum]
        char = hat[key]

        globals()['hint'] += 1
        check_letters(word, char, lives)
    elif answer.lower() == 'no' or answer.lower() == 'n':
        game_play(word, lives)
    else:
        hint_question(word, char, lives)


def quit_question(word, char, lives):
    screen_clear()
    print("Would you like to quit? Yes/No")
    answer = input()
    mute(answer, lives)
    if answer.lower() == "yes" or answer.lower() == 'y':
        goodBye()
    elif answer.lower() == 'no' or answer.lower() == 'n':
        game_play(word, lives)
    else:
        mute(char, lives)
        quit_question(word, char, lives)


def game_play(word, lives):
    # kiválasztom a megfelelő regex-et és elkérem az akasztófa képeket
    reg = regex_choose(globals()['lang'])
    pics = globals()['pics']
# ha nincs még jelenlegi állapot akkor készítűnk egy szó hosszúságú listát  "_"-ból
    if not globals()['stage']:
        for char in word:
            if char != ' ':
                globals()['stage'].append('_')
            else:
                globals()['stage'].append(' ')

# ha már nincs benne aláhúzás akkor megvan minden betű tehát nyert
    if "_" not in globals()['stage']:
        end_screen("win")
# ha van még mit kitalálni akkor kiírja az üzenetet ha van pl.: 'ez a betű már megvan' 'ezeket már felhasználtad'
    else:
        screen_clear()

        print(message)
# itt összefűzöm az aktuálís allapotot szóközökkel és kiírom a képernyőre az aktuális akasztófaképpel együtt
        print(f"""
  
  {" ".join(globals()['stage'])}
  {pics[len(pics)-lives-1]}""")
        print("Please give me a guess!")
        char = input()
# lehet csalni
        if char.upper() == "I am a hacker!".upper():
            end_screen("win")
# ha csak egy karakter és benne van betűkjészletben akkor vizsgálja hogy benne van-e a szóban		
        elif regex.findall(reg, char, regex.IGNORECASE):
            check_letters(word, char, lives)
# ha benne van a szókészletben vagy a speciális szavak között van akkor jön a kérdés h rákérdez vagy csak valami 
# segítséget akar vagy némítást ilyesmi
        elif char in globals()['words'] or char in globals()['specWords']:
            guess_question(word, char, lives)
# ha semmi ilyesmi akkor ugyanott folytatódik a játék
        else:
            play(word, lives)


def check_letters(word, char, lives):
    success = './sounds/success.wav'
    fail = './sounds/fail.wav'
# ha rákérdezett és eltalálta akkor nyert
    if word.lower() == char.lower():
        end_screen("win")
# ha benne van a szóban és csak egyetlen karakter akkor végig megy a szavon
# és a megfelelő indexekre beteszi a karaktert az aktuális állapot listájába
    if char.casefold() in word and len(char) == 1:
        for i, item in enumerate(word):

            if char.casefold() == item.casefold():
                globals()['stage'][i] = word[i]
# ha nincs benne a használt karakterekben akkor beleteszi 
# nem üzen semmit lejátszik egy kis csilingelés egy másik szálon
#  hogy itt tudjon tovább futni
# persze csak ha nincs némítva
# és a játék folytatódik
        if char.upper() not in usedLetters:

            usedLetters.add(char.upper())
            globals()['message'] = ""
            if not globals()['muted']:
                threading.Thread(target=playsound, args=(
                    success,), daemon=True).start()

            play(word, lives)
# ha benne van a használt karakterek listájában akkor 
# lejátszik egy hangot az üzenetet beállítja arra hogy már megtalálta korábban
        else:
            if not globals()['muted']:
                threading.Thread(target=playsound, args=(
                    fail,), daemon=True).start()
            if len(char) == 1:
                
                globals()['message'] = "You have already found "+char.upper()
                play(word, lives)
# ha nincs benne a szóban a karakter és nem az utolsó élete van akkor
# az üzenet a már használt betűk lesznek az élet csökken ha nincs a használtak közt 
# ha nincs a használtak közt akkor még beleteszi
# és megy tovább a játék
# ha ez volt az utolsó élete akkor jön a vesztet képernyő
    else:

        globals()['message'] = 'You have already used: "' + \
            " ".join(sorted(usedLetters))+'" I hope it helps!'
        if char.upper() in usedLetters:
            if not globals()['muted']:
                threading.Thread(target=playsound, args=(
                    fail,), daemon=True).start()

            play(word, lives)
        else:
            if not globals()['muted']:
                threading.Thread(target=playsound, args=(
                    fail,), daemon=True).start()
            lives = lives-1
            if lives == 0:
                end_screen("lose")
    
            if len(char) == 1:
                globals()['usedLetters'].add(char.upper())
            globals()['message'] = 'You have already used: "' + \
                " ".join(sorted(usedLetters))+'" I hope it helps!'
            play(word, lives)
    
        
def difficulty_choose(argument):
    switch = {
        "1": 7,
        "2": 5,
        "3": 3,

    }
    return switch.get(argument, "")


def read_words(lang):
    f = open(f"""./lang/{lang}.txt""", "r")
    return f.read().splitlines()


def game_start():
    screen_clear()

    globals()["usedLetters"] = set()
    globals()['stage'] = []
    globals()['message'] = ""
    globals()['hint'] = 0
    lives = globals()['lives']
    lives = 0
    globals()['difficulty'] = 0
    globals()['muted'] = False
    globals()['pickedWord'] = ""

    globals()['lang'] = ""
    for pic in introPics:
        screen_clear()
        print(pic)
        time.sleep(0.4)

    time.sleep(1)
    while not globals()['lang']:
        screen_clear()
        print("""Please select a language! Type:
          
	  en for   English
	  hu for   Hungarian
	  it for   Italian
	  fr for   French
          es for   Spanish


    Or if you changed your mind, type "quit"
 """)
        lang = input()
        mute(lang, lives)
        quit(lang)
        if lang.lower() == 'en' or lang.lower() == 'it' or lang.lower() == 'fr' or lang.lower() == 'es' or lang.lower() == 'hu':
            globals()['lang'] = lang.lower()
            globals()['words'] = read_words(globals()['lang'])

    while not lives:
        screen_clear()
        print("""Please select a difficulty press:
          
	  1 for EASY (7 lives)
	  2 for MODERATE (5 lives)
	  3 for HARD (3 lives)
 
    Or if you changed your mind, type "quit"
 """)
        difficulty = input()
        mute(difficulty, lives)
        quit(difficulty)
        lives = difficulty_choose(difficulty)

    pickedWord = globals()['words'][random.randint(
        0, len(globals()['words'])-1)]
    globals()['word'] = pickedWord

    game_play(pickedWord, lives)


def goodBye():
    screen_clear()
    goodbye = './sounds/goodbye.wav'
    print("""  /$$$$$$                            /$$ /$$                          
 /$$__  $$                          | $$| $$                          
| $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$$| $$$$$$$  /$$   /$$  /$$$$$$ 
| $$ /$$$$ /$$__  $$ /$$__  $$ /$$__  $$| $$__  $$| $$  | $$ /$$__  $$
| $$|_  $$| $$  \ $$| $$  \ $$| $$  | $$| $$  \ $$| $$  | $$| $$$$$$$$
| $$  \ $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$_____/
|  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$$| $$$$$$$/|  $$$$$$$|  $$$$$$$
 \______/  \______/  \______/  \_______/|_______/  \____  $$ \_______/
                                                   /$$  | $$          
                                                  |  $$$$$$/          
                                                   \______/           """)
    if not globals()['muted']:
        playsound(goodbye)
    exit()


def win():
    screen_clear()
    applause = './sounds/applause.wav'
    if not globals()['muted']:
        threading.Thread(target=playsound, args=(
            applause,), daemon=True).start()
    print(f"""You found the answer which is: {globals()['word']}
	 
	 """)
    print(""" /$$     /$$                        /$$      /$$ /$$           /$$
|  $$   /$$/                       | $$  /$ | $$|__/          | $$
 \  $$ /$$//$$$$$$  /$$   /$$      | $$ /$$$| $$ /$$ /$$$$$$$ | $$
  \  $$$$//$$__  $$| $$  | $$      | $$/$$ $$ $$| $$| $$__  $$| $$
   \  $$/| $$  \ $$| $$  | $$      | $$$$_  $$$$| $$| $$  \ $$|__/
    | $$ | $$  | $$| $$  | $$      | $$$/ \  $$$| $$| $$  | $$    
    | $$ |  $$$$$$/|  $$$$$$/      | $$/   \  $$| $$| $$  | $$ /$$
    |__/  \______/  \______/       |__/     \__/|__/|__/  |__/|__/
                                                                   """)
    if globals()['hint'] >= (len(list(globals()['word']))-1)/2:
        print("""But I helped a lot! You have to admit!
	   
	   """)
    print("Would you like to play again? Yes/No")
    answer = input()
    mute(answer, lives)
    if answer.lower() == "yes" or answer.lower() == 'y':
        game_start()
    elif answer.casefold() == 'no' or answer.lower() == 'n':
        goodBye()
    else:
        win()


def game_over():
    screen_clear()

    print(f"""Game Over
            The answer was: {globals()['word']}
   """)
    print(pics[7])
    print("Would you like to play again? Yes/No")
    answer = input()
    mute(answer, lives)
    if answer.lower() == "yes" or answer.lower() == 'y':
        game_start()
    elif answer.lower() == 'no' or answer.lower() == 'n':
        goodBye()
    else:
        game_over()


def end_screen(score):
    if score == "win":
        win()

    else:
        game_over()
		
def main():
    game_start()

if __name__=='__main__':
    main()
