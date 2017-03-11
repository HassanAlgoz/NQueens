import sys
import random
import time

# Pick a random assignment.
# Randomly select a variable for update. Use min-Conflict measure to set the value of the selected variable.
# Instead of building things step by step, we pick a complete assignment and fix it
# States: 4 queens in 4 columns (4^4 = 256 states)
# Operators: Move queen in column
# Goal test: No attacks
# Evaluation: c(n) = number of attacks

# Constants
QUEEN = "Q"
EMPTY = "#"

def conflicts(row, col):
	numThreats = 0
	# Column
	for i in range(n):
		if board[i][col] == QUEEN and i != row:
			numThreats += 1

	# Top-Left to Bottom-Right (Diagonal)
	m = min(row, col)
	i = row-m
	j = col-m
	while(i < n and j < n):
		if board[i][j] == QUEEN and i != row and j != col:
			numThreats += 1
		i += 1
		j += 1

	# Top-Right to Bottom-Left (Diagonal)
	m = min(row, n-col-1)
	i = row-m
	j = col+m
	while(i < n and j >= 0):
		if board[i][j] == QUEEN and i != row and j != col:
			numThreats += 1
		i += 1
		j -= 1

	return numThreats


def updateConflicts(row, col):
	# Update conflicts on values who might be affected
	# Affected Variables are variables who are either
	# in the same column, or diagonals. So we update
	# them. This way we don't have to check the whole
	# board.

	# Column
	for i in range(n):
		if board[i][col] == QUEEN and i != row:
			rowConflicts[i] = conflicts(i, col)

	# Top-Left to Bottom-Right (Diagonal)
	m = min(row, col)
	i = row-m
	j = col-m
	while(i < n and j < n):
		if board[i][j] == QUEEN and i != row and j != col:
			rowConflicts[i] = conflicts(i, j)
		i += 1
		j += 1

	# Top-Right to Bottom-Left (Diagonal)
	m = min(row, n-col-1)
	i = row-m
	j = col+m
	while(i < n and j >= 0):
		if board[i][j] == QUEEN and i != row and j != col:
			rowConflicts[i] = conflicts(i, j)
		i += 1
		j -= 1


def move(row, old, new):
	row[old] = EMPTY
	row[new] = QUEEN

def printBoard():
	for i in range(n):
		print("".join(board[i]))


if __name__ == "__main__":
	# Get Input
	n = int(sys.argv[1])
	print("Solving for " +str(n)+ " Queens..")

	# Initialize Board: random assignment to all variables (rows)
	board = []
	for i in range(n):
		row = []
		r = random.randint(0, n-1)
		for j in range(n):
			row.append(EMPTY)
		row[r] = QUEEN
		board.append(row)

	timeStart = float(time.time())

	# Lookup table for minimum conflicts of variables (rows)
	# Updated when necessary only, rather than having to check
	# all queens. We only check affected variables. O(n) Space Complexity
	rowConflicts = []
	for i in range(n):
		col = board[i].index(QUEEN)
		rowConflicts.append(conflicts(i, col))


	# -------------------------------------------------------------------
	# Game Loop (one game)
	numberOfMoves = 0
	while(True):
		numberOfMoves += 1

		# Goal Test
		if sum(rowConflicts) == 0:
			# printBoard()
			timeEnd = float(time.time())
			timeDiff = timeEnd - timeStart
			print "DONE!"
			print "     \tN\tSeconds\tMoves"
			print "     \t%d\t%.2f\t%d" % (n, timeDiff, numberOfMoves)
			break

		# Select a random variable (row)
		r = random.randint(0, n-1)
		# while(rowConflicts[r] == 0):
		# 	r = random.randint(0, n-1)
		# Assign it to minimum conflict column
		myRow = board[r]
		minConflict = rowConflicts[r]
		initialIndex = board[r].index(QUEEN)
		minConflictIndex = initialIndex
		cellsConflicts = []
		for j in range(n):
			conflictResult = conflicts(r, j)
			if (conflictResult < minConflict):
				minConflict = conflictResult
			cellsConflicts.append(conflictResult)
		# Break ties randomly
		while True:
			rnd = random.randint(0,n-1)
			if cellsConflicts[rnd] == minConflict:
				minConflictIndex = rnd
				break

		# Move Queen: assign another value to the variable (row)
		move(myRow, initialIndex, minConflictIndex)
		rowConflicts[r] = minConflict
		# Update conflicts on variables who have conflict with
		# the position of this Queen before the move and after.
		updateConflicts(r, initialIndex)
		updateConflicts(r, minConflictIndex)

		# printBoard()
	# print(rowConflicts)