#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classes import Box
import random

class fill():
    def __init__(self, result):
        self.result = result
        self.con = result.con
        self.cols = self.con.fieldconfig.cols
        self.rows = self.con.fieldconfig.rows
    def start(self):
        self.__prepare()
        self.__generate()
        self.__finalsteps()
    
    def __prepare(self):
        # SORT WORDS BY LENGTH
        for word in self.con.all_words:
            if word not in self.con.words_in_any_result:
                self.result.words_not_in_grid.append(word)
        self.result.words_not_in_grid.sort(key=len, reverse=True)
        
        # CREATE GRID
        for col in range(55):
            for row in range(55):
                self.result.boxes[ (col, row) ] = Box(col, row)
        
        self.result.sorted_boxes = self.result.boxes.keys()
        
    def __finalsteps(self):
        # DAS KREUTWORT-FELD WIRD HIER AUF DIE ANGEGEBENE GROESSE ZUGESCHNITTEN (colXROW)
        newbox = []  #[ COL1, COL2 ]    |    COLx = [ROW, ROW]
        for _ in range(self.cols+1): newbox.append( [] )
        
        mincol1 = self.result.minCOL #-1
        mincol2 = self.result.minCOL+self.cols
        if mincol2 > 49:
            deltacol = mincol2-49
            mincol1 -= deltacol
            mincol2 = 49
        
        minrow1 = self.result.minROW #-1
        minrow2 = self.result.minROW+self.rows
        if minrow2 > 49:
            deltarow = minrow2-49
            minrow1 -= deltarow
            minrow2 = 49
        
        self.startCol = mincol1
        self.endCol = mincol2
        self.startRow = minrow1
        self.endRow = minrow2
        
        colCount = -1
        for col in range(mincol1, mincol2): #self.minCOL, self.minCOL+self.cols):
            colCount += 1
            rowCount = -1
            for row in range(minrow1, minrow2):
                rowCount += 1
                newbox[colCount].append(self.result.boxes[ (col, row) ])
    
        self.result.FINAL_BOXES = newbox
        
    def __generate(self):
        bevor = 0 #woerter, die zuvor einsortiert waren
        nachher = -1 #woerter, die anschleissend einsortiert waren
        while bevor != nachher:
            bevor = len(self.result.words_not_in_grid)
            self.__einsortieren()
            nachher = len(self.result.words_not_in_grid)
            if bevor == nachher:
                self.__insert_other_words(onlyone=True)
                nachher = len(self.result.words_not_in_grid)
            
    
    def __insert_other_words(self, onlyone=False):
        """
        Diese Funktion fuegt die Woerter ein, die bisher noch nicht einsortiert werden konnten; hier ohne zwingende schnittpunkte
        """
        
        for word in self.result.words_not_in_grid:
            if not self.__passt_wort_in_crossword(word): continue
            do_break = False
            
            for vertical in self.__get_random_vertical_horizontal():
                if do_break: break
                for startCol, startRow in self.result.sorted_boxes:
                    if do_break: break
                    if self.__check_valid_position(word, startCol, startRow, vertical, False):
                        self.__add_word(startCol, startRow, vertical, word)
                        do_break = True
                        self.result.points += 1
                        if onlyone: return
    
    def __einsortieren(self):
        for word in self.result.words_not_in_grid:
            if not self.__passt_wort_in_crossword(word): continue
            
            if len(self.result.words_in_field) == 0:
                # NOCH KEINE WOERTER EINSORTIERT
                start = (50-len(word))/2
                for v in self.__get_random_vertical_horizontal():
                    if v: col = 24; row = start
                    else: col = start; row = 24
                    if self.__check_valid_position(word, col, row, v, False):
                        self.__add_word(col, row, v, word)
                        break
            else:
                word_added = False
                for vertical in self.__get_random_vertical_horizontal():
                    for startCol, startRow in self.result.sorted_boxes:        
                        if self.__check_valid_position(word, startCol, startRow, vertical):
                            self.__add_word(startCol, startRow, vertical, word)
                            word_added = True
                            self.result.points += 5
                            break
                    if word_added: break
                
    def __check_valid_position(self, word, col, row, vertical, needcrosspoint=True):
        if word in self.result.words_in_field: return False #wort bereits im crossword
        
        newMinCOL = self.result.minCOL
        newMinROW = self.result.minROW
        newMaxCOL = self.result.maxCOL
        newMaxROW = self.result.maxROW
        
        if col < newMinCOL: newMinCOL = col
        if row < newMinROW: newMinROW = row
        if col+len(word) > newMaxCOL: newMaxCOL = col+len(word)
        if row+len(word) > newMaxROW: newMaxROW = row+len(word)
        
        if newMaxCOL-newMinCOL > self.cols: return False #field to big
        if newMaxROW-newMinROW > self.rows: return False #field to big
        
        crossedWords = []
        for pos in range(len(word)):
            try:
                if vertical: box = self.result.boxes[ (col+pos, row) ]
                else:        box = self.result.boxes[ (col, row+pos) ]
            except KeyError: return False
            if box.countwords == 0: continue
            if box.wordVertical != None and vertical: return False #zwei wörter übereinander vertikal
            elif box.wordHorizontal and not vertical: return False
            for w in [box.wordVertical, box.wordHorizontal]:
                crossedWords.append(w)            
                if word.getChar(pos) != box.getChar(): return False #zwei verschiedene Buchstaben
        if needcrosspoint and len(crossedWords) == 0: return False #hat keinen anderen buchstabe gekreuzt
            
        pointsToCheck = []
        if vertical:
            for rVerschub in [-1,0,1]:
                for c in range(col-1, col+len(word)+1):
                    if c not in range(49): continue
                    if row+rVerschub not in range(49): continue
                    pointsToCheck.append( (c, row+rVerschub) )
        else:
            for cVerschub in [-1,0,1]:
                for r in range(row-1, row+len(word)+1):
                    if r not in range(49): continue
                    if col+cVerschub not in range(49): continue
                    pointsToCheck.append( (col+cVerschub, r) )            
        for point in pointsToCheck:
            box = self.result.boxes[ point ]
            for crossedword in [box.wordVertical, box.wordHorizontal]:
                if crossedword == word: continue
                elif crossedword in crossedWords: continue
                elif crossedword == None: continue ###!!! TEST
                #elif not needcrosspoint: continue ####!!!! TEST
                else: return False
        
        return True
    
    def __add_word(self, col, row, vertical, word):
        """
        Diese Funktion fuegt das Wort word dem Result zu und errechnet diverse Attribute neu
        """
        
        if col < self.result.minCOL: self.result.minCOL = col
        if row < self.result.minROW: self.result.minROW = row
        if vertical:
            if col+len(word) > self.result.maxCOL: self.result.maxCOL = col+len(word)
        else:
            if row+len(word) > self.result.maxROW: self.result.maxROW = row+len(word)

        for pos in range(len(word)):
            self.result.boxes[ (col, row) ].set(word, pos, vertical)
            if vertical: col += 1
            else: row += 1
        
        self.result.words_in_field.append(word)
        for wnig_key in range(len(self.result.words_not_in_grid)):
            if self.result.words_not_in_grid[wnig_key] == word:
                del(self.result.words_not_in_grid[ wnig_key ])
                break
    
    def __passt_wort_in_crossword(self, word):
        """
        Diese Funktion überprüft ob ein Wort in das Crossword passen könnte oder klar nicht hineinpass
        """
        if len(word) > self.cols and len(word) > self.rows: return False

        charCountInCrossword = 0
        wordsAroundCount = 0
        for box in self.result.boxes.values():
            if box.getChar() != None: charCountInCrossword += 1
        for wordIC in self.result.words_in_field:
            wordsAroundCount += len(wordIC)
            
        if (self.rows*self.cols)-(charCountInCrossword+wordsAroundCount) < len(word): return False
        return True
    
    def __get_random_vertical_horizontal(self):
        """
        Diese Funktion gibt zufällig [True, False], oder [False, True] zurueck
        """
        return random.choice( [ [True, False], [False, True] ] )
    
def fill_result(result):
    """
    Diese Funktion fuellt ein Result-Objekt mit den "optimalen" Daten
    """
    
    filler = fill(result)
    filler.start()