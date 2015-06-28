#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy, threading, time
from classes import Connection, Result
from globals import STATUS_WORKING, STATUS_FINISHED, STATUS_ERROR, STATUS_CANCEL, SPEED_FAST, SPEED_NORMAL, SPEED_SLOW
from algo import fill_result

def start_creating_new_crossword(con):
    con.status = STATUS_WORKING
    old_len___words_in_any_result = -1
    while old_len___words_in_any_result != len(con.words_in_any_result):
        old_len___words_in_any_result = len(con.words_in_any_result)
        
        results = [] #alle results, die erstelt wurden
        
        if con.fieldconfig.speed == SPEED_FAST: repeat = 4
        elif con.fieldconfig.speed == SPEED_NORMAL: repeat = 8
        elif con.fieldconfig.speed == SPEED_SLOW: repeat = 12
        else: repeat = 8
        
        for _ in range(repeat):
            if con.status == STATUS_CANCEL: return
            r = Result(con) #create result
            fill_result(r) #fuellt das result mit den "optimalen" Daten
            results.append(r)
        best_result = sorted(results, key=len, reverse=True)[0] #der result mit der hoesten punktzahl wird ermittelt
        
        for wordInField in best_result.words_in_field: #alle woerter, die im besten result einsortiert wurden werden der con beigefuegt
            con.words_in_any_result.append(wordInField)
        
        con.results[len(con.results.keys())] = best_result #der beste result wird dem result-dict beigefuegt
    con.status = STATUS_FINISHED

class startThread(threading.Thread):
    def __init__(self, con):
        self.con = con
        threading.Thread.__init__(self)
    def run(self):
        time.sleep(0.2)
        try:
            start_creating_new_crossword(self.con)
        except:
            self.con.status = STATUS_ERROR
            raise
    
def create_new_crossword(words, fieldconfig):
    """
    Diese Funktion startet das Erstellen eines neuen
    Kreuzwortes und gibt ein Connection-Objekt zurueck
    """
    
    con = Connection()
    con.all_words = copy.deepcopy(words)
    con.fieldconfig = fieldconfig
    
    startThread(con).start()
    
    return con