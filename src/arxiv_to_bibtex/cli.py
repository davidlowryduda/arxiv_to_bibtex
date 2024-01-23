"""
cli.py - commandline interface

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


from .arxiv import arxiv_to_bibtex


def _flatten(lst):
    ret = []
    for item in lst:
        if isinstance(item, list):
            ret.extend(_flatten(item))
        else:
            ret.append(item)
    return ret


def main_cli():
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
