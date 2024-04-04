# Extract data from Arxiv papers and store them on a disc
import arxiv
import tarfile



# Construct the default API client.
client = arxiv.Client()

# TODO Function that takes query as an argument for arxiv search and returns the results
def search_arxiv(query: str) -> arxiv.Search:
    pass

# Search for the 10 most recent articles matching the keyword "quantum."
search = arxiv.Search(
  query = "safety in AI",
  max_results = 10,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

results = client.results(search)

# TODO Download results to a separate folder. Create function that takes results and name of the folder as an input.
# This should be a temporary folder. 
def download_results(results: arxiv.Results, folder: str):
    pass


# TODO Unpack dowloaded archives, but only .tex files and store them in a separate folder.
def unpack_archives(folder: str):
    pass


