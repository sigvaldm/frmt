frmt
====

Lightweight formatting of tables and times in Python.

The library only has these functions, which are more thoroughly explained in the sequel:

* ``format_table()``
* ``format_time()``
* ``fit_text()``

Installation
------------
Install from PyPI using ``pip`` (preferred method)::

    pip install frmt

Or download the GitHub repository https://github.com/sigvaldm/frmt.git and run::

    python setup.py install


``format_table()``
------------------
``format_table()`` formats a table represented as a 2D array of strings into a nice big string suitable for printing. Example::

    table = [[''      , 'Math', 'English', 'History', 'Comment'          ],
             ['Bob'   , 'A'   , 'B'      , 'F'      , 'Failed at history'],
             ['Jane'  , 'C'   , 'A'      , 'A'      , 'Quite good'       ],
             ['Trevor', 'B'   , 'D'      , 'C'      , 'Somewhat average' ]]

    print(format_table(table))

Returns::

            Math  English  History  Comment
    Bob     A     B        F        Failed at history
    Jane    C     A        A        Quite good
    Trevor  B     D        C        Somewhat average
    
The signature of ``format_table()`` looks as follows::

    format_table(table,
                 align='<',
                 colwidth=None,
                 maxwidth=None,
                 spacing=2,
                 truncate=0,
                 suffix="..."
                )
    
Alignment
~~~~~~~~~

The ``align`` parameter can be used to change cell alignment:

* ``'<'`` - Left aligned (default)
* ``'^'`` - Centered
* ``'>'`` - Right aligned

It is also possible to have different alignments for different columns by having one character for each column. For instance, to have the first column left aligned and the subsequent four right aligned, set ``align`` to:

``'<>>>>'`` or ``'<>'``

Note that if only some columns are specified, the last specified alignment is repeated.

It is also possible to have different alignments for differnt rows by having a list of alignment strings for each row. Again, if not all rows are specified, the last alignment string in the list will apply to all subsequent rows. For instance::

    print(format_table(table, ['^','<^^^<']))

Returns::

            Math  English  History       Comment
    Bob      A       B        F     Failed at history
    Jane     C       A        A     Quite good
    Trevor   B       D        C     Somewhat average

On the header row all cells are centered (``'^'``). On the subsequent rows the leftmost column is left aligned, the three next ones are centered, and the last is also left aligned (``'<^^^<'``).

Width and spacing
~~~~~~~~~~~~~~~~~

The ``colwidth`` parameter can be used to change column widths, which by default is just big enough to fit the contents. Setting it to ``10``, for instance, means that all columns are 10 characters wide. Setting it to ``[20, 10]`` means that the first column is 20 characters wide and the subsequent ones are 10. Unless all columns are specified, the last specified width is repeated for the remaining columns.

Content that is too long for its cell is truncated using the string ``suffix`` (default: ``'...'``). Example::

    print(format_table(table,colwidth=[10]))
    
Returns::

                Math        English     History     Comment   
    Bob         A           B           F           Failed ...
    Jane        C           A           A           Quite good
    Trevor      B           D           C           Somewha...

The spacing between the columns is ``spacing`` characters (default: ``2``).

If the total table width exceeds ``maxwidth`` the column indicated by ``truncate`` (default: ``0``) is truncated on rows that are too long. If ``maxwidth`` is not specified it will be taken as the terminal width minus 1. This truncation overrides settings in ``colwidth``.

Beware that no columns can have zero or negative width. If for instance ``maxwidth`` is 80 and ``colwidth`` is ``[10, 30, 30, 30]`` with spacing 2 the total width will initially be 10+2+30+2+30+2+30=106. That's 26 characters too much, so a width of 26 will be removed from the truncated column. If ``truncate`` is 0, column 0 will have a width of -16 which is not permitted.

Extended example: Sorting and formatting a table with numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``format_table()`` deliberately cannot do anything but format arrays of strings. Non string entries are converted using ``str()`` but that's all. It cannot format the contents of the cells, sort the table, or anything of like that. I advocate composability over extensibility, and these operations are best done separately and then used along with ``format_table()``. It is also not very hard to do separately, as this example demonstrates.

Consider printing the race times of a 10km run. The data is already in a table, and we supply a separate header row::

    header =  ['Name'  , 'Time']
    table  = [['John'  , 3672  ],
              ['Martha', 2879  ],
              ['Stuart', 2934  ],
              ['Eduard', 2592  ]]

The race times are in seconds. Let's sort the rows by best time::

    table.sort(key=lambda row: row[1])

Next, let's convert the times to strings::

    for row in table:
        row[1] = format_time(row[1])
    
This uses the fact that ``row`` will be a reference/view to the table row, such that changing ``row`` will change the actual row in the table (this is actually one of the behaviors in Python I don't like). While this example uses frmt's own ``format_time()`` function, any function that converts your data to string will do. At last, let's add the header, and print the table::

    table.insert(0, header)
    print(format_table(table, '<>'))

Returns::

    Name       Time
    Eduard    43:12
    Martha    47:59
    Stuart    48:54
    John    1:01:12

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
