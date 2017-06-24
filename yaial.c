#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <math.h>

#include "cJSON.h"
#include "hashtable.h"
#include "hashtable_itr.h"

typedef struct hashtable hashtable_t;
typedef struct hashtable_itr iterator_t;

#ifdef USE_HT_FUNCTIONS
	DEFINE_HASHTABLE_INSERT(insert_lang, char, hashtable_t);
	DEFINE_HASHTABLE_SEARCH(search_lang, char, hashtable_t);
	DEFINE_HASHTABLE_REMOVE(remove_lang, char, hashtable_t);

	DEFINE_HASHTABLE_INSERT(insert_meaning, char, entry_list_t);
	DEFINE_HASHTABLE_SEARCH(search_meaning, char, entry_list_t);
	DEFINE_HASHTABLE_REMOVE(remove_meaning, char, entry_list_t);

	DEFINE_HASHTABLE_INSERT(insert_count, char, double);
	DEFINE_HASHTABLE_SEARCH(search_count, char, double);
	DEFINE_HASHTABLE_REMOVE(remove_count, char, double);
#elif defined(USE_HT_GENERICS)
	#define insert_lang(h,k,v) hashtable_insert(_Generic(h, hashtable_t *: h), _Generic(k, char *: k), _Generic(v, hashtable_t *: v))
	#define search_lang(h,k) (hashtable_t *)hashtable_search(_Generic(h, hashtable_t *: h), _Generic(k, char *: k))
	#define remove_lang(h,k) hashtable_remove(_Generic(h, hashtable_t *: h), _Generic(k, char *: k))

	#define insert_meaning(h,k,v) hashtable_insert(_Generic(h, hashtable_t *: h), _Generic(k, char *: k), _Generic(v, entry_list_t *: v))
	#define search_meaning(h,k) (entry_list_t *)hashtable_search(_Generic(h, hashtable_t *: h), _Generic(k, char *: k))
	#define remove_meaning(h,k) hashtable_remove(_Generic(h, hashtable_t *: h), _Generic(k, char *: k))

	#define insert_count(h,k,v) hashtable_insert(_Generic(h, hashtable_t *: h), _Generic(k, char *: k), _Generic(v, double *: v))
	#define search_count(h,k) (double *)hashtable_search(_Generic(h, hashtable_t *: h), _Generic(k, char *: k))
	#define remove_count(h,k) hashtable_remove(_Generic(h, hashtable_t *: h), _Generic(k, char *: k))
#else
	#define insert_lang hashtable_insert
	#define search_lang hashtable_search
	#define remove_lang hashtable_remove

	#define insert_meaning hashtable_insert
	#define search_meaning hashtable_search
	#define remove_meaning hashtable_remove

	#define insert_count hashtable_insert
	#define search_count hashtable_search
	#define remove_count hashtable_remove
#endif

int StatusCode = EXIT_SUCCESS;

#ifdef DEBUG
#define dbprintf(fmt, ...) printf("[%d] " fmt, __LINE__, ##__VA_ARGS__)
#endif

#define _err(fmt, ...) {fprintf(stderr, "[%d] " fmt, __LINE__, ##__VA_ARGS__); StatusCode = EXIT_FAILURE; goto End_Of_Program;}

#define OOM_ERROR() _err("out of memory\n")
#define FOPEN_ERROR(fn) _err("failed to open file %s\n", fn)
#define IO_ERROR() _err("error reading file\n")

// generic min and max macros (from http://stackoverflow.com/a/30918240)
#define GENERIC_MAX(x, y) ((x) > (y) ? (x) : (y))
#define GENERIC_MIN(x, y) ((x) <= (y) ? (x) : (y))

#define ENSURE_int(i)   _Generic((i), int:   (i))
#define ENSURE_float(f) _Generic((f), float: (f))
#define ENSURE_double(f) _Generic((f), double: (f))

