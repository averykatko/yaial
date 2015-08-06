#!/usr/bin/env python3
from distance import *
from collections import defaultdict
from GA import GA
import random, math

# Native speaker counts from Nationalencyklopedin
# Total speaker counts from Ethnologue
# Family speaker counts from Ethnologue

ar = {
	'#native': 295,
	'#total': 452,
	'#family': 381, # Afro-Asiatic
	'human': {'insan': 1, 'basyar': 1},
	'child': {'tipr': 1},
	'big': {'kabir': 1},
	'small': {'sagir': 1},
	'water': {'ma': 1},
	'1s': {'ana': 1},
	'2s': {'anta': 1, 'anti': 1},
	'3s': {'uwa': 1, 'iya': 1},
	'-PL': {'un': 1, 'in': 1},
	'-GEN': {'i': 1, 'in': 1},
	'NEG': {'ra': 1, 'ma': 1, 'ram': 1, 'ran': 1, 'raisa': 1},
	'and': {'wa': 1},
	'or': {'au': 1},
	'zero': {'sepr': 1},
	'one': {'waid': 1},
	'two': {'itnan': 1},
	'three': {'tarata': 1},
	'four': {'arbaa': 1},
	'five': {'kamsa': 1},
	'six': {'sita': 1},
	'seven': {'ˈsaba': 1},
	'eight': {'tamaniya': 1},
	'nine': {'ˈtisa': 1},
	'ten': {'asyara': 1},
}

cmn = {
	'#native': 955,
	'#total': 1026,
	'#family': 1268, # Sino-Tibetan
	'human': {'sen': 1},
	'child': {'kaidyi': 1, 'artun': 1},
	'big': {'da': 1, 'dai': 1, 'tai': 1},
	'small': {'syau': 1},
	'water': {'swei': 1},
	'1s': {'wo': 1},
	'2s': {'ni': 1},
	'3s': {'ta': 1},
	'-PL': {'man': 1},
	'-GEN': {'da': 1},
	'NEG': {'bu': 1, 'mei': 1, 'meiyou': 1},
	'and': {'ko': 1, 'wi': 1, 'yidyi': 1},
	'or': {'kwo': 1, 'kwodyo': 1},
	'zero': {'rin': 1},
	'one': {'yi': 1},
	'two': {'ar': 1, 'ryan': 1},
	'three': {'san': 1},
	'four': {'si': 1},
	'five': {'wu': 1},
	'six': {'ryou': 1},
	'seven': {'tyi': 1},
	'eight': {'ba': 1},
	'nine': {'dyou': 1},
	'ten': {'ss': 1}, # ????
}

en = {
	'#native': 360,
	'#total': 841,
	'#family': 2914, # Indo-European
	'human': {'yuman': 1},
	'child': {'tyaird': 1, 'kid': 1},
	'big': {'big': 1, 'rardy': 1, 'greit': 1},
	'small': {'smar': 1, 'ritar': 1, 'taini': 1},
	'water': {'watar': 1},
	'1s': {'ai': 1, 'mi': 1},
	'2s': {'yu': 1},
	'3s': {'i': 1, 'syi': 1, 'it': 1, 'dei': 1},
	'-PL': {'s': 1, 'is': 1},
	'-GEN': {'s': 1, 'is': 1},
	'NEG': {'nat': 1, 'dount': 1},
	'and': {'and': 1},
	'or': {'or': 1},
	'zero': {'sirou': 1},
	'one': {'won': 1},
	'two': {'tu': 1},
	'three': {'tri': 1},
	'four': {'por': 1},
	'five': {'paib': 1},
	'six': {'siks': 1},
	'seven': {'seban': 1},
	'eight': {'eit': 1},
	'nine': {'nain': 1},
	'ten': {'ten': 1},
	}

es = {
	'#native': 405,
	'#total': 489,
	'#family': 2914, # Indo-European
	'human': {'umano': 1, 'umana': 1},
	'child': {'ninyo': 1, 'ninya': 1, 'tyiko': 1, 'tyika': 1},
	'big': {'grande': 1},
	'small': {'pekenyo': 1, 'pekenya': 1, 'tyiko': 1, 'tyika': 1},
	'water': {'agwa': 1},
	'1s': {'dyo': 1, 'me': 1, 'mi': 1},
	'2s': {'tu': 1, 'te': 1, 'ti': 1, 'bos': 1, 'usted': 1},
	'3s': {'er': 1, 'erya': 1, 'eryo': 1, 're': 1, 'ro': 1, 'ra': 1},
	'-PL': {'s': 1, 'es': 1},
	'-GEN': {},
	'NEG': {'no': 1},
	'and': {'i': 1},
	'or': {'o': 1, 'u': 1},
	'zero': {'sero': 1},
	'one': {'uno': 1},
	'two': {'dos': 1},
	'three': {'tres': 1},
	'four': {'kwatro': 1},
	'five': {'sinko': 1},
	'six': {'ses': 1},
	'seven': {'syete': 1},
	'eight': {'otyo': 1},
	'nine': {'nwebe': 1},
	'ten': {'dyes': 1},
	}

