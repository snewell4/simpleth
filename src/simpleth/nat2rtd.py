"""
Convert a smart contract's Natspec comments to Read the Docs format.

This is used to build `simpleth` project `Read the Docs` pages for the
included smart contracts.

``compile.py`` creates the input files and writes them to the `artifact`
directory.

``make html`` processes the output files found in the `docs/source`
directory.

Inputs two JSON files,  ``<contract>.docdev`` and ``<contract>.docuser``,
that are created by the Solidity compiler that hold the Natspec comments
from the smart contract source.

The default for``in_dir`` is the `artifact` directory.

Outputs one `reStructured Text` file, ``<contract>.rst``, with the markup
suitable for processing by the `Sphinx` command, ``make html``, that is used
to generate an HTML page that shows the smart contract's `Natspec` comments
in a `Read the Docs` style.

The default for ``out_dir`` is the directory where `Sphinx` looks for the `rst`
files used to build the documentation for `simpleth`.

**USAGE**

.. code-block:: none

   nat2rtd.py [-h] [-i IN_DIR] [-s | -o OUT_DIR] <contract> [<contract> ...]


**EXAMPLES**

.. code-block::

   nat2rtd.py HelloWorld1.sol
   nat2rtd.py -f txt -s HelloWorld1.sol
   nat2rtd.py -f rtd -i ../artifacts -o ../doc HelloWorld1.sol HelloWorld2.sol


**TO MAKE SIMPLETH CONTRACT DOCUMENTATION**

From a command prompt, do:

.. code-block:: none

   nat2rtd.py ``contract``
   make html


**ASSUMES**

The file type, ``.py``, has been associated with `Python`. Otherwise, use:

.. code-block:: none

   python nat2rtd.py <args>


**NOTES**

   -  Follows the use of `Natspec tags` as shown in:
      https://docs.soliditylang.org/en/v0.8.9/natspec-format.html
   -  The ``@inheritdoc`` and ``@custom:`` Natspec tags are ignored.


**SEE ALSO**

-  To see the full help plus the default ``format``, ``in_dir``,
   and ``out_dir``, from a command line do:

   .. code-block:: none

      compile.py -h


**MODULES**
"""
import json
from argparse import ArgumentParser
import sys

import simpleth

#
# 3/26/21 sn - seems to be bug in solc.exe v7.5 about generating .docdev
# for a parent class methods and events. The child class has everything
# but for the parent only the .docuser info shows up. You'll find that
# events and methods for the parent will not output the "Notes:" and
# "Parameters:". I see this missing from the .docdev file so it's happening
# in solc. A newer release may fix.
#

TEXT_FILE_SUFFIX = '.txt'
MD_FILE_SUFFIX = '.md'
RST_FILE_SUFFIX = '.rst'
DOCUSER_FILE_SUFFIX = '.docuser'
DOCDEV_FILE_SUFFIX = '.docdev'


def get_docuser(file_name: str) -> dict:
    """Return dictionary of Natspec docuser file.

    :param file_name: file name of `.docuser` file created by
        the Solidity compiler
    :type file_name: str
    :rtype: dict
    :return: dictionary with `key` of user topics and `values` with
        comments from the smart contract source for that topic.

    """
    with open(file_name, encoding="latin-1") as docuser_file:
        docuser: dict = json.load(docuser_file)
    return docuser


def get_docdev(file_name: str) -> dict:
    """Return dictionary of Natspec docdev file.

    :param file_name: file name of `.docdev` file created by
        the Solidity compiler
    :type file_name: str
    :rtype: dict
    :return: dictionary with `key` of developer topics and `values` with
        comments from the smart contract source for that topic.

    """
    with open(file_name, encoding="latin-1") as docdev_file:
        docdev: dict = json.load(docdev_file)
    return docdev


def get_c_comments(docdev: dict, docuser: dict) -> dict:
    """Return the Natspec contract comments found in docdev and docuser.

    :param docdev: dictionary of docdev comments
    :type docdev: dict
    :param docuser: dictionary of docuser comments
    :type docuser: dict
    :rtype: dict
    :return: dictionary for the contract Natspec comments with
        `key` values for the topics and `values` with the text strings
        given for the topics related to the contract.
        (An empty string means the developer did not
        provide information for the topic).
    :notes: For some reason,the ``@dev`` that is specified in the
        contract for the developer's name appears for the
        ``details`` key.
    :see also: :meth:`get_docdev` and :meth:`get_docuser` to create
        ``docdev`` and ``docuser``.
    """
    c_comments: dict = {
        'title': '',
        'author': '',
        'notice': '',
        'dev': ''
        }
    if 'title' in docdev.keys():
        c_comments['title'] = docdev['title']
    if 'author' in docdev.keys():
        c_comments['author'] = docdev['author']
    if 'notice' in docuser.keys():
        c_comments['notice'] = docuser['notice']
    if 'details' in docdev.keys():
        c_comments['dev'] = docdev['details']
    return c_comments


