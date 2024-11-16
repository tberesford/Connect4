# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np  
import math
import copy
import random

import torch

import neural_net_trainer as neural_net
    
class Player:    
    def __init__(self,value, opp_value,algorithm_value,depth,colour):
        self.player_number = value
        self.opponent_number = opp_value
        self.player_algorithm = algorithm_value
        self.player_colour = colour
        self.is_alpha_beta = False
        self.player_score = 0
        self.player_moves = 0
        self.depth = depth
        self.cnn = neural_net.ConvNet()
    
    def get_player_score(self):
        """
        Gets the player's score.

        Returns
        -------
        int
            The score of the player.
        """
        return self.player_score
    
    def get_player_moves(self):
        """
        Gets the number of moves the player made.

        Returns
        -------
        int
            The number of moves made by player.
        """
        return self.player_moves
    
    def get_player_number(self):
        """
        Returns the value associated to the player (1 or 2)

        Returns
        -------
        int
            The value associated to the player.
        """
        return self.player_number
    
    def get_player_algorithm(self):
        #########
        return self.player_algorithm
    
    def get_row(self,x,grid):
        """
        Returns the row the piece should be placed at
        Parameters
        ----------
        x : int
            Column that is being looked at.
        grid : list
            Current state of the game.

        Returns
        -------
        y : int
            The height at which the disc should be played to.
        """
        for y in range(6):
            if grid[y][x]!=0 and y!=0:
                return y-1
        return y
            
    def get_possible_columns(self,grid):
        """
        Gets the columns that are playable.
        
        Parameters
        ----------
        grid : LIST
            Current state of the game.

        Returns
        -------
        possible_columns : LIST
            A list of the columns that can legally be played to.
        """
        possible_columns = []   #I have hard coded this as sources suggest that the viewing order of possible positions
        if grid[0][3]==0:       #can affect the performance of Alpha-Beta.
            possible_columns.append(3)
        if grid[0][2]==0:
            possible_columns.append(2)
        if grid[0][4]==0:
            possible_columns.append(4)
        if grid[0][1]==0:
            possible_columns.append(1)
        if grid[0][5]==0:
            possible_columns.append(5)
        if grid[0][0]==0:
            possible_columns.append(0)
        if grid[0][6]==0:
            possible_columns.append(6)
        return possible_columns
    
    def use_player_algorithm(self,grid):
        """
        Acquires the algorithm that the player is supposed to use.
        
        Parameters
        ----------
        grid : list
            Current state of the game.

        Returns
        -------
        None.
        """
        if self.player_algorithm=='Random':
            return(self.__random(grid))
        elif self.player_algorithm=='Minimax':
            return(self.__minimax_move(grid,False))
        elif self.player_algorithm=='Minimax with A-B Pruning':
            return(self.__minimax_move(grid,True))
        elif self.player_algorithm=='Artificial Neural Network':
           return self.__convolutional_neural_net(grid)
    
    def __random(self,grid):
        """
        Function that performs the random algorithm.

        Parameters
        ----------
        grid : list
            Current state of the game.

        Returns
        -------
        y : int
            Height at which the disc should be played to.
        x : int
            Randomly selected column.
        """
        x = random.randint(0,6)
        y = self.get_row(x,grid)
        return y,x
    
    def __minimax_move(self,grid,is_alpha_beta):
        """
        Initiates the Minimax algorithm and obtains the optimal move from the algorithm.

        Parameters
        ----------
        grid : list
            Current state of the game.
        is_alpha_beta : bool
            Boolean value to determine if alpha-beta pruning is included in the algorithm.

        Returns
        -------
        y : int
            Height at which the disc should be played to.
        x : int
            Column at which the disc should be played to.
        """
        self.is_alpha_beta = is_alpha_beta
        x,score = self.__minimax(self.depth, -math.inf, math.inf, grid, True)
        y = self.get_row(x,grid)
        return y,x
    
    def __minimax(self,depth,alpha,beta,grid,is_maximiser): 
        """
        Function that performs the Minimax algorithm, as well as having alpha-beta pruning.

        Parameters
        ----------
        depth : int
            Depth that the algorithm should explore the game tree to.
        alpha : int
            Initial value of alpha for alpha-beta pruning.
        beta : int
            Initial value of beta for alpha-beta pruning.
        grid : int
            Current state of the game.
        is_maximiser : BOOLEAN
            Boolean value to tell the algorithm to maximise or minimise.

        Returns
        -------
        optimal_move : int
            The optimal column that should be played to.
        value : int
            The value associated to the move.
        """
        if is_victory(grid,self.player_number):
            return 0, math.inf
        elif is_victory(grid,self.opponent_number):
            return 0, -math.inf
        elif is_grid_full(grid):
            return 0, 0
        elif depth==0:
            if self.depth==8:
                return 0, 0
            else:
                return 0,self.__grid_evaluation(grid)
        
        columns = self.get_possible_columns(grid)
        best_move = columns[0]
        
        if is_maximiser:
            max_score = -math.inf
            for x in columns:
                y = self.get_row(x,grid)
                copied_grid = copy.deepcopy(grid) 
                copied_grid[y][x] = self.player_number
                move,score = self.__minimax(depth-1, alpha, beta, copied_grid, False)
                if score>max_score:
                    best_move = x
                    max_score = score
                if self.is_alpha_beta:
                    alpha = max(alpha,max_score)
                    if alpha>=beta:
                        break
            return best_move, max_score
        else:
            min_score = math.inf
            for x in columns:
                y = self.get_row(x,grid)
                copied_grid = copy.deepcopy(grid)
                copied_grid[y][x] = self.opponent_number
                move,score = self.__minimax(depth-1, alpha, beta, copied_grid, True)
                if score<min_score:
                    best_move = x
                    min_score = score
                if self.is_alpha_beta:
                    beta = min(beta,min_score)
                    if beta<=alpha:
                        break
            return best_move, min_score

    def __user(self):
        """
        Function to enable user gameplay.

        Returns
        -------
        x : int
            Column that the player wants to play to.
        Y : int
            Row that the player wants to play to.
        """
        x = input ('Enter x:')
        y = input ('Enter y:')
        return int(y),int(x)

    def __grid_evaluation(self,grid):
        """
        Heuristic function of Minimax to evaluate the current game state.

        Parameters
        ----------
        grid : list
            The current game state.

        Returns
        -------
        score : int
            The overall score associated to the game state.
        """

        score = 0
        #Centre column is worth extra value, as allows wins in both directions
        score += np.count_nonzero(grid[:,3]==self.player_number) * 2
        for x in range(3,7):
            for y in range(3):
                items = [grid[y][x],grid[y+1][x-1],grid[y+2][x-2],grid[y+3][x-3]]
                score += self.__score_evaluation(items)
        for x in range(3,7):
           for y in range(3,6):
               items = [grid[y][x],grid[y-1][x-1],grid[y-2][x-2],grid[y-3][x-3]]
               score += self.__score_evaluation(items)
               
        for y in range(6):
            row = grid[y]      #Obtains row of Connect4 to perform checks for across
            for x in range(3):
                items = row[x:x+4] #Separates row into 4, and performs the counts below
                score += self.__score_evaluation(items)
                
        for x in range(7):
            column = grid[:,x] #Obtains column of Connect4 to perform checks for upward/downward
            for y in range(3):
                items = column[y:y+4]
                score += self.__score_evaluation(items)
        return score
    
    def __score_evaluation(self,items):
        """
        Scores the discs that are connected based upon how many there are of the same type.

        Parameters
        ----------
        items : int
            A list of 4, connecting values from the grid.

        Returns
        -------
        score : int
            The score determined from list items.
        """
        score = 0    
        # I believe this works better than: += 25, +=15, -=30, -=10
        if np.count_nonzero(items==self.player_number)==3 and np.count_nonzero(items==0)==1:
            score += 5
        elif np.count_nonzero(items==self.player_number)==2 and np.count_nonzero(items==0)==2:
            score += 3

        if np.count_nonzero(items==self.opponent_number)==3 and np.count_nonzero(items==0)==1:
           score -= 4
        elif np.count_nonzero(items==self.opponent_number)==2 and np.count_nonzero(items==0)==2:
            score -= 2
        return score

    def __convolutional_neural_net(self,grid):
        device = 'cpu'
        cnn_state_dict = torch.load('cnnmodel.pt')
        self.cnn.load_state_dict(cnn_state_dict) 
        data = torch.tensor(grid).float().flatten()
        data = data.view(1,1,6,7)
        data.to(device)
        output = self.cnn(data)
        output = output.detach().numpy()[0]
        
        max_val = -math.inf
        for x in range(len(output)):
            y = self.get_row(x,grid)
            if grid[y][x]==0 and output[x]>max_val:
                column = x
                max_val = output[x]
        y = self.get_row(column,grid)
        return y,column

def is_victory(grid,val):
    """
    Checks the game for winning states.

    Parameters
    ----------
    grid : list
        Current state of the game.
    val : int
        The value that represents the players.

    Returns
    -------
    bool
        Returns True if there is a winning state.
    """
    for y in range(6):
        row = grid[y]
        for x in range(4):
            items = row[x:x+4]
            if np.count_nonzero(items==val)==4:
                return True
    for x in range(7):
        column = grid[:,x]
        for y in range(3):
            items = column[y:y+4]
            if np.count_nonzero(items==val)==4:
                return True
    for x in range(3,7):
        for y in range(3):
            if grid[y][x]==val and grid[y+1][x-1]==val and grid[y+2][x-2]==val and grid[y+3][x-3]==val:
                return True
    for x in range(3,7):
       for y in range(3,6):
           if grid[y][x]==val and grid[y-1][x-1]==val and grid[y-2][x-2]==val and grid[y-3][x-3]==val:
               return True
   
def is_grid_full(grid):
    """
    Determines if the grid is full (resulting in a draw)

    Parameters
    ----------
    grid : list
        Current state of the game.

    Returns
    -------
    bool
        Returns False if the game is full.
    """
    for x in range(7):
        if grid[0][x]==0:
            return False
    return True            