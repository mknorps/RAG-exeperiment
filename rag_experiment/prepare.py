# Transform LaTex data into plain text and make it ready for storing in the vector database
import pydetex.pipelines as pp
from langchain_text_splitters import RecursiveCharacterTextSplitter

# test of pydetex library
with open("./papers/test1/Sections/Experiments.tex") as f:
     latex = f.read()

text = "This is a \\textbf{LaTex} code..."
out = pp.strict(latex)
print(out)