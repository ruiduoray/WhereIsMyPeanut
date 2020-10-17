"""
Graphic designed by Yujie Qiu
yujieqiu55@gmail.com

Music and sound by Xinyu Yang
yangx520@newschool.edu

Programmed by Ray Gong
ruiduoray@berkeley.edu

Final edited on Nov 26th, 2018
"""
from random import randint
from tkinter import *
import os

"""Board class, game logistics are written in this class"""
class Board:
    def __init__(self,size,peanut):
        self.board = [['-'] * size for _ in range(size)]
        self.size = size
        self.generate_peanuts(peanut)
        self.over = False
        self.found_peanuts = []
        
        
    def __str__(self):
        indent = len(str(self.size))
        stri = ' ' * indent
        for i in range(self.size):
            stri = stri + ' '*(indent - len(str(i + 1)))
            stri = stri+' '+str(i+1)
        stri = stri + '\n'
        for i in range(self.size):
            stri = stri + ' '*(indent - len(str(i + 1)))
            stri = stri + str(i + 1)
            for j in range(self.size):
                stri = stri + ' ' * (indent - len(self.board[i][j]) + 1) + self.board[i][j]
            stri = stri + '\n'
        return stri

    def generate_peanuts(self, peanut):
        self.peanuts = []
        while True:
            position = randint(0, self.size * self.size - 1)
            if position in self.peanuts:
                continue
            self.peanuts.append(position)
            if len(self.peanuts) >= peanut:
                break

    def make_move(self,row,column):
        position = self.find_position(row,column)
        if position in self.peanuts:
            self.update_board(row,column,'0')
            self.found_peanuts.append(position)
            if len(self.found_peanuts) >= len(self.peanuts):
                self.over = True
            return 0
        for n in range(1,self.size):
            checklst = self.find_circle(position,n)
            for x in checklst:
                if x in self.peanuts:
                    self.update_board(row,column,str(n))
                    return n

    def reveal_peanuts(self):
        for x in self.peanuts:
            row,column = self.find_row_column(x)
            self.update_board(row,column,'0')

        
    def update_board(self,row,column,new):
        self.board[row][column] = new
        
    def find_position(self,row,column):
        return row*self.size + column

    def find_row_column(self,position):
        return (position//self.size,position%self.size)

    def find_circle(self,position,n):
        lst = []
        left,right = [],[]
        top,bot = [],[]
        row = position // self.size
        column = position % self.size
        lst.extend([position - self.size * n, position + self.size * n])
        for i in range(1,n+1):
            if column - i < 0:
                break
            left.extend([x-i for x in lst])
        for i in range(1,n+1):
            if column + i >= self.size:
                break
            right.extend([x+i for x in lst])
        lst.extend(left)
        lst.extend(right)
        if column - n >= 0:
            top.extend([position-n - self.size*i for i in range(0,n)])
            bot.extend([position-n + self.size*i for i in range(1,n)])
        if column + n < self.size:
            top.extend([position+n - self.size*i for i in range(0,n)])
            bot.extend([position+n + self.size*i for i in range(1,n)])
        lst.extend(top)
        lst.extend(bot)
        return lst

    def reveal_all(self):
        for i in range(0,self.size):
            for j in range(0,self.size):
                self.make_move(i,j)
        self.over = False


"""Squirrel class that each squirrel has different rules to count the score"""
class Squirrel:
    music = 0
    
    def __init__(self,board,game,rate = 1,food = 10,bonus = 5,bonus_food = 2):
        self.score = 0
        self.live = True
        self.food = food
        self.rate = rate
        self.board = board
        self.bonus = bonus
        self.buttons = []
        self.game = game
        self.bonus_food = bonus_food
        self.images = {
            '-': PhotoImage(file = "小松鼠图/blank.png"),
            '0': PhotoImage(file = "小松鼠图/peanut.png"),
            '1': PhotoImage(file = "小松鼠图/1.png"),
            '2': PhotoImage(file = "小松鼠图/2.png"),
            '3': PhotoImage(file = "小松鼠图/3.png"),
            '4': PhotoImage(file = "小松鼠图/4.png"),
            '5': PhotoImage(file = "小松鼠图/5.png"),
            '6': PhotoImage(file = "小松鼠图/6.png"),
            '7': PhotoImage(file = "小松鼠图/7.png"),
            '8': PhotoImage(file = "小松鼠图/8.png"),
            }

        for i in range(self.board.size):
            row_of_buttons = []
            for j in range(self.board.size):
                row_of_buttons.append(self.bind_button_to_cell(i,j))
            self.buttons.append(row_of_buttons)
        



        
    def bind_button_to_cell(self,row,column):
        button = Button(self.game.frame,image = self.images[self.board.board[row][column]])
        button.bind("<Button-1>",lambda event: self.left_click(row,column))
        return button

    def left_click(self,row,column):
        self.make_move(row,column)
        self.buttons[row][column].config(image=self.images[self.board.board[row][column]])


    def make_move(self,row,column):
        if self.board.board[row][column] != '-' or not self.live:
            return
        score = self.board.make_move(row,column)*self.rate
        if score == 0:
            self.score += self.bonus
            self.food += self.bonus_food
            if Squirrel.music: 
                os.system("afplay Sounds/Peanut.wav&")
        else:
            self.score += score
            if Squirrel.music: 
                os.system("afplay Sounds/Score.wav&")
        self.food -= 1
        if self.food <= 0:
            self.live = False
        self.game.score_label.config(text = str(self.score))
        self.game.food_label.config(text = str(self.food))
        if not self.live:
            self.end_game()
            if Squirrel.music:
                os.system("afplay Sounds/Over.wav&")
        else:
            self.update_label(score)

    def update_label(self,score):
        if score == 0:
            text = "Found a peanut!\nGot "+ str(self.bonus) +" points and "+ str(self.bonus_food) +" extra food"
        else:
            text = "Peanut is "+str(score//self.rate) + " away! Got " + str(score) +" points"
        self.game.ending_label.config(text = text)

    def end_game(self):
        text = "Food Empty! Your final score is: " + str(self.score)
        self.game.ending_label.config(text = text)
        game_mode_1.last_score = self.score
        game_mode_1.last_pick = self.game.pick
        if self.score > game_mode_1.best_score:
            game_mode_1.best_score = self.score
            game_mode_1.best_pick = self.game.pick
        end_label = Label(self.game.frame,text="Play a new game?",bg='#F0DD95',fg='#3D2D04')
        end_button_yes= Button(self.game.frame,text = "Yes! ",fg="green",command = self.yes)
        end_button_no= Button(self.game.frame,text = "No..",fg="red",command = self.no)
        end_label.grid(row = 12,column = 1,columnspan = 6)
        end_button_yes.grid(row = 13,column = 1,columnspan = 3)
        end_button_no.grid(row = 13,column = 4, columnspan= 3)

    def yes(self):
        self.game.frame.destroy()
        choose_squirrel(self.game.root)

    def no(self):
        if Squirrel.music:
            os.system("killall afplay")
        self.game.root.destroy()
        

            

             
"""The only game mode it currently has right now:
To find peanuts to survive while trying to get a higher score"""
class game_mode_1:
    last_score = 0
    last_pick = 0
    best_score = 0
    best_pick = 0
    def __init__(self,root,squirrel_pick):
        self.pick = squirrel_pick
        game_mode_1.frame = Frame(root)
        self.frame.pack()
        self.board = Board(8,10)
        self.get_squirrel()
        self.IMAGES ={
            1:PhotoImage(file='小松鼠图/squirrel_norm_50.png'),
            2:PhotoImage(file='小松鼠图/squirrel_small_50.png'),
            3:PhotoImage(file='小松鼠图/squirrel_fat_50.png'),
            4:PhotoImage(file='小松鼠图/bestscore.png'),
            5:PhotoImage(file='小松鼠图/score.png'),
            6:PhotoImage(file='小松鼠图/food.png'),
            }
        self.root = root
        self.score_text = Label(self.frame,text = "Score")
        self.food_text = Label(self.frame,text = "Food")
        self.score_label = Label(self.frame,text = '0',bg='#F0DD95',fg='#3D2D04')
        self.food_label = Label(self.frame,text = str(self.squirrel.food),bg='#F0DD95',fg='#3D2D04')
        self.ending_label = Label(self.frame,text = '')
        self.display()
        
    def display(self):
        for i in range(8):
            for j in range(8):
                self.squirrel.buttons[i][j].grid(row = i,column = j)
        self.score_text.grid(row = 0,column = 8,rowspan = 2,columnspan = 2,sticky='E')
        self.score_label.grid(row = 0, column = 10, rowspan = 2,columnspan = 2,sticky='W')
        self.food_text.grid(row = 2,column = 8,rowspan = 2,columnspan = 2,sticky='E')
        self.food_label.grid(row = 2, column = 10, rowspan = 2,columnspan = 2,sticky='W')
        self.ending_label.grid(row = 8, column = 0, columnspan = 12,sticky="W")
        sqr_img = Label(self.frame,image = self.IMAGES[self.pick])
        sqr_img.grid(row = 5, column = 8, rowspan = 3,columnspan = 3)
        
    def get_squirrel(self):
        if self.pick == 1:
            self.squirrel = Squirrel(self.board,self)
        elif self.pick == 2:
            self.squirrel = Squirrel(self.board,self, rate = 2, food = 5,bonus_food = 3)
        elif self.pick == 3:
            self.squirrel = Squirrel(self.board,self,bonus = 10, food = 12)
        
    
"""Loading interface for choosing the squirrels and showing best scores etc."""
class choose_squirrel:
    def __init__(self,root):
        self.root = root
        self.frame = Frame(root)
        self.titleframe = Frame(root)
        self.titleframe.pack()
        self.frame.pack(side="top")
        self.IMAGES = {
            1:PhotoImage(file='小松鼠图/squirrel_norm.png'),
            2:PhotoImage(file='小松鼠图/squirrel_small.png'),
            3:PhotoImage(file='小松鼠图/squirrel_fat.png'),
            4:PhotoImage(file='小松鼠图/squirrel_norm_50.png'),
            5:PhotoImage(file='小松鼠图/squirrel_small_50.png'),
            6:PhotoImage(file='小松鼠图/squirrel_fat_50.png'),
            7:PhotoImage(file='小松鼠图/normal_tag.png'),
            8:PhotoImage(file='小松鼠图/small_tag.png'),
            9:PhotoImage(file='小松鼠图/fat_tag.png'),
            10:PhotoImage(file='小松鼠图/title.png'),
            }
        self.choose_buttons()
        self.show_previous()
        

    def choose_buttons(self):
        normal_button = Button(self.frame, image = self.IMAGES[1],command=lambda:self.choose(1))
        normal_label = Button(self.frame,image = self.IMAGES[7],command = lambda:self.explaination(1))
        small_button = Button(self.frame, image = self.IMAGES[2],command=lambda:self.choose(2))
        small_label = Button(self.frame,image = self.IMAGES[8],command = lambda:self.explaination(2))
        fat_button = Button(self.frame, image = self.IMAGES[3],command=lambda:self.choose(3))
        fat_label = Button(self.frame,image = self.IMAGES[9],command = lambda:self.explaination(3))
        self.title_label = Label(self.titleframe,image = self.IMAGES[10])
        normal_button.grid(row= 1,column = 0,rowspan= 3,columnspan=3)
        normal_label.grid(row = 4,column = 0, columnspan = 3)
        small_button.grid(row= 5,column = 0,rowspan= 3,columnspan=3)
        small_label.grid(row = 8,column = 0, columnspan = 3)
        fat_button.grid(row= 9,column = 0,rowspan= 3,columnspan=3)
        fat_label.grid(row = 12,column = 0, columnspan = 3)

    def show_previous(self):
        if game_mode_1.best_score == 0:
            self.title_label.grid(row = 0,column = 0,columnspan = 3)
            return
        self.title_label.grid(row = 0,column = 0,columnspan = 6)
        best_score = Label(self.frame,text="Best Score:\n"+str(game_mode_1.best_score),bg='#E39D55',fg='#3D2D04')
        best_pick_label = Label(self.frame, text = "with squirrel:")
        best_pick_image = Label(self.frame,image=self.IMAGES[game_mode_1.best_pick+3])
        last_score = Label(self.frame,text="Last Score:\n"+str(game_mode_1.last_score),bg='#E39D55',fg='white')
        last_pick_label = Label(self.frame, text = "with squirrel:")
        last_pick_image = Label(self.frame,image=self.IMAGES[game_mode_1.last_pick+3])
        best_score.grid(row=1,column = 5, rowspan = 2, columnspan = 3)
        best_pick_label.grid(row = 3, column =5,columnspan = 3)
        best_pick_image.grid(row = 4, column = 5, rowspan = 2, columnspan = 3)
        last_score.grid(row=6,column = 5, rowspan = 2, columnspan = 3)
        last_pick_label.grid(row = 8, column =5,columnspan = 3)
        last_pick_image.grid(row = 9, column = 5, rowspan = 2, columnspan = 3)

    def choose(self,n):
        self.titleframe.destroy()
        self.frame.destroy()
        game_mode_1(self.root,n)

    def explaination(self,n):
        self.frame.forget()
        self.explainframe = Frame(self.root)
        self.explainframe.pack()
        if n == 1:
            text = """
                    This is a normal squirrel who loves peanuts 
                    that were given by Berkeley students. He starts
                    with 10 amount of food, each move costs him
                    1 food. When he gets a peanut, it gives him
                    2 extra food and 5 points. He also scores
                    the number he lands on. Those numbers
                    represents how far the most closed peanut is."""
        elif n == 2:
            text = """
                    This is a newborn squirrel. Very soon, he
                    already knows to look for peanuts. To
                    encourage him to find more peanuts, he scores
                    double amount of the number he lands on.
                    However, since he is very small, he only
                    starts with 5 amount of food, but each peanut
                    will give him 3 extra food instead of 2. 
                    """
        elif n == 3:
            text = """
                    This is a fat squirrel. He is fat not because
                    that the winter is coming, but because
                    that he loves eating peanuts. When he gets
                    a peanut, he is much happier than other
                    squirrels, so he scores 10 points on peanuts.
                    He also stores a lot of food, so he starts with
                    12 peanuts.
                    """
        explainlabel = Label(self.explainframe, text = text,bg='#F0DD95',justify = LEFT)
        explainlabel.grid(row = 0, column = 1)
        closebutton = Button(self.explainframe, text = "close", command = self.close)
        closebutton.grid(row = 1, column = 1, sticky = E)


    def close(self):
        self.explainframe.destroy()
        self.frame.pack(side='top')
        
                           
    


"""Code version that the programmer(me) used to debug the board"""
def code_game():
    size = int(input("size: "))
    peanut = int(input("peanut: "))
    board = Board(size,peanut)
    while not board.over:
        print(board)
        row = int(input("Row: ")) - 1
        if row == -1:
            board.reveal_peanuts()
            continue
        if row == -2:
            board.reveal_all()
            continue
        column = int(input("Column: ")) - 1
        
        board.make_move(row,column)
def code_run():
    while True:
        game()
        choice = str(input("New Game? Y/N\n"))
        if choice == 'Y' or choice == 'y':
            continue
        break

    
"""Functions to create the menu bar"""
def creat_menu(root):
    menu = Menu(root)
    root.config(menu=menu)
    submenu1 = Menu(menu)
    submenu2 = Menu(menu)
    menu.add_cascade(label = "Setting" ,menu = submenu1)
    menu.add_cascade(label = "Game" ,menu = submenu2)
    submenu1.add_command(label = "Music",command = turn_music)
    submenu2.add_command(label = "Quit",command = lambda:quit_game(root))
    submenu2.add_command(label = "New Game",command = lambda:new_game(root))
def turn_music():
    if Squirrel.music == 1:
        os.system("killall afplay")
        Squirrel.music = 0
    else:
        os.system("afplay Sounds/Game.wav&")
        Squirrel.music = 1
def quit_game(root):
    if Squirrel.music ==1:
        os.system("killall afplay")
    root.destroy()
def new_game(root):
    game_mode_1.frame.destroy()
    choose_squirrel(root)

            
"""Game Main"""
def game():
    root = Tk()
    root.title("Where Is My Peanut")
    root.minsize(401,501)
    root.geometry("401x501+500+200")
    creat_menu(root)
    bkgrd_img = PhotoImage(file = "小松鼠图/bg.png")
    bkgrd_label = Label(root,image = bkgrd_img)
    bkgrd_label.place(x=0,y=0)
    bkgrd_label.image = bkgrd_img
    choose_squirrel(root)
    root.mainloop()

"""Run The Game"""
game()