def get_e_comments(docdev: dict, docuser: dict) -> list:
    """Return the Natspec event comments found in docdev and docuser.

    :param docdev: dictionary of docdev comments
    :type docdev: dict
    :param docuser: dictionary of docuser comments
    :type docuser: dict
    :return: list
    :return: list with dictionary items; each item has all
        Natspec comments for one `event`. The `key` is the
        topic and the `value` is the comment from the smart
        contract source file. If the `value` is an empty string,
        the developer did not provide a comment for that topic.
    :see also: :meth:`get_docdev` and :meth:`get_docuser` to create
        ``docdev`` and ``docuser``.
    """
    # get all comments for `events` from docdev
    if 'events' in docdev.keys():
        events_dev: set = set(docdev['events'].keys())
    else:
        events_dev = set()

    # get all comments for `events` from docuser
    if 'events' in docuser.keys():
        events_user: set = set(docuser['events'].keys())
    else:
        events_user = set()

    # create a list of the `event` names that have at least one
    # Natspec comment from either docdev or docuser. Sort the
    # method names alphabetically.
    event_names_list: list = list(events_dev.union(events_user))
    event_names_list.sort()

    # build a list of dictionary items that pertain to all
    # `methods` in the contract
    e_comments: list = []
    for e_name in event_names_list:
        e_comment: dict = {
            'event': e_name,
            'notice': '',
            'dev': '',
            'params': ''
            }
        if e_name in docuser['events'].keys():
            if 'notice' in docuser['events'][e_name].keys():
                e_comment['notice'] = docuser['events'][e_name]['notice']
        if e_name in docdev['events'].keys():
            if 'details' in docdev['events'][e_name].keys():
                e_comment['dev'] = docdev['events'][e_name]['details']
            if 'params' in docdev['events'][e_name].keys():
                e_comment['params'] = docdev['events'][e_name]['params']
        e_comments.append(e_comment)
    return e_comments


def get_m_comments(docdev: dict, docuser: dict) -> list:
    """Return the Natspec method comments found in docdev and docuser.

    :param docdev: dictionary of docdev comments
    :type docdev: dict
    :param docuser: dictionary of docuser comments
    :type docuser: dict
    :rtype: dict
    :return: list
    :return: list with dictionary items; each item has all
        Natspec comments for one `method`. The `key` is the
        topic and the `value` is the comment from the smart
        contract source file. If the `value` is an empty string,
        the developer did not provide a comment for that topic.
    :see also: :meth:`get_docdev` and :meth:`get_docuser` to create
        ``docdev`` and ``docuser``.
    """
    # get all comments for `methods` from docdev
    if 'methods' in docdev.keys():
        methods_dev: set = set(docdev['methods'].keys())
    else:
        methods_dev = set()

    # get all comments for `methods` from docuser
    if 'methods' in docuser.keys():
        methods_user: set = set(docuser['methods'].keys())
    else:
        methods_user = set()

    # create a list of the `method` names that have at least one
    # Natspec comment from either docdev or docuser. Sort the
    # method names alphabetically.
    method_names_list = list(methods_dev.union(methods_user))
    method_names_list.sort()

    # build a list of dictionary items that pertain to all
    # `methods` in the contract
    m_comments: list = []
    for m_name in method_names_list:
        m_comment: dict = {
            'method': m_name,
            'notice': '',
            'dev': '',
            'params': '',
            'returns': ''
            }
        if m_name in docuser['methods'].keys():
            if 'notice' in docuser['methods'][m_name].keys():
                m_comment['notice'] = docuser['methods'][m_name]['notice']
        if m_name in docdev['methods'].keys():
            if 'details' in docdev['methods'][m_name].keys():
                m_comment['dev'] = docdev['methods'][m_name]['details']
            if 'params' in docdev['methods'][m_name].keys():
                m_comment['params'] = docdev['methods'][m_name]['params']
            if 'returns' in docdev['methods'][m_name].keys():
                m_comment['returns'] = docdev['methods'][m_name]['returns']
        m_comments.append(m_comment)
        # move the constructor to front of list and add `()` to it
        m_comments = put_constructor_first_with_parens(m_comments)
    return m_comments