hi = {
	'#native': 376, # Hindi + Urdu
	'#total': 538, # Hindi + Urdu
	'#family': 2914, # Indo-European
	'human': {'manusya': 1, 'insan': 1, 'admi': 1},
	'child': {'batya': 1, 'syisyu': 1, 'bar': 1},
	'big': {'bara': 1, 'bari': 1},
	'small': {'tyota': 1, 'tyoti': 1},
	'water': {'pani': 1, 'dyar': 1, 'ab': 1},
	'1s': {'main': 1, 'muty': 1, 'ham': 1},
	'2s': {'tu': 1, 'tuty': 1, 'tum': 1, 'ap': 1},
	'3s': {'ye': 1, 'is': 1, 'wo': 1, 'hai': 1},
	'-PL': {'on': 1},
	'-GEN': {'ka': 1, 'ke': 1, 'ki': 1},
	'NEG': {'nain': 1, 'na': 1, 'mat': 1},
	'and': {'aur': 1},
	'or': {'wa': 1},
	'zero': {'syunya': 1, 'sipar': 1},
	'one': {'ek': 1},
	'two': {'do': 1},
	'three': {'tin': 1},
	'four': {'tyar': 1},
	'five': {'panty': 1},
	'six': {'tye': 1},
	'seven': {'sat': 1},
	'eight': {'at': 1},
	'nine': {'nau': 1},
	'ten': {'das': 1},
	}

def distance(w1, w2):
	return edit_distance(w1, w2)

def getFitnessFunction(langs, word, weightFunc):
	words = defaultdict(int)
	for l in langs:
		weightSum = sum([v for k,v in l[word].items()])
		for wd,wt in l[word].items():
			words[wd] += weightFunc(l) * wt/weightSum
	return lambda w: -1 * sum([wt * distance(w, wd) for wd, wt in words.items()])

def rs(pop, fitness):
	popFitnesses = list(map(fitness, pop))
	minFitness = min(popFitnesses)
	if minFitness < 0:
		posFitnesses = list(map((lambda x: x-minFitness), popFitnesses))
	else:
		posFitnesses = list(popFitnesses)
	fitsum = sum(posFitnesses)
	if fitsum == 0: # all equally fit
		index = random.randrange(len(pop))
		return pop[index]
	normalizedFits = list(map((lambda x: x/fitsum), posFitnesses))
	rfits = list(normalizedFits)
	#print(len(rfits))
	for i in range(1,len(pop)):
		rfits[i] += rfits[i-1]
	#assert rfits[-1] == 1.0 # hmm floats might make this problematic
	rand = random.random()
	for i in range(len(pop)):
		if rand <= rfits[i]:
			return pop[i]
	return pop[-1] # shouldn't have to do this, probably? but floats

def rep(x, y):
	minlen = min(len(x), len(y))
	if minlen <= 1:
		return x + y
	split = random.randrange(minlen)
	sx = x[:split]
	sy = y[split:]
	return sx + sy

def mut(s):
	chars = list(s)
	if s is '':
		choice = random.choice(['insert', 'overwrite'])
	else:
		choice = random.choice(['insert','delete','overwrite'])
	if choice is 'insert':
		index = random.randint(0, len(chars))
		char = random.choice('mpbntdsrkgywieaou')
		chars.insert(index, char)
	elif choice is 'delete':
		index = random.randrange(len(chars))
		del chars[index]
	elif choice is 'overwrite':
		index = random.randrange(len(chars))
		char = random.choice('mpbntdsrkgywieaou')
		chars[index] = char
	return str.join('', chars)

class weight(object):
	native = lambda x: x['#native']
	total = lambda x: x['#total']
	family = lambda x: x['#family']
	const = lambda x: 1

def gen_words(langs, words, weightFunc, popsize, generations, mutationProb):
	out = {}
	for word in words:
		fitness = getFitnessFunction(langs, word, weightFunc)
		population = []
		for l in langs:
			for wd, wt in l[word].items():
				population.append(wd)
		popfactor = math.ceil(popsize/len(population))
		ga = GA(population * popfactor, fitness, rs, rep, mutationProb, mut)
		ga.run(generations)
		sortedPop = sorted(ga.population, key=fitness, reverse=True)
		out[word] = list(zip(sortedPop, map(fitness, sortedPop)))
	return out
