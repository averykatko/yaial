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
	# 'old': {'kadim': 1, 'musin': 1},
	# 'young': {},
	# 'fire': {},
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
	'hundred': {'mia': 1},
	'thousand': {'arp': 1},
}

bn = {
	'#native': 205,
	'#total': 208,
	'#family': 2914, # Indo-European
	'human': {'manusa': 1},
	'child': {'syisyu': 1},
	'big': {'boro': 1},
	'small': {'tyoto': 1},
	# 'old': {'purono': 1, 'probin': 1},
	# 'young': {},
	# 'fire': {},
	'water': {'dyor': 1, 'pani': 1},
	'1s': {'ami': 1, 'amake': 1},
	'2s': {'tui': 1, 'tumi': 1, 'apni': 1, 'toke': 1, 'tomake': 1, 'apnake': 1},
	'3s': {'e': 1, 'ini': 1, 'o': 1, 'uni': 1, 'sye': 1, 'tini': 1, 'eke': 1, 'oke': 1, 'take': 1},
	'-PL': {},
	'-GEN': {'r': 1},
	'NEG': {'na': 1},
	'and': {'ebon': 1, 'ar': 1},
	'or': {'ba': 1},
	'zero': {'syunya': 1},
	'one': {'ak': 1},
	'two': {'dui': 1},
	'three': {'tin': 1},
	'four': {'tyar': 1},
	'five': {'paty': 1},
	'six': {'tyoe': 1},
	'seven': {'syat': 1},
	'eight': {'at': 1},
	'nine': {'noe': 1},
	'ten': {'dosy': 1},
	'hundred': {'syata': 1, 'ekasy': 1},
	'thousand': {'adyar': 1},
	}

cmn = {
	'#native': 955,
	'#total': 1026,
	'#family': 1268, # Sino-Tibetan
	'human': {'sen': 1},
	'child': {'kaidyi': 1, 'artun': 1},
	'big': {'da': 1, 'dai': 1, 'tai': 1},
	'small': {'syau': 1},
	# 'old': {'dyu': 1, 'rau': 1, 'gurau': 1},
	# 'young': {},
	# 'fire': {},
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
	'hundred': {'bai': 1},
	'thousand': {'tyen': 1},
}

en = {
	'#native': 360,
	'#total': 841,
	'#family': 2914, # Indo-European
	'human': {'yuman': 1},
	'child': {'tyaird': 1, 'kid': 1},
	'big': {'big': 1, 'rardy': 1, 'greit': 1},
	'small': {'smar': 1, 'ritar': 1, 'taini': 1},
	# 'old': {'ourd': 1},
	# 'young': {'yon': 1},
	# 'fire': {'pair': 1},
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
	'hundred': {'ondred': 1},
	'thousand': {'tausand': 1},
	}

es = {
	'#native': 405,
	'#total': 489,
	'#family': 2914, # Indo-European
	'human': {'umano': 1, 'umana': 1},
	'child': {'ninyo': 1, 'ninya': 1, 'tyiko': 1, 'tyika': 1},
	'big': {'grande': 1},
	'small': {'pekenyo': 1, 'pekenya': 1, 'tyiko': 1, 'tyika': 1},
	# 'old': {'kadim': 1, 'musin': 1},
	# 'young': {},
	# 'fire': {},
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
	'hundred': {'syen': 1, 'syento': 1},
	'thousand': {'mir': 1},
	}

fr = {
	'#native': 74,
	'#total': 163,
	'#family': 2914, # Indo-European
	'human': {'yumen': 1},
	'child': {'anpan': 1},
	'big': {'gran': 1, 'grand': 1},
	'small': {'pati': 1, 'patit': 1},
	'water': {'o': 1},
	'1s': {'sya': 1, 'ma': 1, 'mwa': 1},
	'2s': {'tyu': 1, 'ta': 1, 'twa': 1, 'bu': 1},
	'3s': {'ir': 1, 'er': 1, 'ra': 1, 'rwi': 1},
	'-PL': {'s': 1},
	'-GEN': {},
	'NEG': {'na': 1, 'pa': 1},
	'and': {'e': 1},
	'or': {'u': 1},
	'zero': {'sero': 1},
	'one': {'en': 1},
	'two': {'dyo': 1},
	'three': {'trwa': 1},
	'four': {'katr': 1},
	'five': {'senk': 1},
	'six': {'sis': 1},
	'seven': {'set': 1},
	'eight': {'wit': 1},
	'nine': {'nyop': 1},
	'ten': {'dis': 1},
	'hundred': {'san': 1},
	'thousand': {'mir': 1},
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
	'hundred': {'sau': 1, 'saikra': 1},
	'thousand': {'asar': 1, 'saasr': 1},
	}

