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
from . import arxiv
from . import bibtex_record
from . import cli


__all__ = ["arxiv", "bibtex_record", "cli"]


__VERSION__ = "0.5"
