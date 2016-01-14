# Conway's Game of life
# Escande Damien
# May 2015

import tkinter as tk
from tkinter import messagebox
import math
import os
from tkinter import simpledialog
import random
from tkinter import ttk


class Cell:
    cells = []
    running = False
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = False
        self.neighbours =[]
        self.alive_neighbours = []
    def compute_neighbours(self):
         return [c for c in Cell.cells if int( math.hypot(self.x - c.x, self.y - c.y) ) == ( abs(1) )]
    def draw_life(self):
        if self.is_alive:
            canvas.create_rectangle( self.x*20, self.y*20, self.x*20+20, self.y*20+20, fill="dodgerblue" )
        elif not self.is_alive:
            canvas.create_rectangle( self.x*20, self.y*20, self.x*20+20, self.y*20+20, fill="white" )

# activate cell.is_alive on mouseclick if event.x and event.y within cell boundaries (x*20 to x*20+19
def toggle_cell_life(e=None):
    for c in Cell.cells:
        if (e.x >= c.x*20 and e.x <= c.x*20+20) and (e.y >= c.y*20 and e.y <= c.y*20+20):
            if e.num == 1:
                c.is_alive = True
            else:
                c.is_alive = False
        c.draw_life()


# TODO save current setup, choose name for file with popup
def save_setup():
    pause_on_click()
    file_name = simpledialog.askstring(title="Enter file name",prompt="file name")
    file_to_save =""
    for c in Cell.cells:
        if c.is_alive:
            file_to_save+="*"
        else:
            file_to_save+="o"
    with open("./presets/{}.txt".format(file_name), "wt") as out_file:
        out_file.write(file_to_save)
    drop_down['values'] = sorted(os.listdir('./presets'))


def pause_on_click(e=None):
    Cell.running = False


def start_on_click(e=None):
    Cell.running =  True
    run_life()

def run_life():
    if Cell.running:
        root.after(350, run_life )
        gen_count.set(gen_count.get() + 1)
        canvas.delete("all")
        draw_grid(canvas)
        start_life()


def clear_on_click():
    pause_on_click()
    gen_count.set(0)
    for c in Cell.cells:
        c.is_alive = False
    canvas.delete("all")
    draw_grid(canvas)

def start_life():
    for c in Cell.cells:
        c.alive_neighbours = [1 for cell in c.neighbours if cell.is_alive]
    for c in Cell.cells:
        if len(c.alive_neighbours) < 2 and c.is_alive:
            c.is_alive = False
        elif len(c.alive_neighbours) == 2 and c.is_alive:
            c.is_alive = True
        elif len(c.alive_neighbours) == 3 and c.is_alive:
            c.is_alive = True
        elif len(c.alive_neighbours) == 3 and not c.is_alive:
            c.is_alive = True
        elif len(c.alive_neighbours) > 3 and c.is_alive:
            c.is_alive = False
        c.draw_life()

def draw_grid(can):
    for i in range(45): # 45 squares width, 25 height
        can.create_line(20 * i, 0, 20 * i, 500, fill="gray") # corresponds to canvas height
        can.create_line(0, 20 * i, 900, 20 * i, fill="gray") # corresponds to canvas width

def create_life():
    for c in Cell.cells:
        r = random.randint(1,10)
        if r == 1:
            c.is_alive = True

        c.draw_life()
# assigning cells
def create_cells():
    cells = []
    k = 0
    j = 0
    for i in range(45*25):
        if i % 45 == 0 and i is not 0:
            j+=1
            c = Cell(i,j)
        else:
            c = Cell(i,j)
        cells.append(c)

    for c in cells:
        if k > 44:
            k = 0
            c.x = k
        else:
            c.x = k
        k +=1
    return cells

def load_preset():
    """
    Loading preset pattern in plaintext from filesystem
    """
    with open("./presets/{}".format(preset_var.get() ) ) as f:
        data = f.read()
    allowed_chars = ('o','*','\n')
    if [c for c in data if c not in allowed_chars] or len(data) > 1125:
        warn = messagebox._show("Bad format","File format is invalid, it should be \nmade of 1125 chars containing 'o' or '*'")

    else:
        for i in range(len(data)):
            if data[i] == "*":
                Cell.cells[i].is_alive = True
                Cell.cells[i].draw_life()

def load_intro():
    with open("./intro/intro.txt") as f:
        data = f.read()
    if [ c for c in data if c not in ('o','*','\n')] or len(data) > 1125:
        warn = messagebox._show("Bad format","You messed up the intro pattern")
    else:
        for i in range(len(data)):
            if data[i] == "*":
                Cell.cells[i].is_alive = True
                Cell.cells[i].draw_life()

# Main
Cell.cells = create_cells()
for c in Cell.cells:
    c.neighbours = c.compute_neighbours()

# End starting setup
root = tk.Tk()
root.windowIcon = tk.PhotoImage("photo", file="./gof_glider.gif") # setting icon
root.tk.call('wm','iconphoto',root._w,root.windowIcon)
root.title("Yet another Conway's Game Of Life")
root.geometry("1150x640")
root['bd'] = 2
root['bg'] = 'gray25'
#root.resizable(0,0)
root.style = ttk.Style()
root.style.theme_use('clam')
gen_count = tk.IntVar()


# CANVAS
canvas = tk.Canvas(root,bg='white',relief=tk.FLAT,width=900,height=500)
canvas.grid(row=0,column=0,columnspan=3,sticky=tk.W+tk.S+tk.NE,rowspan=3)
# BUTTONS
start_button = ttk.Button(root, command=start_on_click,text="Start \n------->")
clear_button = ttk.Button(root, command=clear_on_click,text="Clear grid")
pause_button = ttk.Button(root,command=pause_on_click, text="Pause\n    ||")
tk.Label( root, textvariable = gen_count,bg="gray25",fg="cyan",font="Georgia 15 italic",padx=10).grid(row=3,column=3)
load_current_button = ttk.Button(root, command= save_setup,text = "Save current state").grid(row=2,column=3,sticky=tk.NW)
clear_button.grid(row=3,column=2,sticky=tk.NW)
start_button.grid(row=3,column=0,sticky=tk.NW)
pause_button.grid(row=3,column=1,sticky=tk.NW)

preset_var = tk.StringVar()
drop_down = ttk.Combobox(root,values = sorted(os.listdir('./presets')) ,justify=tk.CENTER,height=30,textvariable=preset_var)
drop_down.grid(row=0,column=3,sticky=tk.SW)
drop_down.current(0)

preset_button = ttk.Button(root,text="Load pattern",command=load_preset)
preset_button.grid(row=1,column=3,sticky=tk.NW)
explain_label = tk.Label(root, bg="gray25",fg="white",text="Left click the cells in the grid to activate, right click to kill, \n click start or press ENTER to launch, PAUSE or spacebar to halt",font="Verdana 10 italic",pady=20).grid(row=4,column=1)
draw_grid(canvas)

#create_life()
for el in Cell.cells:
    el.draw_life()
canvas.bind('<Button-1>', toggle_cell_life )
canvas.bind('<Button-3>', toggle_cell_life )
root.bind("<BackSpace>", pause_on_click )
root.bind("<Return>", start_on_click )
root.bind("<space>", pause_on_click)
load_intro()
root.mainloop()
