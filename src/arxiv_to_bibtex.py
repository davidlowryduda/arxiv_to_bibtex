"""
arxiv_to_bibtex.py - a simple tool to get bibtex from arxiv ids

This is really a super tiny wrapper around the arXiv API.

# **********************************************************************
#  This is arxiv_to_bibtex, a simple tool to get bibtex from arxiv ids.
#       Copyright (c) 2024 David Lowry-Duda <david@lowryduda.com>
#       All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
#                 <http://www.gnu.org/licenses/>.
# **********************************************************************
"""
import argparse
import datetime
import requests
import string
import time


from bs4 import BeautifulSoup
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class BibtexRecord:
    """
    A single bibtex record.
    """
    authors: list[str]
    arxiv_doi: str
    primary_category: str
    title: str
    url: str
    publication_date: datetime.date
    updated_date: datetime.date


def first_significant_word(title: str) -> str:
    """
    Extract the first nontrivial word from a title.

    Args:
        title (str): The input title.

    Returns:
        str: The first nontrivial word.
    """
    unimportant_words = [
        "a", "an", "the", "and", "or", "but", "towards", "for", "in", "with",
        "to", "of", "on", "at", "by", "from", "up", "down", "about", "after",
        "before", "over", "under", "between", "through", "into", "out",
        "during", "since", "until", "upon", "around", "throughout", "as", "if",
        "though", "because", "while", "when", "where", "whether", "while",
        "not", "only", "just", "both", "neither", "either", "all", "some",
        "few", "many", "most", "other", "another", "such", "this", "that",
        "these", "those", "one", "two", "three", "four", "five", "six",
        "seven", "eight", "nine", "ten"
    ]
    words = title.split()
    for word in words:
        if word.lower() not in unimportant_words:
            return ''.join(
                [l for l in word if l not in string.punctuation]
            )
    return ""


def standard_bibtex_formatter(r: BibtexRecord) -> str:
    """
    Generate a standard BibTeX string from a BibtexRecord.

    Args:
        r (BibtexRecord): The input BibtexRecord.

    Returns:
        str: The BibTeX string.
    """
    # Format authors
    author_str = ' and '.join(r.authors)

    # Create citation key
    first_important_word = first_significant_word(r.title)
    first_author_last_name = r.authors[0].split()[-1].lower().strip(',. ')
    first_author_stripped_name = ''.join(
        [l for l in first_author_last_name if l not in string.punctuation]
    )
    citation_key = f"{first_author_stripped_name}{r.publication_date.year}{first_important_word.lower()}"

    # Format BibTeX string
    bibtex_str = f"@misc{{{citation_key},\n"
    bibtex_str += f"      title={{{r.title}}},\n"
    bibtex_str += f"      author={{{author_str}}},\n"
    bibtex_str += f"      year={{{r.publication_date.year}}},\n"
    bibtex_str += f"      howpublished=\"\\url{{{r.url}}}\",\n"
    bibtex_str += f"      note={{arXiv:{r.primary_category}:{r.arxiv_doi}}},\n"
    bibtex_str += "}"

    return bibtex_str


def extract_arxiv_identifier(url: str) -> str:
    """
    Extract the arXiv identifier from an arXiv URL.

    Args:
        url (str): The input arXiv URL.

    Returns:
        str: The arXiv identifier.

    NOTE: this applies to both old and new type arxiv urls, such as
        url1 = "https://arxiv.org/abs/2002.05234"       --> 2002.05234
        url2 = "https://arxiv.org/abs/hep-ex/0307015v1" --> hep-ex/0307015v1
    """
    parsed_url = urlparse(url)
    if not parsed_url.path.startswith("/abs/"):
        raise ValueError("Invalid url")
    # remove `/abs/`
    return parsed_url.path[5:]


def _query_arxiv_raw(arxiv_ids: str) -> requests.Response:
    """
    Make a request to the arXiv API and return the raw response.

    Args:
        arxiv_ids (str): The arXiv identifier, concatenated by commas if there
        are multiple.

    Returns:
        requests.Response: The raw response from the arXiv API.
    """
    api_url = f"https://export.arxiv.org/api/query?id_list={arxiv_ids}"
    response = requests.get(api_url)
    # Check if the request was unsuccessful (status code 200)
    if response.status_code != 200:
        response.raise_for_status()
    return response


