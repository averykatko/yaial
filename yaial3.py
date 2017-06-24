#!/usr/bin/env python3
import json
import heapq
import math
from distance import *

def mylog2(n):
	table = [
		0, 58, 1, 59, 47, 53, 2, 60, 39, 48, 27, 54, 33, 42, 3, 61,
		51, 37, 40, 49, 18, 28, 20, 55, 30, 34, 11, 43, 14, 22, 4, 62,
		57, 46, 52, 38, 26, 32, 41, 50, 36, 17, 19, 29, 10, 13, 21, 56,
		45, 25, 31, 35, 16, 9, 12, 44, 24, 15, 8, 23, 7, 6, 5, 63 ]

	n |= n >> 1;
	n |= n >> 2;
	n |= n >> 4;
	n |= n >> 8;
	n |= n >> 16;
	n |= n >> 32;

	return table[(n * 0x03f6eaf2cd271461) >> 58]

class Candidate(object):
	"""docstring for Candidate"""
	def __init__(self, word, utility=0.0):
		super(Candidate, self).__init__()
		self.word = word
		self.utility = utility

	def __lt__(self, other):
		return self.utility < other.utility
	def __le__(self, other):
		return self.utility <= other.utility
	def __eq__(self, other):
		return self.utility == other.utility
	def __ne__(self, other):
		return self.utility != other.utility
	def __gt__(self, other):
		return self.utility > other.utility
	def __ge__(self, other):
		return self.utility >= other.utility

candidates = []
langdata = None

Initials = "'mpbntdslkg"
Vowels = "aeiou"
NumInitials = len(Initials)
NumVowels = len(Vowels)
NumSylls = NumInitials * NumVowels
LogNumSylls = math.log(NumSylls)

def mylog(n):
	return 0.0 if 0 == n else math.log(n)

def get_utility(word, meaning):
	utility = 0.0
	for lang, langwords in langdata.items():
		entries = langwords[meaning]
		total = sum(entries.values())
		weightedDists = sum([((weight/total) * (edit_distance(word, srcWord)/max(len(word),len(srcWord)))) for srcWord, weight in entries.items()])
		utility += math.log(langwords['#family']) * weightedDists
	return utility

def generate_word(word):
	for i in range(len(candidates)):
		candidates[i].utility = get_utility(candidates[i].word, word)
	heapq.heapify(candidates)
	return candidates[0]

def nsyll_words(n):
	return NumSylls ** n

def syll_initial(syll):
	return Initials[syll // NumVowels]

def syll_vowel(syll):
	return Vowels[syll % NumVowels]

def word_nsylls(word):
	return math.floor(mylog(word) // LogNumSylls) + 1

def word_string(word):
	nsyll = word_nsylls(word)
	nchars = nsyll * 2
	s = ""
	for i in range(0, nchars, 2):
		lastSyll = word % NumSylls
		s += syll_initial(lastSyll)
		s += syll_vowel(lastSyll)
		word //= NumSylls
	return s

def init(maxSylls):
	fp = open("sourcewords.json", "r")
	global langdata
	langdata = json.load(fp)
	fp.close()
	global candidates
	candidates = []
	for i in range(nsyll_words(maxSylls)):
		candidates.append(Candidate(word_string(i)))

