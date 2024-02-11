#!/bin/bash

YOUR_ASM=$1
TEST=$2
TEST_NAME=$(basename -- "${TEST}")
as "$YOUR_ASM" "$TEST" -o merged.o

if [ -f "merged.o" ]; then
	ld merged.o -o merged.out
	if [ -f "merged.out" ]; then
		timeout 60s ./merged.out	
		if [ $? -eq 0 ]; then
			echo -e "${YOUR_ASM} tested with ${TEST_NAME}: \033[32mPASS\033[0m"
			STATUS=0
		else
			echo -e "${YOUR_ASM} tested with ${TEST_NAME}: \033[31mFAIL\033[0m"
			STATUS=1
		fi
	else
		echo -e "${YOUR_ASM} could not be created (ld stage) with ${TEST_NAME}: \033[31mFAIL\033[0m"
		STATUS=1	
	fi
else
	echo -e "${YOUR_ASM} could not be created (as stage) with ${TEST_NAME}: \033[31mFAIL\033[0m"
	STATUS=1		
fi

rm merged.*
exit ${STATUS}