# Calculate perplexity scores for a series of sessions, given a specific model.

import sys
import json
import re
import os
import evaluate

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python calc-perplexity.py <input-file> [<model-name>=mistral-7b]")
        return

    input_file = sys.argv[1]
    if len(sys.argv) == 2:
        model_name = "mistralai/Mistral-7B-v0.1"
    else:
        model_name = sys.argv[2]

    # Load model
    perplexity = evaluate.load("perplexity", module_type="metric")

    # Load input
    input_texts = []
    scores = []
    entries = []
    with open(input_file, 'r') as f:
        for line in f:
            msg = ""
            j = json.loads(line)
            entries.append(j)
            for m in j["messages"]:
                msg += m + "\n"
                if len(msg) > 50000:
                    break
            input_texts.append(msg)

    print(f"Calculating perplexities for {len(input_texts)} messages...")
    scores = perplexity.compute(model_id=model_name, add_start_token=False, predictions=input_texts, batch_size=1)

    # Write perplexities to file
    output_file = input_file + ".perplexities.jsonl"
    with open(output_file, 'w') as f:
        for score, entry in zip(scores["perplexities"], entries):
            entry["perplexity"] = score
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Perplexity scores (stored in {output_file}):")
    print(scores)

if __name__ == "__main__":
    main()
