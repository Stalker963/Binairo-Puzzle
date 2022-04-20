from copy import deepcopy
from collections import deque
import State
        

def check_Adjancy_Limit(state: State):

    #check rows
    for i in range(0,state.size):
        for j in range(0,state.size-2):
            if(state.board[i][j].value.upper()==state.board[i][j+1].value.upper() and 
            state.board[i][j+1].value.upper()==state.board[i][j+2].value.upper() and
            state.board[i][j].value !='_'and 
            state.board[i][j+1].value !='_'and
            state.board[i][j+2].value !='_' ):
                
                return False
    #check cols
    for j in range(0,state.size): # cols
        for i in range(0,state.size-2): # rows
            if(state.board[i][j].value.upper()==state.board[i+1][j].value.upper() 
            and state.board[i+1][j].value.upper()==state.board[i+2][j].value.upper() 
            and state.board[i][j].value !='_'
            and state.board[i+1][j].value !='_'
            and state.board[i+2][j].value !='_' ):
               
                return False
    
    return True

def check_circles_limit(state:State): # returns false if number of white or black circles exceeds board_size/2
    #check in rows
    for i in range(0,state.size): # rows
        no_white_row=0
        no_black_row=0
        for j in range(0,state.size): # each col
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper()=='W' and state.board[i][j].value != '_'): no_white_row+=1
            if (state.board[i][j].value.upper()=='B' and state.board[i][j].value != '_'): no_black_row+=1
        if no_white_row > state.size/2 or no_black_row > state.size/2:
            
            return False
        no_black_row=0
        no_white_row=0

    # check in cols
    for j in range(0,state.size):#cols
        no_white_col=0
        no_black_col=0
        for i in range(0,state.size): # each row
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper()=='W' and state.board[i][j].value != '_'): no_white_col+=1
            if (state.board[i][j].value.upper()=='B' and state.board[i][j].value != '_'): no_black_col+=1
        if no_white_col > state.size/2 or no_black_col > state.size/2:
            
            return False
        no_black_col=0
        no_white_col=0
    
    return True

def is_unique(state:State): # checks if all rows are unique && checks if all cols are unique
    # check rows
    for i in range(0,state.size-1):
        for j in range(i+1,state.size):
            count = 0
            for k in range(0,state.size):
                if(state.board[i][k].value.upper()==state.board[j][k].value.upper()
                and state.board[i][k].value!='_'
                and state.board[j][k].value!='_'):
                    count+=1
            if count==state.size:
                
                return False
            count=0

    # check cols
    for j in range(0,state.size-1):
        for k in range(j+1,state.size):
            count_col =0 
            for i in range(0,state.size):
                 if(state.board[i][j].value.upper()==state.board[i][k].value.upper()
                 and state.board[i][j].value != '_'
                 and state.board[i][k].value != '_' ):
                    count_col+=1
            if count_col == state.size:
               
                return False
            count_col=0 
   
    return True

def is_assignment_complete(state:State): # check if all variables are assigned or not
    for i in range(0,state.size):
        for j in range(0,state.size):
            if(state.board[i][j].value == '_'): # exists a variable wich is not assigned (empty '_')
                
                return False

    
    return True

def is_consistent(state:State):
    
    return check_Adjancy_Limit(state) and check_circles_limit(state) and is_unique(state)

def check_termination(state:State):
    
    return is_consistent(state) and is_assignment_complete(state)

def simple_backtrack(state):
    if is_assignment_complete(state): return state
    unassigned = []
    for i in range(0,state.size):
        for j in range(0,state.size):
            if(state.board[i][j].value == '_'):
                unassigned.append(state.board[i][j])
    first = unassigned[0]
    for d in first.domain:
        local_state = deepcopy(state)
        local_state.board[first.x][first.y].value = d
        if is_consistent(local_state):
            result = simple_backtrack(local_state)
            if result is not None:
                return result
    return None

def modified_backtrack(state):
    if is_assignment_complete(state): return state
    variable = None
    #MRV
    #first look for single domain vars
    for i in range(state.size):
        for j in range(state.size):
            cell = state.board[i][j]
            if(cell.value == '_'):
                if(cell.domain == ['w'] or cell.domain == ['b']):
                    variable = deepcopy(cell)
                    break
        else:
            continue
        break
    #if we didnt find single domain var, choose first unassigned
    if variable is None:
        for i in range(state.size):
            for j in range(state.size):
                cell = state.board[i][j]
                if(cell.value == '_'):
                    variable = deepcopy(cell)
                    break
            else:
                continue
            break
    #LCV
    #if its single domained, we cant do anything different
    if variable.domain == ['b'] or variable.domain == ['w']:
        d = variable.domain[0]
        local_state = deepcopy(state)
        local_state.board[variable.x][variable.y].value = d
        new_state = forward_checking(local_state,variable)
        if (is_consistent(new_state)):
            result = modified_backtrack(new_state)
            if result is not None:
                return result
        
    
    #if its double domained, check corresponding row and column, if it has more whites than blacks,reverse the domain
    row = variable.x
    column = variable.y
    white_colored = 0
    black_colored = 0
    for c in range(state.size):
        cell = state.board[row][c]
        if cell.value == 'w' or cell.value == 'W':
            white_colored += 1
        elif cell.value == 'b' or cell.value == 'B':
            black_colored += 1
    for r in range(state.size):
        cell = state.board[r][column]
        if cell.value == 'w' or cell.value == 'W':
            white_colored += 1
        elif cell.value == 'b' or cell.value == 'B':
            black_colored += 1
    if white_colored > black_colored:
        variable.domain.reverse()
    for d in variable.domain:
        local_state = deepcopy(state)
        local_state.board[variable.x][variable.y].value = d
        new_state = forward_checking(local_state,variable)
        if (is_consistent(new_state)):
            result = modified_backtrack(new_state)
            if result is not None:
                return result
    return None

