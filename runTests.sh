#!/bin/bash
#
# Usage:
# bash runTests.sh -f elli,rosen,sphere,hyperelli,rastrigin,schwefel,bukin,schaffer -o out
#

# Set decimal style as dots instead of commas
export LC_NUMERIC="en_US.UTF-8"

# Process arguments (-f for funciton names to run and -o for output file name without extension)
while getopts f:o: flag
do
    case "${flag}" in
        f) functions_to_run=${OPTARG};;
        o) output_file=${OPTARG};;
    esac
done

IFS=', ' read -r -a functions_to_run <<< "$functions_to_run"

for fun in "${functions_to_run[@]}"
do
	echo "Running tests for $fun function..."
	for dims in $(seq 8 8 16)
	do
		for sigma in $(seq 0.1 0.1 0.5)
		do
			# Run reference test
			python tests.py  --sigma $sigma --dim $dims --xstart gauss --xsgm 0 --xsgstd 1 --estart dull --esgm 0 --esgstd 1 --testf elli -r 1 -o $output_file.csv
			# Run test with random init
			python tests.py  --sigma $sigma --dim $dims --xstart gauss --xsgm 0 --xsgstd 1 --estart gauss --esgm 0 --esgstd 1 --testf elli -r 1 -o $output_file.csv
		done
	done
done