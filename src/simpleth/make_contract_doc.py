"""
Read Solidity contract documentation files and output the selected markup file.

Reads the ``contract`` `.docdev` and `.docuser` files fourd in ``in_dir``, adds
the specified ``markup`` to format them, combines them into one file and writes
that marked-up ``file`` to ``out_dir``.

The defaults are set to make contract documentation ready for the `Sphinx`
``make html`` command. This is the command used to create the `Read The Docs`
`html` files. For normal `simpleth` use, just run:

.. code-block:: none

   make_contract_doc.py ``contract``

**USAGE**

.. code-block:: none

   make_contract_doc.py [-m ``markup``] [-i ``in_dir``] [-o ``out_dir``] ``contract``

**EXAMPLE**

.. code-block::

   make_contract_doc.py HelloWorld.sol

**ASSUMES**

The file type, `.py`, has been associated with `Python`. Otherwise, use:

.. code-block:: none

   python make_contract_doc.py

**SEE ALSO**

-  To see the full help plus the default ``markup``, ``in_dir``,
   and ``out_dir``, from a command line do:

   .. code-block:: none

      compile.py -h

"""
import json
from argparse import ArgumentParser, RawTextHelpFormatter
import sys
import re

#
# 3/26/21 sn - seems to be bug in solc.exe v7.5 about generating .docdev
# for a parent class methods and events. The child class has everything
# but for the parent only the .docuser info shows up. You'll find that
# events and methods for the parent will not output the "Notes:" and
# "Parameters:". I see this missing from the .docdev file so it's happening
# in solc. A newer release may fix.
#


# REF and UML filename matches what doc/SPVCPrototypeDocument.md expects
ARTIFACT_DIR = 'C:/Users/snewe/Desktop/SPVCPrototype/artifact/'
DOC_DIR      = 'C:/Users/snewe/Desktop/SPVCPrototype/doc/'
LIST_FILENAME_PREFIX = ''
DOC_FILENAME_PREFIX = 'Contract_'
UML_FILENAME_PREFIX = 'UMLContract_'
LIST_FILETYPE = '.txt'
DOC_FILETYPE  = '.md'
UML_FILETYPE  = '.md'

def get_docuser(contract, artifact_dir=''):
    if artifact_dir == '' :
        fn = ARTIFACT_DIR + contract + '.docuser' 
    else:
        fn = artifact_dir + contract + '.docuser'
    with open(fn) as f:
        docuser = json.load(f)
    return docuser

def get_docdev(contract, artifact_dir=''):
    if artifact_dir == '' :
        fn = ARTIFACT_DIR + contract + '.docdev' 
    else:
        fn = artifact_dir + contract + '.docdev'
    with open(fn) as f:
        docdev = json.load(f)
    return docdev

def get_ccomments(docdev, docuser):
    # Return the Natspec contract comments
    # If there was no comment in the contract, set it to an empty string.
    # For some reason, @dev comments are found under 'details'
    ccomments = {
        'title'  : '',
        'author' : '',
        'notice' : '',
        'dev'    : ''
        }
    if 'title' in docdev.keys():
        ccomments['title'] = docdev['title']
    if 'author' in docdev.keys():
        ccomments['author'] = docdev['author']
    if 'notice' in docuser.keys():
        ccomments['notice'] = docuser['notice']
    if 'details' in docdev.keys():
        ccomments['dev'] = docdev['details']
    return ccomments

def get_mcomments(docdev, docuser):
    # Return the Natspec method comments

    # Combine names of all methods from both dev and user and sort alphetically
    if 'methods' in docdev.keys():
        methodsdev = set(docdev['methods'].keys())
    else:
        methodsdev = set()
    
    if 'methods' in docuser.keys():
        methodsuser = set(docuser['methods'].keys())
    else:
        methodsuser = set()
    
    method_names_list = list(methodsdev.union(methodsuser))
    method_names_list.sort()

    # Create list of the comments for all methods in the contract
    mcomments = []
    for mname in method_names_list:
        mcomment = {
            'method'  : mname,
            'notice'  : '',
            'dev'     : '',
            'params'  : '',
            'returns' : ''
            }
        if mname in docuser['methods'].keys():
            if 'notice' in docuser['methods'][mname].keys():
                mcomment['notice'] = docuser['methods'][mname]['notice']
        if mname in docdev['methods'].keys():
            if 'details' in docdev['methods'][mname].keys():
                mcomment['dev'] = docdev['methods'][mname]['details']
            if 'params' in docdev['methods'][mname].keys():
                mcomment['params'] = docdev['methods'][mname]['params']
            if 'returns' in docdev['methods'][mname].keys():
                mcomment['returns'] = docdev['methods'][mname]['returns']
        mcomments.append(mcomment)
    return mcomments

