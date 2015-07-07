#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse, time, sys
from pyCrossword import *

def run():
    print("pyCrossword")
    
    parser = argparse.ArgumentParser(prog="pyCrossword")
    
    parser.add_argument("-r",       "--rows",                                           default=10,     type=int,   help="number of rows (default: 10)")
    parser.add_argument("-c",       "--cols",                                           default=10,     type=int,   help="number of cols (default: 10)")
    parser.add_argument(            "--slow",                   action="store_true",                                help="slow but exact")
    parser.add_argument(            "--normal",                 action="store_true",                                help="normal")
    parser.add_argument(            "--fast",                   action="store_true",                                help="fast but not exact")
    parser.add_argument("words",                     nargs='*',                          default=[],                help="word to add in crossword")
    
    args = parser.parse_args()
    
    if args.slow:       speed = SPEED_SLOW
    elif args.fast:     speed = SPEED_FAST
    else:               speed = SPEED_NORMAL
    
    words = []
    for strWord in args.words:
        words.append( Word(strWord) )
    
    fieldconfig = FieldConfig(args.cols, args.rows, speed)
    con = create_new_crossword(words, fieldconfig)
    
    while con.status != STATUS_FINISHED:
        time.sleep(1)
    
    no = 0
    for result in con.results.values():
        no += 1
        if no == len(con.results.keys()):
            continue
        print("RESULT #{}:\n_".format(no))
        printCrossword(result)
        print("_\n")
    

if __name__ == "__main__":
    try:
        #Test:
        #sys.argv = [None, "-r", "12", "-c", "12", "--normal", "Book", "House", "Computer", "Water", "Printer", "Mobile", "Keyboard", "Street", "Car"]
        run()
    except KeyboardInterrupt:
        print("\n\nAbort...")
        sys.exit(1)