import random
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# import numpy as np
import sys
import json
from tqdm import tqdm

vectorizer = CountVectorizer()

def calculate_avg_distance(text, sorted_texts):
    total_distance = 0
    for sorted_text in sorted_texts:
        total_distance += calculate_distance(text, sorted_text)
    return total_distance / len(sorted_texts)

distcache = {}

def calculate_distance(text1, text2):
    if (text1, text2) in distcache:
        return distcache[(text1, text2)]
    # Transform texts into feature vectors
    X = vectorizer.transform([text1, text2])
    
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(X)
    
    # Dissimilarity is 1 - similarity
    distcache[(text1, text2)] = 1 - similarity_matrix[0, 1]
    return distcache[(text1, text2)]

def sort_texts(texts):
    sorted_texts = []
    remaining_texts = texts.copy()

    # Randomly select the first text
    sorted_texts.append(remaining_texts.pop(random.randint(0, len(remaining_texts) - 1)))

    # Iterate through the remaining texts
    for _ in tqdm(range(len(texts) - 1)):
        max_avg_distance = -1
        selected_text = None

        # Find the text with the highest average dissimilarity
        for text in remaining_texts:
            avg_distance = calculate_avg_distance(text, sorted_texts)
            if avg_distance > max_avg_distance:
                max_avg_distance = avg_distance
                selected_text = text

        # Add the selected text to the sorted list and remove it from remaining_texts
        sorted_texts.append(selected_text)
        remaining_texts.remove(selected_text)

    return sorted_texts

def main():
    if len(sys.argv) != 2:
        print("Usage: python ng-clusterize.py <input-file>")
        return

    input_file = sys.argv[1]

    # Load input
    texts = []
    textdict = {}
    with open(input_file, 'r') as f:
        for line in f:
            j = json.loads(line)
            msg = ""
            for m in j["messages"]:
                msg += m + "\n"
                if len(msg) > 2000:
                    break
            texts.append(msg)
            textdict[msg] = j

    # Fit the vectorizer and transform texts into feature vectors
    print(f"Fitting vectorizer to {len(texts)} messages...")
    vectorizer.fit_transform(texts)

    # Sort texts for diversity
    print(f"Sorting {len(texts)} messages...")
    sorted_texts = sort_texts(texts)

    # Write to file
    with open(input_file + ".sorted.jsonl", 'w') as f:
        for text in sorted_texts:
            f.write(json.dumps(textdict[text], ensure_ascii=False) + "\n")

    print("Sorted texts:")
    for text in sorted_texts:
        print(text)

if __name__ == "__main__":
    main()
