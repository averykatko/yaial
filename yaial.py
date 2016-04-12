#!/usr/bin/env python3
from distance import *
from collections import defaultdict
from GA import GA

ar = {
	'#native': 295,
	'human': {'ʔinsaːn': 1, 'bæʃɑr': 1},
	'child': {'tʕifl': 1},
	'big': {'kæbiːr': 1},
	'small': {'sʕɑgiːr': 1},
	'water': {'maːʔ': 1},
	'one': {'wɑːħid': 1},
	'two': {'iθnaːn': 1},
	'three': {'θæˈlæːθæ': 1},
	'four': {'ʔarbaʕa': 1},
	'five': {'xæmsæ': 1},
	'six': {'sitːa': 1},
	'seven': {'ˈsæbʕæ': 1},
	'eight': {'θamaːnija': 1},
	'nine': {'ˈtɪsʕæ': 1},
	'ten': {'ʕɑʃɑrɑ': 1},
}

cmn = {
	'#native': 955,
	'human': {'ʐɛn˧˥': 1},
	'child': {'xai˧˥ʦɨ': 1, 'aɻ˧˥tʰʊŋ˧˥': 1},
	'big': {'ta˥˩': 1, 'taj˥˩': 1, 'tʰaj˥˩': 1},
	'small': {'ɕjɑw': 1},
	'water': {'ʂwej': 1},
	'one': {'ji˥˥': 1},
	'two': {'aɻ˥˩': 1, 'liaŋ˨˩˦': 1},
	'three': {'san˥˥': 1},
	'four': {'sɨ˥˩': 1},
	'five': {'wu˨˩˦': 1},
	'six': {'ljow': 1},
	'seven': {'ʨʰi': 1},
	'eight': {'pa': 1},
	'nine': {'ʨjow': 1},
	'ten': {'ʂʐ': 1}, # ????
}

en = {
	'#native': 360,
	'human': {'hjumən': 1},
	'child': {'ʧajld': 1, 'kɪd': 1},
	'big': {'bɪg': 1, 'laɹʤ': 1, 'gɹejt': 1},
	'small': {'smɑl': 1, 'lɪtəl': 1, 'tajni': 1},
	'water': {'wɑtəɹ': 1},
	'one': {'wʌn': 1},
	'two': {'tu': 1},
	'three': {'θɹi': 1},
	'four': {'fɔːɹ': 1},
	'five': {'fajv': 1},
	'six': {'sɪks': 1},
	'seven': {'sɛvən': 1},
	'eight': {'ejt': 1},
	'nine': {'najn': 1},
	'ten': {'tɛn': 1},
	}

es = {
	'#native': 405,
	'human': {'umano': 1, 'umana': 1},
	'child': {'niɲo': 1, 'niɲa': 1, 'ʧiko': 1, 'ʧika': 1},
	'big': {'grande': 1},
	'small': {'pekeɲo': 1, 'pekeɲa': 1, 'ʧiko': 1, 'ʧika': 1},
	'water': {'aɣwa': 1},
	'one': {'uno': 1},
	'two': {'dos': 1},
	'three': {'trɛs': 1},
	'four': {'kwatro': 1},
	'five': {'siŋko': 1},
	'six': {'sɛs': 1},
	'seven': {'sjete': 1},
	'eight': {'oʧo': 1},
	'nine': {'nweβe': 1},
	'ten': {'djɛs': 1},
	}

hi = {
	'#native': 376, # Hindi + Urdu
	'human': {'mənʊʂjə': 1, 'ɪnsan': 1, 'admi': 1},
	'child': {'baʧa': 1, 'ʃiʃu': 1, 'bal': 1},
	'big': {'bəɽɑː': 1, 'bəɽi': 1},
	'small': {'ʧʰoʈa': 1, 'ʧʰoʈi': 1},
	'water': {'paːniː': 1, 'ʤəl': 1, 'aːb': 1},
	'one': {'ek': 1},
	'two': {'do': 1},
	'three': {'tin': 1},
	'four': {'ʧaːr': 1},
	'five': {'pa~ʧ': 1},
	'six': {'ʧʰɛɦ': 1},
	'seven': {'saːt': 1},
	'eight': {'aːtʰ': 1},
	'nine': {'nau': 1},
	'ten': {'das': 1},
	}

def borrow(word):
	word2 = ''
	for c in word:
		if c in 'aɑæɐəɜɒ':
			word2 += 'a'
		elif c in 'eɛøœ':
			word2 += 'e'
		elif c in 'oɔɤʌɵ':
			word2 += 'o'
		elif c in 'iɪyʏɨjɥ':
			word2 += 'i'
		elif c in 'uʊɯʉw':
			word2 += 'u'
		elif c in 'ˈ˨˦˩˧˥~hɦħʔʰʲʼ.:ː':
			continue
		else:
			word2 += c

	print(word2)

	haveOnset = False
	word3 = ''
	for c in word2:
		if c in 'aeiou':
			word3 += c + '.'
			haveOnset = False
		elif not haveOnset:
			word3 += c
			haveOnset = True
		else:
			if word3[-1] in 'ʦʣʧʤʨʥʃʒɕʑcɟçʝɲ':
				word3 += 'i.'
			else:
				word3 += 'a.'
			word3 += c
	if haveOnset:
		if word3[-1] in 'ʦʣʧʤʨʥʃʒɕʑcɟçʝɲ':
			word3 += 'i.'
		else:
			word3 += 'a.'
	word3 = word3[:-1]
	print(word3)

	out = ''
	for c in word3:
		if c in 'pbƥɓɸβfv':
			out += 'p'
		elif c in 'tdʈɖƭɗʦʣʧʤʨʥθð':
			out += 't'
		elif c in 'kgƙɠqʠɢʛxχɣʁʀcɟçʝ':
			out += 'k'
		elif c in 'szʃʒʂʐɬɮɕʑ':
			out += 's'
		elif c in 'm':
			out += 'm'
		elif c in 'nɲŋɴ':
			out += 'n'
		elif c in 'lʟɭrɹɽɾ':
			out += 'r'
		else:
			out += c
	return out

def distance(w1, w2):
	return edit_distance(w1, w2)

def getFitnessFunction(langs, word, weightFunc):
	words = defaultdict(int)
	for l in langs:
		weightSum = sum([v for k,v in l[word].items()])
		for wd,wt in l[word].items():
			words[wd] += weightFunc(l) * wt/weightSum
	return lambda w: -1 * sum([wt * distance(w, wd) for wd, wt in words.items()])

def compromise(langs, word, maxSylls, weightFunc):
	words = defaultdict(int)
	for l in langs:
		weightSum = sum([v for k,v in l[word].items()])
		for wd,wt in l[word].items():
			words[wd] += weightFunc(l) * wt/weightSum
	candidates = ['']
	for i in range(maxSylls):
		for cand in candidates:
			for c in [''] + list('ptkmnsr'):
				for v in 'aeiou':
					candidates.append(cand + c + v)
	def sortkey(cand):
		return sum([wt * distance(cand, wd) for wd, wt in words.items()])
	candidates.sort(sortkey)
	return candidates
