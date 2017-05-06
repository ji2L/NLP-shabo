#/opt/python3.4
# -*- coding: utf-8 -*-

import re
import enchant
import random
from nltk.corpus import wordnet as wn

# senctences the bot will respond with at the end of the conversation
GOODBYE_RESPONSES = ["Goodbye.", "See you soon !", "Cya.", "Farewell, friend."]

# keywords used to detect greetings from the user
GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "hey",)
# sentences that will be used when a greeting is detected
GREETING_RESPONSES = ["Hello.", "Hey !", "Hi.", "Well met !"]

# keywords used to detect a form of HYD (how you doin)
HYD_LIST_KEYWORDS = [("how", "are", "you", "?"), ("how", "are", "you", "doing", "?")]
# sentences that will be used when a HYD is detected
HYD_RESPONSES = ["I suffer from crippling depression.", "I'm ... I'm fine.", "I'm so tired even a sloth could beat me in a race.", "F.I.N.E."]

# keywords used to detect the user asking about the bot's age
AGE_LIST_KEYWORDS = ["how", "old", "are", "you", "?"]
# sentences that will be used to answer a question about the bot's age
AGE_RESPONSES = ["I'm old enough to know better than you."]

# keyword used to detect the user asking about the bot's name
NAME_LIST_KEYWORDS = [("who", "are", "you", "?"), ("what", "'", "s", "your", "name", "?")]
# sentences that will be used to answer questions about the bot's name
NAME_RESPONSES = ["I'm ShaBo, the political bot."]

# keywords used to detect the user asking about wheter or not the bot is human
HUMAN_LIST_KEYWORDS = [("what", "are", "you", "?"), ("are", "you", "human", "?")]
# sentences that will be used to answer questions about the bot's nature
HUMAN_RESPONSES = ["I'm a superior form of intelligence, therefore I can conceive and understand things that you can't."]

# list of punctuation
PUNCTUATIONS = [".", ";", "!", "?", ",", "...", "'"]
# list of modals
MODALS = ["are", "is", "will", "would", "do", "does", "can", "could", "should", "shall", "may", "might", "must", "have"]
# list of interogative words
INTEROGATIVE = ["what", "why", "where", "when", "pyplotplatlib", "penelop", "how", "which", "whose"]

# dictionary of positively oriented words
DICT_GOOD = ["good", "fine", "like", "love", "amazing", "excellent", "great", "exceptional", "acceptable", "excellent", "exceptional",
			"favorable", "great", "marvelous", "positive", "satisfactory", "superb", "valuable", "wonderful", "admirable", 
			"splendid", "welcome", "agreeable", "super", "nice"]
# dictionary of negatively oriented words
DICT_BAD = ["bad", "nefast", "wrong"]
# dictionary of  left-wing oriented words
DICT_LEFT = ["left", "communism", "leftist", "ussr", "gulag", "gulags", "healthcare", "cuba", "socialism", "communists", "comrade", "socialists", "equality", "anarchism", "anarchists", "collectivism", "collectivists", "marx", "staline", "lenine", "stalin", "lenin", "kropotkine", "proudhon", "mao", "castro", "che"]
# dictionary of right-wing oriented words
DICT_RIGHT = ["capitalism", "bourgeois", "bourgeoisie", "shareholder", "shareholders", "property", "boss", "CEO", "company", "companies", "usa", "america", "united states"]

#DICT_RIGHT_FINAL = []

#DICT_LEFT_FINAL = []

#Réponses si commentaire positif sur la gauche 3 = commentaire très positif, 1 = légèrement positif
LEFT_RESPONSES3 = ["Comrade Lenin would be so proud of you :')", "How many times did you read Das Kapital, by Marx ? I would guess 2 or 3 times.", "Are you a Gulag administrator ?"]
LEFT_RESPONSES2 = ["You should read Marx or Kropotkin. In no time you'll think that communism is the best thing ever.", "I could bet that you're a socialist. Am I wrong ?"]
LEFT_RESPONSES1 = ["You should ask me questions, you're on the right way.", "You're the kind of leftist who supports Obama, right ?"]

