#!/bin/bash
#
# Usage:
# bash runTests.sh -r 20 -f elli,rosen,sphere,hyperelli,rastrigin,schwefel,bukin,schaffer -o out
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

# Sweep sigma, dimension count, start_type parameters for each function
declare -a start_types=("gauss" "uniform" "exp")
# Keep stddev at 1 for now
xstd=1
estd=1
# Keep same seed
seed=123

for fun in "${functions_to_run[@]}"
do
	echo "Running tests for $fun function..."
	for start_type in "${start_types[@]}"
	do
		for dims in $(seq 5 5 10)
		do
			for sigma in 0.05 0.1 0.3 0.9
			do
				# Run reference test
				python tests.py -eps 0.5 0.25 0.1 0.01 0.001 0.0001 --sigma $sigma --dim $dims --seed $seed --xstart $start_type --xsgm 0 --xsgstd $xstd --estart dull --esgm 0 --esgstd 1 --xsumin 0 --xsumax 1 --esumin 0 --esumax 1 --esexpl 1 --xsexpl 1 --testf $fun -r $reps -o $output_file.csv
			done
		done
		for dims in $(seq 5 5 10)
		do
			for sigma in 0.05 0.1 0.3 0.9
			do
				# Run test with random init (gauss)
				python tests.py -eps 0.5 0.25 0.1 0.01 0.001 0.0001 --sigma $sigma --dim $dims --seed $seed --xstart $start_type --xsgm 0 --xsgstd $xstd --estart gauss --esgm 0 --esgstd $estd --xsumin 0 --xsumax 1 --esumin 0 --esumax 1 --esexpl 1 --xsexpl 0.1 --testf $fun -r $reps -o $output_file.csv
			done
		done
		for dims in $(seq 5 5 10)
		do
			for sigma in 0.05 0.1 0.3 0.9
			do
				# Run test with random init (uniform)
				python tests.py -eps 0.5 0.25 0.1 0.01 0.001 0.0001 --sigma $sigma --dim $dims --seed $seed --xstart $start_type --xsgm 0 --xsgstd $xstd --estart uniform --esgm 0 --esgstd $estd --xsumin 0 --xsumax 1 --esumin 0 --esumax 1 --esexpl 1 --xsexpl 0.1 --testf $fun -r $reps -o $output_file.csv
			done
		done
		for dims in $(seq 5 5 10)
		do
			for sigma in 0.05 0.1 0.3 0.9
			do
				# Run test with random init (exp)
				python tests.py -eps 0.5 0.25 0.1 0.01 0.001 0.0001 --sigma $sigma --dim $dims --seed $seed --xstart $start_type --xsgm 0 --xsgstd $xstd --estart exp --esgm 0 --esgstd $estd --xsumin 0 --xsumax 1 --esumin 0 --esumax 1 --esexpl 1 --xsexpl 0.1 --testf $fun -r $reps -o $output_file.csv
			done
		done
	done
done


