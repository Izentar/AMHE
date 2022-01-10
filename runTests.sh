#!/bin/bash
#
# Usage:
# bash runTests.sh -r 1 -f elli,rosen,sphere,hyperelli,rastrigin,schwefel,bukin,schaffer -o out
#

# Set decimal style as dots instead of commas
export LC_NUMERIC="en_US.UTF-8"

# Process arguments
#	-f for funciton names to run,
#	-o for output file name without extension,
#	-r repetitions
while getopts f:o:r: flag
do
    case "${flag}" in
        f) functions_to_run=${OPTARG};;
        o) output_file=${OPTARG};;
        r) reps=${OPTARG};;
    esac
done

# Process list of functions suppplied (comma separated)
IFS=', ' read -r -a functions_to_run <<< "$functions_to_run"

# Sweep sigma, dimension count, xstd and estd parameters for each function
for fun in "${functions_to_run[@]}"
do
	echo "Running tests for $fun function..."
	for dims in $(seq 5 5 10)
	do
		for sigma in $(seq 0.1 0.2 0.3)
		do
			for xstd in 1 10 100
			do
				# Run reference test
				python tests.py  --sigma $sigma --dim $dims --xstart gauss --xsgm 0 --xsgstd $xstd --estart dull --esgm 0 --esgstd 1 --testf $fun -r $reps -o $output_file.csv
			done
		done
	done
	for dims in $(seq 5 5 10)
	do
		for sigma in $(seq 0.1 0.2 0.3)
		do
			for xstd in 1 10 100
			do
				for estd in 1 10 100
				do
					# Run test with random init
					python tests.py  --sigma $sigma --dim $dims --xstart gauss --xsgm 0 --xsgstd $xstd --estart gauss --esgm 0 --esgstd $estd --testf $fun -r $reps -o $output_file.csv
				done
			done
		done
	done
done


