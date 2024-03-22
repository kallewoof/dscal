# Convert a text file into JSONL format fitted for the pippa dataset
# Usage: python convert-to-jsonl.py <input-file> <output-file>

# We take each paragraph (\n\n) as a chunk and write it to the output jsonl file as {"message": "content"}

import sys
import json

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert-to-jsonl.py <input-file> <output-file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        data = f.read()

    chunks = data.split('\n\n')

    with open(output_file, 'w') as f:
        for chunk in chunks:
            if chunk.strip() != '':
                f.write(json.dumps({"message": chunk}) + '\n')

if __name__ == "__main__":
    main()
