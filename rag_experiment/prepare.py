# Transform LaTex data into plain text and make it ready for storing in the vector database
import pydetex.pipelines as pp
from langchain_text_splitters import RecursiveCharacterTextSplitter

# TODO Create a funtion that takes a LaTeX file name and tranforms it into plain text
with open("./papers/test1/Sections/Experiments.tex") as f:
     latex = f.read()

text = "This is a \\textbf{LaTex} code..."
out = pp.strict(latex)
print(out)

# TODO Cretae a function that traverses all files in a given directory and runs transformation to plain text function

# TODO Create a function that takes a plain text and splits it into sentences