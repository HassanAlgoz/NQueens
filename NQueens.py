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
	numThreats = rightAboveConflict(row, col) + rightBottomConflict(row, col)
	numThreats += leftAboveConflict(row, col) + aboveConflict(row, col)
	numThreats += bottomConflict(row, col)
	return numThreats


def updateConflicts(row, col):
	# Update conflicts on values who might be affected
	# Affected Variables are variables who are either
	# in the same column, or diagonals. So we update
	# them. This way we don't have to check the whole
	# board.

	# Above Queen
	i = row
	while(i > 0):
		i -= 1
		if board[i][col] == QUEEN:
			rowConflicts[i] = rowConflicts[i] - 1 + bottomConflict(i, col)
			break

	# Below Queen
	i = row
	while(i < n-1):
		i += 1
		if board[i][col] == QUEEN:
			rowConflicts[i] = rowConflicts[i] - 1 + aboveConflict(i, col)
			break

	# rightAbove Queen
	i = row
	j = col
	while(i > 0 and j < n-1):
		i -= 1
		j += 1
		if board[i][j] == QUEEN:
			rowConflicts[i] = rowConflicts[i] - 1 + leftBottomConflict(i, j)
			break

	# rightBottom Queen
	i = row
	j = col
	while(i < n-1 and j < n-1):
		i += 1
		j += 1
		if board[i][j] == QUEEN:
			rowConflicts[i] = rowConflicts[i] - 1 + leftAboveConflict(i, j)
			break

	# leftAbove Queen
	i = row
	j = col
	while(i > 0 and j > 0):
		i -= 1
		j -= 1
		if board[i][j] == QUEEN:
			rowConflicts[i] = rowConflicts[i] - 1 + rightBottomConflict(i, j)
			break

	# leftBottom Queen
	i = row
	j = col
	while(i < n-1 and j > 0):
		i += 1
		j -= 1
		if board[i][j] == QUEEN:
			rowConflicts[i] = rowConflicts[i] - 1 + rightAboveConflict(i, j)
			break



def aboveConflict(row, col):
	while(row > 0):
		row -= 1
		if board[row][col] == QUEEN:
			return 1
	return 0

def bottomConflict(row, col):
	while(row < n-1):
		row += 1
		if board[row][col] == QUEEN:
			return 1
	return 0

def rightAboveConflict(row, col):
	while(row > 0 and col < n-1):
		row -= 1
		col += 1
		if board[row][col] == QUEEN:
			return 1
	return 0

def rightBottomConflict(row, col):
	while(row < n-1 and col < n-1):
		row += 1
		col += 1
		if board[row][col] == QUEEN:
			return 1
	return 0

def leftAboveConflict(row, col):
	while(row > 0 and col > 0):
		row -= 1
		col -= 1
		if board[row][col] == QUEEN:
			return 1
	return 0

def leftBottomConflict(row, col):
	while(row < n-1 and col > 0):
		row += 1
		col -= 1
		if board[row][col] == QUEEN:
			return 1
	return 0

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

		r = random.randint(0, n-1)
		# Assign it to minimum conflict column
		myRow = board[r]
		minConflict = rowConflicts[r]
		initialIndex = board[r].index(QUEEN)
		minConflictIndex = initialIndex
		# Evaluate conflicts for the whole row
		cellsConflicts = []
		for j in range(n):
			conflictResult = conflicts(r, j)
			if conflictResult < minConflict:
				minConflict = conflictResult
				minConflictIndex = j
			cellsConflicts.append(conflictResult)
		
		# Inlist all indexes, where conflict == minConflict
		# This is used to break ties fast
		minIndexes = []
		for j in range(n):
			# skip self index
			if j == initialIndex:
				continue
			if cellsConflicts[j] == minConflict:
				minIndexes.append(j)

		# Break ties randomly
		# only if there is a duplicate min conflict
		if len(minIndexes) > 0:
			rnd = minIndexes[random.randint(0, len(minIndexes) - 1)]
			minConflictIndex = rnd

			# Move Queen: assign another value to the variable (row)
			# Update conflicts on variables who have conflict with
			# the position of this Queen before the move and after.
			move(myRow, initialIndex, minConflictIndex)
			rowConflicts[r] = minConflict
			updateConflicts(r, initialIndex)
			updateConflicts(r, minConflictIndex)
			# printBoard()
			# print("-"*n)


		if numberOfMoves % 1000 == 0:
			print "%d" % (numberOfMoves)
		# Goal Test
		# if numberOfMoves % (n/10) == 0:
		if sum(rowConflicts) == 0:
			# printBoard()
			timeEnd = float(time.time())
			timeDiff = timeEnd - timeStart
			print "DONE!"
			print "     \tN\tSeconds\tMoves"
			print "     \t%d\t%.2f\t%d" % (n, timeDiff, numberOfMoves)
			break
