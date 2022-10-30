import random
import itertools
import os

# This program play the game 'Hangman'

MAX_TRIES=6


# The seven states of the hanging man
HANGMAN_PHOTOS={1:"x-------x",2:'''x-------x
|
|
|
|
|
    ''',3:'''x-------x
|       |
|       0
|
|
|
    ''',4:'''x-------x
|       |
|       0
|       |
|
|
    ''',5:'''x-------x
|       |
|       0
|      /|\ 
|       
|
    ''',6:'''x-------x
|       |
|       0
|      /|\ 
|      / 
|
    ''',7:'''x-------x
|       |
|       0
|      /|\ 
|      / \ 
|
    '''}

def welcom():
    global MAX_TRIES

    HANGMAN_ASCII_ART="""Welcom to the game Hangman\n
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/"""

    print(HANGMAN_ASCII_ART,"\n","\nMax Tries:\n" ,MAX_TRIES)

def guess_letter():
    char=input("Guess a letter:")
    return char

def game_board(word):
    print('_ '*len(word))

def show_hidden_word(secret_word, old_letters_guessed):
    """
    This function shows to the user his progress in the game
    :param secret_word: represents the secret word that user needs to guess
    :type secret_word: str
    :param old_letters_guessed: letter guessed so far
    :type  old_letters_guessed: list
    :return: string consist from guessed letters and underscors
    :rtype: str
    """
    for letter in old_letters_guessed:
        letter=letter.lower()
    show=''
    for ch in secret_word:
        if ch in old_letters_guessed:
            show+=ch
            show+=' '
        else:
            show+='_'
            show+=' '
    return show

def check_win(secret_word, old_letters_guessed):
    """
    This function check if the user won the game
    :param secret_word: represents the secret word that user needs to guess
    :type secret_word: str
    :param old_letters_guessed: letter guessed so far
    :type  old_letters_guessed: list
    :return: True if all the letters of the secret word are in the list. else, false
    :rtype: bool
    """
    flag=True
    for ch in secret_word:
        if ch in old_letters_guessed:
            continue
        else:
            flag=False
            break
    return flag

def print_hangman(num_of_tries):
    """
    This function Print each time one of the pictures of the situation of the hanging man,
    depending on the number of wrong guesses the player guessed.
    :param num_of_tries: represents the number of failed attempts by the user so far
    :type num_of_tries: int
    :return: print one of the pictures
    :rtype: None
    """
    print(HANGMAN_PHOTOS[num_of_tries+1])


def choose_word(file_path, index):
    '''
    This function choose the secret word from a file with seperates words
    :param file_path: string path to the file
    :param index: index of word in the file
    :return: tuple: ( num of different words in the file, word in the given index
    as the secret word)
    '''
    if not os.path.isfile(file_path):
        print("File not exsist")
        exit()
    with open(file_path,'r') as f:
        words_lists=f.read().split("\n")
    words=[]
    for lst in words_lists:
        words.append(lst.split(" "))
    words=list(itertools.chain.from_iterable(words))

    uniqe_count={}
    for word in words:
        uniqe_count[word]=""

    uniques=len(uniqe_count.keys())

    if index>len(words):
        index=index-len(words)

    word_index=words[index-1]

    return word_index


def check_valid_input(letter_guessed, old_letters_guessed):
    """
    This function check the propriety of the user`s string as input.
    :param letter_guessed: represents the input string from user
    :type letter_guessed: str
    :param old_letters_guessed: represents the input strings from user so far
    :type old_letters_guessed: list
    :return: true if the input consist of one alphabetical and never guessed it before
    :rtype: boolean
    """

    #convert everythin to lowercase for comparison
    letter_guessed=letter_guessed.lower()
    old_letters_guessed=[x.lower() for x in old_letters_guessed]

    if len(letter_guessed)>=2 or letter_guessed.isalpha()==False or\
    letter_guessed in old_letters_guessed: return False

    if len(letter_guessed) == 1 and letter_guessed.isalpha() == True\
        and not letter_guessed in old_letters_guessed:return True

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    This function add the new input guess to the 'old_letters_guessed' list
    or print message that it is not possible to add it.
    :param: letter_guessed: represents the input char from user
    :type letter_guessed: str
    :param old_letters_guessed: represents the input strings guesses from user so far
    :type old_letters_guessed: list
    :return:
    :rtype:
    """
    old_letters_guessed = [x.lower() for x in old_letters_guessed]
    old_letters_guessed.sort()

    if check_valid_input(letter_guessed,old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return old_letters_guessed ,True # The addition was successful
    else:
        print('X')
        print('Guessed letters:')
        print('->'.join(old_letters_guessed))
        return old_letters_guessed ,False
def main():
    old_letters_guessed=[]
    num_of_tries=0 # number of failed attempts

    welcom()
    file_path=input("Please enter file path: ")
    index=int(input("Please enter index: "))

    print("Let's start!")
    print_hangman(0)
    word=choose_word(file_path,index)
    game_board(word)
    lose=False

    while not check_win(word, old_letters_guessed):
        letter = guess_letter().lower()
        old_letters_guessed,flag = try_update_letter_guessed(letter, old_letters_guessed)
        if flag:
            if letter.lower() not in word:
                num_of_tries+=1
                print(':(\n')
                print_hangman(num_of_tries)
                if num_of_tries>=MAX_TRIES:
                    print('LOSE :(')
                    lose=True
                    break
            else:
                print(show_hidden_word(word,old_letters_guessed))
    if not lose:
        print("WIN! :)")


if __name__ == '__main__':
    main()
