# Convert a jsonl file to a parquet file
# Usage: python convert-to-parquet.py <input-file> <output-file>

import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[2]

df = pd.read_json(input_file, lines=True)
df.to_parquet(output_file, index=False)
print(f'Converted {input_file} to {output_file}')
