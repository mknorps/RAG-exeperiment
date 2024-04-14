# Index documents into vector database

from langchain_community.vectorstores import Chroma
from pathlib import Path
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter
from tqdm import tqdm
import chromadb
from prepare import *   # def name

CHROMA_DATA_PATH = Path("data/chroma")


def open_db(
    name="default",
) -> Chroma:
    CHROMA_DATA_PATH.mkdir(exist_ok=True, parents=True)
    persistent_client = chromadb.PersistentClient(str(CHROMA_DATA_PATH))
    collection = persistent_client.get_or_create_collection(name)
    # collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(
        client = persistent_client,
        collection_name = name,
        embedding_function=embedding_model,
    )


# TODO Embed plain text documents into vectors
# Use documents as input with metadata allowing 
# to identify the article the document is created from and the file it originates from
# https://api.python.langchain.com/en/latest/documents/langchain_core.documents.base.Document.html#langchain_core.documents.base.Document
def populate_db(name: str):
    db = open_db(
        name=name,
    )
    docs = ... # documents in plain text converted from LaTex, add a function with prepare
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    print(f"Indexing {len(docs)} documents")
    for doc in tqdm(docs):
        splitted_docs = splitter.split_documents([doc])
        db.add_documents(splitted_docs)


# TODO function to search for documents in the database
def search_for_documents(query: str, db_name: str):
    db = open_db(name=db_name)
    results = db.similarity_search(query)
    return results


def test_db(db_name: str):
    populate_db(name=db_name)

    search_query = ...
    search_results = search_for_documents(query=search_query, db_name=db_name)

    print("Search Results:")
    for result in search_results:
        print(result)