Style Guide for Simpleth
========================
This document serves as an example of reSTructured Text
formatting and style to be used.
Website in `Links`_ has full Sphinx Cheat Sheet.


.. seealso::

   1. `Sphinx Tutorial Cheat Sheet <https://sphinx-tutorial.readthedocs.io/cheatsheet/>`_
   2. `RST / Sphinx / Sublime / Github Cheat Sheet <https://sublime-and-sphinx-guide.readthedocs.io/en/latest/index.html#work-with-rst-content>`_


.. image:: ../images/section_separator.png

Headings
********

Level 1
"""""""
Use ``======``

Level 2
"""""""
Use ``*****``

Level 3
"""""""
Use ``"""""``

Level 4
"""""""
Use ``^^^^^``

Notes:

- The heading structure is determined by order; not by characters used.
  That order is set by the first document. For simpleth, **use the characters above** .
- Heading overline is optional.
- See website in `External`_ for list of permissible underline characters.


.. image:: ../images/section_separator.png

Inline formatting
*****************

Italic
""""""
*looks like this*

Bold
""""
**looks like this**

Verbatim (for code)
"""""""""""""""""""
``looks like this``

Must have whitespace before and after the **\*** and **\\** chars.
So, long\ *ish* is done with ``long\ *ish*``


.. image:: ../images/section_separator.png

Links
*****

Internal
""""""""
Link to a heading within this file:
`Level 2`_

External
""""""""
Link to a website: `Sphinx Tutorial Cheat Sheet <https://sphinx-tutorial.readthedocs.io/cheatsheet/>`_


.. image:: ../images/section_separator.png

Lists
*****
Lists must have blank line before and after.

Bulleted list
"""""""""""""

- Item 1
- Item 2
- Item 3 is much longer to show how to have a multi-line
  item that formats properly.

Bullet characters include: **-**, **+**, and **\***. Use: ``-``

Numbered list
"""""""""""""
There are two approaches. Most flexible to use **#**

**Created using #**

#. Item 1
#. Item 2
#. Item 3

**Created using digits**

1. Item 1
2. Item 2
3. Item 3


Nested Items
""""""""""""
Seems like only one level of nesting is supported.

**Sub-item in unordered list**

- Item 1

  - Item 1A

- Item 2

**Sub-item in ordered list**

1. Item 1

   a. Item 1A

2. Item 2


.. image:: ../images/section_separator.png

Definition List
***************

First term
   Definition of this term.
   With multiple lines.

Second term
   Definition of this term.

   With a second paragraph.


.. image:: ../images/section_separator.png

Tables
******

Simple Table
""""""""""""

=======  =======  =======
Header1  Header2  Header3
=======  =======  =======
xxx      yyyy     zzzz
xxx      yyyy     zzzz
xxx      yyyy     zzzz
=======  =======  =======


Grid Table
""""""""""

+-----------+---------+---------+
|  Header1  | Header2 | Header3 |
+===========+=========+=========+
| xxx       | yyy     | zzz     |
+-----------+---------+---------+
| xxx       | yyy     | zzz     |
+-----------+---------+---------+
| Horizontal span     | zzz     |
+-----------+---------+---------+
| xxx       | yyy     | Vertical|
+-----------+---------+ span    |
| xxx       | yyy     |         |
+-----------+---------+---------+


List Table
""""""""""

.. list-table:: Title of List Table
   :widths: 25 25 50
   :header-rows: 1
   :align: center

   * - Header1
     - Header2
     - Header3
   * - xxx
     -
     - zzz
   * - xxx
     - yyy
     - zzz


CSV Table
"""""""""
You can create a CSV table in an external file and pull it in.
See: `Using a CSV table <https://sublime-and-sphinx-guide.readthedocs.io/en/latest/tables.html#csv-files>`_


.. image:: ../images/section_separator.png

Code Block
**********

Python
""""""

**No directives for highlighting**

.. code-block:: python

  pygments_style = 'sphinx'
  test[0] = 'string'
  dict['key'] = value

**Directives for highlighting**

.. code-block:: python
  :linenos:
  :emphasize-lines: 1, 3
  :caption: Python code sample with caption, line nums, highlighting

  pygments_style = 'sphinx'
  test[0] = 'string'
  dict['key'] = value


Shell
"""""
.. code-block:: shell-session

  $ nat2rtd.py -I ../test


Literal Block
"""""""""""""
Literal block::

  Line 1
  Line 2
  Line 3

Literal block without the ':' at end of this line ::

  Line 1
  Line 2
  Line 3


HTML
""""
**Source:**

.. code-block:: HTML

   <i>HTML italic</i>
   <p></p>

**Formatted:**

.. raw:: html

   <i>HTML italic</i>
   <p></p>


.. image:: ../images/section_separator.png

Note Block
**********
.. note::
   This is note text. Use a note for information you want the user to
   pay particular attention to.

   If note text runs over a line, make sure the lines wrap and are indented to
   the same level as the note tag. If formatting is incorrect, part of the note
   might not render in the HTML output.

   Notes can have more than one paragraph. Successive paragraphs must
   indent to the same level as the rest of the note.


.. image:: ../images/section_separator.png

Warning Block
*************
.. warning::
   This is warning text. Use a warning for information the user must
   understand to avoid negative consequences.

   Warnings are formatted in the same way as notes. In the same way,
   lines must be broken and indented under the warning tag.


.. image:: ../images/section_separator.png


Other Content Blocks
********************
.. attention:: Attention text

.. caution:: Caution text

.. danger:: Danger text

.. error:: Error text

.. hint:: Hint text

.. important:: Important text

.. tip:: Tip text

.. seealso:: See Also text.

   `Style Guide for Simpleth`_ has an example.

.. deprecated:: V2.3
   Deprecated text

.. versionadded:: V2.5
   Version Added text

.. versionchanged:: V2.4
   Version Changed text

.. math:: Math text


.. image:: ../images/section_separator.png

Comments
********
A single line comment follows this line and does not show up.

.. Single line comment

A multi-line comment follows this line and  does not show up.

..
   Line 1
   Line 2
   Line 3

End line of visible text.


.. image:: ../images/section_separator.png