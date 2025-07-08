import csv
from typing import List, Dict, Optional

def save_to_csv(papers: List[Dict], filename: Optional[str] = None) -> None:
    """Save paper data to a CSV file or print to console if no filename."""
    if not papers:
        print("No non-academic papers found.")
        return

    fieldnames = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ]

    if filename:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for paper in papers:
                writer.writerow({
                    "PubmedID": paper["PubmedID"],
                    "Title": paper["Title"],
                    "Publication Date": paper["Publication Date"],
                    "Non-academic Author(s)": "; ".join(paper["Non-academic Author(s)"]),
                    "Company Affiliation(s)": "; ".join(paper["Company Affiliation(s)"]),
                    "Corresponding Author Email": paper["Corresponding Author Email"]
                })
        print(f"\n✅ Results saved to {filename}")
    else:
        print("\n🔍 Results:")
        for paper in papers:
            print("-" * 50)
            for key, value in paper.items():
                if isinstance(value, list):
                    value = ", ".join(value)
                print(f"{key}: {value}")
