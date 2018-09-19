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
from copy import deepcopy

try:
    from shutil import get_terminal_size
except ImportError:
    from backports.shutil_get_terminal_size import get_terminal_size

def format_fit(text, width=None, align='<', suffix="..."):
    """
    Fits a piece of text to ``width`` characters by truncating too long text and
    padding too short text with spaces. Defaults to terminal width. Truncation
    is indicated by a customizable suffix. ``align`` specifies the alignment of
    the contents if it is padded, and can be:

    * ``<`` - Left aligned (default)
    * ``^`` - Centered
    * ``>`` - Right aligned
    """

    if width==None:
        width = get_terminal_size().columns

    if len(text)>width:
        if len(suffix)>width:
            return suffix[len(suffix)-width:]
        else:
            return text[:width-len(suffix)]+suffix
    else:
        return "{{:{}{{w}}}}".format(align).format(text,w=width)

def format_time(seconds):
    """
    Formats a string from time given in seconds. For large times
    (``abs(seconds) >= 60``) the format is::

        dd:hh:mm:ss

    For small times (``abs(seconds) < 60``), the result is given in 3
    significant figures, with units given in seconds and a suitable SI-prefix.
    """

    if not isinstance(seconds, (int, float)):
        return str(seconds)

    if math.isnan(seconds):
        return "-"

    if abs(seconds)<60:
        return format_time_small(seconds)
    else:
        return format_time_large(seconds)

def format_time_small(seconds):
    """
    Same as format_time() but always uses SI-prefix and 3 significant figures.
    """

    if not isinstance(seconds, (int, float)):
        return str(seconds)

    if math.isnan(seconds):
        return "-"

    if abs(seconds)<1:
        milliseconds = 1000*seconds
        if abs(milliseconds)<1:
            microseconds = 1000*milliseconds
            if abs(microseconds)<1:
                nanoseconds = 1000*microseconds
                if abs(nanoseconds)<0.5:
                    return "0"
                else:
                    return "{:.0f}ns".format(nanoseconds)
            elif abs(microseconds)<10:
                return "{:.2f}us".format(microseconds)
            elif abs(microseconds)<100:
                return "{:.1f}us".format(microseconds)
            else:
                return "{:.0f}us".format(microseconds)
        elif abs(milliseconds)<10:
            return "{:.2f}ms".format(milliseconds)
        elif abs(milliseconds)<100:
            return "{:.1f}ms".format(milliseconds)
        else:
            return "{:.0f}ms".format(milliseconds)
    elif abs(seconds)<10:
            return "{:.2f}s".format(seconds)
    elif abs(seconds)<100:
        return "{:.1f}s".format(seconds)
    else:
        return "{:.0f}s".format(seconds)

def format_time_large(seconds):
    """
    Same as format_time() but always uses the format dd:hh:mm:ss.
    """

    if not isinstance(seconds, (int, float)):
        return str(seconds)

    if math.isnan(seconds):
        return "-"

    seconds = int(round(seconds))
    if abs(seconds)<60:
        return "{:d}".format(seconds)
    else:
        minutes = int(seconds/60)
        seconds %= 60
        if abs(minutes)<60:
            return "{:d}:{:02d}".format(minutes,seconds)
        else:
            hours = int(minutes/60)
            minutes %= 60
            if abs(hours)<24:
                return "{:d}:{:02d}:{:02d}".format(hours,minutes,seconds)
            else:
                days = int(hours/24)
                hours %= 24
                return "{:d}:{:02d}:{:02d}:{:02d}".format(
                    days,hours,minutes,seconds)

def format_table(table,
                 align='<',
                 format='{:.3g}',
                 colwidth=None,
                 maxwidth=None,
                 spacing=2,
                 truncate=0,
                 suffix="..."
                ):
    """
    Formats a table represented as an iterable of iterable into a nice big string
    suitable for printing.

    Parameters:
    -----------
    align : string or list of strings

            Alignment of cell contents. Each character in a string specifies
            the alignment of one column.

            * ``<`` - Left aligned (default)
            * ``^`` - Centered
            * ``>`` - Right aligned

            The last alignment is repeated for unspecified columns.

            If it's a list of strings, each string specifies the alignment of
            one row. The last string is used repeatedly for unspecified rows.

    format : string/function, or (nested) list of string/function

             Formats the contents of the cells using the specified function(s)
             or format string(s).

             If it's a list of strings/functions each entry specifies formatting
             for one column, the last entry being used repeatedly for
             unspecified columns.

             If it's a list of lists, each sub-list specifies one row, the last
             sub-list being used repeatedly for unspecified rows.

    colwidth : int, list of ints or None

               The width of each column. The last width is used repeatedly for
               unspecified columns. If ``None`` the width is fitted to the
               contents.

    maxwidth : int or None

               The maximum width of the table. Defaults to terminal width minus
               1 if ``None``. If the table would be wider than ``maxwidth`` one
               of the columns is truncated.

    spacing : int

              The spacing between columns

    truncate : int

               Which column to truncate if table width would exceed ``maxwidth``.

    Beware that no columns can have zero or negative width. If for instance
    'maxwidth' is 80 and 'colwidth' is [10, 30, 30, 30] with spacing 2 the total
    width will initially be 10+2+30+2+30+2+30=106. That's 26 characters too
    much, so a width of 26 will be removed from the truncated column. If
    'truncate' is 0, column 0 will have a width of -16 which is not permitted.
    """

    table = list(deepcopy(table))

    if not isinstance(align, list):
        align = [align]

    if not isinstance(format, list):
        format = [format]

    if not isinstance(format[0], list):
        format = [format]

    num_cols = len(table[0])
    if len(set([len(row) for row in table]))>1:
        raise ValueError("All rows must have the same number of columns")

    for i in range(len(table)):
        table[i] = list(table[i])
        colformat = format[min(i,len(format)-1)]
        for j, cell in enumerate(table[i]):
            f = colformat[min(j,len(colformat)-1)]
            if isinstance(f, str):
                fun = lambda x: f.format(x)
            else:
                fun = f
            try:
                table[i][j] = fun(cell)
            except:
                table[i][j] = str(cell)

    if colwidth==None:
        cellwidth = [[len(cell) for cell in row] for row in table]
        colwidth = list(map(max, zip(*cellwidth)))

    elif not isinstance(colwidth, list):
        colwidth = [colwidth]


    colwidth.extend([colwidth[-1]]*(num_cols-len(colwidth)))

    if maxwidth==None:
        maxwidth = get_terminal_size().columns-1

    width = sum(colwidth)+spacing*(num_cols-1)
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
        if i != 0: s += "\n"
        colalign = align[min(i,len(align)-1)]
        colformat = format[min(i,len(format)-1)]
        for j, col in enumerate(row):
            a = colalign[min(j,len(colalign)-1)]
            f = colformat[min(j,len(colformat)-1)]
            w = colwidth[j]
            if j!=0: s+= ' '*spacing
            s += format_fit(format_time(col), w, a, suffix)

    return s

def print_table(*args, **kwargs):
    print(format_table(*args, **kwargs))

def print_time(*args, **kwargs):
    print(format_time(*args, **kwargs))

def print_time_large(*args, **kwargs):
    print(format_time_large(*args, **kwargs))

def print_time_small(*args, **kwargs):
    print(format_time_small(*args, **kwargs))

def print_fit(*args, **kwargs):
    print(format_fit(*args, **kwargs))
