from frmt import *
import shutil

def test_fit_text():
    assert fit_text('abc', 5)      == 'abc  '
    assert fit_text('abc', 5, '<') == 'abc  '
    assert fit_text('abc', 5, '^') == ' abc '
    assert fit_text('abc', 5, '>') == '  abc'
    assert fit_text('abc', 2)      == '..'
    assert fit_text('abcdef', 5)   == 'ab...'
    assert fit_text('abcdef', 5, suffix='!', align='>') == 'abcd!'

def test_fit_text_terminal_width():
    width = shutil.get_terminal_size().columns
    assert fit_text('a'*width)     == 'a'*width
    assert fit_text('a'*(width+1)) == 'a'*(width-3)+'...'

def test_format_time_special():
    assert format_time('text')       == 'text'
    assert format_time(float('nan')) == '-'
    assert format_time(0)            == '0'

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
    assert format_time(60,'small')  == '60.0s'
    assert format_time(99,'small')  == '99.0s'
    assert format_time(100,'small') == '100s'
    assert format_time(0.1,'large') == '0'
    assert format_time(10,'large')  == '10'

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