def get_ecomments(docdev, docuser):
    # Return the Natspec comments for all events

    # Create a list of the contract's event names sorted alphabetically
    if 'events' in docdev.keys():
        eventsdev = set(docdev['events'].keys())
    else:
        eventsdev = set()
    
    if 'events' in docuser.keys():
        eventsuser = set(docuser['events'].keys())
    else:
        eventsuser = set()
    
    event_names_list = list(eventsdev.union(eventsuser))
    event_names_list.sort()

    # get the comments all the events in the event names list 
    ecomments = []
    for ename in event_names_list:
        ecomment = {
            'event'  : ename,
            'notice' : '',
            'dev'    : '',
            'params' : ''
            }
        if ename in docuser['events'].keys():
            if 'notice' in docuser['events'][ename].keys():
                ecomment['notice'] = docuser['events'][ename]['notice']
        if ename in docdev['events'].keys():
            if 'details' in docdev['events'][ename].keys():
                ecomment['dev'] = docdev['events'][ename]['details']
            if 'params' in docdev['events'][ename].keys():
                ecomment['params'] = docdev['events'][ename]['params']
        ecomments.append(ecomment)
    return ecomments

def get_vcomments(docdev, docuser):
    # Create a list of the contract's public state variable names sorted.
    # These comments are only found in docdev.
    if 'stateVariables' in docdev.keys():
        varsdev = set(docdev['stateVariables'].keys())
    else:
        varsdev = set()
    
    var_names_list = list(varsdev)
    var_names_list.sort()
    
    vcomments = []
    for vname in var_names_list:
        vcomment = {
            'stateVariable' : vname,
            'dev' : ''
            }
        if vname in docdev['stateVariables'].keys():
            if 'details' in docdev['stateVariables'][vname].keys():
                vcomment['dev'] = docdev['stateVariables'][vname]['details']
        vcomments.append(vcomment)
    return vcomments

#
# Text list print routines
#
    
def print_separator_list():
    print('============================')

def print_ccomments_list(ccomments):
    print('TITLE:    {}'.format(ccomments['title']))
    print('AUTHOR:   {}'.format(ccomments['author']))
    print('NOTICE:   {}'.format(ccomments['notice']))
    print('DEV:      {}'.format(ccomments['dev']))

def print_mcomment_list(mcomment):
    print('METHOD:   {}'.format(mcomment['method']))
    print('NOTICE:   {}'.format(mcomment['notice']))
    print('DEV:      {}'.format(mcomment['dev']))
    if mcomment['params'] == '':
        print('PARAM:')
    else:
        for param, desc in mcomment['params'].items():
            print('PARAM:    {} - {}'.format(param, desc))
    if mcomment['returns'] =='':
        print('RETURN: ')
    else:
        for ret, desc in mcomment['returns'].items():
            print('RETURN:   {} - {}'.format(ret, desc))

def print_ecomment_list(ecomment):
    print('EVENT:    {}'.format(ecomment['event']))
    print('NOTICE:   {}'.format(ecomment['notice']))
    print('DEV:      {}'.format(ecomment['dev']))
    if ecomment['params'] == '':
        print('PARAM:')
    else:
        for param, desc in ecomment['params'].items():
            print('PARAM:    {} - {}'.format(param, desc))

def print_vcomment_list(vcomment):
    print('VARIABLE: {}'.format(vcomment['stateVariable']))
    print('DEV:      {}'.format(vcomment['dev']))

def print_list(ccomments, mcomments, ecomments, vcomments):
    print_ccomments_list(ccomments)
    print_separator_list()
    
    for vcomment in vcomments:
        print_vcomment_list(vcomment)
        print_separator_list()
    
    for mcomment in mcomments:
        print_mcomment_list(mcomment)
        print_separator_list()
    
    for ecomment in ecomments:
        print_ecomment_list(ecomment)
        print_separator_list()

#
# Markdown SPVC Contract ref doc print routines
#

def print_separator_ref():
    print('---')

def print_blankline_ref():
    print('\\')

def print_ccomment_ref(cname, ccomments):
    print('# {}'.format(cname))
    print('**Description:** {}'.format(ccomments['title']))
    print_blankline_ref()
    print('**Purpose:**  {}'.format(ccomments['notice']))
    print_blankline_ref()
    print('**Notes:**  {}'.format(ccomments['dev']))
    print_blankline_ref()
    print('**Author:**  {}'.format(ccomments['author']))

def print_vcomment_hdr_ref():
    print('## State Variables')
    print('')
    print('|Name|Description|')
    print('|----|-----------|')

def print_vcomment_ref(vcomment):
    print('|`{}`|{}|'.format(vcomment['stateVariable'], vcomment['dev']))
    
def print_mcomment_hdr_ref():
    print('## Methods')

def print_mcomment_ref(mcomment):
    print('### {}'.format(mcomment['method']))
    if mcomment['notice']:
        print('**Purpose:**      {}'.format(mcomment['notice']))
    if mcomment['dev']:
        print('**Notes:**  {}'.format(mcomment['dev']))
    else:
        print('')
    if mcomment['params']:
        print('')
        print('**Parameters:**')
        print('')
        print('|Name|Description|')
        print('|----|-----------|')
        for param, desc in mcomment['params'].items():
            print('|`{}`|{}|'.format(param, desc))
        print('')
    if mcomment['returns']:
        print('')
        print('**Returns:**')
        print('')
        print('|Name|Description|')
        print('|----|-----------|')
        for ret, desc in mcomment['returns'].items():
            print('|`{}`|{}|'.format(ret, desc))
        print('')
    