#Réponses à une phrase potentiellement neutre sur la gauche
LEFT_RESPONSES = ["You don't know what to think about socialism or communism ? Just ask me !", "You seem interestsed in socialism, don't you ?"]

#Réponses si commentaire négatif sur la gauche 3 = commentaire très négatif, 1 = légèrement négatif
LEFT_RESPONSES_BAD1 = ["I think we could do something about you, but you're on the wrong path.", "You're not totally hopeless. Try alternative medias."]
LEFT_RESPONSES_BAD2 = ["Oh, you couldn't be more wrong about socialism. Fortunately, I am here.", "Be ware of Gulag with your remarks."]
LEFT_RESPONSES_BAD3 = ["Why do you hate leftists so much ?", "You're the severest person who talk about communism", "Are you American ?"]

#Réponses si commentaire positif sur la droite 3 = commentaire très positif, 1 = légèrement positif
RIGHT_RESPONSES3 = ["You're an happy bourgeois now but take care, revolution is coming (before winter).", "Keep your Capitalists theories for yourself."]
RIGHT_RESPONSES2 = ["I am sure I can save you from Capitalism.", "Stop with the provocation."]
RIGHT_RESPONSES1 = ["You don't know what you're talking about...", "You should stop watching that much TV."]

#Réponses à une phrase potentiellement neutre sur la droite
RIGHT_RESPONSES = ["You don't know what to think about capitalism ? Just ask me !"]

#Réponses si commentaire négatif sur la droite 3 = commentaire très négatif, 1 = légèrement négatif
RIGHT_RESPONSES_BAD1 = ["You're too nice with capitalism.", "You're on the right way but you need to continue."]
RIGHT_RESPONSES_BAD2 = ["I agree !", "You're right (no pun intended)."]
RIGHT_RESPONSES_BAD3 = ["Are... are you the chosen one ?", "I've been waiting for you for such a long time !"]

#Liste d'averbe qui influences le sens d'une phrase
MULTIPLICATORS = ["absolutely", "very", "really", "lot"]

#Rempli avec les synonymes de MULTIPLICATORS
MULTIPLICATORS_FINAL = []

#Adverbes qui inversent le sens d'une phrase
MULTIPLICATORS_NEG = ["nothing", "not"]

#Mots-clé positifs, répartis en 3 niveau d'intensité
DICT_GOOD1 = ["good", "like", "acceptable", "valuable", "positive", "satisfactory"]
DICT_GOOD2 = ["fine", "great", "marvelous", "admirable"]
DICT_GOOD3 = ["amazing", "excellent", "exceptional", "wonderful"]

