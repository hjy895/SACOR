import gc
import torch
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

model_size = ["1.3B", "3.3B"][0]

if model_size == "1.3B":
	tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-1.3B")
	model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-1.3B").cuda()
	output_name = "outputs_1.3B"
else:
	tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-3.3B")
	model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-3.3B").cuda()
	output_name = "outputs_3.3B"

translator = pipeline(
	'translation', 
	model=model, 
	tokenizer=tokenizer, 
	max_length=400, 
	device=0,
	num_beams=3, 
	early_stopping=True
)

datasets = {
	"PAN": "../datasets/PAN-test.tsv",
	"PBT": "../datasets/PBT-test.tsv",
	"SND": "../datasets/SND-test.tsv",
	"SKR": "../datasets/SKR-test.tsv",
	"URD": "../datasets/URD-test.tsv",
	"BAL": "../datasets/BAL-test.tsv",
	"HND": "../datasets/HND-test.tsv",
	"BRH": "../datasets/BRH-test.tsv"
}

for lang_code in datasets:
	source_en, target = list(), list()
	with open(datasets[lang_code], 'r', encoding='utf-8') as f:
		for i in f.read().splitlines()[1:]:
			parts = i.split("\t")
			if len(parts) >= 2:
				source_en.append(parts[0].strip())
				target.append(parts[1].strip())

	results = {"target": target, 
				"source_en": source_en,
				"translations": {
					 "eng_Latn": {"eng_Latn":[]},
					 "urd_Arab": {"eng_Latn":[]},
					 "hin_Deva": {"eng_Latn":[]}
				}}
		
	for idx, tgt_text in enumerate(target):
		source_languages = ["eng_Latn", "urd_Arab", "hin_Deva"]

		for source_lang in source_languages:
			for target_lang in ["eng_Latn"]:
				print("Processing %s (from %s to %s)..."%(lang_code, source_lang, target_lang))
				try:
					translation = translator(tgt_text, src_lang=source_lang, tgt_lang=target_lang)[0]['translation_text']
					results["translations"][source_lang][target_lang].append(translation)
					print(f"Processed {idx + 1}/{len(target)} rows")
				except Exception as e:
					print(f"Error translating line {idx}: {e}")
					results["translations"][source_lang][target_lang].append("")

	output_file = f"experiments/zero-shot-eval/{output_name}/{lang_code}_results.json"
	import os
	os.makedirs(os.path.dirname(output_file), exist_ok=True)
	with open(output_file, 'w', encoding='utf-8') as out_f:
		json.dump(results, out_f, ensure_ascii=False, indent=4)

	print(f"Finished processing {lang_code}. Results saved to {output_file}.")

	# Free up GPU memory
	gc.collect()
	torch.cuda.empty_cache()

