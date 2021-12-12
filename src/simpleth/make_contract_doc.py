"""
Read Solidity contract documentation files and output documentation in the
selected markup file.

Reads the ``contract`` `.docdev` and `.docuser` files found in ``in_dir``, adds
the specified ``format`` markup, combines them into one file and writes
that marked-up documentation file to ``out_dir`` or `STDOUT`.

The defaults are set to make contract documentation ready for the `Sphinx`
``make html`` command. This is the command used to create the `Read The Docs`
`html` files. For normal `simpleth` use, just run:

.. code-block:: none

   make_contract_doc.py ``contract``

**USAGE**

.. code-block:: none

   make_contract_doc.py [-h] [-f {rst,text,md,uml}] [-i IN_DIR] [-s | -o OUT_DIR] <contract> [<contract> ...]

**EXAMPLE**

.. code-block::

   make_contract_doc.py HelloWorld.sol

**ASSUMES**

The file type, `.py`, has been associated with `Python`. Otherwise, use:

.. code-block:: none

   python make_contract_doc.py

**SEE ALSO**

-  To see the full help plus the default ``format``, ``in_dir``,
   and ``out_dir``, from a command line do:

   .. code-block:: none

      compile.py -h

"""
import json
from argparse import ArgumentParser, RawTextHelpFormatter
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
    return m_comments


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
# Markdown format print functions
#
def print_blank_line_md() -> None:
    """Output a blank line - formatted for markdown.

    Called by :meth:`print_md`

    :rtype: None
    """
    print('\\')


def print_c_comments_md(c_name: str, c_comments: dict) -> None:
    """Output comments for one contract - formatted for markdown.

    Called by :meth:`print_md`

    :param c_name: contract name
    :type c_name: str
    :param c_comments: all comments for the just the contract
    :type c_comments: dict
    :rtype: None
    """
    print('# {}'.format(c_name))
    print('**Description:** {}'.format(c_comments['title']))
    print_blank_line_md()
    print('**Purpose:**  {}'.format(c_comments['notice']))
    print_blank_line_md()
    print('**Notes:**  {}'.format(c_comments['dev']))
    print_blank_line_md()
    print('**Author:**  {}'.format(c_comments['author']))


def print_e_comment_hdr_md() -> None:
    """Output header for events section - formatted for markdown.

    Called by :meth:`print_md`

    :rtype: None
    """
    print('## Events')


def print_e_comment_md(e_comment: dict) -> None:
    """Output comments for one event - formatted for markdown.

    Called by :meth:`print_md`

    :param e_comment: all comments for one event
    :type e_comment: dict
    :rtype: None
    """
    print('### {}'.format(e_comment['event']))
    if e_comment['notice']:
        print('**Purpose:**      {}'.format(e_comment['notice']))
    if e_comment['dev']:
        print('**Notes:**  {}'.format(e_comment['dev']))
    else:
        print('')
    if e_comment['params']:
        print('')
        print('**Parameters:**')
        print('')
        print('|Name|Description|')
        print('|----|-----------|')
        for param, desc in e_comment['params'].items():
            print('|`{}`|{}|'.format(param, desc))
        print('')


def print_m_comment_hdr_md() -> None:
    """Output header for methods section - formatted for markdown.

    Called by :meth:`print_md`

    :rtype: None
    """
    print('## Methods')


def print_m_comment_md(m_comment: dict) -> None:
    """Output comments for one method - formatted for markdown.

    Called by :meth:`print_md`

    :param m_comment: all comments for one method
    :type m_comment: dict
    :rtype: None
    """
    print('### {}'.format(m_comment['method']))
    if m_comment['notice']:
        print('**Purpose:**      {}'.format(m_comment['notice']))
    if m_comment['dev']:
        print('**Notes:**  {}'.format(m_comment['dev']))
    else:
        print('')
    if m_comment['params']:
        print('')
        print('**Parameters:**')
        print('')
        print('|Name|Description|')
        print('|----|-----------|')
        for param, desc in m_comment['params'].items():
            print('|`{}`|{}|'.format(param, desc))
        print('')
    if m_comment['returns']:
        print('')
        print('**Returns:**')
        print('')
        print('|Name|Description|')
        print('|----|-----------|')
        for ret, desc in m_comment['returns'].items():
            print('|`{}`|{}|'.format(ret, desc))
        print('')