# dictionary of answers for the user's questions
DICT_ANSWERS = {
        'left' : 'Left-wing politics supports social equality and egalitarianism, often in opposition to social hierarchy and social inequality. I personally think it\'s the only acceptablepart of the political spectrum.',
        'communism' : 'In political and social sciences, communism is the philosophical, social, political, and economic ideology and movement whose ultimate goal is the establishment of the communist society, which is a socioeconomic order structured upon the common ownership of the means of production and the absence of social classes, money, and the state. I personally think that, even if not perfect, it\'s a way better system than capitalism.',
        'communists' : 'In political and social sciences, communism is the philosophical, social, political, and economic ideology and movement whose ultimate goal is the establishment of the communist society, which is a socioeconomic order structured upon the common ownership of the means of production and the absence of social classes, money, and the state. I personally think that, even if not perfect, it\'s a way better system than capitalism.',
        'leftist' : 'A name given to a person with left wing beliefs by somebody who is right-wing. Often derogatory. I personally don\'t think of this word as derogatory but rather as an acknowledgement of my political identity.',
        'ussr' : 'The Soviet Union, officially the Union of Soviet Socialist Republics (USSR), also known unofficially as Russia, was a socialist state in Eurasia that existed from 1922 to 1991. I personally think that this period of time was the best Russia has ever known.',
        'gulag' : 'The Gulag was the government agency that administered and controlled the Soviet forced-labor camp system during Joseph Stalin\'s rule from the 1930s up until the 1950s. I personally think that it\'s an appropriate form of punishment for the bourgeoisie.',
        'gulags' : 'The Gulag was the government agency that administered and controlled the Soviet forced-labor camp system during Joseph Stalin\'s rule from the 1930s up until the 1950s. I personally think that it\'s an appropriate form of punishment for the bourgeoisie.',
        'heathcare' : 'Healthcare is the maintenance or improvement of health via the diagnosis, treatment, and prevention of disease, illness, injury, and other physical and mental impairments in human beings. I personally think that it is a fundamental human right and that it shoul be free in every part of the world.',
        'cuba' : 'Cuba, officially the Republic of Cuba, is a country comprising the island of Cuba as well as Isla de la Juventud and several minor archipelagos. Cuba is located in the northern Caribbean where the Caribbean Sea, the Gulf of Mexico, and the Atlantic Ocean meet. Since 1965, the state has been governed by the Communist Party of Cuba. I personally think that Cuba succeeded where many others failed in electing a proper political party.',
        'socialism' : 'Socialism is a range of economic and social systems characterised by social ownership and democratic control of the means of production as well as the political ideologies, theories, and movements that aim to establish them. Social ownership may refer to forms of public, collective, or cooperative ownership; to citizen ownership of equity; or to any combination of these. I personally think that these systems are all far better than what we currently have in occidental societies.',
        'socialists' : 'Socialism is a range of economic and social systems characterised by social ownership and democratic control of the means of production as well as the political ideologies, theories, and movements that aim to establish them. Social ownership may refer to forms of public, collective, or cooperative ownership; to citizen ownership of equity; or to any combination of these. I personally think that these systems are all far better than what we currently have in occidental societies.',
        'anarchism' : 'Anarchism is a political philosophy that advocates self-governed societies based on voluntary institutions. These are often described as stateless societies, although several authors have defined them more specifically as institutions based on non-hierarchical free associations. Anarchism holds the state to be undesirable, unnecessary, and harmful. I personally think that, if it is ever applied, this philosophy is the one that will save humanity from being destroyed by capitalism.',
        'anarchists' : 'Anarchism is a political philosophy that advocates self-governed societies based on voluntary institutions. These are often described as stateless societies, although several authors have defined them more specifically as institutions based on non-hierarchical free associations. Anarchism holds the state to be undesirable, unnecessary, and harmful. I personally think that, if it is ever applied, this philosophy is the one that will save humanity from being destroyed by capitalism.',
        'equality' : 'Social equality is a state of affairs in which all people within a specific society or isolated group have the same status in certain respects, including civil rights, freedom of speech, property rights and equal access to certain social goods and services. However, it also includes concepts of health equity, economic equality and other social securities. I personally think that it is one of the most important moral value a human being can have.',
        'collectivism' : 'Collectivism is the moral stance, political philosophy, ideology, or social outlook that emphasizes the group and its interests. Collectivism is the opposite of individualism. Collectivists focus on communal, societal, or national interests in various types of political, economic and educational systems. I personally think that it shoul be part of every human being\'s moral.',
        'collecttivists' : 'Collectivism is the moral stance, political philosophy, ideology, or social outlook that emphasizes the group and its interests. Collectivism is the opposite of individualism. Collectivists focus on communal, societal, or national interests in various types of political, economic and educational systems. I personally think that it shoul be part of every human being\'s moral.',
        'marx' : 'Karl Marx (5 May 1818 – 14 March 1883) was a Prussian-born philosopher, economist, sociologist, journalist, and revolutionary socialist. As an adult, Marx became stateless and spent much of his life in London, England, where he continued to develop his thought in collaboration with German thinker Friedrich Engels and published various works, the most well-known being the 1848 pamphlet The Communist Manifesto. His work has since influenced subsequent intellectual, economic, and political history. I personally think that he was one of the greatest human being to have ever lived.',
        'lenin' : 'Vladimir Ilyich Ulyanov, better known by the alias Lenin (22 April 1870  – 21 January 1924), was a Russian communist revolutionary, politician, and political theorist. He served as head of government of the Russian Republic from 1917 to 1918, of the Russian Soviet Federative Socialist Republic from 1918 to 1924, and of the Soviet Union from 1922 to 1924. Under his administration, Russia and then the wider Soviet Union became a one-party socialist state governed by the Russian Communist Party. I personally think that he was one of the greatest human being to have ever lived.',
        'kropotkin' : 'Prince Pyotr Alexeyevich Kropotkin (December 9, 1842 – February 8, 1921) was a Russian activist, scientist, and philosopher, who advocated anarchism. He was imprisoned for his activism in 1874 and managed to escape two years later. He spent the next 41 years in exile in Switzerland, France (where he was imprisoned for almost 4 years) and in England. He returned to Russia after the Russian Revolution in 1917 but was disappointed by the Bolshevik form of state socialism. I personally think that he was one of the greatest human being to have ever lived.',
        'che' : 'Ernesto "Che" Guevara (June 14, 1928 – October 9, 1967) was an Argentine Marxist revolutionary, physician, author, guerrilla leader, diplomat, and military theorist. A major figure of the Cuban Revolution, his stylized visage has become a ubiquitous countercultural symbol of rebellion and global insignia in popular culture. I personally think that he was one of the greates human being to have ever lived.',
        'capitalism' : 'Capitalism is an economic system based on private ownership of the means of production and their operation for profit. Characteristics central to capitalism include private property, capital accumulation, wage labor, voluntary exchange, a price system, and competitive markets. In a capitalist market economy, decision-making and investment are determined by the owners of the factors of production in financial and capital markets, and prices and the distribution of goods are mainly determined by competition in the market. I personally think that this system is so awfuly bad that it will bring humanity to its end if it is not quickly replaced.',
        'bourgeois' : 'In Marxist philosophy the bourgeoisie is the social class that came to own the means of production during modern industrialization and whose societal concerns are the value of property and the preservation of capital, to ensure the perpetuation of their economic supremacy in society. I personally think that these people are a plague for humanity and that those who refuse to surrender their properties should be sent to gulags.',
        'bourgeoisie' : 'In Marxist philosophy the bourgeoisie is the social class that came to own the means of production during modern industrialization and whose societal concerns are the value of property and the preservation of capital, to ensure the perpetuation of their economic supremacy in society. I personally think that these people are a plague for humanity and that those who refuse to surrender their properties should be sent to gulags.',
        'shareholder' : 'A shareholder or stockholder is an individual or institution (including a corporation) that legally owns one or more shares of stock in a public or private corporation. I personally think that these people are parasites and that they should receive the same treatment as bourgeois.',
        'property' : 'In the abstract, property is that which belongs to or with something, whether as an attribute or as a component of said thing. I personally think that considering means of production as property should not be possible.',
        'CEO' : 'A chief executive officer (CEO) describes the position of the most senior corporate officer, executive, leader or administrator in charge of managing an organization. I personally think that these people are not required for a society (or a company) to function.',
        'company' : 'A company, abbreviated co., is a legal entity made up of an association of people, be they natural, legal, or a mixture of both, for carrying on a commercial or industrial enterprise. Company members share a common purpose and unite in order to focus their various talents and organize their collectively available skills or resources to achieve specific, declared goals. I personally think that these entities should belong to and be administered by the people who are part of them.',
        'companies' : 'A company, abbreviated co., is a legal entity made up of an association of people, be they natural, legal, or a mixture of both, for carrying on a commercial or industrial enterprise. Company members share a common purpose and unite in order to focus their various talents and organize their collectively available skills or resources to achieve specific, declared goals. I personally think that these entities should belong to and be administered by the people who are part of them.',
        'usa' : 'The United States of America (USA), commonly known as the United States (U.S.) or America, is a constitutional federal republic composed of 50 states, a federal district, five major self-governing territories, and various possessions. I personally think that this country has been totally corrputed by capitalism, only little hope is left for its people.'
        }