ja = {
	'#native': 125,
	'#total': 128,
	'#family': 129, # Japonic
	'human': {'ningen': 1, 'kyito': 1},
	'child': {'kodomo': 1, 'ko': 1},
	'big': {'oki': 1, 'okina': 1},
	'small': {'tyisai': 1},
	'water': {'misu': 1},
	'1s': {'watasi': 1, 'watakusi': 1, 'ware': 1, 'ore': 1, 'boku': 1, 'atasi': 1, 'atakusi': 1},
	'2s': {'anata': 1, 'anta': 1, 'otaku': 1, 'omae': 1, 'kimi': 1},
	'3s': {'kore': 1,'sore': 1, 'are': 1}, #??
	'-PL': {'tati': 1, 'ra': 1, 'tomo': 1},
	'-GEN': {'no': 1},
	'NEG': {'nai': 1, 'masen': 1},
	'and': {'to': 1, 'katu': 1, 'ya': 1},
	'or': {'matawa': 1, 'aruiwa': 1, 'ka': 1, 'soretomo': 1},
	'zero': {'rei': 1, 'sero': 1},
	'one': {'iti': 1, 'kyito': 1},
	'two': {'ni': 1, 'puta': 1},
	'three': {'san': 1, 'mi': 1},
	'four': {'yo': 1, 'yon': 1, 'si': 1},
	'five': {'go': 1, 'itu': 1},
	'six': {'mu': 1, 'roku': 1},
	'seven': {'siti': 1, 'nana': 1},
	'eight': {'hati': 1, 'ya': 1},
	'nine': {'ku': 1, 'kyu': 1, 'kono': 1},
	'ten': {'so': 1, 'to': 1},
	'hundred': {'yaku': 1},
	'thousand': {'sen': 1},
	}

jv = {
	'#native': 82,
	'#total': 84,
	'#family': 323, # Austronesian
	'human': {'manunsa': 1},
	'child': {'anak': 1}, #??
	'big': {'gede': 1},
	'small': {'tyilik': 1, 'arit': 1},
	'water': {'banyu': 1},
	'1s': {'aku': 1, 'kura': 1, 'darem': 1},
	'2s': {'kowe': 1, 'sampeyan': 1, 'pandyenenan': 1}, #????
	'3s': {'deweke': 1, 'pandyenenanipun': 1}, #????
	'-PL': {},
	'-GEN': {},
	'NEG': {'dudu': 1, 'ora': 1},
	'and': {'ran': 1, 'sarta': 1},
	'or': {}, #????
	'zero': {'nor': 1},
	'one': {'sidyi': 1, 'setungar': 1},
	'two': {'roro': 1, 'kali': 1},
	'three': {'telu': 1, 'tiga': 1},
	'four': {'papat': 1, 'sekawan': 1},
	'five': {'rima': 1, 'gansai': 1},
	'six': {'enem': 1},
	'seven': {'pitu': 1},
	'eight': {'woru': 1},
	'nine': {'sana': 1},
	'ten': {'sepulu': 1, 'sedasa': 1},
	'hundred': {'atus': 1},
	'thousand': {'ewu': 1},
	}

ms = {
	'#native': 77,
	'#total': 163,
	'#family': 323, # Austronesian
	'human': {'manusya': 1},
	'child': {'ana': 1},
	'big': {'basar': 1, 'raya': 1, 'gadan': 1},
	'small': {'ketyir': 1},
	'water': {'air': 1},
	'1s': {'aku': 1, 'saya': 1},
	'2s': {'kamu': 1, 'anda': 1},
	'3s': {'ya': 1, 'dya': 1},
	'-PL': {'an': 1}, #??
	'-GEN': {},
	'NEG': {'tida': 1},
	'and': {'dan': 1},
	'or': {'atau': 1},
	'zero': {'koson': 1, 'sipar': 1, 'nor': 1, 'nier': 1},
	'one': {'satu': 1, 'asa': 1, 'tungar': 1, 'eka': 1, 'aat': 1},
	'two': {'dua': 1, 'dwi': 1},
	'three': {'tiga': 1, 'teru': 1, 'tari': 1},
	'four': {'ampat': 1, 'tyator': 1},
	'five': {'rima': 1, 'pantya': 1},
	'six': {'anam': 1},
	'seven': {'tudyo': 1, 'pitu': 1, 'sapta': 1},
	'eight': {'rapan': 1, 'sarapan': 1, 'asta': 1},
	'nine': {'sambiran': 1, 'sarapan': 1, 'nawa': 1},
	'ten': {'sapulo': 1, 'ekadasa': 1},
	'hundred': {'ratus': 1},
	'thousand': {'ribu': 1},
	}

