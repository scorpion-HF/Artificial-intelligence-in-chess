import tkinter as tk
from tkinter import *
from anytree import Node
import time
#********************************************************************************************************************

class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=60, color1="white", color2="blue"):
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.places = {}
        self.playercoords = (7 , 7)
        canvas_width = columns * size
        canvas_height = rows * size
        tk.Frame.__init__(self, parent)
        self.startbutton = tk.Button(self , text = 'start' , command = self.move)
        self.startbutton.pack()
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
            width=canvas_width, height=canvas_height, background="black")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = (y1 + self.size)
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="green", fill=color  , tags =str(row*8+col))
                self.places[row*8+col] = [row , col]
                color = self.color1 if color == self.color2 else self.color2
                self.canvas.bind("<Button-1>",self.disable)
                
    def addpiece(self, name, image, row=0, column=0):
        self.canvas.create_image(0,0, image=image, tags=('player'), anchor="c")
        self.player = name
        self.placepiece(row, column)
        
    def placepiece(self, row, column):
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords('player', x0, y0)
        self.playercoords = (x0 , y0)
        
    def disable(self , event):
        self.canvas.find_all()
        if (self.canvas.find_withtag(CURRENT)):
            if (len(self.places[int(self.canvas.gettags(CURRENT)[0])]) == 3) :
                if (self.places[int(self.canvas.gettags(CURRENT)[0])][2] != "lock") :
                    self.canvas.itemconfig(CURRENT , fill = 'yellow')
                    self.places[int(self.canvas.gettags(CURRENT)[0])].append("block")
            else :
                self.canvas.itemconfig(CURRENT , fill = 'yellow')
                self.places[int(self.canvas.gettags(CURRENT)[0])].append("block")

    def get_knight_moves(self,x,ps):
        l = []
        if [x[0]+1,x[1]+2] in ps:
            l.append((x[0]+1,x[1]+2))
        if [x[0]-1,x[1]+2] in ps:
            l.append((x[0]-1,x[1]+2))
        if [x[0]+2,x[1]+1] in ps:
            l.append((x[0]+2,x[1]+1))
        if [x[0]+2,x[1]-1] in ps:        
            l.append((x[0]+2,x[1]-1))
        if [x[0]+1,x[1]-2] in ps:
            l.append((x[0]+1,x[1]-2))
        if [x[0]-1,x[1]-2] in ps:    
            l.append((x[0]-1,x[1]-2))
        if [x[0]-2,x[1]-1] in ps:
            l.append((x[0]-2,x[1]-1))
        if [x[0]-2,x[1]+1] in ps:        
            l.append((x[0]-2,x[1]+1))
        return l

    def get_pawn_moves(self,x,ps,s):
        l = []
        if (s == 'd'):
            if(([x[0]-1,x[1]] in ps)):
               l.append((x[0]-1,x[1]))
            if([x[0]-1,x[1]+1,'block'] in ps):
                l.append((x[0]-1,x[1]+1))
            if([x[0]+1,x[1]+1,'block'] in ps):
                l.append((x[0]+1,x[1]+1))
            if([x[0]+1,x[1]-1,'block'] in ps):
                l.append((x[0]+1,x[1]-1))
            if([x[0]-1,x[1]-1,'block'] in ps):
                l.append((x[0]-1,x[1]-1))
            return l
        else :
            if(([x[0]+1,x[1]] in ps)):
               l.append((x[0]+1,x[1]))
            return l

    def get_bishop_moves(self,x,ps):
        l = []
        z = x
        while(z[0] < 8 and z[1] > -1):
            z = (z[0]+1 , z[1]-1)
            temp = list(z)
            temp.append('block')
            if temp in ps:
                break
            if list(z) in ps:
                l.append(z)
        z = x
        while(z[0] < 8 and z[1] < 8):
            z = (z[0]+1 , z[1]+1)
            temp = list(z)
            temp.append('block')
            if temp in ps:
                break
            if list(z) in ps:
                l.append(z)
        z = x
        while(z[0] > -1 and z[1] > -1):
            z = (z[0]-1 , z[1]-1)
            temp = list(z)
            temp.append('block')
            if temp in ps:
                break
            if list(z) in ps:
                l.append(z)
        z = x
        while(z[0] > -1 and z[1] < 8):
            z = (z[0]-1 , z[1]+1)
            temp = list(z)
            temp.append('block')
            if temp in ps:
                break
            if list(z) in ps:
                l.append(z)
        return l
    
    def search(self):
        if self.player == 'Knight':
            get_moves = self.get_knight_moves
        elif self.player == 'Bishop':
            get_moves = self.get_bishop_moves
        elif self.player == 'Pawn':
            get_moves = self.get_pawn_moves
        ps1 = list(self.places.values())
        ps2 = list(self.places.values())
        ps1.remove([7,7])
        states1 = [Node((7,7))]
        ps2.remove([0,0])
        states2 = [Node((0,0))]
        sres = []
        dres = []
        states3 = []
        states4 = []
        ans1 = 0
        ans2 = 0
        flag = True
        while(flag):
            sres = []
            dres = []
            for i in states1:
                if self.player == 'Pawn':
                    l1 = get_moves(i.name,ps1,'d')
                else :
                    l1 = get_moves(i.name,ps1)
                for j in l1:
                    sres.append(Node(j,parent = i))
                    if list(j) in ps1:
                        ps1.remove(list(j))
                    else :
                       x = list(j)
                       x.append('block')
                       ps1.remove(x)
            states1 = sres[:]
            for k in sres:
                states3.append(k.name)
            for i in states2:
                if self.player == 'Pawn':
                    l2 = get_moves(i.name,ps2,'u')
                else :
                    l2 = get_moves(i.name,ps2)
                for j in l2:
                    dres.append(Node(j,parent = i))
                    if list(j) in ps2:
                        ps2.remove(list(j))
                    else :
                       x = list(j)
                       x.append('block')
                       ps2.remove(x) 
                    if dres[-1].name in states3:
                        flag = False
                        ans2 = dres[-1]
                        for k in sres:
                            if k.name == dres[-1].name:
                                ans1 = k
                        break
                if not dres:
                    for i in states2:
                        if i.name in states3:
                            ans2 = i
                            for j in sres:
                                if j.name == i.name:
                                    ans1 = j
                                    flag = False
                                    break
            if(ans1 and ans2):
                states3 = []
                states4 = []

                for i in ans2.ancestors:
                    states3.insert(0,i.name)
                for i in ans1.ancestors:
                    states4.append(i.name)
                states4.append(ans2.name)
                return states4+states3
            
            if dres:            
                states2 = dres[:] 
            if(not (sres)):
                break
            for k in dres:
                states4.append(k.name)
            states3 = []
            states4 = []
            
    def move(self):
        l = self.search()
        if (l):
            for i in l:
                self.after(1000)
                self.placepiece(i[0] , i[1])
                self.update()
