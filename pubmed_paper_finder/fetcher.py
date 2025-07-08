import requests
from typing import List, Dict

# Constants for the PubMed API
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
EMAIL = "trishatree2307@gmail.com"  

def fetch_pubmed_ids(query: str, retmax: int = 20) -> List[str]:
    """Fetch PubMed IDs for a given query."""
    url = f"{BASE_URL}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
        "email": EMAIL
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_pubmed_details(paper_ids: List[str]) -> List[Dict]:
    """Fetch detailed metadata for each PubMed paper ID."""
    url = f"{BASE_URL}efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml",
        "email": EMAIL
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text  