pa = {
	'#native': 102,
	'#total': 92,
	'#family': 2914, # Indo-European
	'human': {'manuk': 1},
	'child': {'batya': 1},
	'big': {'bara': 1},
	'small': {'tyota': 1},
	'water': {'pani': 1},
	'1s': {'me': 1},
	'2s': {'tun': 1, 'tusin': 1},
	'3s': {'e': 1, 'is': 1, 'enan': 1, 'o': 1, 'us': 1, 'onan': 1},
	'-PL': {'an': 1, 'e': 1, 'ian': 1},
	'-GEN': {'da': 1, 'di': 1},
	'NEG': {'nain': 1},
	'and': {'ate': 1},
	'or': {'dya': 1}, #???
	'zero': {'sipar': 1},
	'one': {'ik': 1},
	'two': {'do': 1},
	'three': {'tin': 1},
	'four': {'tyar': 1},
	'five': {'pandy': 1},
	'six': {'tye': 1},
	'seven': {'sat': 1},
	'eight': {'at': 1},
	'nine': {'naun': 1},
	'ten': {'das': 1},
	'hundred': {'sau': 1},
	'thousand': {'asar': 1},
	}

pt = {
	'#native': 215,
	'#total': 231,
	'#family': 2914, # Indo-European
	'human': {'umanu': 1, 'umana': 1},
	'child': {'piryu': 1, 'pirya': 1, 'kriansa': 1, 'mininu': 1, 'minina': 1},
	'big': {'grandyi': 1},
	'small': {'pikenu': 1, 'pikena': 1},
	'water': {'agwa': 1},
	'1s': {'eu': 1, 'me': 1, 'mi': 1, 'min': 1},
	'2s': {'tu': 1, 'te': 1, 'tyi': 1, 'bose': 1},
	'3s': {'eri': 1, 'era': 1, 'u': 1, 'ru': 1, 'nu': 1, 'a': 1, 'ra': 1, 'na': 1},
	'-PL': {'s': 1, 'is': 1},
	'-GEN': {},
	'NEG': {'naun': 1, 'nun': 1},
	'and': {'i': 1},
	'or': {'ou': 1},
	'zero': {'seru': 1},
	'one': {'un': 1},
	'two': {'dois': 1},
	'three': {'tres': 1},
	'four': {'kwatru': 1},
	'five': {'sinku': 1},
	'six': {'seis': 1},
	'seven': {'setyi': 1},
	'eight': {'oitu': 1},
	'nine': {'nobi': 1},
	'ten': {'des': 1},
	'hundred': {'sein': 1, 'sentu': 1},
	'thousand': {'mir': 1},
	}

ru = {
	'#native': 155,
	'#total': 276,
	'#family': 2914, # Indo-European
	'human': {'tyirawek': 1, 'tyek': 1},
	'child': {'ribyonak': 1, 'dyitya': 1},
	'big': {'barsoi': 1, 'barsoye': 1, 'barsaya': 1, 'wirikii': 1, 'wirikaya': 1, 'wirikoye': 1, 'krupnii': 1, 'krupnaya': 1, 'krupnoye': 1},
	'small': {'marinkii': 1, 'marinkaya': 1, 'marinkoye': 1, 'marii': 1, 'maraya': 1, 'maroye': 1},
	'water': {'wada': 1},
	'1s': {'ya': 1, 'minya': 1},
	'2s': {'ti': 1, 'tibya': 1, 'wi': 1, 'was': 1},
	'3s': {'on': 1, 'ano': 1, 'ana': 1, 'yiwo': 1, 'niwo': 1},
	'-PL': {'i': 1, 'op': 1, 'a': 1, 'ya': 1, 'ei': 1},
	'-GEN': {'i': 1, 'a': 1, 'ya': 1},
	'NEG': {'ne': 1, 'ni': 1},
	'and': {'i': 1, 'da': 1},
	'or': {'iri': 1, 'ribo': 1},
	'zero': {'nur': 1, 'nor': 1, 'siro': 1},
	'one': {'adin': 1},
	'two': {'dwa': 1},
	'three': {'tri': 1},
	'four': {'tyitirya': 1},
	'five': {'pyat': 1},
	'six': {'sest': 1},
	'seven': {'sem': 1},
	'eight': {'wosim': 1},
	'nine': {'dewit': 1},
	'ten': {'desit': 1},
	'hundred': {'sto': 1, 'sotnya': 1},
	'thousand': {'tisyatya': 1},
	}

