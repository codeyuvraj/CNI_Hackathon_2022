# CNI_Hackathon_2022

## Task
Conquer more number of cells than your opponent bot.  
### Rules.  
1. If a cell is unoccupied then it is conquered by the bot who reaches there first.  
2. If a bot conquers and makes a complete rectangle(maximum 6*6), and no cell inside being conquered by the opponent bot, then all the cells inside      will also get conquered.  
3. Representation. 
        1. B[i][j] = 0 means the cell is unconquered
        2. B[i][j] = 1 means the cell is conquered by Player 1
        3. B[i][j] = 2 means the cell is conquered by Player 2
    
    ```
    def move(self,B,N,cur_x,cur_y):
    B: the board (list of lists of 30 element each). It represents
    the current state of the board.
    N: the size of the N x N board (N=30 by default)
    cur_x: current x location of your bot
    cur_y: current y location of your bot
    ```

# Guide

1. Fork this repository. It has two files.
    1. game.py - This is the code for the game which was provided by the Hackathon organising team. Don’t make any changes in this code.
    2. Player1.py - This is the code of the bot which I submitted for the contest.
    3. Player2.py - This is your bot. You need to complete the move function. Delete the demo code inside the move function and complete it with the code of your bot.
2. Install the pygame package to run the game.py file. 
3. Run the game.py file to pit your bot against mine.
4. Task - Conquer more number of cells than your opponent bot.
    
    

Tips - Comment out line 84 in game.py (sleep(0.1)) to speed up the computation.

Check out this official hackathon link to get more clarification. https://www.cnihackathon.in/AIchallenge.html

Happy Coding!!!
