import re
import unicodedata

# Configuration - update these for your language
file_name = "path/to/corpus.txt"
lang_code = "PAN"  # Change to PAN, PBT, SND, SKR, URD, BAL, HND, or BRH

with open(file_name, "r", encoding='utf-8') as f:
	corpus = f.read()

def extract_sentences(text):
	# Remove anything before and including the '/', '-', or ':' character in each sentence
	text = re.sub(r'.*?[\/\-:]', '', text)

	# This regex pattern matches sentence-ending punctuation followed by a space or end of string
	sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\n|\،|\؟|\؛)\s')

	sentences = sentence_endings.split(text)
	
	# cleaning to handle cases where the text doesn't adhere to strict punctuation
	cleaned_sentences = []
	for sentence in sentences:
		# Removing leading and trailing spaces
		sentence = sentence.strip()
		
		if sentence:
			# Check for allowed punctuation and characters
			if not re.search(r'[^?!.,;:،؟؛\s\w]', sentence):
				# Skip sentences containing diacritics
				if not re.search(r'[\u064B-\u065F]', sentence):
					# Skip sentences with double dots
					if '..' not in sentence:
						# Ensure the sentence is clean
						if re.match(r'^[\u0600-\u06FF\u0A00-\u0A7F\s\.\,\?\!؛:،؟]+$', sentence):
							cleaned_sentences.append(sentence.strip())
	
	return cleaned_sentences

def contains_digits(text):
	for i in "0123456789٠١٢٣٤٥٦٧٨٩":
		if i in text:
			return True
	return False

def is_valid(text):
	if '\t' not in text and "“" not in text and "”" not in text and len(text) < 200 and len(text) > 5 and "…" not in text and "\"" not in text and ".." not in text \
		and "(" not in text and ")" not in text and "-" != text[0] and "," not in text:
		return True
	return False

if lang_code == "PAN":
	# For Punjabi (Gurmukhi script)
	sentences = [i for i in list(set(extract_sentences(corpus))) if i[-1] == "।" and len(i) < 200 and not contains_digits(i) and len(i.split()) > 1]
else:
	# For script-based languages
	sentences = [i.replace("!.", ".") for i in list(set(extract_sentences(corpus))) if i[-1] == "." and len(i) < 200 and not contains_digits(i) and len(i.split()) > 1]

print("Number of sentences:", len(sentences))

import os
os.makedirs(f"corpora/{lang_code}", exist_ok=True)
with open(f"corpora/{lang_code}/{lang_code}_sentences.txt", "w", encoding='utf-8') as f:
	f.write("\n".join(sentences))

