import os
import warnings

# Suppress TensorFlow logs and warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
warnings.filterwarnings('ignore')

from transformers import pipeline

# unmasker = pipeline('fill-mask',model='distilbert-base-uncased')

# result = unmasker("The goal of this bootcamp is to [MASK] the assignment.")

# print(result)

textclassify = pipeline('text-classification',model='distilbert/distilbert-base-uncased-finetuned-sst-2-english')
texts = [
    "I am absolutely thrilled with the Hugging Face library!",
    "This product is terrible and I hate it.",
    "The weather is okay today.",
    "Amazing experience, highly recommended!",
    "Not sure how I feel about this."
]

results = textclassify(texts)

print(results)


for i , result in enumerate(results):
    print(f"Text {i+1} : {texts[i]}")
    print(f"Result : {result}")
    print("_" * 50)