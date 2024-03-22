# Convert a jsonl file with ensure_ascii into a jsonl file without ensure_ascii

import sys
import json

def main():
    if len(sys.argv) != 3:
        print("Usage: python utify.py <input-file> <output-file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as i:
        with open(output_file, 'w') as o:
            for line in i.readlines():
                o.write(json.dumps(json.loads(line), ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
