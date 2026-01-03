import argparse
from aggregator import get_stats, count_overlap_source

def main():
	parser = argparse.ArgumentParser(description='Get paths for different categories.')

	# Define arguments for each category
	parser.add_argument('-test', type=str, help='Path for test data')
	parser.add_argument('-all', type=str, help='Path for all data')
	parser.add_argument('-val', type=str, help='Path for validation data')
	parser.add_argument('-train', type=str, help='Path for train data')

	args = parser.parse_args()

	with open(args.all, "r", encoding='utf-8') as f:
		full = f.read().splitlines()[1:]

	with open(args.test, "r", encoding='utf-8') as f:
		test = f.read().splitlines()[1:]

	with open(args.val, "r", encoding='utf-8') as f:
		val = f.read().splitlines()[1:]

	if type(args.train) == str:
		with open(args.train, "r", encoding='utf-8') as f:
			train = f.read().splitlines()[1:]
	else:
		train = []

	# check if there are duplicates in individual files
	if len(set(test)) < len(test):
		print("Test file contains duplicates.")
	elif len(set(val)) < len(val):
		print("Val file contains duplicates.")
	elif len(set(train)) < len(train):
		print("Train file contains duplicates.")
	else:
		print("==== No duplicates found in individual files.")

	# check how many source sentences overlap across test and val
	print("==== %s instances overlap in train-test source sentences."%count_overlap_source(test, train))
	print("==== %s instances overlap in train-val source sentences."%count_overlap_source(val, train))
	print("==== %s instances overlap in test-val source sentences."%count_overlap_source(test, val))
	print("==== %s instances overlap in full-val source sentences."%count_overlap_source(val, full))

	print("All set stats (%s instances):"%len(full))
	for i, j in get_stats(full).items():
		print(i, j)
	print()
	print("Test set stats (%s instances):"%len(test))
	for i, j in get_stats(test).items():
		print(i, j)
	print()
	print("Valid set stats (%s instances):"%len(val))
	for i, j in get_stats(val).items():
		print(i, j)
	print()
	print("Train set stats (%s instances):"%len(train))
	for i, j in get_stats(train).items():
		print(i, j)

if __name__ == '__main__':
	main()

