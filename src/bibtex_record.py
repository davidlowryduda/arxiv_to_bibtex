"""
bibtex_record.py - BibtexRecord class and its formatters

This is where BibtexRecord and standard_bibtex_formatter are defined. The
BibtexRecord class holds most of the relevant data **for things coming from the
arxiv**, which means that it doesn't include some basic information typically
found in bibliographies. For example, there won't be information on the actual
publication, even though this is some time ad-hoc encoded in arxiv's "comment"
metadata.

A formatter is just a function with the signature

    formatter(r: BibtexRecord) -> str

that produces a bibtex string from a given BibtexRecord. It is straightforward
to change or exchange the formatter. Here, I have the formatter I use in my
notes.

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
import datetime
import string


from dataclasses import dataclass


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


UNIMPORTANT_WORDS = [
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


def first_significant_word(title: str) -> str:
    """
    Extract the first nontrivial word from a title.

    Args:
        title (str): The input title.

    Returns:
        str: The first nontrivial word.
    """
    words = title.split()
    for word in words:
        if word.lower() not in UNIMPORTANT_WORDS:
            return ''.join(
                [l for l in word if l not in string.punctuation]
            )
    return ""
