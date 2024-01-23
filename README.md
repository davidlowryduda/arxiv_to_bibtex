
# arxiv_to_bibtex #

**arxiv_to_bibtex** is a simple commandline tool that takes one or more urls to
[the arXiv](https://arxiv.org/) and returns bibtex for them.

This is strongly inspired by Sven Porst's
[arxiv2bibtex](https://arxiv2bibtex.org/), which I used for several years. But
I was looking for a programmatic way to handle this conversion recently and I
saw that Porst's code is intermixed in a `cgi` script that runs the site.

I wanted a version that is leaner and simpler, and which separates the code for
interacting with the arXiv API and utility. In practice, this is nothing more
than a small wrapper around the arXiv API.

This repository contains two distinct implementations. The first is a python
package, `arxiv_to_bibtex`, contained in [./src](./src). The second is a
standalone HTML+CSS+javascript version that contains the same logic, but in
javascript form.


## `arxiv_to_bibtex` in Python ##

As this is not on the [Python Package Index](https://pypi.org/) at the moment,
it is first necessary to obtain a copy of the code. The easiest way to do this
is by cloning the repository (or just the `/src/arxiv_to_bibtex` directory).
The directory `/src/arxiv_to_bibtex` is a callable module. For example, with
this directory in your current directory, you can call it with

    python -m arxiv_to_bibtex -h

to see a commandline *usage* message. Alternately, you can clone the repository
and then perform a local pip installation (`pip install .` from the cloned
repository). If you do this, you will now have a command `arxiv_to_bibtex`.

In either case, the commandline utility has exactly one interface command. This
is to do

    arxiv_to_bibtex --url [ARXIVURL ..]

with either one or more urls of arxiv papers. For example,

    arxiv_to_bibtex --url https://arxiv.org/abs/2007.14324 https://arxiv.org/abs/2204.01651

will give the output


    @misc{hulse2020arithmetic,
          title={Arithmetic Progressions of Squares and Multiple Dirichlet Series},
          author={Thomas A. Hulse and Chan Ieong Kuan and David Lowry-Duda and Alexander Walker},
          year={2020},
          howpublished="\url{http://arxiv.org/abs/2007.14324v4}",
          note={arXiv:math.NT:2007.14324v4},
    }
    @misc{anderson2022improved,
          title={Improved bounds on number fields of small degree},
          author={Theresa C. Anderson and Ayla Gafni and Kevin Hughes and
                  Robert J. Lemke Oliver and David Lowry-Duda and
                  Frank Thorne and Jiuya Wang and Ruixiang Zhang},
          year={2022},
          howpublished="\url{http://arxiv.org/abs/2204.01651v3}",
          note={arXiv:math.NT:2204.01651v3},
    }

(I added a couple of linebreaks for readability). These are ready for direct
insertion into a bibtex database.

As we can observe, the rule for the citation key is to take the last name of
the first author, the year, and then the first word of the paper. There is a
small amount of normalization: some punctuation is stripped from last names (so
my last name would become `lowryduda`), and "unimportant" words are omitted
from titles. There is a short list of "unimportant" words in the source, and
the program simply looks for the first word in the title that *isn't*
unimportant.


### As a library ###

The basic utilities are exposed in the code as a very simple library. There is
one tool of interest (that fits into my own use case). Internally, there are
commands to

- find an arxiv identifier from a url (e.g. extract `2204.01651` from
  `https://arxiv.org/abs/2204.01651`),
- query the arxiv API for a url (or really, to batch a list of urls into a
  single API call),
- to parse the arxiv API response into a custom dataclass called
  `BibtexRecord`, and
- format a `BibtexRecord` into a bibtex string.

If you wanted to alter the output of this code to produce a different bibtex
string for the same record, it is only necessary to write a `formatter`
function that takes a `BibtexRecord` and outputs the desired string; then pass
this formatter as the second optional parameter to
`arxiv.arxiv_to_bibtex`.

The default formatter is called `bibtex_record.standard_bibtex_formatter`, and
can be used as a model.

(I do not expect anyone to ever this except for me. If you do, let me know!)


## `arxiv_to_bibtex` in Javascript ##

I should preface by saying that I'm great at javascript. Nonetheless, the task
of querying the arXiv API and producing bibtex is very straightforward and there
is no reason why users of `arxiv_to_bibtex` need their own server.

In `/html_version/`, there is a single `html` page (with mediocre CSS included)
that contains a javascript version of `arxiv_to_bibtex`. Opening this page in
your preferred browser (or serving the page with, e.g., `python -m http.server`
and opening that page) opens a web version.

The only interaction in this web version is to ping the arxiv's API and parse
the response, all client-side with javascript.

At some point in the future, I'll probably have a version of this page running.
