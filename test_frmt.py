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

from frmt import *
import pytest

try:
    from shutil import get_terminal_size
except ImportError:
    from backports.shutil_get_terminal_size import get_terminal_size

def test_format_fit():
    assert format_fit('abc', 5)      == 'abc  '
    assert format_fit('abc', 5, '<') == 'abc  '
    assert format_fit('abc', 5, '^') == ' abc '
    assert format_fit('abc', 5, '>') == '  abc'
    assert format_fit('abc', 2)      == '..'
    assert format_fit('abcdef', 5)   == 'ab...'
    assert format_fit('abcdef', 5, suffix='!', align='>') == 'abcd!'

def test_format_fit_terminal_width():
    width = get_terminal_size().columns
    assert format_fit('a'*width)     == 'a'*width
    # Terminal is zero-width on Python 2 on CI
    assert format_fit('a'*(width+1)) == 'a'*(width-3)+'.'*min(3,width)

def test_format_time_special():
    assert format_time('text')             == 'text'
    assert format_time_large('text')       == 'text'
    assert format_time_small('text')       == 'text'
    assert format_time(float('nan'))       == '-'
    assert format_time_large(float('nan')) == '-'
    assert format_time_small(float('nan')) == '-'
    assert format_time(0)                  == '0'
    assert format_time_large(0)            == '0'
    assert format_time_small(0)            == '0'

def test_format_time_lower_limits():
    assert format_time(4e-10)  == '0'
    assert format_time(5e-10)  == '1ns'
    assert format_time(-4e-10) == '0'
    assert format_time(-5e-10) == '-1ns'

def test_format_time_scaling():
    assert format_time(1e-9)     == '1ns'
    assert format_time(1e-8)     == '10ns'
    assert format_time(1e-7)     == '100ns'
    assert format_time(1e-6)     == '1.00us'
    assert format_time(1e-5)     == '10.0us'
    assert format_time(1e-4)     == '100us'
    assert format_time(1e-3)     == '1.00ms'
    assert format_time(1e-2)     == '10.0ms'
    assert format_time(1e-1)     == '100ms'
    assert format_time(1e0)      == '1.00s'
    assert format_time(1e1)      == '10.0s'
    assert format_time(59)       == '59.0s'
    assert format_time(60)       == '1:00'
    assert format_time(60**2)    == '1:00:00'
    assert format_time(24*60**2) == '1:00:00:00'

def test_format_time_rounding():
    assert format_time(1.0049999)  == '1.00s'
    assert format_time(1.0050001)  == '1.01s'
    assert format_time(-1.0049999) == '-1.00s'
    assert format_time(-1.0050001) == '-1.01s'

def test_format_time_mode():
    assert format_time_small(60)  == '60.0s'
    assert format_time_small(99)  == '99.0s'
    assert format_time_small(100) == '100s'
    assert format_time_large(0.1) == '0'
    assert format_time_large(10)  == '10'

# def test_format_num():
#     assert format_num('text')     == 'text'
#     assert format_num(1.23456e-11) == '1.23e-11'
#     assert format_num(1.23456e-3) == '1.23e-3'
#     assert format_num(1.23456e-2) == '1.23e-2'
#     assert format_num(1.23456e-1) == '0.123'
#     assert format_num(1.23456e0)  == '1.23'
#     assert format_num(1.23456e1)  == '12.3'
#     assert format_num(1.23456e2)  == '123'
#     assert format_num(1.23456e3)  == '12.3e3'
#     assert format_num(1.23456e11)  == '12.3e11'

def test_format_table_example1():

    table = [[''      , 'Math', 'English', 'History', 'Comment'          ],
             ['Bob'   , 'A'   , 'B'      , 'F'      , 'Failed at history'],
             ['Jane'  , 'C'   , 'A'      , 'A'      , 'Quite good'       ],
             ['Trevor', 'B'   , 'D'      , 'C'      , 'Somewhat average' ]]

    assert format_table(table, maxwidth=80) == \
        "        Math  English  History  Comment          \n"\
        "Bob     A     B        F        Failed at history\n"\
        "Jane    C     A        A        Quite good       \n"\
        "Trevor  B     D        C        Somewhat average "

    assert format_table(table, ['^','<^^^<'], maxwidth=80) == \
        "        Math  English  History       Comment     \n"\
        "Bob      A       B        F     Failed at history\n"\
        "Jane     C       A        A     Quite good       \n"\
        "Trevor   B       D        C     Somewhat average "

    assert format_table(table, ['^','<^^^<'], maxwidth=47, truncate=4) == \
        "        Math  English  History      Comment    \n"\
        "Bob      A       B        F     Failed at hi...\n"\
        "Jane     C       A        A     Quite good     \n"\
        "Trevor   B       D        C     Somewhat ave..."

    assert format_table(table, maxwidth=80, colwidth=10) == \
        "            Math        English     History     Comment   \n"\
        "Bob         A           B           F           Failed ...\n"\
        "Jane        C           A           A           Quite good\n"\
        "Trevor      B           D           C           Somewha..."

    with pytest.raises(RuntimeError) as e_info:
        # Column 0 is 6 characters. Native width is 49. 42 is 7 too narrow.
        format_table(table, maxwidth=42)

def test_format_table_example2a():

    header =  ['Name'  , 'Time']
    table  = [['John'  , 3672  ],
              ['Martha', 2879  ],
              ['Stuart', 2934  ],
              ['Eduard', 2592  ]]

    table.sort(key=lambda row: row[1])
    for row in table:
        row[1] = format_time(row[1])
    table.insert(0, header)

    assert format_table(table, '<>', maxwidth=80) == \
        "Name       Time\n"\
        "Eduard    43:12\n"\
        "Martha    47:59\n"\
        "Stuart    48:54\n"\
        "John    1:01:12"

def test_format_table_example2b():

    header =  ['Name'  , 'Time']
    table  = [['John'  , 3672  ],
              ['Martha', 2879  ],
              ['Stuart', 2934  ],
              ['Eduard', 2592  ]]

    table.sort(key=lambda row: row[1])
    table.insert(0, header)

    assert format_table(table, '<>', format=format_time, maxwidth=80) == \
        "Name       Time\n"\
        "Eduard    43:12\n"\
        "Martha    47:59\n"\
        "Stuart    48:54\n"\
        "John    1:01:12"

def test_format_table_example3():
    table = \
        [['a', 'b', 'c', 'd', '%'],
         [17.2198804555926,
          15.143854752058406,
          29.24066103281906,
          29.99010896298264,
          0.02078852708040979],
         [9.381666911448356,
          29.36822846449368,
          9.053677658435248,
          0.9823747478441014,
          0.33476190849779475],
         [7.628112421818297,
          17.995011240828724,
          29.82956064972065,
          24.851495494902068,
          0.8006807736678987]]

def test_format_table_numcols():

    table = [[1, 2, 3],[1, 2]]
    with pytest.raises(ValueError) as e_info:
        format_table(table, maxwidth=80)

def test_format_table_inputonlyargument():

    # Make sure format_table isn't changing its input arguments.
    # TBD: This test could perhaps be generalized to something.
    table = [[1,2],[3,4]]
    format_table(table, format=format_time, maxwidth=80)
    assert table[1][1]==4

def test_format_table_auto_width():
    width = get_terminal_size().columns-1
    table = [['a'*(width+1)]]
    if width>0:
        assert format_table(table, suffix='') == 'a'*width

def test_print_fit(capsys):
    print(format_fit('abc', 5, '>'))
    a = capsys.readouterr().out
    print_fit('abc', 5, '>')
    b = capsys.readouterr().out
    assert a==b

