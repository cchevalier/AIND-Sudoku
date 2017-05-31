assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]


# Setting and Encoding the board
#
# box  : Individual cell at the intersection of rows and columns
# unit : A complete row, column, or 3x3 squares (27 in total)
# peers: for a particular box , its peers will be all other boxes that belong to a common unit
#        (namely, those that belong to the same row, column, or 3x3 square)

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
# Top most row: row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']

column_units = [cross(rows, c) for c in cols]
# Left most column: column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']

square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# Top left square: square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

all_units = row_units + column_units + square_units


# Diagonal Sudoku
# A diagonal sudoku is like a regular sudoku, except that among the two main 
# diagonals, the numbers 1 to 9 should all appear exactly once.
diag_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], 
              ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]

all_units = row_units + column_units + square_units + diag_units


units = dict((b, [u for u in all_units if b in u]) for b in boxes)
# units for a given box in a dictionary form
# units['A1']

peers = dict((b, set(sum(units[b],[])) - set([b])) for b in boxes)
# peers for a given box in a dictionary form
# peers['A1']


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    all_digits = '123456789'

    values = dict(zip(boxes, grid))
    assert len(values) == 81

    for b in boxes:
        if values[b] == '.':
            values[b] = all_digits
    
    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """    
    for b in boxes:
        if len(values[b]) == 1:
            digit = values[b]
            for p in peers[b]:
                values[p] = values[p].replace(digit, '')
    
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for u in all_units:
        for d in '123456789':
            possible_boxes = []
            for b in u:
                if d in values[b]:
                    possible_boxes.append(b)
            if len(possible_boxes) == 1:
                values[possible_boxes[0]] = d

    return values


def reduce_puzzle(values):
    stalled = False
    
    while not stalled:

        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False
    
    if all(len(values[b]) == 1 for b in boxes):
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    n, b = min((len(values[b]), b) for b in boxes if len(values[b]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, 
    # and if one returns a value (not False), return that answer!
    #
    # Nota: among all the possibilities in values[b], one has to be true!
    for v in values[b]:
        new_values = values.copy()
        new_values[b] = v

        result = search(new_values)

        if result:
            return result


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values


if __name__ == '__main__':

    # grid_1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    # display(solve(grid_1))

    # grid_2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    # display(solve(grid_2))
    
    # hard_1 = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    # display(solve(hard_1))

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))


    # try:
    #     from visualize import visualize_assignments
    #     visualize_assignments(assignments)

    # except SystemExit:
    #     pass
    # except:
    #     print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
