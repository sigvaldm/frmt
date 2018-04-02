Frmt
====

Lightweight formatting of tables, times, etc. in Python.

The library only has a few simple functions, which will be briefly described here. Complete documentation is available in their docstring.

``format_table()``
------------------
Formats a table represented as a 2D array of strings into a nice big string suitable for printing. Example::

    table = [[''      ,'Math','English','History', 'Comment'          ],
             ['Bob'   ,'A'   ,'B'      ,'F'      , 'Failed at history'],
             ['Jane'  ,'C'   ,'A'      ,'A'      , 'Quite good'       ],
             ['Trevor','B'   ,'D'      ,'C'      , 'Somewhat average' ]]

    print(format_table(table))

Returns::

            Math  English  History  Comment
    Bob     A     B        F        Failed at history
    Jane    C     A        A        Quite good
    Trevor  B     D        C        Somewhat average

The ``align`` parameter can be used to change cell alignment:

    ``<`` - Left aligned (default)
    ``^`` - Centered
    ``>`` - Right aligned

It is also possible to have different alignments for different columns by having one character for each column, e.g. to have the first column left aligned and the subsequent four right aligned:

    ``<>>>>``     or equivalently     ``<>``

If only some columns are specified, the last specified alignment is repeated. It is also possible to have different alignments for differnt rows by having a list of alignment strings for each row. Again, if only the first rows are specified, the last alignment string in the list will apply to all subsequent rows. For instance,

    print(format_table(table, ['^','<^^^<']))

Returns::

            Math  English  History       Comment
    Bob      A       B        F     Failed at history
    Jane     C       A        A     Quite good
    Trevor   B       D        C     Somewhat average

On the header row all cells are centered (``^``). On the subsequent rows the leftmost column is left aligned, the three next ones are centered, and the last is also left aligned (``<^^^<``).

The ``colwidth`` parameter can be used to change column widths, which by default is just big enough to fit the contents. E.g. setting it to 10 means that all columns are 10 characters wide. Setting it to [20, 10] means that the first column is 20 characters wide and the subsequent ones are 10. Again, the last specified width is repeated for the remaining columns.

The spacing between the columns is ``spacing`` characters (default: 2).

If the total table width exceeds ``maxwidth`` the column indicated by ``truncate`` (default: 0) is truncated with a suffix ``suffix`` (default: "...") on rows that are too long. If ``maxwidth`` is not specified it will be taken as the terminal width minus 1. This truncation overrides settings in ``colwidth``.

Beware that no columns can have zero or negative width. If for instance ``maxwidth`` is 80 and ``colwidth`` is [10, 30, 30, 30] with spacing 2 the total width will initially be 10+2+30+2+30+2+30=106. That's 26 characters too much, so a width of 26 will be removed from the truncated column. If ``truncate`` is 0, column 0 will have a width of -16 which is not permitted.
