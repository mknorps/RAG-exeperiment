# Index documents into vector database

from langchain_community.vectorstores import Chroma
from pathlib import Path
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from tqdm import tqdm
import chromadb

import uuid

CHROMA_DATA_PATH = Path("data/chroma")


def open_db(name="default",) -> Chroma:
    CHROMA_DATA_PATH.mkdir(exist_ok=True, parents=True)
    persistent_client = chromadb.PersistentClient(str(CHROMA_DATA_PATH))
    collection = persistent_client.get_or_create_collection(name)
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
def populate_db(name: str, docs: list):
    db = open_db(name=name,)
    print(f"Indexing {len(docs)} documents")
    for doc in tqdm(docs):
        db.add_documents(doc)


'''# Function for testing txt files
def populate_and_prepare_db(name: str, docs: list):
    db = open_db(name=name,)
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    print(f"Indexing {len(docs)} documents")
    for doc in tqdm(docs):
        splitted_docs = splitter.split_documents([doc])
        db.add_documents(splitted_docs)'''



def populate_and_prepare_db(name: str, texts: list, metadatas: list, chunk_size=500, chunk_overlap=50):
    db = open_db(name=name,)
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    print(f"Indexing {len(texts)} documents")
    for text, metadata in tqdm(zip(texts, metadatas), total=len(texts)):
        # Split documents into chunks and prepare metadata for each chunk
        splitted_texts = splitter.split_text(text)

        if not splitted_texts:
            continue

        # Filter out metadata types which can't be used in chromadb 
        filtered_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)):
                filtered_metadata[key] = value

        metadata_copies = [filtered_metadata] * len(splitted_texts)
        ids = [str(uuid.uuid4()) for _ in range(len(splitted_texts))]

        db.add_texts(texts=splitted_texts, metadatas=metadata_copies, ids=ids)

    print("Documents and metadata have been added to the Chroma collection.")

# Function to search for documents in the database
def search_for_documents(query: str, db_name: str, top_k: int = 5):
    db = open_db(name=db_name)

    results = db.similarity_search(query, k=top_k)

    return results