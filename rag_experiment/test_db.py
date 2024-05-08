from index import populate_and_prepare_db, search_for_documents


class Document:
    def __init__(self, page_content, metadata=None):
        if metadata is None:
            metadata = {}
        self.page_content = page_content
        self.metadata = metadata


def test_db(db_name: str):
    with open("book_1.txt") as my_file:
        book_1 = my_file.read()

    with open("book_2.txt") as my_file:
        book_2 = my_file.read()

    doc = [Document(book_1, {}), Document(book_2, {})]

    populate_and_prepare_db(name=db_name, docs=doc)

    search_query = "What was Jenny doing?"
    search_results = search_for_documents(query=search_query, db_name=db_name)

    print("\nSearch Results:")
    for result in search_results:
        print(result)

test_db('book')