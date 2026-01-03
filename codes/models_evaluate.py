import torch
from transformers import M2M100ForConditionalGeneration, AutoTokenizer
from sacrebleu.metrics import BLEU, CHRF
import pandas as pd
from pathlib import Path
import json
import time
from tqdm import tqdm

# Evaluation script for X>Eng MT models
def load_test_data(file_path, lang_code):
	"""Load test data from TSV file"""
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			_ = f.readline()  # skip header
			lines = f.readlines()
		
		english_refs = []  # English references
		source_texts = []  # Source language texts
		
		for line in lines:
			parts = line.strip().split('\t')
			if len(parts) >= 2:
				english_refs.append(parts[0].strip())  # English reference
				source_texts.append(parts[1].strip())  # Source language text
		
		print(f"Loaded {len(source_texts)} pairs from {file_path}")
		if len(source_texts) > 0:
			print(f"Sample pair from {lang_code}:")
			print(f"Source text: {source_texts[0]}")
			print(f"English reference: {english_refs[0]}")
			
		return source_texts, english_refs
		
	except Exception as e:
		print(f"Error reading file {file_path}: {str(e)}")
		raise

def translate(model, tokenizer, texts, source_lang, batch_size=8, device="cpu"):
	"""Translate source texts to English"""
	model = model.to(device)
	translations = []
	
	# Set tokenizer languages
	tokenizer.src_lang = source_lang  # Source language
	tokenizer.tgt_lang = "eng_Latn"   # Target is English
	
	for i in tqdm(range(0, len(texts), batch_size), desc="Translating"):
		batch = texts[i:i+batch_size]
		try:
			inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
			with torch.no_grad():
				generated_tokens = model.generate(
					**inputs,
					forced_bos_token_id=tokenizer.get_lang_id("eng_Latn"),
					max_length=128,
					num_beams=5,
					early_stopping=True
				)
			translated = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
			translations.extend(translated)
		except Exception as e:
			print(f"Error translating batch {i}: {str(e)}")
			translations.extend([""] * len(batch))
	
	return translations

def save_translations(sources, references, translations, output_file):
	"""Save translations to TSV file"""
	df = pd.DataFrame({
		'source': sources,
		'reference': references,
		'translation': translations
	})
	df.to_csv(output_file, sep='\t', index=False)

def main():
	# Check for CUDA availability
	device = "cuda" if torch.cuda.is_available() else "cpu"
	print(f"Using device: {device}")
	
	# Models to evaluate
	models_dir = Path("experiments/models")
	model_paths = [
		"nllb_finetuned_base",
		"nllb_finetuned_augmented"
	]
	output_dir = Path("experiments/evaluation_results")
	
	# Test sets
	test_dir = Path("../datasets")
	output_dir.mkdir(exist_ok=True)
	
	languages = {
		"PAN": "pan_Arab",
		"PBT": "pbt_Arab",
		"SND": "snd_Arab",
		"SKR": "skr_Arab",
		"URD": "urd_Arab",
		"BAL": "bal_Arab",
		"HND": "hnd_Arab",
		"BRH": "brh_Arab"
	}
	
	all_results = {}
	
	for model_path in model_paths:
		full_model_path = models_dir / model_path
		if not full_model_path.exists():
			print(f"Model path {full_model_path} does not exist, skipping...")
			continue
		
		print(f"\nLoading model from {full_model_path}")
		tokenizer = AutoTokenizer.from_pretrained(full_model_path)
		model = M2M100ForConditionalGeneration.from_pretrained(full_model_path)
		model.eval()
		
		model_results = {}
		
		for lang_code, lang_id in languages.items():
			test_file = test_dir / f"{lang_code}-test.tsv"
			if not test_file.exists():
				print(f"Test file {test_file} does not exist, skipping {lang_code}...")
				continue
			
			print(f"\nEvaluating {lang_code} ({lang_id})...")
			source_texts, english_refs = load_test_data(test_file, lang_code)
			
			if len(source_texts) == 0:
				print(f"No test data for {lang_code}, skipping...")
				continue
			
			# Translate
			translations = translate(model, tokenizer, source_texts, lang_id, device=device)
			
			# Calculate metrics
			bleu = BLEU()
			chrf = CHRF()
			
			bleu_score = bleu.corpus_score(translations, [english_refs])
			chrf_score = chrf.corpus_score(translations, [english_refs])
			
			# Save results
			model_output_dir = output_dir / model_path
			model_output_dir.mkdir(parents=True, exist_ok=True)
			
			output_file = model_output_dir / f"{lang_code}_results.tsv"
			save_translations(source_texts, english_refs, translations, output_file)
			
			model_results[lang_code] = {
				"BLEU": float(bleu_score.score),
				"chrF2": float(chrf_score.score)
			}
			
			print(f"{lang_code} - BLEU: {bleu_score.score:.2f}, chrF2: {chrf_score.score:.2f}")
		
		# Save metrics
		metrics_file = model_output_dir / "metrics.json"
		with open(metrics_file, 'w', encoding='utf-8') as f:
			json.dump(model_results, f, indent=2, ensure_ascii=False)
		
		all_results[model_path] = model_results
	
	# Save all results
	all_metrics_file = output_dir / "all_metrics.json"
	with open(all_metrics_file, 'w', encoding='utf-8') as f:
		json.dump(all_results, f, indent=2, ensure_ascii=False)
	
	print("\nEvaluation completed!")

if __name__ == "__main__":
	main()