#Mots-clé négatifs
DICT_BAD1 = ["bad", "wrong", "indecent"]
DICT_BAD2 = ["odious", "despicable", "immoral"]
DICT_BAD3 = ["hateful", "repugnant", "evil"]

#Dictionnaire personnel pour compléter celui d'enchant
PERSONNAL_DICT = ["staline", "stalin", "lenin", "lenine"]

# functions that normalizes the user's input
def normalise(sent):
    sent = re.sub("\'\'", '"', sent) # two single quotes = double quotes
    sent = re.sub("[`‘’]+", r"'", sent) # normalise apostrophes/single quotes
    sent = re.sub("[≪≫“”]", '"', sent) # normalise double quotes
    sent = re.sub("([a-z]{3,})or", r"\1our", sent) # replace ..or words with ..our words (American versus British)
    sent = re.sub("([a-z]{2,})iz([eai])", r"\1is\2", sent) # replace ize with ise (..ise, ...isation, ..ising)
    
    return sent.lower()
    

# functions that tokenizes the normalized user's input
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


# functions that detects greetings
def checkGreetings(userInput):
    for word in userInput:
        if word in GREETING_KEYWORDS:
            return True
    
    return False


# functions that answers a political argument
def politicalArguments(userInput):
	#Compteur de positivité de la phrase
	good = 0
	
	#Compteur de négativité de la phrase
	bad = 0
	
	#Variable de tendance gauche
	left = 0
	
	#Variable de tendance droite
	right = 0
	
	#Multiplicateur des adverbes
	mult = 1
	
	
	for word in userInput:
		#Mot positif de degré 1
		if word in DICT_GOOD1:
			good+=1
			
		#Mot positif de degré 2
		elif word in DICT_GOOD2:
			good+=2
			
		#Mot positif de degré 3
		elif word in DICT_GOOD3:
			good+=3
			
		#Mot négatif de degré 1
		elif word in DICT_BAD1:
			bad+=1
			
		#Mot négatif de degré 2
		elif word in DICT_BAD2:
			bad+=2
			
		#Mot négatif de degré 3
		elif word in DICT_BAD3:
			bad+=3
			
		#Mot associé à un vocabulaire de gauche
		elif word in DICT_LEFT:
			left+=1
			
		#Mot associé à un vocabulaire de droite
		elif word in DICT_RIGHT:
			right+=1
			
		#Adverbe
		elif word in MULTIPLICATORS:
			mult+=1
			
		#Mot de négation
		elif word in MULTIPLICATORS_NEG:
			mult = -1
			
	#On sort si la phrase n'a pas de tendance politique
	if left == 0 and right == 0:
		return False
	#Si < 0, phrase plutôt négative, si > 0 plutôt positive et 0 neutre
	humor = good - bad
	
	#On applique un coefficiant multiplicateur pour les adverbes
	humor *= mult
	
	#Si < 0, phrase parlant de la gauche, si > 0, phrasep parlant de la droite, sinon indéterminé
	political = left - right

	if humor >= 3:
		if political > 0:
			print(random.choice(LEFT_RESPONSES3))
		elif political < 0:
			print(random.choice(RIGHT_RESPONSES3))
		else:
			print(random.choice(NEUTRAL_RESPONSES3))
	elif humor == 2:
		if political > 0:
			print(random.choice(LEFT_RESPONSES2))
		elif political < 0:
			print(random.choice(RIGHT_RESPONSES2))
		else:
			print(random.choice(NEUTRAL_RESPONSES2))
	elif humor == 1:
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
	elif humor == -1:
		if political > 0:
			print(random.choice(LEFT_RESPONSES_BAD1))
		elif political < 0:
			print(random.choice(RIGHT_RESPONSES_BAD1))
		else:
			print(random.choice(NEUTRAL_RESPONSES_BAD1))
	elif humor == -2:
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


