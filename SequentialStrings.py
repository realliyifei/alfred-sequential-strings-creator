# encoding: utf-8 
#
# Copyright (c) 2020 https://github.com/yli/
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2020-09-01
#
# Alfred-Workflow: https://www.deanishe.net/alfred-workflow/index.html

import sys
from workflow import Workflow3

__version__ = '1.1.0'

# GitHub repo to check for updates
UPDATE_SETTINGS = {
    'github_slug': 'yli/Alfred-Sequential-Strings-Creator',
    'version': __version__
}

# GitHub Issues
HELP_URL = 'https://github.com/yli/Alfred-Sequential-Strings-Creator/issues'

def main(wf):
    """Run the workflow"""
    # Update settings format
    if wf.update_available:
        wf.start_update()
    
    # Main    
    try:
        query = wf.args[0]
        
        subtitle_vertical = "Press 'Enter' and copy to clipboard vertically"
        result_str_v = sequential_strings_creator(query, '\n')
        wf.add_item(title = result_str_v, subtitle = subtitle_vertical, arg = result_str_v, valid = True)   
                
        subtitle = "Press 'Enter' and copy to clipboard horizontally"
        result_str_h = sequential_strings_creator(query, ' ')
        wf.add_item(title = result_str_h, subtitle = subtitle, arg = result_str_h, valid = True)
        
    except:
        wf.add_item("Invalid input. Format: strings {number-number} strings")
    
    wf.send_feedback() 
    
def sequential_strings_creator(query, join_string):
    """
    Generates a series of sequential strings, supporting either integer or one-digit float
    
    :param str query: The whole string input from alfred workflow input
    :param str join_string: String that seperates the sequentail string
    :reutrn: A series of sequential strings
    :rtype: string
    """
    str_before_num = query[:query.index('{')]
    str_after_num = query[query.index('}')+1:]
    num_range = query[query.index('{')+1 : query.index('}')]
    open_num = num_range[:num_range.index('-')]
    close_num = num_range[num_range.index('-')+1:]
    
    if isint(open_num) & isint(close_num):
        num_list = range(int(open_num), int(close_num)+1, 1)
    elif isfloat(open_num) & isfloat(close_num):
        # don't use numpy.arange here: favors other users who don't have numpy package
        num_list = [0.1 * x for x in range(int(float(open_num)*10), int(float(close_num)*10)+1, 1)]
        num_list = [round(i,1) for i in num_list] # prevent numerical precision problem 
    else:
        raise Exception
    
    result_list = [str_before_num + str(i) + str_after_num for i in num_list]
    result =  join_string.join(result_list)
    
    return result

def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b

if __name__ == '__main__':
    # create a workflow3 boject
    wf = Workflow3(
        update_settings = UPDATE_SETTINGS,
        help_url = HELP_URL,
    ) 
    sys.exit(wf.run(main)) 