from sacrebleu.metrics import BLEU, CHRF

def evaluate_translations(hypotheses, references):
	"""Calculate BLEU and chrF scores"""
	bleu = BLEU()
	chrf = CHRF()
	
	bleu_score = bleu.corpus_score(hypotheses, [references])
	chrf_score = chrf.corpus_score(hypotheses, [references])
	
	return bleu_score.score, chrf_score.score

# Example usage for evaluating translations
# This script can be used to evaluate translation quality for South Asian languages