def get_v_comments(docdev: dict) -> list:
    """Return the Natspec variable comments found in docdev.

    :param docdev: dictionary of docdev comments
    :type docdev: dict
    :return: list
    :return: list with dictionary items; each item has all
        Natspec comments for one `variable`. The `key` is the
        topic and the `value` is the comment from the smart
        contract source file. If the `value` is an empty string,
        the developer did not provide a comment for that topic.
    :notes: `variable` comments are only found in docdev.
    :see also: :meth:`get_docdev` to create ``docuser``.
    """
    # get comments for `variables` (only found in docdev)
    if 'stateVariables' in docdev.keys():
        vars_dev: set = set(docdev['stateVariables'].keys())
    else:
        vars_dev = set()

    # create a list of the `variable` names that have at least one
    # Natspec comment in docdev. Sort the method names
    # alphabetically.
    var_names_list = list(vars_dev)
    var_names_list.sort()

    # build a list of dictionary items that pertain to all
    # `methods` in the contract
    v_comments = []
    for v_name in var_names_list:
        v_comment = {
            'stateVariable': v_name,
            'dev': ''
            }
        if v_name in docdev['stateVariables'].keys():
            if 'details' in docdev['stateVariables'][v_name].keys():
                v_comment['dev'] = docdev['stateVariables'][v_name]['details']
        v_comments.append(v_comment)
    return v_comments


#
# Read the Docs format print functions
#
# Uses rst markup tailored to make the output look good in a
# Read the Docs-style web page generated by Sphinx.
#
def print_blank_line() -> None:
    """Output a blank line - formatted for restructured text.

    :rtype: None
    """
    print('')


def print_c_section(c_comments: dict) -> None:
    """Output comments for one contract - formatted for restructured text.

    :param c_comments: all comments for the just the contract
    :type c_comments: dict
    :rtype: None
    """
    print('**Description:** {}'.format(c_comments['title']))
    print_blank_line()
    print('**Purpose:**  {}'.format(c_comments['notice']))
    print_blank_line()
    print('**Notes:**  {}'.format(c_comments['dev']))
    print_blank_line()
    print('**Author:**  {}'.format(c_comments['author']))


def print_e_section(e_comments: list) -> None:
    """Output the Events subsection

    :param e_comments: dictionary items, each with all comments
        about one event in the contract
    :type e_comments: list
    :rtype: None

    """
    for e_comment in e_comments:
        if e_comment['event']:
            print_heading4(e_comment['event'])
        if e_comment['notice']:
            print(f'**Purpose:**      {e_comment["notice"]}')
            print_blank_line()
        if e_comment['dev']:
            print(f'**Notes:**  {e_comment["dev"]}')
            print_blank_line()
        else:
            print_blank_line()
        if e_comment['params']:
            print_blank_line()
            print('**Parameters:**')
            print_blank_line()
            print_dict_as_list(e_comment['params'])
            print_blank_line()


def print_m_section(m_comments: list) -> None:
    """Output the Methods subsection

    :param m_comments: dictionary items, each with all comments
        about one public state variable in the contract
    :type m_comments: list
    :rtype: None

    """
    for m_comment in m_comments:
        if m_comment['method']:
            print_heading4(m_comment['method'])
        if m_comment['notice']:
            print(f'**Purpose:**  {m_comment["notice"]}')
            print_blank_line()
        if m_comment['dev']:
            print(f'**Notes:**  {m_comment["dev"]}')
            print_blank_line()
        else:
            print_blank_line()
        if m_comment['params']:
            print_blank_line()
            print('**Parameters:**')
            print_blank_line()
            print_dict_as_list(m_comment['params'])
            print_blank_line()
        if m_comment['returns']:
            print_blank_line()
            print('**Returns:**')
            print_blank_line()
            print_dict_as_list(m_comment['returns'])
            print_blank_line()


def print_v_section(v_comments: list):
    """Output the Variables subsection

    :param v_comments: dictionary items, each with all comments
        about one public state variable in the contract
    :type v_comments: list
    :rtype: None

    """
    print_blank_line()
    for v_comment in v_comments:
        print_dict_as_list(v_comment)
    print_blank_line()


def print_separator() -> None:
    """Output a separator - formatted for restructured text.

    Called by :meth:`print_rst`

    :rtype: None
    """
    print()
    print(f'{"_" * 80}')
    print()


def print_heading1(section_title: str) -> None:
    """Output header for events section - formatted for restructured text.

    :param section_title: name of the subsection
    :type section_title: str
    :rtype: None
    """
    print(f'{section_title}')
    print('=' * len(section_title))


def print_heading2(subsection_title: str) -> None:
    """Output header for events section - formatted for restructured text.

    :param subsection_title: name of the subsection
    :type subsection_title: str
    :rtype: None
    """
    print(f'{subsection_title}')
    print('*' * len(subsection_title))


def print_heading3(subsubsection_title: str) -> None:
    """Output header for events section - formatted for restructured text.

    :param subsubsection_title: name of the subsection
    :type subsubsection_title: str
    :rtype: None
    """
    print(f'{subsubsection_title}')
    print('#' * len(subsubsection_title))


