# 
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
name=raw_input("Please enter your name: ")
SCRABBLE_LETTER_VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}

WORDLIST_FILENAME = "words.txt"

#loading words
def loadWords():
    """Returns a list of valid words. Words are strings of lowercase letters."""
    
    print ''
    print "Hi " +name +", welcome to the Word Game !!"
    print " "
    print "Loading word list from dictionary. Word list updated: 2013"
    
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print len(wordList), "words loaded."
    return wordList

#checking frequency of an element
def getFrequencyDict(sequence):
    """Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary"""

    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

#Scoring a word
def getWordScore(word, n):
    """Returns the score for a word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    word: string (lowercase letters)
    n: integer
    returns: int >= 0"""

    score=0
    for i in word:
        if i in SCRABBLE_LETTER_VALUES:
            score+=SCRABBLE_LETTER_VALUES[i]
            
    score=score*len(word)
    if len(word)==n:
        score+=50
        return score
    else:
        return score

# display the hand
def displayHand(hand):
    """ Displays the letters currently in the hand.

    For example:displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e

    hand: dictionary (string -> int)"""
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line

#deal new hand
def dealHand(n):
    """Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are letters and the values are the number of times the 
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)"""
    hand={}
    numVowels = n / 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#Update a hand by removing letters
def updateHand(hand, word):
    """uses up the letters in the given word
    and returns the new hand, without those letters in it.

    does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)"""

    hand1 = hand.copy()
    for i in word:
        if i in hand1:
            if hand1[i]>0:
               hand1[i]-=1
    return hand1

#Test word validity
def isValidWord(word, hand, wordList):
    """Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings"""
 
    check=0
    hand1=hand.copy()
    for i in word:
        if i in hand1:
            check+=1
            if hand1[i]>0:
                hand1[i]-=1
            else:
                break
        else:
            break
     
    if check==len(word):
        if word in wordList:
            return True
        else:
            return False
        
    else:
        return False

#Playing a hand
def calculateHandlen(hand):
    """Returns number of letters in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer"""
    
    count =0
    for i in hand:
        count+=hand[i]
    return count

#play the hand
def playHand(hand, wordList, n):
    """Allows the user to play the given hand
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE)"""

    Tscore=0
    Uhand=hand.copy()
    wordcountself=0
    while calculateHandlen(Uhand)>0:
        print ''
        print'Current Hand: ',
        displayHand(Uhand)
        word=raw_input('ENTER WORD, OR "." TO INDICATE THAT YOU ARE FINISHED: ')
        
        if word=='.':
            
            print 'Goodbye ' + name+ '!'
            print 'Total score: ', str(Tscore), 'points.'
            print 'Number of words: ' +str(wordcountself)
          
            break
        
        elif isValidWord(word, hand, wordList)==False:
            print 'Invalid word, please try again.'
            print ''
        
        else:
            wordcountself+=1
            Tscore+=getWordScore(word, n)
            print '"'+word+'"'+ ' earned '+ str(getWordScore(word, n))+' points. Total: '+ str(Tscore)+' points'
            Uhand=updateHand(Uhand, word)
    else:
        print ''
        print name+ ',' + ' you have run out of letters.'
        print 'Total score: '+ str(Tscore)
        print 'Number of words: ' +str(wordcountself)


# Computer chooses a word
def compChooseWord(hand, wordList, n):
    """Given a hand and a wordList, find the word that gives 
    the maximum value score, and return it.

    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)

    returns: string or None"""
    
    maxscore=0
    
    bestword=None
    
    for word in wordList:
        wordcount=0
        if isValidWord(word, hand, wordList):
             for  letter in word:
                 if letter in hand.keys():
                     wordcount+=1
             if wordcount==len(word):
                 if getWordScore(word, n)>maxscore:
                     maxscore=getWordScore(word, n)
                     bestword=word
    return bestword        

# Computer plays a hand
def compPlayHand(hand, wordList, n):
    """Allows the computer to play the given hand,the computer 
    chooses the words.
    1)After every valid word: the word and the score for that word is 
    displayed, the remaining letters in the hand are displayed, and the 
    computer chooses another word.
    
    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE)"""
    
    Tscore=0
    Uhand=hand.copy()
    wordcountcomp=0
    while calculateHandlen(Uhand)>0:
        print ''
        print'Current Hand: ',
        displayHand(Uhand)
        word=compChooseWord(Uhand, wordList, n)
        wordcountcomp+=1
        
        if word!= None:
            Tscore+=getWordScore(word, n)
            print '"'+word+'"'+ ' earned '+ str(getWordScore(word, n))+' points. Total: '+ str(Tscore)+' points'
            Uhand=updateHand(Uhand, word)
        elif word==None:
            break
    
    print ''
    print 'Total score: '+ str(Tscore)+' points.'
    print 'Number of words: ' +str(wordcountcomp)

# Playing a game
def playGame(wordList):
    """
    Asks the user to input 'n' for new hand or 'r' for repeat hand or 'e' for end game.
    Asks the user to input a 'u' for the user to play or a 'c' for the computer to play.
    wordList: list (string)"""
    
    loopcount=0
    loop=None
    
    while True:
      choose=raw_input('ENTER "n" TO DEAL A NEW HAND, "r" TO REPLAY THE LAST HAND, OR "e" TO END GAME: ')
      if choose=='e':
         print 'Goodbye ' + name+ '!'
         break
         
      elif choose=='n':
         who=raw_input('ENTER "u" TO HAVE YOURSELF PLAY, "c" TO HAVE THE COMPUTER PLAY: ')
         loopcount+=1
         hand=dealHand(HAND_SIZE)
         loop=hand.copy()
         
         if who!='u' and who!='c':
             while who!='u' and who!='c':
                    print 'Invalid command.'
                    who=raw_input('ENTER "u" TO HAVE YOURSELF PLAY, "c" TO HAVE THE COMPUTER PLAY: ')
         
         if who=='u':
             playHand(hand, wordList, HAND_SIZE) 
         
         elif who=='c':
             compPlayHand(hand, wordList, HAND_SIZE)
         
                    
      elif choose=='r':
         if loopcount==0:
                 print 'You have not played a hand yet. Please play a new hand first!' 
                 
         else:
             who2=raw_input('ENTER "u" TO HAVE YOURSELF PLAY, "c" TO HAVE THE COMPUTER PLAY: ')
             
             if who2!='u' and who2!='c':
               while who2!='u' and who2!='c':
                    print 'Invalid command.'
                    who2=raw_input('ENTER "u" TO HAVE YOURSELF PLAY, "c" TO HAVE THE COMPUTER PLAY: ')
         
             if who2=='u':
                 playHand(loop, wordList, HAND_SIZE)

         
             elif who2=='c':
                 compPlayHand(loop, wordList, HAND_SIZE)
             
        
      else:
         print 'Invalid command.'

wordList = loadWords()
playGame(wordList)