#define MAX(type, x, y) \
	(type)GENERIC_MAX(ENSURE_##type(x), ENSURE_##type(y))

#define MIN(type, x, y) \
	(type)GENERIC_MIN(ENSURE_##type(x), ENSURE_##type(y))

// could possibly make inventory, phonotactics somewhat user-specified later
char Initials[] = "'mpbntdsrkg";
char Vowels[] = "aeiou";

int NumInitials;
int NumVowels;
int NumSylls;
double Log2NumSylls;

typedef uint_least64_t word_t;
typedef double util_t;

typedef struct
{
	word_t word;
	util_t utility;
} cand_t;

typedef struct
{
	char *string;
	double weight;
} entry_t;

typedef struct
{
	int length;
	entry_t *entries;
} entry_list_t;

//
util_t get_utility(word_t word, char *meaning, hashtable_t *table, hashtable_t *nums);

// 64-bit integer log2 (from http://stackoverflow.com/a/23000588)
// returns 0 for 0 (maybe desired here?)
int mylog2(uint_least64_t n);

// compare cand_t elements of the candidate array by utility when sorting
int compare(const void *p, const void *q);

static unsigned int hash_function(void *k);
static int keys_equal(void *k1, void *k2);

word_t nsyll_words(int n);
char syll_initial(word_t syll);
char syll_vowel(word_t syll);
int word_nsylls(word_t word);

// return new heap-allocated string for word index
char *word_string(word_t word);

// return levenshtein distance between s and t
int edit_distance(char *s, char *t);

int main(int argc, char const *argv[])
{
	// set global constants
	NumInitials = strlen(Initials);
	NumVowels = strlen(Vowels);
	NumSylls = NumInitials * NumVowels;
	Log2NumSylls = mylog2(NumSylls);

	word_t numCandidates = nsyll_words(MAX_SYLLS);
	cand_t *candidates = (cand_t *) calloc(numCandidates, sizeof(cand_t));
	if(NULL == candidates)
	{
		OOM_ERROR();
	}
	FILE *fp = fopen("sourcewords.json", "r");
	if(NULL == fp)
	{
		FOPEN_ERROR("sourcewords.json");
	}
	char *jsonString = NULL;
	size_t len = 0;
	if(-1 == getdelim(&jsonString, &len, '\0', fp))
	{
		IO_ERROR();
	}
	fclose(fp); // TODO error checking? (is it necessary for read-only, single-thread?)
	dbprintf("read jsonString: %s\n", jsonString);
	cJSON *jsonRoot = cJSON_Parse(jsonString);
	if(NULL == jsonRoot)
	{
		OOM_ERROR();
	}
	// load json data into hashtable for faster retrieval
	hashtable_t *langdata = create_hashtable(5, &hash_function, &keys_equal);
	hashtable_t *langnums = create_hashtable(5, &hash_function, &keys_equal); // for speaker counts etc
	for(cJSON *jsonLang = jsonRoot->child; NULL != jsonLang; jsonLang = jsonLang->next)
	{
		hashtable_t *meanings = create_hashtable(16, &hash_function, &keys_equal);
		hashtable_t *counts = create_hashtable(3, &hash_function, &keys_equal);
		// TODO test for oom
		for(cJSON *jsonMeaning = jsonLang->child; NULL != jsonMeaning; jsonMeaning = jsonMeaning->next)
		{
			if('#' == jsonMeaning->string[0])
			{
				// TODO if json freed, copy double, ...
				insert_count(counts, jsonMeaning->string, &(jsonMeaning->valuedouble));
				continue;
			}
			int size = 4;
			entry_t *entries = (entry_t *) calloc(size, sizeof(entry_t));
			if(NULL == entries)
			{
				OOM_ERROR();
			}
			int index = 0;
			for(cJSON *jsonEntry = jsonMeaning->child; NULL != jsonEntry; jsonEntry = jsonEntry->next)
			{
				if(index >= size)
				{
					size *= 2;
					entries = (entry_t *) realloc(entries, size);
					if(NULL == entries)
					{
						OOM_ERROR();
					}
				}
				// TODO if json object is to be freed after this, must copy strings
				entries[index].string = jsonEntry->string;
				entries[index].weight = jsonEntry->valuedouble;
				++index;
			}
			// TODO if json object is to be freed, must copy string key
			entry_list_t *entryList = (entry_list_t *) malloc(sizeof(entry_list_t));
			if(NULL == entryList)
				OOM_ERROR();
			entryList->length = size;
			entryList->entries = entries;
			insert_meaning(meanings, jsonMeaning->string, entryList);
		}
		// TODO if json object is to be freed, must copy string key
		insert_lang(langdata, jsonLang->string, meanings);
		insert_lang(langnums, jsonLang->string, counts);
	}

	// TODO possibly parallelize loop with OpenMP if speedup desirable?
	// TODO possibly incorporate first word's utility pass into this pass
	for(word_t i = 0; i < numCandidates; ++i)
	{
		candidates[i].word = i;
	}
	// TODO use something other than argv for this
	for (int j = 1; j < argc; ++j) // iterate thru meanings
	{
		// TODO possibly parallelize
		for(word_t i = 0; i < numCandidates; ++i)
		{
			candidates[i].utility = get_utility(candidates[i].word, argv[j], langdata, langnums);
		}
		qsort(candidates, numCandidates, sizeof(cand_t), &compare);
		// TODO output chosen words, possibly runners-up
		printf("best for %s: %s (%f)\n", argv[j], word_string(candidates[0].word), candidates[0].utility);
		for(int r = 1; r < 5; ++r)
		{
			printf("\t%dth best: %s (%f)\n", r+1, word_string(candidates[r].word), candidates[r].utility);
		}
		putchar('\n');
	}
	
	End_Of_Program: // on error, will goto here to ensure all memory freed
	// TODO free all memory allocated
	// free json object
	cJSON_Delete(jsonRoot);
	free(jsonRoot);
	// free candidates array
	free(candidates);
	// free hashtables including all sub-tables, arrays, strings, etc
	iterator_t *langIter = hashtable_iterator(langdata);
	hashtable_t *prevMeanings = NULL;
	if (NULL != langIter) do
	{
		hashtable_t *meanings = hashtable_iterator_value(langIter);
		hashtable_destroy(prevMeanings, 1);
		free(prevMeanings);
		prevMeanings = meanings;

		iterator_t *meaningIter = hashtable_iterator(meanings);
		entry_list_t *prevEntryList = NULL;
		entry_t *prevEntries = NULL;
		if (NULL != meaningIter) do
		{
			entry_list_t *entryList = hashtable_iterator_value(meaningIter);
			entry_t *entries = entryList->entries;
			for(int i = 0; NULL != prevEntryList && i < prevEntryList->length; ++i)
			{
				free(prevEntries[i].string);
			}
			free(prevEntryList);
			prevEntryList = entryList;
			free(prevEntries);
			prevEntries = entries;

		} while(hashtable_iterator_advance(meaningIter));

	} while(hashtable_iterator_advance(langIter));
	free(langIter);
	hashtable_destroy(langdata, 1);
	free(langdata);

	iterator_t *numsIter = hashtable_iterator(langnums);
	hashtable_t *prevCounts = NULL;
	if (NULL != numsIter) do
	{
		hashtable_t *counts = hashtable_iterator_value(numsIter);
		hashtable_destroy(prevCounts, 1);
		free(prevCounts);
		prevCounts = counts;

	} while(hashtable_iterator_advance(numsIter));
	free(numsIter);
	hashtable_destroy(langnums, 1);
	free(langnums);

	return StatusCode;
} // main

util_t get_utility(word_t word, char *meaning, hashtable_t *table, hashtable_t *nums)
{
	util_t utility = 0.0;
	char *wordString = word_string(word);
	iterator_t *langIter = hashtable_iterator(table);
	do//(...language in table...)
	{
		char *langname = hashtable_iterator_key(langIter);
		hashtable_t *meanings = hashtable_iterator_value(langIter);
		hashtable_t *counts = search_lang(nums, langname);
		char *numKey = "#family";
		double numSpeakers = *search_count(counts, numKey);
		entry_list_t *entryList = search_meaning(meanings, meaning);

		//sum counts
		double total = 0.0;
		for(int i = 0; i < entryList->length; ++i)
		{
			total += entryList->entries[i].weight;
		}
		//sum weighted distances
		double weightedDists = 0.0;
		for(int i = 0; i < entryList->length; ++i)
		{
			weightedDists += entryList->entries[i].weight * -edit_distance(wordString, entryList->entries[i].string) / total;
			// TODO maybe put normalization back when lang data first read in instead of doing every time
		}
		//add to utility weighted by speakers
		utility += numSpeakers * weightedDists;

	} while(hashtable_iterator_advance(langIter));
	free(langIter);
	free(wordString);
	return utility;
}

int mylog2(uint_least64_t n)
{
	static const int_least8_t table[64] = {
		0, 58, 1, 59, 47, 53, 2, 60, 39, 48, 27, 54, 33, 42, 3, 61,
		51, 37, 40, 49, 18, 28, 20, 55, 30, 34, 11, 43, 14, 22, 4, 62,
		57, 46, 52, 38, 26, 32, 41, 50, 36, 17, 19, 29, 10, 13, 21, 56,
		45, 25, 31, 35, 16, 9, 12, 44, 24, 15, 8, 23, 7, 6, 5, 63 };

	n |= n >> 1;
	n |= n >> 2;
	n |= n >> 4;
	n |= n >> 8;
	n |= n >> 16;
	n |= n >> 32;

	return table[(n * 0x03f6eaf2cd271461) >> 58];
}

int compare(const void *p, const void *q)
{
	util_t x = (*(const cand_t *)p).utility;
	util_t y = (*(const cand_t *)q).utility;
	if(x < y)
		return -1;
	else if(x > y)
		return 1;
	return 0;
}

// djb2 hash function by dan bernstein, from http://www.cs.yorku.ca/~oz/hash.html
static unsigned int hash_function(void *k)
{
	unsigned long hash = 5381;
	int c;

	while (c = *((char *)k++))
		hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

	return hash;
}

static int keys_equal(void *k1, void *k2)
{
	return (0 == strcmp((char *) k1, (char *) k2));
}

word_t nsyll_words(int n)
{
	return (word_t) pow(NumSylls, n);
}

char syll_initial(word_t syll)
{
	return Initials[syll / NumVowels];
}

char syll_vowel(word_t syll)
{
	return Vowels[syll % NumVowels];
}

int word_nsylls(word_t word)
{
	return floor(mylog2(word) / Log2NumSylls) + 1;
}

char *word_string(word_t word)
{
	word_t nsyll = word_nsylls(word);
	word_t nchars = nsyll * 2;
	char *s = (char *) calloc(nchars + 1, sizeof(char));
	for(int i = 0; i < nchars; i += 2)
	{
		word_t lastSyll = word % NumSylls;
		s[i] = syll_initial(lastSyll);
		s[i+1] = syll_vowel(lastSyll);
		word /= NumSylls;
	}
	return s;
}

int edit_distance(char *s, char *t)
{
	int n = strlen(s);
	int m = strlen(t);

	// degenerate cases
	if (0 == strcmp(s,t)) return 0;
	if (0 == n) return n;
	if (0 == m) return m;

	// create two work vectors of integer distances
	int v0[m + 1];
	int v1[m + 1];

	// initialize v0 (the previous row of distances)
	// this row is A[0][i]: edit distance for an empty s
	// the distance is just the number of characters to delete from t
	for (int i = 0; i <= m; ++i)
		v0[i] = i;

	for (int i = 0; i < n; ++i)
	{
		// calculate v1 (current row distances) from the previous row v0

		// first element of v1 is A[i+1][0]
		//   edit distance is delete (i+1) chars from s to match empty t
		v1[0] = i + 1;

		// use formula to fill in the rest of the row
		for (int j = 0; j <= m; ++j)
		{
			int cost = (s[i] == t[j]) ? 0 : 1;
			v1[j + 1] = MIN(int, v1[j] + 1, v0[j + 1] + 1);
			v1[j + 1] = MIN(int, v1[j+1], v0[j] + cost);
		}

		// copy v1 (current row) to v0 (previous row) for next iteration
		for (int j = 0; j <= m; ++j)
			v0[j] = v1[j];
	}

	return v1[m];
}
