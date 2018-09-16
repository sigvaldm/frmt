frmt
====

.. image:: https://travis-ci.com/sigvaldm/frmt.svg?branch=master
    :target: https://travis-ci.com/sigvaldm/frmt

.. image:: https://coveralls.io/repos/github/sigvaldm/frmt/badge.svg?branch=master
    :target: https://coveralls.io/github/sigvaldm/frmt?branch=master

.. image:: https://img.shields.io/pypi/pyversions/frmt.svg
    :target: https://pypi.org/project/Frmt

frmt is a pretty-printing library for tables and times. The core philosophy is that it should work with minimal hassle, yet offer flexibility through elegant, lightweight design. 

The library consist of the following functions:

* ``format_table()``/``print_table()``
* ``format_time()``/``print_time()``
* ``format_fit()``/``print_fit()``

The ``format_*()`` functions formats a certain type of data to a nice string and returns it. The ``print_*()``-functions are simple wrappers that act identically except that they print the string directly to the output. Each are described in what follows.

Installation
------------
Install from PyPI using ``pip`` (preferred method)::

    pip install frmt

Or download the GitHub repository https://github.com/sigvaldm/frmt.git and run::

    python setup.py install


``format_table()``/``print_table()``
------------------------------------
The ``*_table()`` functions formats a table represented as a list of lists. Consider this example using a table of grades from 1.0 (best) to 6.0 (worst)::

    >>> from frmt import print_table
    >>> grades = [[''      , 'Math', 'English', 'History', 'Comment'          ],
    ...           ['Bob'   , 1.2   , 2.1      , 5.9      , 'Failed at history'],
    ...           ['Jane'  , 2.4   , 1.1      , 1.4      , 'Quite good'       ],
    ...           ['Trevor', 2.2   , 4.4      , 3.2      , 'Somewhat average' ]]

    >>> print_table(grades)
            Math  English  History  Comment          
    Bob     1.2   2.1      5.9      Failed at history
    Jane    2.4   1.1      1.4      Quite good       
    Trevor  2.2   4.4      3.2      Somewhat average 

The functions also work with other kinds of iterables of iterables, for instance NumPy arrays. It also supports custom alignment and formatting for each individual cell.
    
The signature of ``*_table()`` looks as follows::

    *_table(table,
            align='<',
            format='{:.3g}',
            colwidth=None,
            maxwidth=None,
            spacing=2,
            truncate=0,
            suffix="..."
           ):
    
Alignment
~~~~~~~~~

The ``align`` parameter can be used to change cell alignment:

* ``'<'`` - Left aligned (default)
* ``'^'`` - Centered
* ``'>'`` - Right aligned

It is also possible to have different alignments for different columns by having one character for each column. For instance, to have the first column left aligned and the subsequent four right aligned, set ``align`` to ``'<>>>>'`` or, equivalently, to ``'<>'``::

    >>> print_table(grades, '<>')
            Math  English  History            Comment
    Bob      1.2      2.1      5.9  Failed at history
    Jane     2.4      1.1      1.4         Quite good
    Trevor   2.2      4.4      3.2   Somewhat average

Note that if only some columns are specified, the last specified alignment is repeated. This is useful typically when the left column is text and the remaining columns are numbers (although here it would be better to left align the rightmost column). This pattern of "repeating the last" is a core philosophy used throughout frmt to achieve flexibility.

It is also possible to have different alignments for different *rows* by having a list of alignment strings for each row. Again, if not all rows are specified, the last alignment string in the list is repeated for subsequent rows. For instance::

    >>> print_table(grades, ['^','<^^^<'])
            Math  English  History       Comment     
    Bob     1.2     2.1      5.9    Failed at history
    Jane    2.4     1.1      1.4    Quite good       
    Trevor  2.2     4.4      3.2    Somewhat average 

On the header row all cells are centered (``'^'``). On the subsequent rows the leftmost column is left aligned, the three next ones are centered, and the last is also left aligned (``'<^^^<'``).

Cell formatting
~~~~~~~~~~~~~~~

The ``format`` parameter can be used to format the cell contents. By default the `format string`_ ``'{:.3g}'`` is used to format numbers. This is a reasonable default, but often one would like to tune the formatting. For instance if we do not wish to display decimals in the above grading example, it can be easily achieved::

    >>> print_table(grades, format='{:.0f}')
            Math  English  History  Comment          
    Bob     1     2        6        Failed at history
    Jane    2     1        1        Quite good       
    Trevor  2     4        3        Somewhat average 

