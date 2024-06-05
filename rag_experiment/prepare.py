# Transform LaTex data into plain text and make it ready for storing in the vector database
from typing import List, Tuple
import os
import glob

import pydetex.pipelines as pp
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def latex_file_to_plain_text(filename: str) -> str:
    """Takes a LaTeX file name and transforms its content into plain text."""
    with open(filename, encoding="utf-8", errors="ignore") as f:
        latex = f.read()
        return pp.strict(latex)


def files_to_plain_text(dir_path: str, name_pattern: str = "*.tex", recursive: bool = False) -> Tuple[
        List[str], List[str]]:
    """Traverses all files in a given directory and runs transformation to plain text function.
    Saves results to files of the same name, but with .txt added at the end.
    Returns tuple with list of created files' names and list of files' names where an error occurred."""
    pattern = os.path.join(dir_path, "**", name_pattern)
    filenames = glob.glob(pattern, recursive=recursive)
    created = []
    errors = []
    for filename in filenames:
        try:
            plain = latex_file_to_plain_text(filename)
            with open(filename+".txt", 'w', errors='ignore') as f:
                f.write(plain)
                created.append(filename+".txt")
        except Exception as e:
            errors.append(filename)
    return created, errors


def split_to_sentences(text: str, **kwargs) -> List[Document]:
    """Takes a plain text and splits it into sentences."""
    text_splitter = RecursiveCharacterTextSplitter(
        **kwargs,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.create_documents([text])


if __name__ == "__main__":
    filenames, errors = files_to_plain_text("papers_example", recursive=False)
    print(filenames)
    print(errors)
