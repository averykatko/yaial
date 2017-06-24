CC = clang
CFLAGS = -g -std=c11 -D MAX_SYLLS=2 -D USE_HT_GENERICS -D DEBUG

default: yaial

yaial: yaial.c hashtable.h hashtable.c hashtable_itr.h hashtable_itr.c hashtable_private.h cJSON.h cJSON.c
	${CC} ${CFLAGS} yaial.c hashtable.c hashtable_itr.c cJSON.c -o yaial 

clean:
	rm -rf yaial *.o *.dSYM

#