``format`` also accepts a function as an input to allow for greater flexibility. As an example, consider formatting the grades as letters::

    >>> def letter_grade(x):
    ...     return 'ABCDEF'[round(x)-1]

    >>> print_table(grades, format=letter_grade)
            Math  English  History  Comment          
    Bob     A     B        F        Failed at history
    Jane    B     A        A        Quite good       
    Trevor  B     D        C        Somewhat average 

The function ``letter_grade()`` throws a ``TypeError`` when applied to for instance "Bob", so ``print_table()`` will not use it for "Bob". Likewise for format strings; when using them on some cell content would result in an exception, ``print_table()`` resorts to using ``str()`` on it.

Following a pattern similar to ``align``, different format strings/functions can be applied to different columns by putting them in a list. The last specified format string/function will be repeated for all subsequent columns. One can also specify different format strings/functions for different *rows*. In that case the lists are nested; a list with one list for each row. For example, to uppercase the header row::

    >>> def str_upper(s):
    ...     return s.upper()

    >>> print_table(grades, format=[[str_upper],[letter_grade]])
            MATH  ENGLISH  HISTORY  COMMENT          
    Bob     A     B        F        Failed at history
    Jane    B     A        A        Quite good       
    Trevor  B     D        C        Somewhat average 

Using the ``format`` option is not the only, and not always the best way to format the cell contents. Sometimes it may be just as good to format the cell contents before passing it to ``*_table()``, like in this example::

    >>> measurements = \
    ... [[0.0, 0.16159999923218293, 0.05832942704771176],
    ...  [0.001, 0.5415871693699631, 0.1038533048639953],
    ...  [0.002, 1.0020586304683154, 0.06263011126285473],
    ...  [0.003, 1.6493888138044273, 0.1633588946456795],
    ...  [0.004, 2.158470579371153, 0.16602352409683588],
    ...  [0.005, 2.543489191597334, 0.18539040280004443],
    ...  [0.006, 3.1235687589204497, 0.24946423631204423],
    ...  [0.007, 3.6155358393212573, 0.19856685230794482],
    ...  [0.008, 4.111913772930216, 0.19223623526732384],
    ...  [0.009000000000000001, 4.505017235628538, 0.20666111673691043],
    ...  [0.01, 5.0961076665212595, 0.1259131288654157]]

    >>> for row in measurements:
    ...     row[0] = '{:.1f}ms'.format(row[0]*1e3)
    ...     row[1] = '{:.1f}V'.format(row[1])
    ...     row[2] = '{:.0f}mA'.format(row[2]*1e3)

    >>> header = ['Time', 'Voltage', 'Current']
    >>> measurements.insert(0, header)

    >>> print_table(measurements, '>')
      Time  Voltage  Current
     0.0ms     0.2V     58mA
     1.0ms     0.5V    104mA
     2.0ms     1.0V     63mA
     3.0ms     1.6V    163mA
     4.0ms     2.2V    166mA
     5.0ms     2.5V    185mA
     6.0ms     3.1V    249mA
     7.0ms     3.6V    199mA
     8.0ms     4.1V    192mA
     9.0ms     4.5V    207mA
    10.0ms     5.1V    126mA

_`format string` https://docs.python.org/3.7/library/string.html#format-string-syntax

Width and spacing
~~~~~~~~~~~~~~~~~

The ``colwidth`` parameter can be used to change column widths, which by default is just big enough to fit the contents. Setting it to ``10``, for instance, means that all columns are 10 characters wide. Setting it to ``[20, 10]`` means that the first column is 20 characters wide and the subsequent ones are 10. Unless all columns are specified, the last specified width is repeated for the remaining columns.

Content that is too long for its cell is truncated using the string ``suffix`` (default: ``'...'``). Example::

    >>> print_table(grades, colwidth=10)
                Math        English     History     Comment   
    Bob         1.2         2.1         5.9         Failed ...
    Jane        2.4         1.1         1.4         Quite good
    Trevor      2.2         4.4         3.2         Somewha...

The spacing between the columns is ``spacing`` characters (default: ``2``).

If the total table width exceeds ``maxwidth`` the column indicated by ``truncate`` (default: ``0``) is truncated on rows that are too long. If ``maxwidth`` is not specified it will be taken as the terminal width minus 1. This truncation overrides settings in ``colwidth``.

Beware that no columns can have zero or negative width. If for instance ``maxwidth`` is 80 and ``colwidth`` is ``[10, 30, 30, 30]`` with spacing 2 the total width will initially be 10+2+30+2+30+2+30=106. That's 26 characters too much, so a width of 26 will be removed from the truncated column. If ``truncate`` is 0, column 0 will have a width of -16 which is not permitted.

