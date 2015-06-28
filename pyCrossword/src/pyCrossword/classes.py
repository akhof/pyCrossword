#!/usr/bin/env python
# -*- coding: utf-8 -*-

from globals import STATUS_STARTED, SPEED_NORMAL
import time

class Word():
    def __init__(self, word, *args, **kwds):
        self.word = word.upper().replace(" ", "_")
        self.args = args
        self.kwds = kwds
        self.length = len(word)
    
    def getChar(self, pos): return self.word[pos]
    def __len__(self):      return self.length
    def __repr__(self):     return self.word

class Box():
    def __init__(self, col, row):
        self.col = col
        self.row = row
        
        self.char = None
        self.wordVertical = None
        self.wordHorizontal = None
        self.firstCharVertical = False #hat das vertikale wort hier seinen ersten buchstaben?
        self.firstCharHorizontal = False #hat das horizontale wort hier seinen ersten buchstaben?
        self.countwords = 0 #Anzahl an Woertern, die in der Box enthalten sind (0, 1, 2)
    
    def set(self, word, pos, vertical):
        self.char = word.getChar(pos)
        if vertical:
            self.wordVertical = word
            if pos == 0: self.firstCharVertical = True
        else:
            self.wordHorizontal = word
            if pos == 0: self.firstCharHorizontal = True
        self.countwords += 1
    def getChar(self): return self.char

class Result():
    def __len__(self): #sDiese Funktion wird fuer die Sortierung benoetigt
        return 0 if self.points<0 else self.points 
    def __init__(self, con):
        self.con = con
        self.points = -1
        self.words_in_field = [] #liste aller Word-Objekte, die in das Feld einsortiert wurden
        self.boxes = {} #Dict. mit allen Box-Objekten (KEY: (col, row); VALUE: Box-obj)
        self.sorted_boxes = [] #Liste mit allen Box-Objekten, in der Reihenfolge werden Tests durchgeführt
        self.words_not_in_grid = [] #Liste an Woertern, die noch NICHT einsoriert sind
        
        self.minCOL =  9999
        self.minROW =  9999
        self.maxCOL = -9999
        self.maxROW = -9999
        self.startCol = -1
        self.endCol = -1
        self.startRow = -1
        self.endRow = -1
        
        self.FINAL_BOXES = [] #[ COL1, COL2 ]    |    COLx = [ROW, ROW]    |    ROW=Box()
    
class FieldConfig():
    def __init__(self, cols, rows, speed=SPEED_NORMAL):
        self.cols = cols #anzahl der spalten
        self.rows = rows #anzahl der zeilen
        self.speed = speed #Geschwindigkeit, in der das Krwuzwort generiert wird

class Connection():
    def __init__(self):
        self.fieldconfig = None #Eine Fieldconfig-Instanz
        self.all_words = [] #Liste aller Word-Objekte
        self.words_in_any_result = [] #Liste aller Word-Objekte, die in irgendeinem Result einsortiert wurden
        self.status = STATUS_STARTED #Status
        self.results = {} #Dict. an Results (KEY=result_id; VALUE=result-object)
        self.starttime = time.time() #Zeitstempel beim Beginn des Vorgangs
        