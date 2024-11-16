# -*- coding: utf-8 -*-

import numpy as np
import time
import sys
import pickle
import os

import tkinter as tk
from tkinter import ttk

import connect4_algorithms as al        

# A class that sets up the Connect 4 grid and manages the gameplay
# play_move: Places the players disc at given position
# move_checked: Checks the given position to make sure it is a legal move
# make_move: Initiates player's algorithm to obtain position the player wants to play in
#and ensures players alternate turns
# determine_player: determines which players turn it is
class SetGame:
    def __init__(self,next_player,file_name,players):
        self.grid = np.zeros((6,7))
        self.next_player = next_player
        self.x = 0
        self.y = 0
        self.file_name = file_name
        self.players = players
       
    def play_move(self,player_value):
        """
        Plays the player's disc at specified position.

        Parameters
        ----------
        player_value : int
            Player's associated value.

        Returns
        -------
        None.
        """
        self.grid[self.y][self.x] = player_value
       
    def move_checked(self):
        """
        Checks whether the move to make is legal.

        Returns
        -------
        bool
            Returns True if the move is legal or False if it is not.
        """
        if self.grid[self.y][self.x]!=0:
            return False
        elif self.y==5:
            return True
        elif self.grid[self.y+1][self.x]==0:
            return False
        else:
            return True
                
    def make_move(self):
        """
        Obtains the position to place a disc and plays it.

        Returns
        -------
        None.
        """
        move_made = False           
        while not move_made:
            self.y,self.x, = self.players[self.next_player].use_player_algorithm(self.grid)
            if SetGame.move_checked(self):
                move_made = True
        SetGame.play_move(self,self.players[self.next_player].player_number)
        #if self.players[self.next_player].player_algorithm == 3:   #Used to create training files
            #file_array = []
            #for n in range(7):
                #if n==self.x:
               #     file_array.append(1)
              #  else:
             #       file_array.append(0)
            
            #with open(self.file_name,"ab") as f:
            #    pickle.dump([self.grid,file_array],f)
            #f.close()
        self.players[self.next_player].player_moves += 1
    
    def determine_player(self): 
        """
        Determines which player is to play next.

        Returns
        -------
        None.
        """
        SetGame.make_move(self)
        player = self.next_player
        if self.next_player > 0:
            self.next_player -= 1
        else:
            self.next_player += 1
        return self.x,self.y,player
            
            
class GUIController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.title('Connect 4')
        container = tk.Frame(self)
        container.pack(fill='both',expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.players = []
        
        self.frames = {}
        for F in (GameGUI,StartMenu):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column=0, sticky="nsew")     
        self.show_frame(StartMenu)
    
    def show_frame(self,name):
        """
        Shows different GUI frames.

        Parameters
        ----------
        name : Class name
            Frame class to be called.

        Returns
        -------
        None.

        """
        frame = self.frames[name]
        frame.tkraise()
        
        
