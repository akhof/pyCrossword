#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyCrossword import *
import time

if __name__ == "__main__":
    cols = 20
    rows = 20
    
    words = [
                Word("Tokyo"),
                Word("Jakarta"),
                Word("Seoul"),
                Word("Delphi"),
                Word("Shanghai"),
                Word("Berlin"),
                Word("New York"),
                Word("Beijing"),
                Word("Moscow"),
                Word("Paris"),
                Word("London"),
                Word("Essen"),
                Word("Bangkok"),
                Word("Toronto"),
                Word("Boston"),
                Word("Surat"),
                Word("Osaka"),
                Word("Mumbai"),
                Word("Lagos"),
                Word("Istanbul"),
             ]
    
    fieldconfig = FieldConfig(cols, rows, SPEED_NORMAL)
    con = create_new_crossword( words, fieldconfig )
    
    while con.status != STATUS_FINISHED:
        time.sleep(1)
    
    no = 0
    for result in con.results.values():
        no += 1
        print("RESULT #{}:".format(no))
        printCrossword(result)
        print("\n")