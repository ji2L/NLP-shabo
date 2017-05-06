#/opt/python3.4
# -*- coding: utf-8 -*-

import re
import enchant
import random
from nltk.corpus import wordnet as wn

# sentences we'll respond with if the user greeted us
GOODBYE_RESPONSES = ["Goodbye.", "See you soon !", "Cya.", "Farewell, friend."]
GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "hey",)
GREETING_RESPONSES = ["Hello.", "Hey !", "Hi.", "Well met !"]
HYD_LIST_KEYWORDS = [("how", "are", "you", "?"),("how", "are", "you", "doing", "?")]
HYD_RESPONSES = ["I suffer from crippling depression.", "I'm ... I'm fine.", "I'm so tired even a sloth could beat me in a race.", "F.I.N.E."]
AGE_LIST_KEYWORDS = ["how", "old", "are", "you", "?"]
AGE_RESPONSES = ["I'm old enough to know better than you."]
PUNCTUATIONS = (".", ";", "!", "?", ",", "...", "'")
MODALS = ("are", "is", "will", "would", "do", "does", "can", "could", "should", "shall", "may", "might", "must", "have")
INTEROGATIVE = ("what", "why", "where", "when", "pyplotplatlib", "penelop", "how", "which", "whose")
DICT_GOOD = ("good", "fine", "like", "love", "amazing", "excellent", "great", "exceptional", "acceptable", "excellent", "exceptional",
			"favorable", "great", "marvelous", "positive", "satisfactory", "superb", "valuable", "wonderful", "ace", "admirable", 
			"splendid", "welcome", "agreeable", "super", "nice")
DICT_BAD = ("bad")
DICT_LEFT = ("left")
DICT_RIGHT = ("right")
	


def normalise(sent):
    sent = re.sub("\'\'", '"', sent) # two single quotes = double quotes
    sent = re.sub("[`‘’]+", r"'", sent) # normalise apostrophes/single quotes
    sent = re.sub("[≪≫“”]", '"', sent) # normalise double quotes
    sent = re.sub("([a-z]{3,})or", r"\1our", sent) # replace ..or words with ..our words (American versus British)
    sent = re.sub("([a-z]{2,})iz([eai])", r"\1is\2", sent) # replace ize with ise (..ise, ...isation, ..ising)
    
    return sent.lower()
    

def tokenise(sent):
    sent = re.sub("([^ ])\'", r"\1 '", sent) # separate apostrophe from preceding word by a space if no space to left
    sent = re.sub(" \'", r" ' ", sent) # separate apostrophe from following word if a space is left

    # separate on punctuation
    cannot_precede = ["M", "Prof", "Sgt", "Lt", "Ltd", "co", "etc", "[A-Z]", "[Ii].e", "[eE].g"] # non-exhaustive list
    regex_cannot_precede = "(?:(?<!"+")(?<!".join(cannot_precede)+"))"
    sent = re.sub(regex_cannot_precede+"([\.\,\;\:\)\(\"\?\!]( |$))", r" \1", sent)
    sent = re.sub("((^| )[\.\?\!]) ([\.\?\!]( |$))", r"\1\2", sent) # then restick several fullstops ... or several ?? or !!
    sent = sent.split() # split on whitespace

    return sent


def checkGreetings(userInput):
    for word in userInput:
        if word in GREETING_KEYWORDS:
            return True
    
    return False


def checkHYD(userInput):
    for sublist in HYD_LIST_KEYWORDS:
        fail = False
        if len(userInput) >= len(sublist):
            for keyword, word in zip(sublist, userInput):
                if keyword != word:
                    fail = True
                    break

            if not fail:
                return True

    return False


def checkAge(userInput):
    fail = False
    for keyword, word in zip(AGE_LIST_KEYWORDS, userInput):
        if keyword != word:
            fail = True
            break

    return not fail


def respond(userInput):
    if checkGreetings(userInput):
        print(random.choice(GREETING_RESPONSES))
    elif checkHYD(userInput):
        print(random.choice(HYD_RESPONSES))
    elif checkAge(userInput):
        print(random.choice(AGE_RESPONSES))
    else:
        print("I did not understand, could you please repeat or reformulate ?")
        

def is_question(first_token, last_token):
	if (last_token == "?"):
		if (first_token in MODALS) or (first_token in INTEROGATIVE):
			return True
	else:
		return False
		

# tutoriel pour sysnets : https://pythonprogramming.net/wordnet-nltk-tutorial/
def print_synonym(word):
	for syn in wn.synsets(word):
		print(syn.lemmas()[0].name())


def dialogue():
    exit = True

    print("..:://ShaBo\\\\::..")

    while(exit):
        rawInput = input(">>>")
        d = enchant.Dict("en_US")

        if rawInput == "bye":
            exit = False
        else:
            normalisedInput = normalise(rawInput)
            tokenisedInput = tokenise(normalisedInput)

            print(tokenisedInput)
            
            if (is_english_sentence(tokenisedInput)):
                print("correct sentence")
                respond(tokenisedInput)
            else:
                print("incorrect sentence")
            if (is_question(tokenisedInput[0], tokenisedInput[len(tokenisedInput)-1])):
                print("it is a question")
            else:
                print("it is not a question")


    

def is_english_sentence(tokens):
    d = enchant.Dict("en_US")
    for token in tokens:
        if (not (token in PUNCTUATIONS)) and (not (d.check(token))):
            return False
    return True


if __name__ == '__main__':
    dialogue()
    print(random.choice(GOODBYE_RESPONSES))

