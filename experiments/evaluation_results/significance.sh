# Statistical significance testing for SACOR evaluation results

# Compare augmented to base model
sacrebleu base_merged.ref -i base_merged.hyp augmented_merged.hyp --paired-bs --paired-bs-n 1000