sw = {
	'#native': 26,
	'#total': 150, # ????
	'#family': 437, # Niger-Congo
	'human': {'binadamu': 1},
	'child': {'mtoto': 1, 'mwana': 1},
	'big': {'kubwa': 1},
	'small': {'dogo': 1},
	'water': {'madyi': 1},
	'1s': {'mimi': 1, 'ni': 1},
	'2s': {'wewe': 1, 'u': 1, 'ku': 1},
	'3s': {'yeye': 1, 'a': 1, 'yu': 1, 'm': 1},
	'-PL': {},
	'-GEN': {},
	'NEG': {'i': 1},
	'and': {'na': 1},
	'or': {'au': 1},
	'zero': {'sipuri': 1}, #????
	'one': {'modya': 1, 'mosi': 1},
	'two': {'wiri': 1, 'piri': 1},
	'three': {'tatu': 1},
	'four': {'nne': 1},
	'five': {'tano': 1},
	'six': {'sita': 1},
	'seven': {'saba': 1},
	'eight': {'nane': 1},
	'nine': {'tisa': 1},
	'ten': {'kumi': 1},
	'hundred': {'mia': 1},
	'thousand': {'erpu': 1},
	}

yo = {
	'#native': 28,
	'#total': 19,
	'#family': 437, # Niger-Congo
	'human': {'omoniyan': 1, 'eniyan': 1},
	'child': {'omo': 1, 'ewe': 1},
	'big': {'nra': 1, 'tobi': 1, 'gborin': 1},
	'small': {'kere': 1, 'die': 1},
	'water': {'omi': 1},
	'1s': {'emi': 1, 'mi': 1},
	'2s': {'iwo': 1},
	'3s': {'oun': 1, 'un': 1, 'o': 1},
	'-PL': {},
	'-GEN': {},
	'NEG': {'ko': 1},
	'and': {'ati': 1},
	'or': {'tabi': 1},
	'zero': {'odo': 1}, #????
	'one': {'eni': 1, 'okan': 1},
	'two': {'edyi': 1},
	'three': {'eta': 1},
	'four': {'erin': 1},
	'five': {'arun': 1},
	'six': {'epa': 1},
	'seven': {'edye': 1},
	'eight': {'edyo': 1},
	'nine': {'esan': 1},
	'ten': {'ewa': 1},
	'hundred': {'ogorun': 1},
	'thousand': {'egberun': 1},
	}

def distance(w1, w2):
	return edit_distance(w1, w2)

def getFitnessFunction(langs, word, weightFunc, avg=True):
	if not avg:
		return gff2(langs, word, weightFunc)
	words = defaultdict(int)
	for l in langs:
		weightSum = sum([v for k,v in l[word].items()])
		for wd,wt in l[word].items():
			words[wd] += weightFunc(l) * wt/weightSum
	return lambda w: -1 * sum([wt * distance(w, wd) for wd, wt in words.items()])

def gff2(langs, word, weightFunc):
	def ff(w):
		cost = 0
		for l in langs:
			if len(l[word]) > 0:
				cost += weightFunc(l) * min(map(lambda x: distance(w, x), l[word]))
		return -1 * cost
	return ff

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

def gen_words(langs, words, weightFunc, popsize, generations, mutationProb, avg=True):
	out = {}
	for word in words:
		fitness = getFitnessFunction(langs, word, weightFunc, avg)
		population = []
		for l in langs:
			for wd, wt in l[word].items():
				population.append(wd)
		popfactor = math.ceil(popsize/len(population))
		ga = GA(population * popfactor, fitness, rs, rep, mutationProb, mut)
		ga.run(generations)
		sortedPop = sorted(ga.population, key=fitness, reverse=True)
		out[word] = list(zip(sortedPop, map(fitness, sortedPop)))
		print('best for %s: %s (fitness %f)' % (word, out[word][0][0], out[word][0][1]))
	return out

def pick_words(langs, words, weightFunc):
	out = {}
	for word in words:
		candidates = []
		fitness = getFitnessFunction(langs, word, weightFunc)
		for l in langs:
			for wd, wt in l[word].items():
				candidates.append(wd)
		out[word] = sorted(candidates, key=fitness, reverse=True)[0]
	return out