def forward_checking(state, variable):
    local_state = deepcopy(state)
    row = variable.x
    column = variable.y

    # if we have half of same color, other half must be other color

    #go column-wise
    white_colored = 0
    black_colored = 0
    for c in range(0,local_state.size):
        color = local_state.board[row][c].value
        if color == 'w' or 'W':
            white_colored += 1
        elif color == 'b' or 'B':
            black_colored += 1
    if white_colored == local_state.size / 2:
        for c in range(0,local_state.size):
            cell = local_state.board[row][c]
            if cell.value == '_':
                cell.value = 'b'
    elif black_colored == local_state.size /2:
        for c in range(0,local_state.size):
            cell = local_state.board[row][c]
            if cell.value == '_' :
               cell.value = 'w'

    #go row-wise
    white_colored = 0
    black_colored = 0
    for r in range(0,local_state.size):
        color = local_state.board[r][column].value
        if color == 'w' or 'W':
            white_colored += 1
        elif color == 'b' or 'B':
            black_colored += 1
    if white_colored == local_state.size / 2:
        for r in range(0,local_state.size):
            cell = local_state.board[r][column]
            if cell.value == '_':
               cell.value = 'b'
    elif black_colored == local_state.size /2:
        for r in range(0,local_state.size):
            cell = local_state.board[r][column]
            if cell.value == '_':
                cell.value = 'w'

    # if we have two neighbours of same color, surronding variables must be of the other color

    # go column-wise
    current_cell = 'n'
    next_cell = 'n'
    for c in range(0,local_state.size):
        color = local_state.board[row][c].value
        current_cell = next_cell
        next_cell = color
        
        if (current_cell.lower() == next_cell.lower()):
            if (current_cell == 'w' or current_cell =='W'):
                try:
                    cell = local_state.board[row][c-2]
                    if cell.value == '_':
                        cell.value = 'b'
                except:
                    pass
                try:
                    cell = local_state.board[row][c+1]
                    if cell.value == '_':
                       cell.value = 'b'
                except:
                    pass
            elif (current_cell == 'b' or current_cell == 'B'):
                try:
                    cell = local_state.board[row][c-2]
                    if cell.value == '_':
                       cell.value = 'w'
                except:
                    pass
                try:
                    cell = local_state.board[row][c+1]
                    if cell.value == '_':
                        cell.value = 'w'
                except:
                    pass
        

    # go row_wise
    current_cell = 'n'
    next_cell = 'n'
    for r in range(0,local_state.size):
        color = local_state.board[r][column].value
        current_cell = next_cell
        next_cell = color
        if (current_cell.lower() == next_cell.lower()):
            if (current_cell == 'w' or current_cell == 'W'):
                try:
                    cell = local_state.board[r-2][column]
                    if cell.value == '_':
                        cell.value = 'b'
                except:
                    pass
                try:
                    cell = local_state.board[r+1][column]
                    if cell.value == '_':
                        cell.value = 'b'
                except:
                    pass
            elif (current_cell == 'b' or current_cell == 'B'):
                try:
                    cell = local_state.board[r-2][column]
                    if cell.value == '_':
                        cell.value = 'w'
                except:
                    pass
                try:
                    cell = local_state.board[r+1][column]
                    if cell.value == '_':
                       cell.value = 'w'
                except:
                    pass
    return local_state

def check_domain_is_empty(state):
    for i in range(state.size):
        for j in range(state.size):
            if not state.board[i][j].domain:
                return True
    return False

def AC3(state): #does not do anything useful for this problem!
    local_state = deepcopy(state)
    q = deque()

    #initialize the queue
    for i in range(state.size):
        for j in range(state.size):
            cell = local_state.board[i][j]
            if cell.value == '_':
                for c in range(state.size):
                    if c != j:
                        q.append((cell,local_state.board[i][c]))
                for r in range(state.size):
                    if r != i:
                        q.append((cell,local_state.board[r][j]))
    while q:
        arc = q.popleft()
        first_cell = arc[0]
        second_cell = arc[1]
        if first_cell.value == '_':
            for d in first_cell.domain:
                new_state = deepcopy(state)
                new_state.board[first_cell.x][first_cell.y].value = d
                not_consistent_with_all = True
                if second_cell.value == '_':
                    for d2 in second_cell.domain:
                        new_state.board[second_cell.x][second_cell.y].value = d2
                        if is_consistent(new_state):
                            not_consistent_with_all = False
                            break
                else:
                    if is_consistent(new_state):
                            not_consistent_with_all = False
                if not_consistent_with_all:
                    if len(first_cell.domain) == 1: #domain will get empty and return failure
                        return False
                    first_cell.domain.remove(d)
                    first_cell.value = first_cell.domain[0]
                    #add to queue every relating cell to first cell
                    for c in range(state.size):
                        if c != first_cell.y:
                            q.append((local_state.board[first_cell.x][c],first_cell))
                    for r in range(state.size):
                        if r != first_cell.x:
                            q.append((local_state.board[r][first_cell.y],first_cell))
        return local_state


        


