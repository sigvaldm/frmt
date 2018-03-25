"""
Copyright 2018 Sigvald Marholm <marholm@marebakken.com>

This file is part of frmt.

frmt is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

frmt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with frmt.  If not, see <http://www.gnu.org/licenses/>.
"""

import math
import numpy as np
import shutil

def fit_text(text, width=None, suffix="..."):
    """
    Fits a piece of text to 'width' characters by truncating too long text and
    padding too short text with spaces. Defaults to terminal width. Truncation
    is indicated by a customizable suffix (default: "...").
    """

    if width==None:
        width = shutil.get_terminal_size().columns

    if len(text)>width:
        if len(suffix)>width:
            return suffix[len(suffix)-width:]
        else:
            return text[:width-len(suffix)]+suffix
    else:
        return "{:{w}}".format(text,w=width)

def format_time(seconds):
    """
    Formats a string from time given in seconds. For large times (seconds >= 60)
    the format is:

        dd:hh:mm:ss

    where dd, hh, mm and ss refers to days, hours, minutes and seconds,
    respectively. If the time is less than one day, the first block (dd:) is
    omitted, and so forth. Examples:

        format_time(24*60*60)       returns     "1:00:00:00"
        format_time(60*60)          returns     "1:00:00"
        format_time(60)             returns     "1:00"

    For small times (seconds < 60), the result is given in 3 significant
    figures, with units given in seconds and a suitable SI-prefix. Examples:

        format_time(10)             returns     "10.0s"
        format_time(1)              returns     "1.00s"
        format_time(0.01255)        returns     "12.6ms"

    The finest resolution is 1ns. At last;

        format_time(float('nan'))   returns     "-"

    """

    if math.isnan(seconds):
        return "-"

    # Small times
    elif seconds<1:
        milliseconds = 1000*seconds
        if milliseconds<1:
            microseconds = 1000*milliseconds
            if microseconds<1:
                nanoseconds = 1000*microseconds
                return "{:.0f}ns".format(nanoseconds)
            elif microseconds<10:
                return "{:.2f}us".format(microseconds)
            elif microseconds<100:
                return "{:.1f}us".format(microseconds)
            else:
                return "{:.0f}us".format(microseconds)
        elif milliseconds<10:
            return "{:.2f}ms".format(milliseconds)
        elif milliseconds<100:
            return "{:.1f}ms".format(milliseconds)
        else:
            return "{:.0f}ms".format(milliseconds)
    elif seconds<10:
            return "{:.2f}s".format(seconds)
    elif seconds<60:
            return "{:.1f}s".format(seconds)

    # Large times
    else:
        seconds = int(seconds)
        minutes = int(seconds/60)
        seconds %= 60
        if minutes<60:
            return "{:d}:{:02d}".format(minutes,seconds)
        else:
            hours = int(minutes/60)
            minutes %= 60
            if hours<24:
                return "{:d}:{:02d}:{:02d}".format(hours,minutes,seconds)
            else:
                days = int(hours/24)
                hours %= 24
                return "{:d}:{:02d}:{:02d}:{:02d}".format(
                    days,hours,minutes,seconds)

def format_table(table,
                 align='<',
                 colwidth=None,
                 maxwidth=None,
                 spacing=2,
                 truncate=0,
                 suffix="..."
                ):
    """
    Formats a table represented as a 2D array of strings into a nice big string
    suitable for printing. Example:

        table = [[''      ,'Math','English','History', 'Comment'          ],
                 ['Bob'   ,'A'   ,'B'      ,'F'      , 'Failed at history'],
                 ['Jane'  ,'C'   ,'A'      ,'A'      , 'Quite good'       ],
                 ['Trevor','B'   ,'D'      ,'C'      , 'Somewhat average' ]]

        print(format_table(table))

    Returns:

                Math  English  History  Comment
        Bob     A     B        F        Failed at history
        Jane    C     A        A        Quite good
        Trevor  B     D        C        Somewhat average

    The 'align' parameter can be used to change cell alignment:

        '<' - Left aligned (default)
        '^' - Centered
        '>' - Right aligned

    It is also possible to have different alignments for different columns by
    having one character for each column, e.g. to have the first column left
    aligned and the subsequent four right aligned:

        '<>>>>'     or equivalently     '<>'

    If only some columns are specified, the last specified alignment is
    repeated. It is also possible to have different alignments for differnt rows
    by having a list of alignment strings for each row. Again, if only the first
    rows are specified, the last alignment string in the list will apply to all
    subsequent rows. For instance,

        print(format_table(table, ['^','<^^^<']))

    Returns:

                Math  English  History       Comment
        Bob      A       B        F     Failed at history
        Jane     C       A        A     Quite good
        Trevor   B       D        C     Somewhat average

    On the header row all cells are centered ('^'). On the subsequent rows the
    leftmost column is left aligned, the three next ones are centered, and the
    last is also left aligned ('<^^^<').

    The 'colwidth' parameter can be used to change column widths, which by
    default is just big enough to fit the contents. E.g. setting it to 10 means
    that all columns are 10 characters wide. Setting it to [20, 10] means that
    the first column is 20 characters wide and the subsequent ones are 10.
    Again, the last specified width is repeated for the remaining columns.

    The spacing between the columns is 'spacing' characters (default: 2).

    If the total table width exceeds 'maxwidth' the column indicated by
    'truncate' (default: 0) is truncated with a suffix 'suffix' (default: "...")
    on rows that are too long. If 'maxwidth' is not specified it will be taken
    as the terminal width minus 1. This truncation overrides settings in
    'colwidth'.

    Beware that no columns can have zero or negative width. If for instance
    'maxwidth' is 80 and 'colwidth' is [10, 30, 30, 30] with spacing 2 the total
    width will initially be 10+2+30+2+30+2+30=106. That's 26 characters too
    much, so a width of 26 will be removed from the truncated column. If
    'truncate' is 0, column 0 will have a width of -16 which is not permitted.
    """

    table = np.array(table)
    num_cols = table.shape[1]

    if colwidth==None:
        colwidth = list(np.max(np.array([[len(a) for a in b] for b in
                                         table]),0))
    elif not isinstance(colwidth, (list, np.array)):
        colwidth = [colwidth]

    if not isinstance(align, list):
        align = [align]

    colwidth.extend([colwidth[-1]]*(num_cols-len(colwidth)))

    if maxwidth==None:
        maxwidth = shutil.get_terminal_size().columns-1

    width = np.sum(colwidth)+spacing*(num_cols-1)
    if width>maxwidth:
        colwidth[truncate] -= (width-maxwidth)

    for j, cw in enumerate(colwidth):
        if cw<1:
            raise RuntimeError("Column {} in format_table() has width {}. "
                               "Make sure all columns have width >0. "
                               "Read docstring for further details."
                               .format(j,cw)
                              )

    s = ''
    for i, row in enumerate(table):
        colalign = align[min(i,len(align)-1)]
        for j, col in enumerate(row):
            a = colalign[min(j,len(colalign)-1)]
            w = colwidth[j]
            if j!=0: s+= ' '*spacing
            s += fit_text('{{:{}{{w}}}}'.format(a).format(col,w=w),w,suffix)
        s += "\n"

    return s
