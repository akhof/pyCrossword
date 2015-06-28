#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classes import *
from globals import *
from newCrossword import create_new_crossword
from printCrossword import *

howto = """
=============
== globals ==
=============

- STATUS_STARTED
- STATUS_WORKING
- STATUS_CANCEL
- STATUS_FINISHED
- STATUS_ERROR
- SPEED_FAST
- SPEED_NORMAL
- SPEED_SLOW



=============
== classes ==
=============

Word
    - word
    - args
    - kwds
    + __init__(word, *args, **kwds)
Box
    - col
    - row
    - char
    - wordVertical
    - wordHorizontal
    - firstCharVertical
    - firstCharHorizontal
    - countwords
    + getChar()
Result
    - FINAL_BOXES
        = [COL1, COL2]
            |_[ROW1, ROW2]
               |_Box()
FinalConfig
    - cols
    - rows
    - speed
    + __init__(cols, rows, speed)
        speed = SPEED_NORMAL
Connection
    - starttime
        = time.time()
    - status
        = STATUS_STARTED or STATUS_WORKING or STATUS_CANCEL or STATUS_FINISHED or STATUS_ERROR
        set status to STATUS_CANCEL to cancel build-progress
    - results
        = { resultID : Result() }



===============
== functions ==
===============

create_new_crossword(words, fieldconfig)
 |                    |      |_ a Fieldconfig()-object
 |                    |_a list of Word()-objects
 |_ returns a Connection()-object
 |_ is starting the process in a thread. all finished pages (one result) are in the dict Connection.results
createStrCrossword(result)
 |_ returns the generated result
printCrossword(result)
 |_ prints the generated result
"""