Example: Sorting a Table
~~~~~~~~~~~~~~~~~~~~~~~~
Consider printing sorted table of the race times of a 10km run. The race times in seconds is already in a table, and we supply a separate header row::

    >>> from frmt import format_time

    >>> header =  ['Name'  , 'Time']
    >>> race   = [['John'  , 3672  ],
    ...           ['Martha', 2879  ],
    ...           ['Stuart', 2934  ],
    ...           ['Eduard', 2592  ]]

    >>> race.sort(key=lambda row: row[1])
    >>> race.insert(0, header)

    >>> print_table(race, '<>', format_time)
    Name       Time
    Eduard    43:12
    Martha    47:59
    Stuart    48:54
    John    1:01:12

Example: Transposing a Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A table can be transposed using ``zip`` along with the ``*`` operator::

    >>> print_table(zip(*grades))
             Bob                Jane        Trevor          
    Math     1.2                2.4         2.2             
    English  2.1                1.1         4.4             
    History  5.9                1.4         3.2             
    Comment  Failed at history  Quite good  Somewhat average

``zip(*grades)``, which is the equivalent of ``zip(grades[0], grades[1], grades[2], grades[3])``, isn't actually a list of lists. It is nonetheless an iterable of an iterable, and therefore perfectly understandable by ``*_table()``.
If you still want a list of list, e.g. for preprocessing the table, you could do ``list(map(list,zip(*grades)))``. 

A common pattern is having a set of lists (or 1D NumPy arrays) and wanting to print them as columns. Here's an example of that::

    >>> time = [0.0, 0.001, 0.002, 0.003, 0.004, 0.005,
    ...         0.006, 0.007, 0.008, 0.009, 0.01]

    >>> voltage = [0.16159999923218293, 0.5415871693699631, 1.0020586304683154,
    ...            1.6493888138044273, 2.158470579371153, 2.543489191597334,
    ...            3.1235687589204497, 3.6155358393212573, 4.111913772930216,
    ...            4.505017235628538, 5.0961076665212595]

    >>> current = [0.05832942704771176, 0.1038533048639953, 0.06263011126285473,
    ...            0.1633588946456795, 0.16602352409683588, 0.18539040280004443,
    ...            0.24946423631204423, 0.19856685230794482,
    ...            0.19223623526732384, 0.20666111673691043, 0.1259131288654157]

    >>> header = ['Time', 'Voltage', 'Current']
    >>> measurements = list(zip(time, voltage, current))
    >>> measurements.insert(0, header)

    >>> print_table(measurements, '>', '{:.3f}')
     Time  Voltage  Current
    0.000    0.162    0.058
    0.001    0.542    0.104
    0.002    1.002    0.063
    0.003    1.649    0.163
    0.004    2.158    0.166
    0.005    2.543    0.185
    0.006    3.124    0.249
    0.007    3.616    0.199
    0.008    4.112    0.192
    0.009    4.505    0.207
    0.010    5.096    0.126

``format_time()``
-----------------
Signature: ``format_time(seconds, mode='auto')``

``format_time()`` represents time given in seconds as a convenient string. For large times (``abs(seconds) >= 60``) the output format is::

    dd:hh:mm:ss

where ``dd``, ``hh``, ``mm`` and ``ss`` refers to days, hours, minutes and seconds, respectively. Blocks that are zero are omitted. For instance, if the time is less than one day, the part ``dd:`` is omitted, and so forth. Examples::

    format_time(24*60*60)       returns     "1:00:00:00"
    format_time(60*60)          returns     "1:00:00"
    format_time(60)             returns     "1:00"

For small times (``abs(seconds) < 60``), the result is given in 3 significant figures, with units given in seconds and a suitable SI-prefix. Examples::

    format_time(10)             returns     "10.0s"
    format_time(1)              returns     "1.00s"
    format_time(0.01255)        returns     "12.6ms"   (with correct round-off)

The finest resolution is 1ns. Finally::

    format_time(float('nan'))    returns     "-"

``mode`` can be set equal to either ``'small'`` or ``'large'`` to lock the format to that of small or large times, respectively.

``fit_text()``
--------------
Signature: ``fit_text(text, width=None, align='<', suffix="...")``

``fit_text()`` fits a piece of text to ``width`` characters by truncating too long text and padding too short text with spaces. Truncation is indicated by a customizable suffix ``suffix`` (default: ``'...'``). Examples::

    fit_text('abcdefgh', 6)     returns     'abc...'    (truncation)
    fit_text('abcd', 6)         returns     'abcd  '    (padding)

If ``width`` is not specified it is taken to be the terminal width. Hence to print a string ``s`` to terminal that truncates rather than spilling across multiple lines if it's too long::

    print(fit_text(s))

Content alignment in case of padding can be specified using ``align`` which can take the following values:

* ``<`` - Left aligned (default)
* ``^`` - Centered
* ``>`` - Right aligned
