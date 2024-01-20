
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

To be written. <!-- TODO -->


## `arxiv_to_bibtex` in Javascript ##

I should preface by saying that I'm great at javascript. Nonetheless, the task
of querying the arXiv API and producing bibtex is very straightforward and there
is no reason why users of `arxiv_to_bibtex` need their own server.

To be written. <!-- TODO -->