def print_md(
        c_name: str,
        c_comments: dict,
        m_comments: list,
        e_comments: list,
        v_comments: list
    ) -> None:
    """Output all comments for a contract - formatted for markdown.

    This is the function that controls the printing of all comments
    for one contract to the output file.

    :param c_name: contract name
    :type c_name: str
    :param c_comments: all comments about the contract
    :type c_comments: dict
    :param m_comments: dictionary items, each with all comments
        about one method (ie., function) in the contract
    :type m_comments: list
    :param e_comments: dictionary items, each with all comments
        about one event in the contract
    :type e_comments: list
    :param v_comments: dictionary items, each with all comments
        about one public state variable in the contract
    :type v_comments: list
    """
    print_c_comments_md(c_name, c_comments)
    print_separator_md()

    if v_comments:
        print_v_comment_hdr_md()
        for v_comment in v_comments:
            print_v_comment_md(v_comment)
        print_separator_md()

    if m_comments:
        print_m_comment_hdr_md()
        m_comments = put_constructor_first_with_parens(m_comments)
        for m_comment in m_comments:
            print_m_comment_md(m_comment)
            print_separator_md()

    if e_comments:
        print_e_comment_hdr_md()
        for e_comment in e_comments:
            print_e_comment_md(e_comment)
            print_separator_md()


def print_separator_md() -> None:
    """Output a separator - formatted for markdown.

    Called by :meth:`print_md`

    :rtype: None
    """
    print('---')


def print_v_comment_hdr_md() -> None:
    """Output header for state variables section - formatted for
    markdown.

    Called by :meth:`print_md`

    :rtype: None
    """
    print('## State Variables')
    print('')
    print('|Name|Description|')
    print('|----|-----------|')


def print_v_comment_md(v_comment: dict) -> None:
    """Output comments for one state variable - formatted for markdown.

    Called by :meth:`print_md`

    :param v_comment: all comments for one state variable
    :type v_comment: dict
    :rtype: None
    """
    print('|`{}`|{}|'.format(v_comment['stateVariable'], v_comment['dev']))


#
# reStructured format print functions
#
def print_blank_line_rst() -> None:
    """Output a blank line - formatted for restructured text.

    Called by :meth:`print_rst`

    :rtype: None
    """
    print('')


def print_c_comments_rst(c_name: str, c_comments: dict) -> None:
    """Output comments for one contract - formatted for restructured text.

    Called by :meth:`print_rst`

    :param c_name: contract name
    :type c_name: str
    :param c_comments: all comments for the just the contract
    :type c_comments: dict
    :rtype: None
    """
    print('=' * len(c_name))
    print(f'{c_name}')
    print('=' * len(c_name))
    print('**Description:** {}'.format(c_comments['title']))
    print_blank_line_rst()
    print('**Purpose:**  {}'.format(c_comments['notice']))
    print_blank_line_rst()
    print('**Notes:**  {}'.format(c_comments['dev']))
    print_blank_line_rst()
    print('**Author:**  {}'.format(c_comments['author']))


def print_e_comment_hdr_rst() -> None:
    """Output header for events section - formatted for restructured text.

    Called by :meth:`print_rst`

    :rtype: None
    """
    print_subsection_hdr_rst('Events')



def print_e_comment_rst(e_comment: dict) -> None:
    """Output comments for one event - formatted for restructured text.

    Called by :meth:`print_rst`

    :param e_comment: all comments for one event
    :type e_comment: dict
    :rtype: None
    """
    print_subsubsection_hdr_rst(e_comment['event'])
    if e_comment['notice']:
        print(f'**Purpose:**      {e_comment["notice"]}')
    if e_comment['dev']:
        print(f'**Notes:**  {e_comment["dev"]}')
    else:
        print('')
    if e_comment['params']:
        print('')
        print('**Parameters:**')
        print('')
        print('+----+-----------+')
        print('|Name|Description|')
        print('+----+-----------+')
        for param, desc in e_comment['params'].items():
            print(f'|``{param}``|{desc}|')
            print('+----+-----------+')
        print('')


def print_m_comment_hdr_rst() -> None:
    """Output header for methods section - formatted for restructured text.

    Called by :meth:`print_rst`

    :rtype: None
    """
    print_subsection_hdr_rst('Methods')