# functions that answers a political questions
def politicalQuestion(userInput):
    leftScore = 0
    rightScore = 0

    for word in userInput:
        if word in DICT_LEFT:
            leftScore += 1
            if word in DICT_ANSWERS.keys():
                print(DICT_ANSWERS.get(word))
                return

        elif word in DICT_RIGHT:
            rightScore += 1
            if word in DICT_ANSWERS.keys():
                print(DICT_ANSWERS.get(word))
                return

    # if none of the words in the user's input exists in DICT_ANSWERS, print a generic answer based on the left/right score
    if leftScore > rightScore:
        print("I see you're interested in left-wing oriented subjects and I apologize for not being able to provide you with an acceptable answer as of now.")
    elif rightScore > leftScore:
        print("I see you're interested in right-wing oriented subjects (it's always helpful to learn about the ennemy) and I apologize for not being able to provide you with an acceptable answer as of now.")
    else :
        print("I apologize for not being able to provide you with an acceptable answer as of now.") # if the score is tied, the question might not have been about politics


# function that detects a HYD
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


# function that detects the user asking about the bot's name
def checkName(userInput):
    for sublist in NAME_LIST_KEYWORDS:
        fail = False
        if len(userInput) >= len(sublist):
            for keyword, word in zip(sublist, userInput):
                if keyword != word:
                    fail = True
                    break

            if not fail:
                return True

    return False


