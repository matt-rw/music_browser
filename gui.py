#!/usr/bin/env python
"""GUI."""
import math

import tkinter as tk

from browser.yt_browser import YouTubeBrowser


class InvalidKeyError(AttributeError):
    pass


class Window(tk.Tk):
    """Window overriding Tkinter.

    Start with mainloop(self) and stop with destroy(self).

    """
    def __init__(self):
        super().__init__()
        self.title('Umusi')
        self.minsize(500, 400)
        self.elements: dict = {}
        self.page = 0

        # Add elements
        self.add_label('artist-label', 'Artist', 20, 0, 0)
        self.add_entry('artist-entry', 20, 1, 0)
        self.add_label('song-label', 'Song', 20, 0, 1)
        self.add_entry('song-entry', 20, 1, 1)
        self.add_button('window-button', 'Open window', 0, 2)
        self.add_button('live-button', 'Live version', 1, 2)
       
        self.make_frames()
        
        # Handlers for control sequences
        self.bind('<Return>', self.handle_return)
        self.bind('<Escape>', self.handle_escape)

    def add_label(self, key: str, text: str, width: int, row: int, column: int):
        """Add an element with text."""
        if key in self.elements:
            raise InvalidKeyError('Name already in use to identify an element')
        label = tk.Label(master=self, text=text, width=width)
        label.grid(row=row, column=column, padx=5, pady=5, sticky='w')
        self.elements[key] = label

    def add_entry(self, key: str, width: int, row: int, column: int):
        """Add a textbox element."""
        entry = tk.Entry(master=self, width=width)
        entry.grid(row=row, column=column, padx=5, pady=5, sticky='w')
        self.elements[key] = entry

    def reset_entry(self, entry):
        """Clear entry text."""
        entry['state'] = 'normal'
        entry.delete(0, tk.END)

    def add_button(self, key: str, text: str, row: int, column: int):
        """Add a clickable button."""
        variable = tk.IntVar()
        button = tk.Checkbutton(
            master=self,
            text=text,
            variable=variable,
            onvalue=1,
            offvalue=0
        )
        button.grid(row=row, column=column, padx=5, pady=5, sticky='w')
        self.elements[key] = (variable, button)

    def add_button_func(self, key: str, text: str, row: int, column: int, func):
        """Add a button with a handler."""
        button = tk.Button(master=self, text=text)
        button.bind('<Button-1>', func)
        button.grid(row=row, column=column, padx=5, pady=5, sticky='w')
        self.elements[key] = button

    def make_frames(self):
        """Create a 10 x 10 grid for the GUI."""
        self.frames = []
        for i in range(10):
            frame = tk.Frame(master=self, relief=tk.RAISED, borderwidth=1)
            frame.grid(row=i+2, column=0, padx=0, pady=0, sticky="w")
            self.frames.append(frame)

    def clear_frames(self):
        for frame in self.frames:
            frame.destroy()
    
    def close_button(self, event):
        self.server.browser.quit()
        # self.server = None
        self.elements['close-button'].destroy()
        
    def handle_escape(self, event):
        """Clear all input."""
        self.reset_entry(self.elements['artist-entry'])
        self.reset_entry(self.elements['song-entry'])

        self.elements['back-button'].destroy()
        self.elements['next-button'].destroy()
        self.clear_frames()
    
    def handle_key(self, event):
        """Handle input."""
        if event.char == 'Escape':
            artist_entry = self.elements['artist-entry']
            artist_entry['state'] = 'normal'
            artist_entry.delete(0, tk.END)
            song_entry = self.elements['song-entry']
            song_entry['state'] = 'normal'
            song_entry.delete(0, tk.END)

            self.clear_frames()

        # Select one of the links in the page
        if event.char.isnumeric():
            # if self.server:
            #    self.server.quit()
            index = int(event.char)
            # launch link
            link = self.links[index+(self.page*10)][1]
            self.add_button_func('close-button', 'Close', 3, 2, self.close_button)
            
            show = self.elements['window-button'][0].get()
            self.server.show_link(link, show)
        
    def handle_return(self, event):
        """Action to search for links."""
        self.clear_frames()
        self.make_frames()

        artist = self.elements['artist-entry'].get()
        song = self.elements['song-entry'].get()
        
        # page forward or back
        self.add_button_func('back-button', 'Back', 2, 2, self.button_back)
        self.add_button_func('next-button', 'Next', 2, 3, self.button_next)

        # create new browser and search
        self.server = YouTubeBrowser()
        args = [artist, song]
        if self.elements['live-button'][0].get():
            args.append('[live]')
        url = self.server.read_input(*args)
        self.links = self.server.retrieve_links(url)
        
        # display links
        for i in range(0, 10):
            link = self.links[i+(self.page*10)]
            label = tk.Label(
                    master=self.frames[i],
                    text=f'{i} : {link[0]}',
                    )
            label.pack(padx=0, pady=0)
        
        self.server.browser.quit()
        # self.server = None

        self.elements['artist-entry']['state'] = 'readonly'
        self.elements['song-entry']['state'] = 'readonly'

        self.bind('<Key>', self.handle_key)
   
    def button_back(self, event):
        """Pagination handler for back."""
        if self.page > 0:
            self.page -= 1
            self.handle_return(None)
        
    def button_next(self, event):
        """Pagination handler for next."""
        num = len(self.links)
        max_pages = math.floor(num/10)
        if self.page < max_pages:
            self.page += 1
            self.handle_return(None)


if __name__ == '__main__':
    window = Window()
    window.mainloop()