def print_m_comment_rst(m_comment: dict) -> None:
    """Output comments for one method - formatted for restructured text.

    Called by :meth:`print_rst`

    :param m_comment: all comments for one method
    :type m_comment: dict
    :rtype: None
    """
    print_subsubsection_hdr_rst(m_comment['method'])
    if m_comment['notice']:
        print(f'**Purpose:**      {m_comment["notice"]}')
    if m_comment['dev']:
        print(f'**Notes:**  {m_comment["dev"]}')
    else:
        print('')
    if m_comment['params']:
        print('')
        print('**Parameters:**')
        print('')
        print('+----+-----------+')
        print('|Name|Description|')
        print('+----+-----------+')
        for param, desc in m_comment['params'].items():
            print(f'|``{param}``|{desc}|')
            print('+----+-----------+')
        print('')
    if m_comment['returns']:
        print('')
        print('**Returns:**')
        print('')
        print('+----+-----------+')
        print('|Name|Description|')
        print('+----+-----------+')
        for ret, desc in m_comment['returns'].items():
            print(f'|``{ret}``|{desc}|')
            print('+----+-----------+')
        print('')


def print_rst(
        c_name: str,
        c_comments: dict,
        m_comments: list,
        e_comments: list,
        v_comments: list
        ) -> None:
    """Output all comments for a contract - formatted for restructured text.

    This is the function that controls the printing of all comments
    for one contract to the output file.

    :param c_name: contract name
    :type c_name: str
    :param c_comments: all comments about the contract
    :type c_comments: dict
    :param m_comments: dictionary items, each with all comments
        about one method (ie., function) in the contract
    :type m_comments: list
    :param e_comments: dictionary items, each with all comments
        about one event in the contract
    :type e_comments: list
    :param v_comments: dictionary items, each with all comments
        about one public state variable in the contract
    :type v_comments: list
    """
    print_c_comments_rst(c_name, c_comments)
    print_separator_rst()

    if v_comments:
        print_v_comment_hdr_rst()
        for v_comment in v_comments:
            print_v_comment_rst(v_comment)
        print_v_comment_table_close_rst()
        print_separator_rst()

    if m_comments:
        print_m_comment_hdr_rst()
        m_comments = put_constructor_first_with_parens(m_comments)
        for m_comment in m_comments:
            print_m_comment_rst(m_comment)
            print_separator_rst()

    if e_comments:
        print_e_comment_hdr_rst()
        for e_comment in e_comments:
            print_e_comment_rst(e_comment)
            print_separator_rst()


def print_separator_rst() -> None:
    """Output a separator - formatted for restructured text.

    Called by :meth:`print_rst`

    :rtype: None
    """
#   print('~' * 80)
    print()


def print_subsection_hdr_rst(subsection_title: str) -> None:
    """Output header for events section - formatted for restructured text.

    :param subsection_title: name of the subsection
    :type subsection_title: str
    :rtype: None
    """
    print(f'{subsection_title}')
    print('-' * len(subsection_title))


def print_subsubsection_hdr_rst(subsubsection_title: str) -> None:
    """Output header for events section - formatted for restructured text.

    :param subsubsection_title: name of the subsection
    :type subsubsection_title: str
    :rtype: None
    """
    print(f'{subsubsection_title}')
    print('^' * len(subsubsection_title))



def print_v_comment_hdr_rst() -> None:
    """Output header for state variables section - formatted for
    restructured text.

    Called by :meth:`print_rst`

    :rtype: None
    """
    print_subsection_hdr_rst('State Variables')
    print('')
    print('+----+-----------+')
    print('|Name|Description|')
    print('+----+-----------+')


def print_v_comment_rst(v_comment: dict) -> None:
    """Output comments for one state variable - formatted for restructured text.

    Called by :meth:`print_rst`

    :param v_comment: all comments for one state variable
    :type v_comment: dict
    :rtype: None
    """
    print(f'|``{v_comment["stateVariable"]}``|{v_comment["dev"]}|')

def print_v_comment_table_close_rst() -> None:
    print('+----+-----------+')
    print()


#
# Text format print routines
#
def print_c_comments_text(c_comments: dict) -> None:
    """Output comments for one contract - formatted for plain text.

    Called by :meth:`print_text`

    :param c_comments: all comments for the just the contract
    :type c_comments: dict
    :rtype: None
    """
    print('TITLE:    {}'.format(c_comments['title']))
    print('AUTHOR:   {}'.format(c_comments['author']))
    print('NOTICE:   {}'.format(c_comments['notice']))
    print('DEV:      {}'.format(c_comments['dev']))


def print_e_comment_text(e_comment: dict) -> None:
    """Output comments for one event - formatted for plain text.

    Called by :meth:`print_text`

    :param e_comment: all comments for one event
    :type e_comment: dict
    :rtype: None
    """
    print('EVENT:    {}'.format(e_comment['event']))
    print('NOTICE:   {}'.format(e_comment['notice']))
    print('DEV:      {}'.format(e_comment['dev']))
    if e_comment['params'] == '':
        print('PARAM:')
    else:
        for param, desc in e_comment['params'].items():
            print('PARAM:    {} - {}'.format(param, desc))


