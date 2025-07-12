from datasets import load_dataset

imdb_dataset  = load_dataset('imdb')

# print("--- Full Dataset Structure ---")
# print(imdb_dataset)
# print("\n" + "="*50 + "\n")


print("--- First Example from the Training Set ---")
print(imdb_dataset["train"][0])

## You can always verify this yourself with this command:

print(imdb_dataset['train'].features['label'])
# Output: ClassLabel(names=['neg', 'pos'], id=None)
# The 'names' list shows you that index 0 is 'neg' and index 1 is 'pos'.