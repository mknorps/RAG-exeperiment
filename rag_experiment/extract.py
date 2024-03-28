# Extract data from Arxiv papers and store them on a disc
import arxiv
import tarfile



# Construct the default API client.
client = arxiv.Client()

# Search for the 10 most recent articles matching the keyword "quantum."
search = arxiv.Search(
  query = "safety in AI",
  max_results = 10,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

results = client.results(search)