def print_ecomment_hdr_ref():
    print('## Events')

def print_ecomment_ref(ecomment):
    print('### {}'.format(ecomment['event']))
    if ecomment['notice']:
        print('**Purpose:**      {}'.format(ecomment['notice']))
    if ecomment['dev']:
        print('**Notes:**  {}'.format(ecomment['dev']))
    else:
        print('')
    if ecomment['params']:
        print('')
        print('**Parameters:**')
        print('')
        print('|Name|Description|')
        print('|----|-----------|')
        for param, desc in ecomment['params'].items():
            print('|`{}`|{}|'.format(param, desc))
        print('')

def print_ref(cname, ccomments, mcomments, ecomments, vcomments):
    print_ccomment_ref(cname, ccomments)
    print_separator_ref()

    if vcomments:
        print_vcomment_hdr_ref()
        for vcomment in vcomments:
            print_vcomment_ref(vcomment)
        print_separator_ref()

    if mcomments:
        print_mcomment_hdr_ref()
        mcomments = put_constructor_first_with_parens(mcomments)
        for mcomment in mcomments:
            print_mcomment_ref(mcomment)
            print_separator_ref()

    if ecomments:
        print_ecomment_hdr_ref()
        for ecomment in ecomments:
            print_ecomment_ref(ecomment)
            print_separator_ref()

#
# Markdown SPVC UML Contract Diagram doc print routines
#

def print_uml(cname, ccomments, mcomments, ecomments, vcomments):
    print('')
    print('|**{}**|'.format(cname))
    print('|----|')
    print('|**Variables**|')
    for vcomment in vcomments:
        print('| + {}|'.format(vcomment['stateVariable']))
    print('|**Events**|')
    for ecomment in ecomments:
        event_without_args = re.sub(r'\(.*\)', '()', ecomment['event'])
        print('|event {}|'.format(event_without_args))
    print('|**Methods**|')
    mcomments = put_constructor_first_with_parens(mcomments)
    for mcomment in mcomments:
        # skip the getter functions. Do not print them.
        # Strip off the ending '()' from the method and check it is not
        # a variable.
        # This code does not work yet.
        # TBD - do I want to do this?
        #
        #method = mcomment['method'].replace('()','')
        #if any(v['stateVariable'] == method for v in vcomments):
        #    print('{} is a getter'.format(method))
        method_without_args = re.sub(r'\(.*\)', '()', mcomment['method'])
        print('| + {}|'.format(method_without_args))
    print('')

def put_constructor_first_with_parens(mcomments):
    for mcomment in mcomments:
        if mcomment['method'] == 'constructor':
            mcomment['method'] = 'constructor()'
            mcomment_constructor = mcomment
            mcomments.remove(mcomment)
            mcomments = [mcomment_constructor] + mcomments
    return mcomments

    
def main():
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawTextHelpFormatter
        )
    parser.add_argument(
        '-s',
        action='store_true',
        help='write output to STDOUT. Default: {}'.format(DOC_DIR)
        )
    parser.add_argument(
        'format',
        choices=['list', 'doc', 'uml'],
        help='text listing, ' +
            'SPVCPrototypeDoc file, ' +
            'SPVCPrototypeDoc UML contract diagram'
        )
    parser.add_argument(
        'contract',
        metavar='<contract>',
        type=str,
        help = 'contract name (same as used for solc; without ".sol")'
        )
    args = parser.parse_args()

    if not args.s:
        if args.format == 'list':
            fn = DOC_DIR + LIST_FILENAME_PREFIX + args.contract + LIST_FILETYPE
        elif args.format == 'doc':
            fn = DOC_DIR + DOC_FILENAME_PREFIX + args.contract + DOC_FILETYPE
        elif args.format == 'uml':
            fn = DOC_DIR + UML_FILENAME_PREFIX + args.contract + UML_FILETYPE
        sys.stdout = open(fn, 'w')
    
    docuser = get_docuser(args.contract)
    docdev = get_docdev(args.contract)
    
    ccomments = get_ccomments(docdev, docuser)
    mcomments = get_mcomments(docdev, docuser)
    ecomments = get_ecomments(docdev, docuser)
    vcomments = get_vcomments(docdev, docuser)

    if args.format == 'list':
        print_list(ccomments, mcomments, ecomments, vcomments)
    elif args.format == 'doc':
        print_ref(args.contract, ccomments, mcomments, ecomments, vcomments)
    elif args.format == 'uml':
        print_uml(args.contract, ccomments, mcomments, ecomments, vcomments)

if __name__ == '__main__':
    main()
