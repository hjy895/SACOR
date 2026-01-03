"""
This script creates a benchmark for MT evaluation and training based on individual tsv files.
It is run after processing where the most common sentences across datasets are extracted.
This script selects sentences for each language and then, aligns them to the original spreadsheets.

This generates the train/val/test datasets with complete metadata.

-- PARUR-NLP
"""

import json

def count_overlap_source(dataset_1: list, dataset_2: list) -> int:
	# given two datasets containing parallel sentences, count the number of source sentences that are common in the two datasets
	sources_1 = {line.split("\t")[0] for line in dataset_1}
	sources_2 = {line.split("\t")[0] for line in dataset_2}

	# Find the intersection of the two sets
	overlap = sources_1 & sources_2

	# Return the number of common source sentences
	return len(overlap)


def get_stats(dataset: list):
	dialects = {}
	variety = {}
	translators = {}
	variety_region = {}
	
	for line in dataset:
		parts = line.split("\t")
		if len(parts) >= 5:
			# en_sentence, target_sentence, variety, region, translator
			var = parts[2].strip()
			reg = parts[3].strip()
			trans = parts[4].strip()
			
			variety[var] = variety.get(var, 0) + 1
			translators[trans] = translators.get(trans, 0) + 1
			variety_region[f"{var} - {reg}"] = variety_region.get(f"{var} - {reg}", 0) + 1
	
	return {
		"variety": variety,
		"translators": translators,
		"variety_region": variety_region
	}

