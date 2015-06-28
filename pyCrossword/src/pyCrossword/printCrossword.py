#!/usr/bin/env python
# -*- coding: utf-8 -*-

def printCrossword(result):
    print(createStrCrossword(result))

def createStrCrossword(result):
    out = "\n"
    for col in result.FINAL_BOXES:
        for row in col:
            char = row.getChar()
            if char == None: char = " "
            out += char + u" "
        out += "\n"
    return out