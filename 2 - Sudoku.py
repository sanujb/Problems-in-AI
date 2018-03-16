import copy

puzzles = ['001', '002', '010', '015', '025', '026', '048', '051', '062', '076', '081', '082', '090', '095', '099', '100']
num_guesses = 0

def read_puzzles():
    sudoku = {}
    for puzzle in puzzles:
        with open('./Puzzles/puz-'+puzzle+'.txt') as puz_file:
            sudoku[puzzle] = []
            for row in puz_file:
                sudoku[puzzle].append([int(x) if x.isdigit() else None for x in row.split()])

    return sudoku

def next_unassigned_variable(sudoku):
    r, c = 0, 0
    while r < 9:
        c = 0
        while c < 9:
            if sudoku[r][c] is None:
                return (r, c)
            c+=1
        r+=1

    return None

def legal_assignment(sudoku, val, var):
    r, c = var[0], var[1]
    for col in range(0,9):
        if sudoku[r][col] == val:
            return False
    for row in range(0,9):
        if sudoku[row][c] == val:
            return False
    sq_r, sq_c = 3*(r//3), 3*(c//3)
    for col in range(sq_c, sq_c+3):
        for row in range(sq_r, sq_r+3):
            if sudoku[row][col] == val:
                return False
    return True

def recursive_backtracking(sudoku):
    global num_guesses
    var = next_unassigned_variable(sudoku)
    if var is None:
        return True
    num_guesses += 8
    for val in range(1,10):
        if legal_assignment(sudoku, val, var):
            sudoku[var[0]][var[1]] = val
            if recursive_backtracking(sudoku):
                return True
            sudoku[var[0]][var[1]] = None
    return False

def get_domain(sudoku):
    domain = []
    for r in range(9):
        domain.append([])
        for c in range(9):
            domain[r].append([])
            if sudoku[r][c] is not None:
                continue
            for v in range(1,10):
                if legal_assignment(sudoku, v, (r, c)):
                    domain[r][c].append(v)
    return domain

def update_domain_CP(val, puzzle_domain, var, type, changes=None):
    if type == 'remove':
        changes=[]
        for c in range(9):
            if c != var[1] and  val in puzzle_domain[var[0]][c]:
                puzzle_domain[var[0]][c].remove(val)
                changes.append((var[0],c))
        for r in range(9):
            if r != var[0] and val in puzzle_domain[r][var[1]]:
                puzzle_domain[r][var[1]].remove(val)
                changes.append((r,var[1]))
        sq_r, sq_c = 3*(var[0]//3), 3*(var[1]//3)
        for r in range(sq_r, sq_r+3):
            for c in range(sq_c, sq_c+3):
                if (r,c) != var and val in puzzle_domain[r][c]:
                    puzzle_domain[r][c].remove(val)
                    changes.append((r,c))
        return changes

    if type == 'add':
        for pos in changes:
            puzzle_domain[pos[0]][pos[1]].append(val)

def MRV_variable(sudoku, puzzle_domain):
    var = None
    for r in range(9):
        for c in range(9):
            if sudoku[r][c] is None:
                if var is None:
                    var = (r,c)
                if len(puzzle_domain[r][c]) > 0 and len(puzzle_domain[r][c]) < len(puzzle_domain[var[0]][var[1]]):
                    var = (r,c)
                    if len(puzzle_domain[r][c]) == 1:
                        return var
    return var

def MRV_with_CP(sudoku, puzzle_domain):
    global num_guesses
    var = MRV_variable(sudoku, puzzle_domain)
    if var is None:
        return True
    # if len(puzzle_domain[var[0]][var[1]]) > 0:
    # num_guesses += len(puzzle_domain[var[0]][var[1]]) - 1
    num_guesses+=8 # Doing this because it is a requirement.
    for val in puzzle_domain[var[0]][var[1]]:
        sudoku[var[0]][var[1]] = val
        changes = update_domain_CP(val, puzzle_domain, var, 'remove')
        if MRV_with_CP(sudoku, puzzle_domain):
            return True
        sudoku[var[0]][var[1]] = None
        update_domain_CP(val, puzzle_domain, var, 'add', changes)
    return False

def ac3_revise(revised_d, x_i, x_j):
    revised = False
    d_i = revised_d[x_i[0]][x_i[1]]
    d_j = revised_d[x_j[0]][x_j[1]]
    i = 0
    while i < len(d_i):
        satisfied = False
        for d_j_val in d_j:
            if d_i[i] != d_j_val:
                satisfied = True
                break
        if not satisfied:
            del d_i[i]
            revised = True
            continue
        i+=1

    return revised

def ac3(sudoku, puzzle_domain):
    revised_domain = copy.deepcopy(puzzle_domain)
    arcs_queue = []
    unassigned_variables = []
    for r in range(9):
        for c in range(9):
            if sudoku[r][c] is None:
                unassigned_variables.append((r,c))
    for var1 in unassigned_variables:
        sq_r, sq_c = 3*(var1[0]//3),3*(var1[1]//3)
        for var2 in unassigned_variables:
            if (var1[0] == var2[0] or var1[1] == var2[1]) and var1 != var2:
                arcs_queue.append((var1,var2))
            elif (sq_r < var2[0] < sq_r+3) and (sq_c < var2[1] < sq_c) and var2 != var1:
                arcs_queue.append((var1,var2))

    while arcs_queue:
        arc = arcs_queue.pop()
        x_i, x_j = arc[0], arc[1]
        sq_r, sq_c = 3*(x_i[0]//3), 3*(x_i[1]//3)
        x = copy.copy(revised_domain)
        if ac3_revise(revised_domain, x_i, x_j):
            if len(revised_domain[x_i[0]][x_i[1]]) == 0:
                return False
            for potential_neighbour in unassigned_variables:
                if ((potential_neighbour[0] == x_i[0] or potential_neighbour[1] == x_i[1]) and
                        potential_neighbour != x_i and potential_neighbour != x_j and
                        (potential_neighbour,x_i) not in arcs_queue):
                    arcs_queue.append((potential_neighbour, x_i))
                    continue

                if ((sq_r <= potential_neighbour[0] < sq_r+3) and (sq_c <= potential_neighbour[1] < sq_c+3) and
                        potential_neighbour != x_i and potential_neighbour != x_j and
                        (potential_neighbour, x_i) not in arcs_queue):
                    arcs_queue.append((potential_neighbour, x_i))
                    continue
    return revised_domain

def np(sudoku, puzzle_domain):
    for r in range(9):
        for c in range(9):
            if (sudoku[r][c] is None) and len(puzzle_domain[r][c]) == 2:
                for row in range(9):
                    if row != r and (sudoku[row][c] is None) and sorted(puzzle_domain[row][c]) == sorted(puzzle_domain[r][c]):
                        for i in range(9):
                            if i != row and i != r and puzzle_domain[r][c][0] in puzzle_domain[i][c]:
                                puzzle_domain[i][c].remove(puzzle_domain[r][c][0])
                            if i != row and i != r and puzzle_domain[r][c][1] in puzzle_domain[i][c]:
                                puzzle_domain[i][c].remove(puzzle_domain[r][c][1])
                        break

                for col in range(9):
                    if col != c and (sudoku[r][col] is None) and sorted(puzzle_domain[r][col]) == sorted(puzzle_domain[r][c]):
                        for i in range(9):
                            if i != col and i != c and puzzle_domain[r][c][0] in puzzle_domain[r][i]:
                                puzzle_domain[r][i].remove(puzzle_domain[r][c][0])
                            if i != col and i != c and puzzle_domain[r][c][1] in puzzle_domain[r][i]:
                                puzzle_domain[r][i].remove(puzzle_domain[r][c][1])
                        break

                sq_r, sq_c = 3*(r//3), 3*(c//3)
                for row in range(sq_r,sq_r+3):
                    for col in range(sq_c,sq_c+3):
                        if (row,col) != (r,c) and (sudoku[row][col] is None) and sorted(puzzle_domain[row][col]) == sorted(puzzle_domain[r][c]):
                            for i in range(sq_r,sq_r+3):
                                for j in range(sq_c,sq_c+3):
                                    if (i,j) != (r,c) and (i,j) != (row,col) and puzzle_domain[r][c][0] in puzzle_domain[i][j]:
                                        puzzle_domain[i][j].remove(puzzle_domain[r][c][0])
                                    if (i,j) != (r,c) and (i,j) != (row,col) and puzzle_domain[r][c][1] in puzzle_domain[i][j]:
                                        puzzle_domain[i][j].remove(puzzle_domain[r][c][1])

def sudoku_inference(sudoku, puzzle_domain, type):
    if type == 'ac3':
        return ac3(sudoku, puzzle_domain)

    if type == 'np':
        np(sudoku, puzzle_domain)

def recursive_backtracking_waterfall(sudoku, puzzle_domain):
    global num_guesses
    var = MRV_variable(sudoku, puzzle_domain)
    if var is None:
        return True

    if len(puzzle_domain[var[0]][var[1]]) > 0:
        num_guesses += len(puzzle_domain[var[0]][var[1]]) - 1
    for val in puzzle_domain[var[0]][var[1]]:
        sudoku[var[0]][var[1]] = val
        changes_CP = update_domain_CP(val, puzzle_domain, var, 'remove')
        inference = sudoku_inference(sudoku, puzzle_domain, 'ac3')
        if inference != False:
            sudoku_inference(sudoku, inference, 'np')   # Comment out this line to only run AC3
            if recursive_backtracking_waterfall(sudoku, inference):
                return True
        sudoku[var[0]][var[1]] = None
        update_domain_CP(val, puzzle_domain, var, 'add', changes_CP)
    return False

def solve_sudoku(method, sudoku):
    if method == 1:
        recursive_backtracking(sudoku)

    elif method == 2:
        puzzle_domain = get_domain(sudoku)
        MRV_with_CP(sudoku, puzzle_domain)

    elif method == 3:
        puzzle_domain = get_domain(sudoku)
        recursive_backtracking_waterfall(sudoku, puzzle_domain)

sudoku = read_puzzles()
method = 3          ## Change this method in {1,2,3} to see different outputs - explained in readme
print('Guesses for method:', method)
for puzzle in puzzles:
    num_guesses=0
    solve_sudoku(method, sudoku[puzzle])
    print('Puzzle:', puzzle, ', Guesses:',num_guesses)

def get_domains_count(sudoku, d):
    count_domain = 0
    for r in range(9):
        for c in range(9):
            if sudoku[r][c] == None:
                count_domain += len(d[r][c])
    return count_domain

def get_unassigned_count(sudoku):
    count = 0
    for r in range(9):
        for c in range(9):
            if sudoku[r][c] == None:
                count += 1
    return count

def determine_difficulty():
    sudoku = read_puzzles()
    print('\nPuzzle Stats')
    weights = [0.15, 0.4, 0.25, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05]
    for puzzle in puzzles:
        puz_stats = []

        before = 9*get_unassigned_count(sudoku[puzzle])
        d = get_domain(sudoku[puzzle])
        after = get_domains_count(sudoku[puzzle], d)
        puz_stats.append((before-after)/float(before))

        for i in range(4):
            before = after
            d = ac3(sudoku[puzzle], d)
            after = get_domains_count(sudoku[puzzle], d)
            puz_stats.append((before-after)/float(before))

            before = after
            np(sudoku[puzzle], d)
            after = get_domains_count(sudoku[puzzle], d)
            puz_stats.append((before-after)/float(before))

        final_val = sum([puz_stats[x]*weights[x] for x in range(9)])/sum(weights)
        difficulty = ''
        if final_val >= 0.2:
            difficulty = 'Easy'
        elif 0.08 <= final_val < 0.2:
            difficulty = 'Moderate'
        elif 0.07 <= final_val < 0.08:
            difficulty = 'Demanding'
        elif final_val < 0.07:
            difficulty = 'Very Hard'
        print(puzzle,':',difficulty, ', V =', final_val)

determine_difficulty()