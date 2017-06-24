#include <stdio.h>
#include <stdlib.h>
#include "cJSON.h"

int main(int argc, char const *argv[])
{
	char *jsonString = "{\"foo\": \"bar\"}";
	cJSON *jsonRoot = cJSON_Parse(jsonString);
	printf("%s\n", jsonRoot->child->string);
	cJSON_Delete(jsonRoot);
	return 0;
}