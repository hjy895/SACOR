import json
import re
from sacrebleu.metrics import BLEU, CHRF
bleu = BLEU()
chrf = CHRF()

datasets = {
	"PAN": "experiments/zero-shot-eval/outputs_1.3B/PAN_results.json",
	"PBT": "experiments/zero-shot-eval/outputs_1.3B/PBT_results.json",
	"SND": "experiments/zero-shot-eval/outputs_1.3B/SND_results.json",
	"SKR": "experiments/zero-shot-eval/outputs_1.3B/SKR_results.json",
	"URD": "experiments/zero-shot-eval/outputs_1.3B/URD_results.json",
	"BAL": "experiments/zero-shot-eval/outputs_1.3B/BAL_results.json",
	"HND": "experiments/zero-shot-eval/outputs_1.3B/HND_results.json",
	"BRH": "experiments/zero-shot-eval/outputs_1.3B/BRH_results.json",
}

for lang_code in datasets:
	result_bleu, result_chrf = "", ""
	print("\nProcessing %s..."%lang_code)
	try:
		with open(datasets[lang_code], 'r', encoding='utf-8') as f:
			data = json.load(f)
	except FileNotFoundError:
		print(f"File {datasets[lang_code]} not found, skipping...")
		continue
	
	print("=== BLEU Scores ===")
	for source_lang in ["eng_Latn", "urd_Arab", "hin_Deva"]:
		for target_lang in ["eng_Latn"]:
			if source_lang in data["translations"] and target_lang in data["translations"][source_lang]:
				if len(data["translations"][source_lang][target_lang]):
					sys = data["translations"][source_lang][target_lang]
					ref = [data["source_en"]]
					
					bleu_score = bleu.corpus_score(sys, ref)
					bleu_value = float(re.search(r'BLEU = (\d+\.\d+)', str(bleu_score)).group(1))
					print("Source: %s, Target: Eng >>> %s"%(source_lang, bleu_value))
	
	print("\n=== CHrF Scores ===")
	for source_lang in ["eng_Latn", "urd_Arab", "hin_Deva"]:
		for target_lang in ["eng_Latn"]:
			if source_lang in data["translations"] and target_lang in data["translations"][source_lang]:
				if len(data["translations"][source_lang][target_lang]):
					sys = data["translations"][source_lang][target_lang]
					ref = [data["source_en"]]

					chrf_score = chrf.corpus_score(sys, ref)
					chrf_value = float(re.search(r'chrF2 = (\d+\.\d+)', str(chrf_score)).group(1))

					print("Source: %s, Target: Eng >>> %s"%(source_lang, chrf_value))

