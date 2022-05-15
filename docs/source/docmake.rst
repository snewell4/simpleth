:Description: Create Read-the-Docs HTML files

:Purpose:  Run to generate new version of online documentation.

:Usage: ``docmake``

:Important: Run ``make clean`` first to create a fresh set
    documentation files. This is needed when you add or
    remove any <file>.rst files or change the table of contents.

:Notes:  Runs:

* nat2rst.py to create the ReStructured Text files from
  the Natspec comments in smart contracts.
* Sphinx ``make html`` to create RtD HTML pages from the
  '.rst' files in docs\source.

Be sure to recompile contracts if you make any changes to
the Natspec comments. A compile updates the 'docdev' and
'docuser' files in the 'artifacts' directory. nat2rsd.py
reads those files to get the comments.

