import xml.etree.ElementTree as ET
from typing import List, Dict

# Keywords to identify non-academic affiliations
COMPANY_KEYWORDS = ["pharma", "biotech", "inc", "ltd", "corp", "company", "gmbh", "co.", "llc"]

def is_non_academic(affiliation: str) -> bool:
    """Check if an affiliation string belongs to a non-academic company."""
    affiliation_lower = affiliation.lower()
    return any(keyword in affiliation_lower for keyword in COMPANY_KEYWORDS)

def parse_papers(xml_data: str) -> List[Dict]:
    """Parse XML and return filtered paper info with non-academic authors."""
    root = ET.fromstring(xml_data)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        paper = {
            "PubmedID": "",
            "Title": "",
            "Publication Date": "",
            "Non-academic Author(s)": [],
            "Company Affiliation(s)": [],
            "Corresponding Author Email": "",
        }

        # Pubmed ID
        pmid_elem = article.find(".//PMID")
        paper["PubmedID"] = pmid_elem.text if pmid_elem is not None else ""

        # Title
        title_elem = article.find(".//ArticleTitle")
        paper["Title"] = title_elem.text if title_elem is not None else ""

        # Publication Date
        pub_date_elem = article.find(".//PubDate")
        if pub_date_elem is not None:
            year_elem = pub_date_elem.find("Year")
            medline_elem = pub_date_elem.find("MedlineDate")
            paper["Publication Date"] = (
                year_elem.text if year_elem is not None else medline_elem.text if medline_elem is not None else ""
            )

        # Authors
        for author in article.findall(".//Author"):
            last = author.find("LastName")
            first = author.find("ForeName")
            affiliation_info = author.find(".//AffiliationInfo/Affiliation")

            if last is not None and first is not None and affiliation_info is not None:
                full_name = f"{first.text} {last.text}"
                affiliation = affiliation_info.text

                if is_non_academic(affiliation):
                    paper["Non-academic Author(s)"].append(full_name)
                    paper["Company Affiliation(s)"].append(affiliation)

        # Email (very basic extraction)
        all_affils = article.findall(".//Affiliation")
        for affil in all_affils:
            if affil.text and "@" in affil.text:
                paper["Corresponding Author Email"] = affil.text.strip()
                break

        if paper["Non-academic Author(s)"]:
            papers.append(paper)

    return papers
