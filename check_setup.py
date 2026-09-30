"""Quick check that every package installed correctly.  Run: python check_setup.py"""

import sys

import gradio
import numpy
import pandas
import rank_bm25  # noqa: F401  (imported only to check it's installed)
import sentence_transformers
import torch

print("Python:", sys.version.split()[0])
print("numpy:", numpy.__version__)
print("pandas:", pandas.__version__)
print("torch:", torch.__version__)
print("sentence-transformers:", sentence_transformers.__version__)
print("gradio:", gradio.__version__)
print("GPU available:", torch.cuda.is_available())
print("All good!")
