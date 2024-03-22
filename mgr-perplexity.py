# Manager for perplexity enabled session data.
# Can sort by perplexities to get an overview of the most perplexing sessions, as well as trim by a given perplexity threshold, resulting in a few with all entries with a perplexity higher than the threshold weeded out.

import sys
import json
import re
import os
import argparse

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python mgr-perplexity.py <input-file> [<threshold>=0.0] [--brief]")
        print("With no threshold given, the input sorted by perplexities is printed. If --brief is given, the messages are trimmed to 50 characters.")
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input file containing session data.")
    parser.add_argument("threshold", nargs="?", type=float, default=None, help="Perplexity threshold for trimming.")
    parser.add_argument("--brief", action="store_true", help="Trim messages to 50 characters.")
    args = parser.parse_args()

    input_file = args.input_file
    threshold = args.threshold
    brief = args.brief

    # Load input
    entries = []
    with open(input_file, 'r') as f:
        for line in f:
            entries.append(json.loads(line))

    # Sort entries by perplexity
    entries.sort(key=lambda x: x["perplexity"], reverse=True)

    if threshold is not None:
        # Trim entries by perplexity threshold
        entries = [entry for entry in entries if entry["perplexity"] > threshold]

    if brief:
        # {"charname": "Lunata Orion", "messages": ["*As you walk through the jungle completely lost, you suddenly find yourself standing before a log cabin. You knock on the door but no one answers. As you enter the cabin, you find a little girl with blonde hair, green eyes, and sharp ears sitting down at a wooden table relaxing while something that smells great cooks on the stove nearby* \"Oh hey, looks like you found my cabin. I'm Lunata, and I'm a shapeshifter. I can turn into anyone or anything, you want me to shapeshift for you?\"", "Hi there, you said you're a shapeshifter?", "Lunata nods, smiling widely at you* \"Yep! I can turn into any person, animal, or object without any restrictions! I could even turn into air if I wanted to, but I prefer not to since that would mean losing my sense of touch. But yes, I am a shapeshifter who can turn into anything, including you if you want that.\" *She says, now with a playful wink and smirk*"], "chardesc": "Descriptive", "perplexity": 7.838069915771484}
        for entry in entries:
            print(f"Char {entry['charname']}, PPL {entry['perplexity']}:")
            for msg in entry["messages"][:10]:
                print(" - " + msg[:150].replace("\n", "\\n"))
    else:
        # Print results
        print(entries)

if __name__ == "__main__":
    main()