def print_m_comment_text(m_comment: dict) -> None:
    """Output comments for one method - formatted for plain text.

    Called by :meth:`print_text`

    :param m_comment: all comments for one method
    :type m_comment: dict
    :rtype: None
    """
    print('METHOD:   {}'.format(m_comment['method']))
    print('NOTICE:   {}'.format(m_comment['notice']))
    print('DEV:      {}'.format(m_comment['dev']))
    if m_comment['params'] == '':
        print('PARAM:')
    else:
        for param, desc in m_comment['params'].items():
            print('PARAM:    {} - {}'.format(param, desc))
    if m_comment['returns'] == '':
        print('RETURN: ')
    else:
        for ret, desc in m_comment['returns'].items():
            print('RETURN:   {} - {}'.format(ret, desc))


def print_separator_text():
    """Output a separator - formatted for plain text.

    Called by :meth:`print_text`
    """
    print('============================')


def print_v_comment_text(v_comment: dict) -> None:
    """Output comments for one variable - formatted for plain text.

    Called by :meth:`print_text`

    :param v_comment: all comments for one state variable
    :type v_comment: dict
    :rtype: None
    """
    print('VARIABLE: {}'.format(v_comment['stateVariable']))
    print('DEV:      {}'.format(v_comment['dev']))


def print_text(
        c_comments: dict,
        m_comments: list,
        e_comments: list,
        v_comments: list
        ) -> None:
    """Output all comments for a contract - formatted for plain text.

    This is the function that controls the printing of all comments
    for one contract to the output file.

    :param c_comments: all comments about the contract
    :type c_comments: dict
    :param m_comments: dictionary items, each with all comments
        about one method (ie., function) in the contract
    :type m_comments: list
    :param e_comments: dictionary items, each with all comments
        about one event in the contract
    :type e_comments: list
    :param v_comments: dictionary items, each with all comments
        about one public state variable in the contract
    :type v_comments: list
    """
    print_c_comments_text(c_comments)
    print_separator_text()

    for v_comment in v_comments:
        print_v_comment_text(v_comment)
        print_separator_text()

    for m_comment in m_comments:
        print_m_comment_text(m_comment)
        print_separator_text()

    for e_comment in e_comments:
        print_e_comment_text(e_comment)
        print_separator_text()


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
        description='Output formatted Natspec comments with specified markup.',
        formatter_class=RawTextHelpFormatter
        )
    parser.add_argument(
        '-f', '--format',
        choices=['rst', 'md', 'text'],
        default='rst',
        help=(
            'output formatting: reStructured Text, Markdown, or plain text\n'
            'default: %(default)s'
            )
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
        # if user entered contract with filename suffix, remove it.
        contract: str = contract.replace('.sol', '')
        if not args.stdout:
            if args.format == 'text':
                suffix = TEXT_FILE_SUFFIX
            elif args.format == 'md':
                suffix = MD_FILE_SUFFIX
            elif args.format == 'rst':
                suffix = RST_FILE_SUFFIX
            else:
                print(
                    f'ERROR: unexpected format of: "{args.format}". '
                    f'Must exit.'
                    )
                sys.exit()
            out_file: str = f'{args.out_dir}/{contract}{suffix}'
            sys.stdout = open(out_file, 'w', encoding="latin-1")

        docuser_file: str =\
            f'{args.in_dir}/{contract}{DOCUSER_FILE_SUFFIX}'
        docdev_file: str =\
            f'{args.in_dir}/{contract}{DOCDEV_FILE_SUFFIX}'

        docuser: dict = get_docuser(docuser_file)
        docdev: dict = get_docdev(docdev_file)

        c_comments: dict = get_c_comments(docdev, docuser)
        m_comments: list = get_m_comments(docdev, docuser)
        e_comments: list = get_e_comments(docdev, docuser)
        v_comments: list = get_v_comments(docdev)

        if args.format == 'text':
            print_text(
                c_comments,
                m_comments,
                e_comments,
                v_comments
                )
        elif args.format == 'md':
            print_md(
                contract,
                c_comments,
                m_comments,
                e_comments,
                v_comments
                )
        elif args.format == 'rst':
            print_rst(
                contract,
                c_comments,
                m_comments,
                e_comments,
                v_comments
                )


if __name__ == '__main__':
    main()
