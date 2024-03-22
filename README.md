# Dataset Calibration (dscal) Toolkit

This is the starting point for a toolset used in generating a polished dataset for use in calibrating quantized LLM models, such as Exl2 or GGUF models.

## Installation

The toolkit currently has no installation options. Simply check out the git repository and use the python files within.

## Tools

# `sessionize.py`: Convert a .jsonl pippa dataset into a sessionized dataset.
# `calc-perplexity.py`: Calculate the perplexity of the entries in a given sessionized dataset, given a specific model (defaults to mistral-7b v1.0)
# `mgr-perplexity.py`: Given the output produced by the above, order the entries by perplexity, and optionally trim out all entries above a given perplexity threshold.
# `clusterize.py`: Given a session, cluster the entries into heuristically maximally diverse groups using inverse cosine similarity.

Doing the above 4 steps, you should be able to create a polished dataset for use in calibrating a quantized LLM model.

To fine tune the quantization even further (although this is very time consuming), you may choose to do the perplexity calculations against the model being quantized. This will potentially give an even more fine tuned calibration dataset.
