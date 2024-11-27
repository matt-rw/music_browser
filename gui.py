#!/usr/bin/env python
"""GUI."""
import math

import tkinter as tk

from .browser import Browser


"""Overrides Tkinter."""
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Umusi')
        self.minsize(500, 400)
        
        # Text boxes
        self.lbl_artist = tk.Label(master=self, text='Artist', width=20)
        self.lbl_song = tk.Label(master=self, text='Song', width=20)
        self.ent_artist = tk.Entry(master=self, width=20)
        self.ent_song = tk.Entry(master=self, width=20)
        self.lbl_artist.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.lbl_song.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.ent_artist.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_song.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Buttons
        self.var = tk.IntVar()
        self.btn_show = tk.Checkbutton(master=self, text='Show window',
                variable=self.var, onvalue = 1, offvalue = 0)
        self.btn_show.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.var_live = tk.IntVar()
        self.btn_live = tk.Checkbutton(master=self, text='Live version',
                variable=self.var_live, onvalue = 1, offvalue = 0)
        self.btn_live.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        self.makeFrames()
        
        # Pagination
        self.page = 0
        
        # Control sequence handlers
        self.bind("<Return>", self.handleReturn)
        self.bind("<Escape>", self.handleClear)
    
    def handleClose(self, event):
        self.server.browser.quit()
        self.btn_quit.destroy() 
        
    def handleClear(self, event):
        self.ent_artist['state'] = 'normal'
        self.ent_song['state'] = 'normal'
        self.ent_artist.delete(0, tk.END)
        self.ent_song.delete(0, tk.END)
        self.btn_back.destroy()
        self.btn_next.destroy()
        self.clearFrames()
    
    def handleKey(self, event):
        if event.char == 'Escape':
            self.ent_artist['state'] = 'normal'
            self.ent_song['state'] = 'normal'
            self.ent_artist.delete(0, tk.END)
            self.ent_song.delete(0, tk.END)
            self.clearFrames()
        if event.char.isnumeric():
            index = int(event.char)
            # launch link
            link = self.links[index+(self.page*10)][1]
            self.btn_quit = tk.Button(master=self, text='Close server')
            self.btn_quit.bind("<Button-1>", self.handleClose)  
            self.btn_quit.grid(row=3, column=2, padx=5, pady=5, sticky="w")
            
            show = self.var.get()
            self.server.showLink(link, show)
        
    def handleReturn(self, event):
        self.clearFrames()
        self.makeFrames()
        self.artist = self.ent_artist.get()
        self.song = self.ent_song.get()
        
        # make forward, back
        self.btn_back = tk.Button(master=self, text='Back')
        self.btn_next = tk.Button(master=self, text='Next')
        self.btn_back.bind("<Button-1>", self.handleBack)
        self.btn_next.bind("<Button-1>", self.handleNext)
        self.btn_back.grid(row=2, column=2, padx=0, pady=0, sticky="w")
        self.btn_next.grid(row=2, column=3, padx=0, pady=0, sticky="w")
        # pass input to server
        self.server = Browser()
        args = [self.artist, self.song, self.var_live.get()]
        url = self.server.readInput(args)
        self.links = self.server.retrieveLinks(url)
        
        for i in range(0, 10):
            link = self.links[i+(self.page*10)]
            label = tk.Label(
                    master=self.frames[i],
                    text=f"{i} : {link[0]}",
                    )
            label.pack(padx=0, pady=0)
        
        self.server.browser.quit()

        # select link
        self.ent_artist['state'] = 'readonly'
        self.ent_song['state'] = 'readonly'

        self.bind("<Key>", self.handleKey)
   
    def handleBack(self, event):
        if self.page > 0:
            self.page -= 1
            self.handleReturn(None)
        
    def handleNext(self, event):
        num = len(self.links)
        max_pages = math.floor(num/10)
        if self.page < max_pages:
            self.page += 1
            self.handleReturn(None)

    def makeFrames(self):
        self.frames = []
        for i in range(10):
            frame = tk.Frame(
                    master=self,
                    relief=tk.RAISED,
                    borderwidth=1
                    )
            frame.grid(row=i+2, column=0, padx=0, pady=0, sticky="w")
            self.frames.append(frame)

    def clearFrames(self):
        for frame in self.frames:
            frame.destroy()


if __name__ == '__main__':
    window = Window()
    window.mainloop()


main()