def _construct_bibtex(raw_response: str) -> list[BibtexRecord]:
    """
    Construct a BibtexRecord from the raw API response.

    Args:
        raw_response (str): The raw XML response from the arXiv API.

    Returns:
        A list of BibtexRecord: The constructed BibtexRecord from all matching
        entries.
    """
    soup = BeautifulSoup(raw_response, 'xml')
    entries = soup.find_all('entry')

    ret = []
    for entry in entries:
        # Extract relevant information from the XML response
        title = entry.find('title').get_text(strip=True)
        authors = [
            author.find('name').get_text(strip=True)
            for author in entry.find_all('author')
        ]
        arxiv_doi = entry.find('id').get_text(strip=True).split('/')[-1]
        primary_category = entry.find('category')['term']
        url = entry.find('link', rel='alternate')['href']
        publication_date = entry.find('published').get_text(strip=True)
        updated_date = entry.find('updated').get_text(strip=True)

        # Convert date strings to datetime.date objects
        publication_date = _parse_date(publication_date)
        updated_date = _parse_date(updated_date)

        # Create and return the BibtexRecord
        bibtex_record = BibtexRecord(
            authors=authors,
            arxiv_doi=arxiv_doi,
            primary_category=primary_category,
            title=title,
            url=url,
            publication_date=publication_date,
            updated_date=updated_date
        )
        ret.append(bibtex_record)
    return ret


def _parse_date(date_string: str) -> datetime.date:
    """
    Parse a date string without using additional packages.

    Args:
        date_string (str): The input date string.

    Returns:
        datetime.date: The parsed date.
    """
    # Split the date string into date and time parts
    date_parts = date_string.split("T")[0].split("-")

    # Convert date parts to integers
    year, month, day = map(int, date_parts)

    return datetime.date(year, month, day)


def query_arxiv(arxiv_ids: list[str]) -> list[BibtexRecord]:
    """
    Query the arXiv API and return a BibtexRecord for the specified arXiv
    identifiers.

    Args:
        arxiv_ids (list[str]): The arXiv identifiers.

    Returns:
        list[BibtexRecord]: The BibtexRecords for the specified arXiv
        identifiers
    """
    raw_response = _query_arxiv_raw(','.join(arxiv_ids))
    bibtex_records = _construct_bibtex(raw_response.text)
    return bibtex_records


def arxiv_to_bibtex(urls: list[str], formatter=standard_bibtex_formatter) -> str:
    """
    Generate a BibTeX string from an arXiv URL.

    Args:
        urls list[str]: A list of arxiv URLs.
        formatter (function): A function to format the BibTeX record. Default
        is standard_bibtex_formatter.

    Returns:
        str: The BibTeX string.
    """
    ids = []
    for url in urls:
        arxiv_id = extract_arxiv_identifier(url)
        if not arxiv_id:
            raise ValueError("Invalid arXiv URL")
        ids.append(arxiv_id)
    bibtex_records = query_arxiv(ids)
    bibtex_string = []
    for bibtex_record in bibtex_records:
        bibtex_string.append(formatter(bibtex_record))
    return bibtex_string


def _flatten(lst):
    ret = []
    for item in lst:
        if isinstance(item, list):
            ret.extend(_flatten(item))
        else:
            ret.append(item)
    return ret


def main():
    parser = argparse.ArgumentParser(
        description="Generate BibTeX from an arXiv URL",
        epilog=(
            "See https://github.com/davidlowryduda/arxiv_to_bibtex for more.\n"
            "Report bugs to David Lowry-Duda <david@lowryduda.com>"
        ),
    )
    parser.add_argument(
        "--url",
        nargs="+",
        required=True,
        action="append",
        help="arXiv URL to generate BibTeX for. Multiple urls can be given, either with one --url or with multiple."
    )
    args = parser.parse_args()
    bibtex_string_list = arxiv_to_bibtex(_flatten(args.url))
    for bibtex_string in bibtex_string_list:
        print(bibtex_string)


if __name__ == "__main__":
    main()
