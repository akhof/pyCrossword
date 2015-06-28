#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

AUS DEM PACKAGE  crossword_old  ÜBERNOMMEN! NOCH KEINE ANPASSUNGEN AN DAS AKTUELLE PACKAGE!

"""







import wx, threading, time, Queue, thread
from create_grid import create_grid
import loadingDialog

class NoSolution(Exception): pass

def getColour(cw):
    colournames = ["RED", "BLUE", "GREEN", "YELLOW", "ORANGE", "PINK", "BROWN", "GOLD", "AQUAMARINE", "MAGENTA", "KHAKI", "NAVY", "TAN", "PLUM", "MAROON", "ORCHID", "THISTLE", "GREY", "DARK OLIVE GREEN", "DARK GREEN", "FIREBRICK"]
    cw.lastcolourindex += 1
    
    try: return wx.ColourDatabase().Find(colournames[cw.lastcolourindex])
    except: return wx.BLACK

class Legend():
    def __init__(self, col, row, vertical, legendTxt, colour):
        self.col = col
        self.row = row
        self.vertical = vertical
        self.legendTxt = legendTxt
        self.colour = colour

class loadThread(threading.Thread):
    def __init__(self, crossword, durchgaengeQueue, fertigQueue):
        threading.Thread.__init__(self) 
        self.cw = crossword
        self.durchgaengeQueue = durchgaengeQueue
        self.fertigQueue = fertigQueue
        
        self.cancel = False
    def run(self):
        while not self.cw.alleDurchgaengeErzeugt:
            while not self.fertigQueue.empty():
                try:
                    _ = self.fertigQueue.get(timeout=1)
                    self.cw.alleDurchgaengeErzeugt = True
                except Queue.Empty: pass
                finally: break
            while not self.durchgaengeQueue.empty():
                try: self.cw.durchgaenge.append(self.durchgaengeQueue.get(timeout=1))
                except Queue.Empty: break
            if self.cancel: return
            

class Crossword(wx.Panel):
    def __init__(self, parent, cols, rows, words):
        # words  =  { wordToShowInCrossword:wordToShowInLegend }
        
        wx.Panel.__init__(self, parent)
        self.rt = parent.rt
        self.cols = cols
        self.rows = rows
        self.words = words
        
        self.richtig = 0
        self.falsch = 0
        self.nochvokabeln = 0
        self.nochdurchgaenge = 0
        
        self.alleDurchgaengeErzeugt = False
        self.durchgaenge = []
        self.textboxes = {} #{ (col, row) : textctrl() }
        
        self.lastcolourindex = -1
        
        self.loadthread = None
        self.cancel = False
    
    def CANCEL_ABF(self, callfromloadingdia=False):
        ######
        print("Cancel cw-abf...")
        try: self.loadthread.cancel = True
        except AttributeError: pass #!
        self.cancel = True
        if callfromloadingdia:
            self.rt.frame.call("main")
            self.Destroy()
            #self.Disconnect()
            #sorge dafür, dass zum hmenü gewechselt wird...
    
    def LOAD(self):
        durchgaengeQueue, fertigQueue = create_grid(self, self.cols, self.rows, self.words, 10)
        self.loadthread = loadThread(self, durchgaengeQueue, fertigQueue).start()
    
    def START(self):
        dia = loadingDialog.CrosswordLoadingDialog(self)
        def realStart():
            count_words = 0
            for dg in self.durchgaenge: count_words += len(dg.wordsInCrossword)
            self.nochvokabeln = count_words
            self.nochdurchgaenge = len(self.durchgaenge)
        
        def th_func():
            time.sleep(0.1) #!
            while True:
                if len(self.durchgaenge) > 0: break
                if self.alleDurchgaengeErzeugt and len(self.durchgaenge) == 0: raise NoSolution() #!!
            wx.CallAfter(dia.EndModal, 200)
            wx.CallAfter(realStart)
        
        thread.start_new(th_func, ())
        dia.ShowModal()

    
    def build_next_durchgang(self):
        if len(self.durchgaenge) == 0 and self.alleDurchgaengeErzeugt:
            print "Ende :)"
            return
        
        self.lastcolourindex = -1
        result = self.durchgaenge[0]
    
        
        cwpanel = wx.Panel(self)
        cwpanel.SetBackgroundColour(wx.Colour(215, 211, 209))
        cwsizer = wx.FlexGridSizer(self.rows, self.cols, 0, 0)
        
        
        legends = []
        
        for row in range(result.startRow, result.endRow):
            for col in range(result.startCol, result.endCol):
                pos = (col, row)
                
                box = result.boxes[ pos ]
                
                if len(box.words) == 0:
                    cwsizer.Add((25,25))
                    self.textboxes[pos] = None
                else:
                    tc = wx.TextCtrl(cwpanel, style=wx.NO_BORDER)
                    tc.kehrfarbe = None
                    tc.hintergrundfarbe = None
                    tc.SetMaxLength(1)
                    tc.SetSize((25,25))
                    tc.SetMinSize((25, 25))
                    tc.SetMaxSize((25, 25))
                    tc.Bind(wx.EVT_TEXT, self.textctrlchanged)
                    self.textboxes[pos] = tc
                    cwsizer.Add(tc, 0, 0, 0)
                    
                    for winl_k, winl_v in box.firstCharOfWords.iteritems():
                        colour = getColour(self)
                        legends.append( Legend(col, row, winl_v, winl_k, colour) )
                        
                        if (0.2126*colour.Get()[0]) +(0.7152*colour.Get()[1]) + (0.0722*colour.Get()[2]) > 127: kehrfarbe = wx.BLACK
                        else: kehrfarbe = wx.WHITE
            
                        tc.SetBackgroundColour(colour)
                        tc.SetForegroundColour(kehrfarbe)
                        tc.hintergrundfarbe = colour
                        tc.kehrfarbe = kehrfarbe
                    
                
        cwpanel.SetSizer(cwsizer)
        cwsizer.Fit(cwpanel)
        
        legendSizer = wx.GridSizer(15,1,0,0)
        
        
        legendPrinted = []
        for legend in legends:
            legendsWithSamePos = []
            for l in legends:
                if l.col == legend.col and l.row == legend.row:
                    if l not in legendPrinted:
                        legendsWithSamePos.append(l)
                        legendPrinted.append(l)
        
            txt = ""
            for legend in legendsWithSamePos:
                for v in [True, False]:
                    if v == legend.vertical:
                        if len(txt) > 2: txt += "\n"
                        if v: txt += self.rt.get_lang("basic-horiz")+"\t"
                        else: txt += self.rt.get_lang("basic-verti")+"\t"
                        txt += legend.legendTxt.legend
                
            if len(txt) > 0:
                st = wx.StaticText(self, -1, txt)
                st.SetForegroundColour(self.textboxes[ (legend.col, legend.row) ].hintergrundfarbe)
                tt = wx.ToolTip(txt)
                tt.SetDelay(999)
                self.textboxes[ (legend.col, legend.row) ].SetToolTip(tt)
                legendSizer.Add(st, 0, wx.EXPAND, 0)
        

        button_pruefen = wx.Button(self, -1, self.rt.get_lang("basic-pruefen"))
        self.Bind(wx.EVT_BUTTON, self.pruefen, button_pruefen)
        
        cwpanel.SetMinSize(cwpanel.GetBestSize())
        
        mainsizer = wx.FlexGridSizer(2, 2, 0, 10)
        mainsizer.Add(legendSizer, 0, 0, 0) #wx.EXPAND als 3. Argument; 0 zum testen
        mainsizer.Add(cwpanel, 0, 0, 0)
        mainsizer.Add((1,1))
        mainsizer.Add(button_pruefen)
        
        mainsizer.AddGrowableCol(0)
        mainsizer.AddGrowableRow(0)
        
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        self.Parent.next_durchgang()
    
    def textctrlchanged(self, event):
        obj = event.GetEventObject()
        obj.SetForegroundColour(obj.kehrfarbe)
        if obj.GetValue().upper() != obj.GetValue(): obj.SetValue(obj.GetValue().upper())
    
    def pruefen(self, event):
        durchgang = self.durchgaenge[0]
        errors = False

        for pos in self.textboxes.keys():
            box = durchgang.boxes[pos]
            
            if self.textboxes[pos] == None: continue
            enteredChar = self.textboxes[pos].GetValue().upper().strip()
            correctChar = box.getChar()
            
            if enteredChar == correctChar:
                c = wx.GREEN
            else:
                c = wx.RED
                errors = True
            
            if (not self.textboxes[pos].hintergrundfarbe == c) and len(self.textboxes[pos].GetValue()) > 0:
                self.textboxes[pos].SetForegroundColour(c)
            else:
                self.textboxes[pos].SetForegroundColour(self.textboxes[pos].kehrfarbe)
        
        if not errors:
            def weiter():
                del(self.durchgaenge[0])
                
                for tb in self.textboxes.values():
                    if tb != None: tb.Destroy()
                for k in self.textboxes.keys(): del(self.textboxes[k])
                self.GetSizer().DeleteWindows()
                
                self.build_next_durchgang()
            
            if len(self.durchgaenge) > 1:
                weiter()
            else:
                dia = loadingDialog.CrosswordLoadingDialog(None)
            
                def th_func():
                    time.sleep(0.1) #!
                    while True:
                        if len(self.durchgaenge) > 1 or self.alleDurchgaengeErzeugt: break
                    wx.CallAfter(dia.EndModal, 200)
                    wx.CallAfter(weiter)
                
                thread.start_new(th_func, ())
                dia.ShowModal()
    