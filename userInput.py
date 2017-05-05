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
PUNCTUATIONS = [".", ";", "!", "?", ",", "...", "'"]
MODALS = ["are", "is", "will", "would", "do", "does", "can", "could", "should", "shall", "may", "might", "must", "have"]
INTEROGATIVE = ["what", "why", "where", "when", "pyplotplatlib", "penelop", "how", "which", "whose"]
DICT_GOOD = ["good", "fine", "like", "love", "amazing", "excellent", "great", "exceptional", "acceptable", "excellent", "exceptional",
			"favorable", "great", "marvelous", "positive", "satisfactory", "superb", "valuable", "wonderful", "ace", "admirable", 
			"splendid", "welcome", "agreeable", "super", "nice"]
DICT_BAD = ["bad", "nefast", "wrong"]
DICT_LEFT = ["left", "communism", "leftist", "socialism", "communists", "socialists", "equality", "anarchism", "anarchists", "marx", "staline", "lenine", "kropotkine", "proudhon", "mao", "castro", "che"]
DICT_RIGHT = ["capitalism", "bourgeois", "bourgeoisie", "shareholder", "boss", "CEO"]

LEFT_RESPONSES3 = ["Comrade Lenine would be so proud of you :'(", "How many times did you read Capital, by Marx ? I would say 2 or 3 times", "Are you a Gulag administrator ?"]
LEFT_RESPONSES2 = ["You should read Marx or Kropotkine. In no time you'll say that Staline did nothing wrong", "I could bet that you're a socialist. Am I wrong ?"]
LEFT_RESPONSES1 = ["You should ask me questions, you're on the right way", "You're the kind of leftist who supports Obama, right ?"]

LEFT_RESPONSES = ["You don't know what to think about socialism or communism ? Just ask me !", "You seem interessed by socialism, don't you ?"]

LEFT_RESPONSES_BAD1 = ["I think we could do something about you, but you're in the wrong way", "You're not totally lost. Try alternative medias"]
LEFT_RESPONSES_BAD2 = ["Oh, you can't be so wrong about socialism. Fortunately, I am here.", "Be ware of Gulag with your remarks"]
LEFT_RESPONSES_BAD3 = ["Why do you hate so much leftists ?", "You're the severest person who talk about communism", "Are you American ?"]

RIGHT_RESPONSES3 = ["You're an happy bourgeois now but take care, revolution is coming (before winter)", "Keep your Capitalists theory with you."]
RIGHT_RESPONSES2 = ["I am sure I can save you from Capitalism", "Stop your provocation"]
RIGHT_RESPONSES1 = ["You don't know what you're talking about...", "You should stop watching medias"]

RIGHT_RESPONSES = ["You don't know what to think about capitalism ? Just ask me !"]
RIGHT_RESPONSES_BAD1 = ["You're too nice with capitalism.", "You're on the good way but you need to continue"]
RIGHT_RESPONSES_BAD2 = ["I agree !", "You're right (no word play)"]
RIGHT_RESPONSES_BAD3 = ["Are... are you the chosen one ?", "I've been waiting you a long time"]

MULTIPLICATORS = ["absolutly", "very", "really", "lot"]
MULTIPLICATORS_NEG = ["nothing"]

DICT_GOOD1 = ["good", "like", "acceptable", "valuable", "positive", "satisfactory"]
DICT_GOOD2 = ["fine", "great", "marvelous", "admirable"]
DICT_GOOD3 = ["amazing", "excellent", "exceptional", "wonderful"]


	


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
	
def politicalArguments(userInput):
	good = 0
	bad = 0
	left = 0
	right = 0
	mult = 1
	for word in userInput:
		if word in DICT_GOOD1:
			good+=1
		elif word in DICT_GOOD2:
			good+=2
		elif word in DICT_GOOD2:
			good+=3
		elif word in DICT_BAD:
			bad+=1
		elif word in DICT_LEFT:
			left+=1
		elif word in DICT_RIGHT:
			right+=1
		elif word in MULTIPLICATORS:
			mult+=1
		elif word in MULTIPLICATORS_NEG:
			mult-=1
			
	if left == 0 and right == 0:
		return False
	#Si < 0, phrase plutôt négative, si > 0 plutôt positive et 0 neutre
	humor = good - bad
	
	#On applique un coefficiant multiplicateur pour les adverbes
	humor *= mult
	
	#Si < 0, phrase parlant de la gauche, si > 0, phrasep parlant de la droite, sinon indéterminé
	political = left - right
	#print(left)
	#print(right)
	#print(political)
	#print(good)
	#print(bad)
	if humor >= 3:
		if political > 0:
			print(random.choice(LEFT_RESPONSES3))
		elif political < 0:
			print(random.choice(RIGHT_RESPONSES3))
		else:
			print(random.choice(NEUTRAL_RESPONSES3))
	elif humor >= 2:
		if political > 0:
			print(random.choice(LEFT_RESPONSES2))
		elif political < 0:
			print(random.choice(RIGHT_RESPONSES2))
		else:
			print(random.choice(NEUTRAL_RESPONSES2))
	elif humor >= 1:
		if political > 0:
			print(random.choice(LEFT_RESPONSES1))
		elif political < 0:
			print(random.choice(RIGHT_RESPONSES1))
		else:
			print(random.choice(NEUTRAL_RESPONSES1))
	elif humor == 0:
		if political > 0:
			print(random.choice(LEFT_RESPONSES))
		elif political < 0:
			print(random.choice(RIGHT_RESPONSES))
		else:
			print(random.choice(NEUTRAL_RESPONSES))
	elif humor <= -1:
		if political > 0:
			print(random.choice(LEFT_RESPONSES_BAD1))
		elif political < 0:
			print(random.choice(RIGHT_RESPONSES_BAD1))
		else:
			print(random.choice(NEUTRAL_RESPONSES_BAD1))
	elif humor <= -2:
		if political > 0:
			print(random.choice(LEFT_RESPONSES_BAD2))
		elif political < 0:
			print(random.choice(RIGHT_RESPONSES_BAD2))
		else:
			print(random.choice(NEUTRAL_RESPONSES_BAD2))
	elif humor <= -3:
		if political > 0:
			print(random.choice(LEFT_RESPONSES_BAD3))
		elif political < 0:
			print(random.choice(RIGHT_RESPONSES_BAD3))
		else:
			print(random.choice(NEUTRAL_RESPONSES_BAD3))
	return True
		
	


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
    fail = False # A FINIR
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
    elif politicalArguments(userInput):
        return True
    else:
        print("I did not understand, could you please repeat or reformulate ?")
        

def is_question(first_token, last_token):
	if (last_token == "?"):
		if (first_token in MODALS) or (first_token in INTEROGATIVE):
			return True
	else:
		return False
		

# tutorile pour sysnets : https://pythonprogramming.net/wordnet-nltk-tutorial/
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

            #print(tokenisedInput)
            print('\n')
            
            if (is_english_sentence(tokenisedInput)):
                #print("correct sentence")
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