class StartMenu(tk.Frame):
    def __init__(self,parent,controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        algorithms = [
            'Random',
            'Minimax',
            'Minimax with A-B Pruning',
            'User Input',
            'Artificial Neural Network'
        ]
        lb1 = tk.Label(self,text="Player 1", font='Calibri 20')
        lb1.grid(row=0,column=2, padx=10, pady=10)
        
        self.variable_p1 = tk.StringVar(self)
        self.variable_p1.set(algorithms[0])
        menu_p1 = ttk.OptionMenu(self, self.variable_p1,'Random', *algorithms)  #Not setting random as default removes it from selection
        menu_p1.grid(row=1,column=2, padx=10, pady=10)
        
        lb2 = tk.Label(self,text='Player 2', font='Calibri 20')
        lb2.grid(row=0,column=4, padx=10, pady=10)
        
        self.variable_p2 = tk.StringVar(self)
        self.variable_p2.set(algorithms[0])
        menu_p2 = ttk.OptionMenu(self, self.variable_p2,'Random', *algorithms)
        menu_p2.grid(row=1,column=4, padx=10, pady=10)
        
        depths = [
            '2',
            '4',
            '6',
            '8'
        ]
        
        depth1 = tk.Label(self,text='Depth Player 1', font='Calibri 13')
        depth1.grid(row=2,column=2, pady=20)
        self.depth_player1 = tk.StringVar(self)
        self.depth_player1.set(depths[0])
        depth_player1_menu = ttk.OptionMenu(self, self.depth_player1, '2', *depths)
        depth_player1_menu.grid(row=3,column=2,pady=0)
        
        depth2 = tk.Label(self,text='Depth Player 2', font='Calibri 13')
        depth2.grid(row=2,column=4,pady=20)
        self.depth_player2 = tk.StringVar(self)
        self.depth_player2.set(depths[0])
        depth_player2_menu = ttk.OptionMenu(self, self.depth_player2, '2', *depths)
        depth_player2_menu.grid(row=3,column=4,pady=0)
        
        game_stats = ttk.Label(self,text='Game Statistics',font='Calibri 20')
        game_stats.grid(row=4,column=4,padx=10,pady=10)
        self.player1_win = tk.Label(self,text='Player 1 Won 0.0% Games', font='Calibri 13')
        self.player1_win.grid(row=5,column=2, padx=10, pady=10)
        self.player2_win = tk.Label(self,text='Player 2 Won 0.0% Games', font='Calibri 13')
        self.player2_win.grid(row=5,column=6, padx=10, pady=10)
        self.players_draw = tk.Label(self,text='Players drew 0.0% Games', font='Calibri 13')
        self.players_draw.grid(row=5,column=4, padx=10, pady=10)
        self.sim_time = tk.Label(self,text='Simulation time: 0.0 seconds', font='Calibri 13')
        self.sim_time.grid(row=6,column=4, padx=10, pady=10)
        
        num_games = tk.Label(self,text='Number Of Games',font='Calibri 20')
        num_games.grid(row=0,column=6,padx=10,pady=10)

        self.validate_input = (self.register(self.validate),
                               '%d','%P','%s')
        self.sim_input = tk.Entry(self,width=4,font='Calibri 20',validate='key',validatecommand=(self.validate_input))
        self.sim_input.grid(row=1,column=6,padx=10,pady=0)
        
        begin_sim = tk.Button(self,text='Run Simulation',relief='raised',command=self.run_simulation)
        begin_sim.grid(row=2,column=0, padx=10, pady=10)
        
    def validate(self,d,P,s):
        """
        Validates the options users set.

        Parameters
        ----------
        d : int
            1 if a value was entered, 0 if value deleted.
        P : int
            Current set of inputs.
        s : int
            Input before current input.

        Returns
        -------
        bool
            False if user has entered invalid settigs, True otherwise.

        """
        if int(d)==0:
            return True
        elif not str.isdigit(P):
            tk.messagebox.showerror('Error','Must be a value of 0-9')
            return False
        elif len(s)>=4:
            return False
        else:
            return True
        
    def check_val(self,P):
        """
        Another method to perform validation checks, but these cannot be done
        whilst the user is specifying settings.
        Parameters
        ----------
        P : int
            Value user has entered in the input number of games box.

        Returns
        -------
        bool
            False if user has entered invalid settings, True otherwise.

        """
        if not str.isdigit(P):
            msg = 'Please check your inputs'
        elif int(P)>1000:
            msg = 'Max number of simulations is 1000'
        elif int(P)==0:
            msg = 'Must be at least 1 game'
        elif int(P)!=1 and (self.variable_p1.get()=='User Input' or self.variable_p2.get()=='User Input'):
            msg = 'Must be 1 game for User Input'
        else:
            return True
        self.bell()
        tk.messagebox.showerror('Error',msg)
        return False
    
    def set_algorithms(self):
        """
        Creates and initialises the player objects, setting their algorithms and disc colours.
        Returns
        -------
        None.

        """
        if len(self.controller.players)>0:
            self.controller.players.pop()
            self.controller.players.pop()
        player1 = al.Player(1, 2, self.variable_p1.get(),int(self.depth_player1.get()),'yellow')
        player2 = al.Player(2, 1, self.variable_p2.get(),int(self.depth_player2.get()),'red')
        self.controller.players.append(player1)
        self.controller.players.append(player2)
        
    def run_simulation(self):
        """
        Runs the gameplay after user has submitted their settings. Determines if simulation
        requires graphical representation or statistical analysis.
        Returns
        -------
        bool
            True if user settings are valid and simulation complete.
            False if user settings are invalid.

        """
        self.player1_win.configure(text='Player 1 Won 0.0% Games')
        self.player2_win.configure(text='Player 2 Won 0.0% Games')
        self.players_draw.configure(text='Players drew 0.0% Games')
        self.sim_time.configure(text='Simulation time: 0.0 seconds')
        self.update()   #Updates all the labels
        
        if self.check_val(self.sim_input.get()):
            self.set_algorithms()
            if int(self.sim_input.get())>1:
                self.sim_time.configure(text='Simulation time: Running..') #Only needed when running multiple sims
                self.update()
                next_player = 0
                sim_time = time.time()
                for n in range(int(self.sim_input.get())):
                    game_on = True
                    self.game = SetGame(next_player,'',self.controller.players)
                    while game_on:
                        x,y,player = self.game.determine_player()
                        if al.is_victory(self.game.grid, self.controller.players[0].player_number):
                            game_on = False
                            self.controller.players[0].player_score += 1
                        elif al.is_victory(self.game.grid,self.controller.players[1].player_number):
                            game_on = False
                            self.controller.players[1].player_score += 1
                        elif al.is_grid_full(self.game.grid):
                            game_on = False
                    if next_player>0:
                        next_player-=1
                    else:
                        next_player+=1
                sim_time = round(time.time() - sim_time,2)
                player1_score = round(self.controller.players[0].get_player_score() / int(self.sim_input.get()) * 100,2)
                player2_score = round(self.controller.players[1].get_player_score() / int(self.sim_input.get()) * 100,2)
                drawn = round(100 - (player1_score+player2_score),2)
                self.msg_one = 'Player 1 won '+str(player1_score)+'% games'
                self.msg_two = 'Player 2 won '+str(player2_score)+'% games'
                self.msg_three = 'Players drew '+str(drawn)+'% games'
                self.msg_four = 'Simulation time: '+str(sim_time)+' seconds'
                
                self.player1_win.configure(text=self.msg_one)
                self.player2_win.configure(text=self.msg_two)
                self.players_draw.configure(text=self.msg_three)
                self.sim_time.configure(text=self.msg_four)
                return True
            else:
                self.controller.show_frame(GameGUI)
        else:
            return False
             
        
class GameGUI(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.box_columns = []
        self.simulation = False
        self.move_made = False
        self.start_game = tk.Button(self,text='Start',bg='#24D153',command=lambda:self.draw_grid())
        self.start_game.grid(row=0,column=0)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

    def draw_grid(self):
        """
        Draws the grid and the player 'key' counters (the counters to show which player
                                                      is using which colour).
        Returns
        -------
        None.

        """
        self.start_game.grid_forget()
        self.simulation = True
        self.window = tk.Canvas(master=self.controller,width=1000,height=600)
        x1 = 70
        for x in range(7):
            x1+=90
            y1=20
            x2=x1+90
            y2=y1+90
            if len(self.box_columns)<7:     #Caused problems where games would place number of games worth of discs
                self.box_columns.append([x1,y1,x2,y2])
            for y in range(6):
                self.window.create_rectangle(x1,y1,x2,y2, outline='blue',width=6)
                y1=y2 
                y2+=90  
        self.window.create_oval(800,20,850,70,fill=self.controller.players[0].player_colour)
        self.window.create_oval(800,80,850,130,fill=self.controller.players[1].player_colour)
        self.window.create_text(900,45, text=' - Player 1', font='Calibri 15')
        self.window.create_text(900,105,text=' - Player 2', font='Calibri 15')
        self.window.pack()
        self.begin_game()
        
    def begin_game(self):
        """
        Initialises the graphical simulation and maintains the game until an end
        state is reached.
        Returns
        -------
        None.

        """
        self.next_player = 0
        self.player = self.next_player
        self.game = SetGame(self.next_player,'',self.controller.players)
        self.window.update()
        self.maintain_game()

    def maintain_game(self):
        """
        Ensures gameplay is being played, managing if an end state has been reached,
        and getting the algorithms or user to take their turn.
        Returns
        -------
        None.

        """
        if not (al.is_victory(self.game.grid,self.controller.players[0].get_player_number()) or
                al.is_victory(self.game.grid,self.controller.players[1].get_player_number()) or
                al.is_grid_full(self.game.grid)):
            if self.controller.players[self.player].get_player_algorithm()=='User Input':
                self.wait_for_player()
            else:
                time.sleep(0.2)
                x,self.row,self.player = self.game.determine_player()
                self.position_pieces(x)
            self.after(100,self.maintain_game)
        else:
            self.window.unbind("<Button-1>")
            if al.is_victory(self.game.grid, self.controller.players[0].player_number):
                self.controller.players[0].player_score += 1
                victory_message = 'Player 1 Wins!'
            elif al.is_victory(self.game.grid, self.controller.players[1].player_number):
                self.controller.players[1].player_score += 1
                victory_message = 'Player 2 Wins!'
            else:
                victory_message = 'Draw!'
            self.win_label = tk.Label(master=self,text=victory_message,font='Calibri 30')
            self.win_label.grid(row=0,column=0)
            self.columnconfigure(0,weight=1)
            self.rowconfigure(0,weight=1)
            self.return_home_button = tk.Button(self,text='Return Home',command=lambda:self.return_home())
            self.return_home_button.grid(row=2,column=0)
            
    def update_players_turn(self):
        """
        Updates who's turn it is next to place their disc, after
        the current player has placed theirs.
        Returns
        -------
        None.

        """
        if self.player>0:
            self.player-=1
        else:
            self.player+=1
            
    def position_pieces(self,x):
        """
        Obtains the area to which the player's disc should be played to
        on the graphical grid.
        Parameters
        ----------
        x : int
            The column on the grid to which the player has chosen to play to.

        Returns
        -------
        None.

        """
        x = self.box_columns[x]
        self.window.create_oval(x[0]+7,x[1]+(self.row*90)+7,x[2]-7,x[3]+(self.row*90)-7, fill=self.controller.players[self.player].player_colour) #Has to be self.player, else cant change turns
        self.window.pack()
        self.update_players_turn()
    
    def wait_for_player(self):
        """
        Method to keep the program waiting until the user has clicked the 
        column they wish to play to.
        Returns
        -------
        bool
            False if the user has not played yet, True otherwise.

        """
        self.window.bind("<Button-1>",self.user_input)
        if self.move_made:
            self.player = self.game.next_player
            self.window.unbind("<Button-1>")
            self.move_made = False
            return True
        return False
    
    def user_input(self,event):
        """
        When the user has clicked a column, this method obtains the position
        on the grid and places their disc.
        Parameters
        ----------
        event : Button-1 event
            Event when user clicks their left-button on mouse. This allows
            for the column of their choosing to be obtained.

        Returns
        -------
        None.

        """
        for x in self.box_columns:
            if x[0]<event.x<x[2]:
                self.column = self.box_columns.index(x)
                self.row = self.controller.players[self.player].get_row(self.column, self.game.grid)
                self.game.x = self.column
                self.game.y = self.row
                if self.game.move_checked():
                    self.game.grid[self.row][self.column] = self.controller.players[self.player].player_number
                    self.window.create_oval(x[0]+7,x[1]+(self.row*90)+7,x[2]-7,x[3]+(self.row*90)-7, fill=self.controller.players[self.player].player_colour)
                    self.move_made = True
                    if self.game.next_player>0:
                        self.game.next_player-=1
                    else:
                        self.game.next_player+=1
                    self.window.pack()
                    self.update_players_turn()
        
    def return_home(self):
        """
        Clears the graphical representation of the Connect 4 grid and hides the features
        till it is needed again. Returns the user to the main screen/frame.
        Returns
        -------
        None.

        """
        if self.next_player>0:
            self.next_player = 0
        else:
            self.next_player = 1
        self.win_label.grid_forget()
        self.return_home_button.grid_forget()
        self.window.destroy()   #Needed to hide the grid
        self.start_game.grid(row=0,column=0)
        self.controller.show_frame(StartMenu)

# Maintains the running of the program, providing the current interface for users
if __name__ =="__main__":
    window = GUIController()
    window.mainloop()