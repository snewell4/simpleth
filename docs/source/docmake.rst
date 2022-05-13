:Description: Create Read-the-Docs HTML files

:Purpose:  Run to generate new version of online documentation.

:Usage: docmake

:Notes: Runs:

* nat2rst.py to create the ReStructured Text files from
  the Natspec comments in smart contracts.
* Sphinx 'make html' to create RtD HTML pages from the
  '.rst' files in docs\source.

Use command 'make clean' first to clear out existing documentation
files when you change the structure of the documentation
(ie., changing index or file names).

Be sure to recompile contracts if you make any changes to
the Natspec comments. A compile updates the 'docdev' and
'docuser' files in the 'artifacts' directory. nat2rsd.py
reads those files to get the comments.
