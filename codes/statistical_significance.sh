#!/bin/bash

# Base directory
BASE_DIR="../experiments/evaluation_results"

# Array of folder names
FOLDERS=(
  "nllb_finetuned_augmented"
  "nllb_finetuned_base"
)

# Array of file names
FILES=(
  "PAN_translations.tsv"
  "PBT_translations.tsv"
  "SND_translations.tsv"
  "SKR_translations.tsv"
  "URD_translations.tsv"
  "BAL_translations.tsv"
  "HND_translations.tsv"
  "BRH_translations.tsv"
)

# Create a results directory
mkdir -p results

# Loop through each folder and file combination
for folder in "${FOLDERS[@]}"; do
  # Create a folder-specific results directory
  mkdir -p "results/$folder"
  
  echo "Processing folder: $folder"
  
  for file in "${FILES[@]}"; do
    echo "  Processing file: $file"
    
    # Full path to the current file
    FULL_PATH="$BASE_DIR/$folder/$file"
    
    # Extract language code from filename
    LANG_CODE=$(echo "$file" | cut -d'_' -f1)
    
    # Output files
    RESULT_FILE="results/$folder/${LANG_CODE}_results.txt"
    
    # Run the command and save output to file
    echo "Running sacrebleu for $LANG_CODE in $folder..." | tee -a "$RESULT_FILE"
    echo "File: $file" | tee -a "$RESULT_FILE"
    
    # Extract columns and run sacrebleu
    sacrebleu <(awk -F'\t' '{print $2}' "$FULL_PATH") \
              -i <(awk -F'\t' '{print $3}' "$FULL_PATH") \
              -m bleu chrf --confidence -f text --short | tee -a "$RESULT_FILE"
    
    echo "" | tee -a "$RESULT_FILE"  # Add a blank line for readability
  done
  
  echo "Completed processing folder: $folder"
  echo ""
done

echo "All processing complete. Results saved in the 'results' directory."

