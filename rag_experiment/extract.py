# Extract data from Arxiv papers and store them on a disc
import arxiv
import tarfile
import tempfile
import gzip
import os
import shutil
import json

# Construct the default API client.
client = arxiv.Client()

# Function that takes query as an argument for arxiv search and returns the results
def search_arxiv(query: str, max_results: int = 10) -> arxiv.Search:
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    return client.results(search)


# Download results to a separate folder. Create function that takes results and name of the folder as an input.
# This should be a temporary folder. 
def download_results(results: arxiv.Result, temp_dir: str):
    for paper in results:
        try:
            paper.download_source(temp_dir)
        except Exception as e:
            print(f"Failed to download {paper.entry_id} due to {e}")  

# Make a list or dictionaries containing metadata from papers
def extract_metadata(results: arxiv.Result) -> list:
    metadata_list = []
    for paper in results:
        metadata = {
            'authors': [author.name for author in paper.authors],
            'title': paper.title,
            'published': paper.published.strftime('%Y-%m-%d'),
            'domain': paper.primary_category,
            'tags': paper.categories
            }
        metadata_list.append(metadata)
    return metadata_list
        
        
# Unpack dowloaded archives, but only .tex files and store them in a separate folder.
def unpack_archives(source_dir: str, target_dir: str, metadata_list: list):
    for i, file_name in enumerate(os.listdir(source_dir)):
        if file_name.endswith('.tar.gz'):
            # Create a unique subdirectory for each archive
            subdirectory_path = os.path.join(target_dir, os.path.splitext(file_name)[0])
            os.makedirs(subdirectory_path, exist_ok=True)  # Ensure the subdirectory exists
            try:
                # Open the tar.gz file
                with tarfile.open(os.path.join(source_dir, file_name), 'r:gz') as tar:
                    # Filter for .tex files and extract them
                    tex_files = [member for member in tar.getmembers() if member.name.endswith('.tex')]
                    # Extract tex files
                    for member in tex_files:
                        member.name = os.path.basename(member.name)
                        tar.extract(member, path=subdirectory_path)
                        
                with open(os.path.join(subdirectory_path, 'metadata.json'), 'w') as f:
                    json.dump(metadata_list[i], f, indent=4)

            except (tarfile.ReadError, gzip.BadGzipFile) as e:
                print(f"Skipping file {file_name} due to error: {e}")

                

# Extract .tex files to a folder in one function.
def extract_tex_files(query: str, target_dir: str, max_results: int = 10):
    
    # Create a temporary directory to store download archives
    temp_dir = tempfile.mkdtemp()

    try:
        # Search arXiv for the query
        results = list(search_arxiv(query, max_results))
        
        # Download the papers' source files to the temporary directory
        download_results(results, temp_dir)
        
        # Create metadata
        metadata_list = extract_metadata(results)

        # Ensure the target directory exists
        os.makedirs(target_dir, exist_ok=True)

        # Unpack .tex files from the downloaded tar.gz files to the target directory and add metadata.json for each paper
        unpack_archives(temp_dir, target_dir, metadata_list)

    finally:
        # Cleanup: Remove the temporary directory and all its contents
        shutil.rmtree(temp_dir)

    print(f'All .tex files have been downloaded and extracted to a directory "{target_dir}"')


# Example usage:
if __name__ == "__main__":
    extract_tex_files(query="safety in AI", target_dir="papers_example", max_results=10)
