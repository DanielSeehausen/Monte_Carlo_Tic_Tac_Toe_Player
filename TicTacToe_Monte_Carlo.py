"""
Monte Carlo Tic-Tac-Toe Player
Beware: I did not have the ability to use most modules while writing this.
Twice, lists are copied via non-ideal methods.
Highly recommend importing itertools and changing if this is to be used, 
ESPECIALLY if structure is used to work on an unfixed/dynamic grid size
Finally, this uses a board class and several methods that are not included.
As it was originally written without the classes/methods not included
(but used) here, any implementation will need to add these missing methods
however you see fit. 
"""



import random
import poc_ttt_gui 
import poc_ttt_provided as provided

NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

#simple creators useful for debugging
BLANK_GRID = []
for _ in range(0, 3):
    temp = []
    for _ in range(0, 3):
        temp.append(0)
    BLANK_GRID.append(temp)
    
BLANK_SCORE = []
for _ in range(0, 3):
    temp = []
    for _ in range(0, 3):
        temp.append(0)
    BLANK_SCORE.append(temp)

def unshared_copy(in_list):
    '''recursive function to copy list of lists'''
    if isinstance(in_list, list):
        return list( map(unshared_copy, in_list) )
    return in_list

def get_empty_spot(board):
    '''returns a random empty spot on the board'''
    empty_spaces = board.get_empty_squares()
    if not empty_spaces:
        return None
    return random.choice(empty_spaces)

def get_all_empty_spots(board):
    '''returns any and all spots on the board that have a 0,
    which indicates no marker'''
    empty_spaces = []
    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == 0:
                empty_spaces.append((row, col))
    if not empty_spaces:
        return None
    return empty_spaces
    
def print_board(board):
    '''Simple print function to visualize the 3x3 grid in the console'''
    for row in range(0, 3):
        for col in range(0, 3):
            print board[row][col],
        print
    
def mc_trial(board, player):
    '''This function takes a current board and the next player to move. 
    The function plays a game starting with the given player by making 
    random moves, alternating between players. The returns when the game is over. 
    The modified board will contain the state of the game, 
    so the function does not return anything.'''
        
    while board.check_win() == None:
        play_spot = get_empty_spot(board)
        board.move(play_spot[0], play_spot[1], player)	
        player = provided.switch_player(player)
        
        
def mc_update_scores(scores, board, player):
    ''' This function takes a grid of scores (a list of lists) with 
    the same dimensions as the Tic-Tac-Toe board, a board from a completed 
    game, and which player the machine player is. The function scores the completed 
    board and updates the scores grid. As the function updates the scores grid directly, 
    it does not return anything'''
    
    comp_marker = player
    human_marker = provided.switch_player(player)
    print 
    if board.check_win() == comp_marker:
        for row in range(0, board.get_dim()):
            for col in range(0, board.get_dim()):
                if board.square(row, col) == comp_marker:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == human_marker:
                    scores[row][col] -= SCORE_OTHER      
    elif board.check_win() == human_marker:            
        for row in range(0, board.get_dim()):
            for col in range(0, board.get_dim()):
                if board.square(row, col) == human_marker:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == comp_marker:
                    scores[row][col] -= SCORE_OTHER

                    


def get_best_move(board, scores):
    '''This function takes a current board and a grid of scores. 
    The function finds all of the empty squares with the maximum 
    score and randomly returns one of them as a (row, column) tuple. 
    It is an error to call this function with a board that has no empty 
    squares (there is no possible next move). Currently, it does not handle
    this error as invalid boards will not be used to call the function.'''
    empty_spots = board.get_empty_squares()
    if not empty_spots:
        return
    best_spots = []
    best_spots.append((empty_spots[0]))
    best_found = scores[best_spots[0][0]][best_spots[0][1]]
    for spot in empty_spots[1:]:
        if scores[spot[0]][spot[1]] > best_found:
            best_spots = [(spot[0], spot[1])]
            best_found = scores[spot[0]][spot[1]]
        elif scores[spot[0]][spot[1]] == best_found:
            best_spots.append((spot[0], spot[1]))
    
    print "Highest value found:", best_found
    return random.choice(best_spots)
            
def mc_move(board, player, trials):
    '''This function takes a current board, which player the machine player 
    is, and the number of trials to run. The function returns a move for the machine player 
    in the form of a (row, column) tuple.'''
    score_board = []
    for dummy_1 in range(0, board.get_dim()):
        temp_2 = []
        for dummy_3 in range(0, board.get_dim()):
            temp_2.append(0)
        score_board.append(temp_2)

    for dummy_2 in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(score_board, trial_board, player)

    return get_best_move(board, score_board)
