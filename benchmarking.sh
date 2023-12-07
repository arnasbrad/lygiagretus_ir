#!/bin/bash

# Define arrays of thread counts and resize factors
thread_counts=(1 2 4 8)
resize_factors=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1)

# Output file name
output_file="results.csv"

# Output header for Excel
echo "Resize Factor,Thread Count,Output" > "$output_file"

# Loop to run the entire process 5 times
for i in {1..5}; do
    # Loop through each combination of resize factor and thread count
    for resize_factor in "${resize_factors[@]}"; do
        for thread_count in "${thread_counts[@]}"; do
            # Capture the output of the python script
            output=$(python3 main.py $thread_count $resize_factor)

            # Output in CSV format and append to the file
            echo "$resize_factor,$thread_count,$output" >> "$output_file"
        done
    done
done

