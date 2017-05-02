#/opt/python3.4
# -*- coding: utf-8 -*-

import re
import enchant
import random
from nltk.corpus import wordnet as wn

# sentences we'll respond with if the user greeted us
GOODBYE_RESPONSES = ["Goodbye.", "See you soon !", "Cya.", "Farewell, friend."]
GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup",)
GREETING_RESPONSES = ["Hello.", "Hey !", "Hi."]
PUNCTUATIONS = (".", ";", "!", "?", ",", "...", "'")
MODALS = ("are", "is", "will", "would", "do", "does", "can", "could", "should", "shall", "may", "might", "must", "have")
INTEROGATIVE = ("what", "why", "where", "when", "pyplotplatlib", "penelop", "how", "which", "whose")
DICT_GOOD = ("good", "fine", "like", "love", "amazing", "excellent", "great", "exceptional", "acceptable", "excellent", "exceptional",
			"favorable", "great", "marvelous", "positive", "satisfactory", "superb", "valuable", "wonderful", "ace", "admirable", 
			"splendid", "welcome", "agreeable", "super", "nice")
DICT_BAD = ("bad")
DICT_LEFT = ("left")
DICT_RIGHT = ("right")

PERSONAL_ANSWERS_NOUN = {"name" : "My name is Shabo :)",
						 "colour" : "Red of course"}
PERSONAL_ANSWERS_ADJ = {"old" : "I was born with anarchism in 1840",
						"tall" : "49,3 cm"}
PERSONAL_ANSWERS_VERB = {"live" : "I live in Paris"}

	


def normalise(sent, lang):
    sent = re.sub("\'\'", '"', sent) # two single quotes = double quotes
    sent = re.sub("[`‘’]+", r"'", sent) # normalise apostrophes/single quotes
    sent = re.sub("[≪≫“”]", '"', sent) # normalise double quotes

    if lang=="en":
        sent = re.sub("([a-z]{3,})or", r"\1our", sent) # replace ..or words with ..our words (American versus British)
        sent = re.sub("([a-z]{2,})iz([eai])", r"\1is\2", sent) # replace ize with ise (..ise, ...isation, ..ising)
    if lang=="fr":
        replacements = [("keske", "qu' est -ce que"), ("estke", "est -ce que"), ("bcp", "beaucoup")] # etc.
        for (original, replacement) in replacements:
            sent = re.sub("(^| )"+original+"( |$)", r"\1"+replacement+r"\2", sent)
    return sent.lower()
    

def tokenise(sent, lang):
    if lang=="en":
        return tokenise_en(sent)
    elif lang=="fr":
        return tokenise_fr(sent)
    else:
        exit("Lang: "+str(lang)+" not recognised for tokenisation.\n")


def tokenise_en(sent):

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


def respond(userInput):
    if checkGreetings(userInput):
        print(random.choice(GREETING_RESPONSES))
    else:
        print("I did not understand, could you reformulate please ?")
        
def is_question(first_token, last_token):
	if (last_token == "?"):
		if (first_token in MODALS) or (first_token in INTEROGATIVE):
			return True
	else:
		return False
		
# retourne l'indice de "you" ou de "your" pour une question peronnelle
# retourne -1 si la question n'est pas personnelle
def private_question(question):
	# on commence par checker la fin de la phrase (question commence par "how")
	if (question[len(question)-2] == "you"):
		return len(question)-2
	# on check ensuite si on trouve un "your" ou "you" dans la phrase
	elif ((question[0] != "how") and (question[0] in INTEROGATIVE)):
		for i in range(0,len(question)):
			if((question[i] == "your") or (question[i] == "you")):
				return i
	return -1

# réponse à une question privée	
def answer_private_question(pos, question):
	# premier cas : question du genre "what is your name?"
	if ((question[0] == "what") and (question[pos] == "your")):
		# recherche du nom désigné par "your"
		# on élimine les adjectifs et autre "very" etc
		if (question[pos+1] not in PERSONAL_ANSWERS_NOUN):
			pos=pos+1
		if (question[pos+1] not in PERSONAL_ANSWERS_NOUN):
			pos=pos+1
		noun = question[pos+1]
		if (noun in PERSONAL_ANSWERS_NOUN):
			return PERSONAL_ANSWERS_NOUN[noun]
		else:
			return "error answer private question"
	# deuxieme cas : question avec "you" à la fin
	elif (pos == len(question)-2):#A FAIRE
		return "you at the end"
		
# tutorile pour sysnets : https://pythonprogramming.net/wordnet-nltk-tutorial/
def print_synonym(word):
	for syn in wn.synsets(word):
		print(syn.lemmas()[0].name())

def dialogue(lang):
    exit = True

    print("..:://ShaBo\\\\::..")

    while(exit):
        rawInput = input(">>>")
        d = enchant.Dict("en_US")

        if rawInput == "bye":
            exit = False
        else:
            normalisedInput = normalise(rawInput, lang)
            tokenisedInput = tokenise(normalisedInput, lang)

            print(tokenisedInput)
           
            if (is_english_sentence(tokenisedInput)):
                print("correct sentence")
                respond(tokenisedInput)
            else:
                print("incorrect sentence")
            if (is_question(tokenisedInput[0], tokenisedInput[len(tokenisedInput)-1])):
                #print("it is a question")
                if (private_question(tokenisedInput) != -1):
                    #print("it is a private question (", private_question(tokenisedInput), ")")
                    print(answer_private_question(private_question(tokenisedInput), tokenisedInput))
                else:
                    #print("it is not a private question")
            else:
                #print("it is not a question")


    

def is_english_sentence(tokens):
    d = enchant.Dict("en_US")
    for token in tokens:
        if (not (token in PUNCTUATIONS)) and (not (d.check(token))):
            return False
    return True
     


if __name__ == '__main__':
    dialogue("en")
    print(random.choice(GOODBYE_RESPONSES))