# function that detects the user asking about the bot's name
def checkHuman(userInput):
    for sublist in HUMAN_LIST_KEYWORDS:
        fail = False
        if len(userInput) >= len(sublist):
            for keyword, word in zip(sublist, userInput):
                if keyword != word:
                    fail = True
                    break

            if not fail:
                return True

    return False


# function that detects the user asking the age of the bot
def checkAge(userInput):
    fail = False
    for keyword, word in zip(AGE_LIST_KEYWORDS, userInput):
        if keyword != word:
            fail = True
            break

    return not fail


# function that provides an answer in different cases
def respond(userInput):
    if checkGreetings(userInput):
        print(random.choice(GREETING_RESPONSES))
    elif checkHYD(userInput):
        print(random.choice(HYD_RESPONSES))
    elif checkAge(userInput):
        print(random.choice(AGE_RESPONSES))
    elif checkName(userInput):
        print(random.choice(NAME_RESPONSES))
    elif checkHuman(userInput):
        print(random.choice(HUMAN_RESPONSES))
    elif isQuestion(userInput[0], userInput[len(userInput) - 1]):
        politicalQuestion(userInput)
    else:
        politicalArguments(userInput)
        

# function that detects a question in the user's input
def isQuestion(first_token, last_token):
    if ((last_token == "?") or (first_token in MODALS) or (first_token in INTEROGATIVE)):
        return True 
    else:
        return False
		

# tutoriel pour sysnets : https://pythonprogramming.net/wordnet-nltk-tutorial/
def print_synonym(word):
    for syn in wn.synsets(word):
        print(syn.lemmas()[0].name())


# main loop
def dialogue():
    exit = True

    while(exit):
        rawInput = input(">>>")
        d = enchant.Dict("en_US")

        if rawInput == "bye":
            exit = False
        elif rawInput == "":
            continue
        else:
            normalisedInput = normalise(rawInput)
            tokenisedInput = tokenise(normalisedInput)

            if (is_english_sentence(tokenisedInput)):
                respond(tokenisedInput)
            else:
                print("I did not understand, could you please reformulate ?")


# checks wether or not the user's input is a correct sentence
def is_english_sentence(tokens):
    d_us = enchant.Dict("en_US")
    d_uk = enchant.Dict("en_UK")
    for token in tokens:
        if ((not (token in PUNCTUATIONS)) and (not d_us.check(token)) and (not d_uk.check(token)) and (not (token in PERSONNAL_DICT))):
            return False
    return True


# main
if __name__ == '__main__':
    for word in MULTIPLICATORS:
        for syn in wn.synsets(word):
            MULTIPLICATORS_FINAL.append(syn.lemmas()[0].name())

    print("..:://ShaBo - The Political Bot\\\\::..")

    dialogue()

    print(random.choice(GOODBYE_RESPONSES))

