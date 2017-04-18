#/opt/python3.4
# -*- coding: utf-8 -*-

import re
import random

# sentences we'll respond with if the user greeted us
GOODBYE_RESPONSES = ["Goodbye.", "See you soon !", "Cya.", "Farewell, friend."]
GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup",)
GREETING_RESPONSES = ["Hello.", "Hey !", "Hi."]

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


def dialogue(lang):
    exit = True

    print("..:://ShaBo\\\\::..")

    while(exit):
        rawInput = input(">>>")

        if rawInput == "bye":
            exit = False
        else:
            normalisedInput = normalise(rawInput, lang)
            tokenisedInput = tokenise(normalisedInput, lang)
            respond(tokenisedInput)


if __name__ == '__main__':
    dialogue("en")
    print(random.choice(GOODBYE_RESPONSES))