def print_heading4(subsubsection_title: str) -> None:
    """Output header for events section - formatted for restructured text.

    :param subsubsection_title: name of the subsection
    :type subsubsection_title: str
    :rtype: None
    """
    print(f'{subsubsection_title}')
    print('-' * len(subsubsection_title))


def print_heading5(subsubsection_title: str) -> None:
    """Output header for events section - formatted for restructured text.

    :param subsubsection_title: name of the subsection
    :type subsubsection_title: str
    :rtype: None
    """
    print(f'{subsubsection_title}')
    print('"' * len(subsubsection_title))


def print_dict_as_list(dct: dict) -> None:
    """Output a list of comments for one of the sections - formatted as
    restructured text.

    This outputs a list with the key boldfaced and the value next to it.

    :param dct: dictionary to print as a list
    :type dct: dict
    :rtype: None
    """
    for key, value in dct.items():
        print(f'-  *{key}* - {value}')
    print_blank_line()


def put_constructor_first_with_parens(m_comments: list) -> list:
    """Return updated list of method comments with the `constructor()`
    as the first element.

    Look through the list of comments for all methods of a contract
    for the constructor. It may not be in the list. It may not be
    first. If found, put it at the front of the list and change
    its name from `constructor` to `constructor()`.

    :param m_comments: list of method comments. Each element is a
        dictionary describing one comment.
    :type m_comments: list
    :rtype: list
    :return: revised ``m_comments`` where the constructor method,
        if present, has been moved to the front and renamed from
        `constructor` to `constructor()`
    """
    for m_comment in m_comments:
        if m_comment['method'] == 'constructor':
            m_comment['method'] = 'constructor()'
            m_comment_constructor = m_comment
            m_comments.remove(m_comment)
            m_comments = [m_comment_constructor] + m_comments
    return m_comments


def main():
    """Start script processing here"""
    parser = ArgumentParser(
        description='Output Natspec comments in contract to Read the Doc format.'
        )
    parser.add_argument(
        '-i', '--in_dir',
        action='store',
        default=f'{simpleth.PROJECT_HOME}/{simpleth.ARTIFACT_SUBDIR}',
        help=(
            'input directory with artifact files\n'
            'default: %(default)s'
            )
        )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-s', '--stdout',
        action='store_true',
        help='write output to STDOUT'
        )
    group.add_argument(
        '-o', '--out_dir',
        action='store',
        default=f'{simpleth.PROJECT_HOME}/{simpleth.RST_DOC_SUBDIR}',
        help=(
            'output directory for formatted documentation file\n'
            'default: %(default)s'
            )
        )
    parser.add_argument(
        'contracts',
        nargs='+',
        metavar='<contract>',
        help='contract file (use of the suffix ``.sol`` is optional)'
        )

    args = parser.parse_args()

    for contract in args.contracts:
        #
        # Get contract name. If user entered contract with filename
        # suffix, remove it.
        #
        contract: str = contract.replace('.sol', '')

        #
        # Setup the output file. If user asked to use STDOUT,
        # no need to setup any output file.
        #
        if not args.stdout:
            out_file: str = f'{args.out_dir}/{contract}{RST_FILE_SUFFIX}'
            sys.stdout = open(out_file, 'w', encoding="latin-1")

        #
        # Read the JSON info from the .docdev and .docuser files
        # into docdev and docuser.
        #
        docuser_file: str =\
            f'{args.in_dir}/{contract}{DOCUSER_FILE_SUFFIX}'
        docdev_file: str =\
            f'{args.in_dir}/{contract}{DOCDEV_FILE_SUFFIX}'
        docuser: dict = get_docuser(docuser_file)
        docdev: dict = get_docdev(docdev_file)

        #
        # Go through all the Natspec comments in docdev and docuser
        # and separate them into lists of dictionaries grouped
        # into Class, Method, Event, and Variable comments
        #
        c_comments: dict = get_c_comments(docdev, docuser)
        m_comments: list = get_m_comments(docdev, docuser)
        e_comments: list = get_e_comments(docdev, docuser)
        v_comments: list = get_v_comments(docdev)

        #
        # Output the sections with rst markup suitable for
        # Read the Docs formatting.
        #

        print_heading1(contract)
        print_c_section(c_comments)
        print_separator()

        print_heading3('STATE VARIABLES')
        if v_comments:
            print_v_section(v_comments)
        else:
            print('None')
        print_separator()

        print_heading3('METHODS')
        if m_comments:
            print_m_section(m_comments)
        else:
            print('None')
        print_separator()

        print_heading3('EVENTS')
        if e_comments:
            print_e_section(e_comments)
        else:
            print('None')
        print_separator()

    print_separator()
    print_blank_line()   # needed after the final separator


if __name__ == '__main__':
    main()
