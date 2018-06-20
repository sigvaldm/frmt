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

def fit_text(text, width=None, align='<', suffix="..."):
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
        width = shutil.get_terminal_size().columns

    if len(text)>width:
        if len(suffix)>width:
            return suffix[len(suffix)-width:]
        else:
            return text[:width-len(suffix)]+suffix
    else:
        return "{{:{}{{w}}}}".format(align).format(text,w=width)

def format_time(seconds, mode='auto'):
    """
    Formats a string from time given in seconds. For large times
    (``abs(seconds) >= 60``) the format is::

        dd:hh:mm:ss

    For small times (``abs(seconds) < 60``), the result is given in 3
    significant figures, with units given in seconds and a suitable SI-prefix.
    The format can be locked to either 'small' or 'large' using the 'mode'
    argument.

    The finest resolution is 1ns and ``nan`` returns ``-``.
    """

    assert mode in ['auto','small','large'],\
            "mode must be 'auto', 'small' or 'large'"

    if math.isnan(seconds):
        return "-"

    if mode=='auto':
        if abs(seconds)<60:
            mode='small'
        else:
            mode='large'

    if mode=='small':
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
        elif abs(seconds)<60:
            return "{:.1f}s".format(seconds)
        else:
            return "{:.0f}s".format(seconds)

    else:
        seconds = round(seconds)
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
                 colwidth=None,
                 maxwidth=None,
                 spacing=2,
                 truncate=0,
                 suffix="..."
                ):
    """
    Formats a table represented as a 2D array of strings into a nice big string
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

    colwidth : list of int or None

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
            s += fit_text(str(col), w, a, suffix)
        s += "\n"

    return s