#********************************************************************************************************************

def select():
    if v.get() == 3 :
        imagedata = 'Pawn.png'
        window.destroy()
        root = tk.Tk()
        root.resizable(0 ,0)
        board = GameBoard(root)
        board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        player = tk.PhotoImage(file = imagedata)
        board.addpiece('Pawn',player, 7,7)
        l = 3
        for i in range(0,5):
            l += 1
            for j in range(l,9):
                board.canvas.itemconfig((i*8)+j , fill = 'pink')
                board.places[int(board.canvas.gettags((i*8)+j)[0])].append("lock")
        l = 1
        for i in range(3,8):
            l += 1
            for j in range(1,l):
                board.canvas.itemconfig((i*8)+j , fill = 'pink')
                board.places[int(board.canvas.gettags((i*8)+j)[0])].append("lock")
        root.mainloop()
    elif v.get() == 2 :
        imagedata = 'Knight.png'
        window.destroy()
        root = tk.Tk()
        root.resizable(0 ,0)
        board = GameBoard(root)
        board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        player = tk.PhotoImage(file = imagedata)
        board.addpiece('Knight',player, 7,7)
        root.mainloop()
    elif v.get() == 1 :
        imagedata = 'Bishop.png'
        window.destroy()
        root = tk.Tk()
        root.resizable(0 ,0)
        board = GameBoard(root)
        board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        player = tk.PhotoImage(file = imagedata)
        board.addpiece('Bishop',player, 7,7)
        root.mainloop()
        
window = tk.Tk()
window.geometry('400x470')
window.resizable(0,0)
sign = tk.PhotoImage(file = 'sign1.png')
tk.Label(window , image = sign).pack()
imagedata = tk.StringVar()
v = tk.IntVar()       
r1 = tk.Radiobutton(window , text = 'bishop' , variable = v , value = 1 , command = select).pack()
r2 = tk.Radiobutton(window , text = 'knight', variable = v , value = 2, command = select).pack()
r3 = tk.Radiobutton(window , text = 'pawn', variable = v , value = 3, command = select).pack()
    
