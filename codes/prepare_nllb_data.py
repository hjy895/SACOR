#!/usr/bin/env python
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NLLBDatasetPreparation:
	"""Prepares datasets for NLLB fine-tuning with both base and augmented configurations."""
	
	def __init__(self, data_dir: str, output_dir: str):
		"""
		Initialize dataset preparation.
		Args:
			data_dir: Directory containing source TSV files
			output_dir: Directory to save processed datasets
		"""
		self.data_dir = Path(data_dir)
		self.output_dir = Path(output_dir)
	
	def read_tsv_file(self, file_path: str) -> Tuple:
		"""
		Read TSV file with language-specific structure.
		Args:
			file_path: Path to TSV file
		Returns:
			Tuple of (English sources, targets)
		"""
		try:
			source_en, target = [], []
			
			with open(file_path, 'r', encoding='utf-8') as f:
				lines = f.read().splitlines()
				if len(lines) <= 1:  # Empty or header-only file
					logger.warning(f"Empty or header-only file: {file_path}")
					return source_en, target
				
				for line in lines[1:]:  # Skip header
					columns = line.strip().split('\t')
					if len(columns) < 2:
						logger.warning(f"Skipping malformed line in {file_path}: {line}")
						continue
						
					source_en.append(columns[0].strip())
					target.append(columns[1].strip())
			
			logger.info(f"Read {len(source_en)} examples from {file_path}")
			return source_en, target
			
		except Exception as e:
			logger.error(f"Error reading TSV file {file_path}: {str(e)}")
			raise

	def shuffle_dataset(self, dataset: Dict, seed: int = 42) -> Dict:
		"""
		Shuffle source and target pairs consistently.
		Args:
			dataset: Dictionary with 'source' and 'target' lists
			seed: Random seed for reproducibility
		Returns:
			Shuffled dataset
		"""
		random.seed(seed)
		for split in dataset:
			if len(dataset[split]['source']) > 0:
				pairs = list(zip(dataset[split]['source'], dataset[split]['target']))
				random.shuffle(pairs)
				dataset[split]['source'], dataset[split]['target'] = zip(*pairs)
				dataset[split]['source'] = list(dataset[split]['source'])
				dataset[split]['target'] = list(dataset[split]['target'])
		return dataset

	def save_to_jsonl(self, dataset: Dict, output_path: Path):
		"""Save dataset to JSONL format with both combined and language-specific files."""
		jsonl_dir = output_path / 'jsonl'
		jsonl_dir.mkdir(parents=True, exist_ok=True)
		
		# Track unique pairs to avoid duplicates
		seen_pairs = set()
		
		for split in dataset:
			# Dictionary to store entries by language pair
			lang_pairs = {}
			all_entries = []
			
			for src, tgt in zip(dataset[split]['source'], dataset[split]['target']):
				try:
					src_parts = src.split(' ', 1)
					tgt_parts = tgt.split(' ', 1)
					
					if len(src_parts) != 2 or len(tgt_parts) != 2:
						logger.warning(f"Skipping malformed entry: {src} ||| {tgt}")
						continue
					
					src_lang, src_text = src_parts
					tgt_lang, tgt_text = tgt_parts
					
					# Create unique key for deduplication
					pair_key = (src_text, tgt_text)
					if pair_key in seen_pairs:
						continue
					
					seen_pairs.add(pair_key)
					
					# Create entry with exactly two languages
					entry = {
						"translation": {
							src_lang: src_text,
							tgt_lang: tgt_text
						}
					}
					
					# Add to all entries
					all_entries.append(entry)
					
					# Add to language-specific collection
					lang_pair = f"{src_lang}-{tgt_lang}"
					if lang_pair not in lang_pairs:
						lang_pairs[lang_pair] = []
					lang_pairs[lang_pair].append(entry)
					
				except Exception as e:
					logger.warning(f"Error processing entry: {str(e)}")
					continue
			
			# Save language-specific files
			for lang_pair, entries in lang_pairs.items():
				output_file = jsonl_dir / f"{lang_pair}.{split}.jsonl"
				with open(output_file, 'w', encoding='utf-8') as f:
					for entry in entries:
						json.dump(entry, f, ensure_ascii=False)
						f.write('\n')
				logger.info(f"Created {lang_pair} file {output_file} with {len(entries)} entries")

	def save_dataset(self, dataset: Dict, name: str):
		"""Save dataset in both standard and JSONL formats."""
		output_path = self.output_dir / name
		output_path.mkdir(parents=True, exist_ok=True)
		
		# Save standard format
		for split in ['train', 'val']:
			if split in dataset and dataset[split]['source']:
				with open(output_path / f"{split}.source", 'w', encoding='utf-8') as f:
					f.write('\n'.join(dataset[split]['source']))
				with open(output_path / f"{split}.target", 'w', encoding='utf-8') as f:
					f.write('\n'.join(dataset[split]['target']))
		
		# Save JSONL format
		self.save_to_jsonl(dataset, output_path)
		
		# Print statistics
		logger.info(f"\nDataset '{name}' statistics:")
		for split in ['train', 'val']:
			if split in dataset:
				logger.info(f"{split}: {len(dataset[split]['source'])} examples")

	def prepare_base_dataset(self) -> Dict:
		"""Prepare base dataset with source and target translations."""
		dataset = {
			'train': {'source': [], 'target': []},
			'val': {'source': [], 'target': []}
		}
		
		# Language code mapping for South Asian languages
		lang_code_map = {
			'PAN': ('pan_Arab', False),  # Punjabi (Shahmukhi)
			'PBT': ('pbt_Arab', True),   # Pashto
			'SND': ('snd_Arab', True),   # Sindhi
			'SKR': ('skr_Arab', True),   # Saraiki
			'URD': ('urd_Arab', True),   # Urdu
			'BAL': ('bal_Arab', True),   # Balochi
			'HND': ('hnd_Arab', True),   # Hindko
			'BRH': ('brh_Arab', True)    # Brahui
		}
		
		for split in ['train', 'val']:
			for file_path in self.data_dir.glob(f'*-{split}.tsv'):
				if 'trnltr' in file_path.name:
					continue
				
				lang_code = file_path.name.split('-')[0]
				if lang_code not in lang_code_map:
					logger.warning(f"Unknown language code: {lang_code}, skipping")
					continue
				
				target_code, _ = lang_code_map[lang_code]
				
				source_en, target = self.read_tsv_file(str(file_path))
				
				# Add source-target pairs
				for en, tgt in zip(source_en, target):
					dataset[split]['source'].append(f"{target_code} {tgt}")
					dataset[split]['target'].append(f"eng_Latn {en}")
		
		return dataset

	def prepare_augmented_dataset(self) -> Dict:
		"""Prepare augmented dataset with additional translations."""
		# For now, same as base - can be extended with additional reference translations
		return self.prepare_base_dataset()

def main():
	# Configuration
	data_dir = "../datasets"
	output_dir = "../fine-tune"
	
	try:
		# Initialize processor
		processor = NLLBDatasetPreparation(
			data_dir=data_dir,
			output_dir=output_dir
		)
		
		# 1. Base configuration
		logger.info("\nProcessing base configuration...")
		base_dataset = processor.prepare_base_dataset()
		base_dataset = processor.shuffle_dataset(base_dataset)
		processor.save_dataset(base_dataset, "base")
		
		# 2. Augmented configuration
		logger.info("\nProcessing augmented configuration...")
		augmented_dataset = processor.prepare_augmented_dataset()
		augmented_dataset = processor.shuffle_dataset(augmented_dataset)
		processor.save_dataset(augmented_dataset, "augmented")
		
		logger.info("\nDataset preparation completed!")
		logger.info("Datasets have been saved in both standard and JSONL formats.")
		
	except Exception as e:
		logger.error(f"Error during dataset preparation: {str(e)}", exc_info=True)
		raise

if __name__ == "__main__":
	main()

