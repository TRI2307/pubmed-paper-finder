import argparse
from pubmed_paper_finder.fetcher import fetch_pubmed_ids, fetch_pubmed_details
from pubmed_paper_finder.filter import parse_papers
from pubmed_paper_finder.writer import save_to_csv


def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", help="PubMed search query (e.g., 'cancer AND vaccine')")
    parser.add_argument("-d", "--debug", action="store_true", help="Show debug output")
    parser.add_argument("-f", "--file", help="Filename to save the results as CSV")

    args = parser.parse_args()

    if args.debug:
        print(f"\n Query: {args.query}")
        print(f" Output file: {args.file or 'Console'}")

    # Step 1: Fetch IDs
    ids = fetch_pubmed_ids(args.query)
    if args.debug:
        print(f" Found {len(ids)} paper IDs")

    if not ids:
        print(" No papers found for this query.")
        return

    # Step 2: Fetch paper XML data
    xml_data = fetch_pubmed_details(ids)

    # Step 3: Filter for non-academic authors
    filtered = parse_papers(xml_data)
    if args.debug:
        print(f" Found {len(filtered)} papers with non-academic authors")

    # Step 4: Save or print results
    save_to_csv(filtered, args.file)

if __name__ == "__main__":
    main()
