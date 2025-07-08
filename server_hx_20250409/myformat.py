#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os
import textwrap
from pprint import pformat
from itertools import zip_longest, chain
import sys
import time


def create_table(header, rows, footer=False, name=None, str_is_str=False, max_col_width=35):
    def _pformat(obj, width, str_is_str=str_is_str):
        if str_is_str and isinstance(obj, str):
            return obj
        return pformat(obj, width=width)

    # First format each entry
    header = [_pformat(head, width=max_col_width, str_is_str=str_is_str) for head in header]
    rows = [[_pformat(cell, width=max_col_width, str_is_str=str_is_str) for cell in row] for row in rows]

    # Split on newlines, after this point, an entry is a list of rows, not a string
    header = [head.splitlines() for head in header]
    rows = [[cell.splitlines() for cell in row] for row in rows]

    # Finally wrap any lines that are too long, note there are no '\n' in any one line now
#    print([list(chain(*[textwrap.wrap(line, replace_whitespace=False, drop_whitespace=False) for line in head])) for head in header])
    header = [list(chain(*[textwrap.wrap(line, width=max_col_width, replace_whitespace=False, drop_whitespace=False) for line in head])) for head in header]

    rows = [[list(chain(*[textwrap.wrap(line, width=max_col_width, replace_whitespace=False, drop_whitespace=False) for line in cell])) for cell in row] for row in rows]

    assert all(len(row) == len(rows[0]) for row in rows), ('Argument rows must be iterable with '
                                                           'equal length elements')
    assert not rows or len(header) == len(rows[0]), 'Header (wrong len={}) must be same len as row (len={})'.format(
        len(header), len(rows[0]))

    # Calc max width
    col_width = [0]*len(header)

    for row in rows:
        for i in range(len(col_width)):
            if not row[i]:
                continue
            col_width[i] = min(max(col_width[i], len(max(row[i], key=len))), max_col_width)

    for i in range(len(col_width)):
        if  not header[i]:
            continue
        col_width[i] = min(max(col_width[i], len(max(header[i], key=len))), max_col_width)

    row_format = '#' + '|'.join([' {{:<{0}.{0}s}} '.format(w) for w in col_width]) + '#'
    header_format = row_format.replace('<', '^')

    header_rows = [header_format.format(*heads) for heads in zip_longest(*header, fillvalue='')]
    table_width = len(header_rows[0])

    table = ['#'*table_width]
    if name is not None:
        name_format = '#{{:^{0}.{0}}}#'.format(table_width-2)
        table.extend([name_format.format(name_line) for name_line in textwrap.wrap(name, table_width-4)])
        table.append('#'*table_width)
    table.extend(header_rows)
    table.append('#' + '='*(table_width - 2) + '#')
    table.extend(row_format.format(*cells) for row in rows for cells in zip_longest(*row, fillvalue='') )
    if footer:
        table.append('#' + '='*(table_width-2) + '#')
        table.extend(header_rows)
    table.append('#'*table_width)

    return '\n'.join(table)

section_max_len = 99
section_inner_len = section_max_len - 4
section_msg_format = '| {{:^{0}.{0}s}} |'.format(section_inner_len)
subsection_msg_format = '{{:-^{0}.{0}s}}'.format(section_max_len)

def create_section(msg):
    # Looks like
    # --------------------------------------------------------------------------------
    # |                               Config check HDD                               |
    # --------------------------------------------------------------------------------
    #
    return '\n'.join(['-'*section_max_len] +
                     [section_msg_format.format(l) for line in msg.splitlines() for l in textwrap.wrap(line, section_inner_len)] +
                     ['-'*section_max_len])

def create_subsection(msg):
    # Looks like
    # ----------------------------- Config check HDD ---------------------------------
    #
    return '\n'.join([subsection_msg_format.format(l) for line in msg.splitlines() for l in textwrap.wrap(line, section_inner_len)])


def display(msg):
    for line in msg.splitlines():
        logging.info(line)

if __name__ == '__main__':
    logging.info("myformat is running by itself")
