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
	for i in range(len(board)):
		if board[i][col] == QUEEN and i != row:
			numThreats += 1
			break

	# Top-Left to Bottom-Right (Diagonal)
	m = min(row, col)
	i = row-m
	j = col-m
	while(i < len(board) and j < n):
		if board[i][j] == QUEEN and i != row and j != col:
			numThreats += 1
			break
		i += 1
		j += 1

	# Top-Right to Bottom-Left (Diagonal)
	m = min(row, n-col-1)
	i = row-m
	j = col+m
	while(i < len(board) and j >= 0):
		if board[i][j] == QUEEN and i != row and j != col:
			numThreats += 1
			break
		i += 1
		j -= 1

	return numThreats

def updateConflicts(row, col):
	# Column
	for i in range(n):
		if board[i][col] == QUEEN and i != row:
			rowConflicts[i] = conflicts(i, col)
			break

	# Top-Left to Bottom-Right (Diagonal)
	m = min(row, col)
	i = row-m
	j = col-m
	while(i < n and j < n):
		if board[i][j] == QUEEN and i != row and j != col:
			rowConflicts[i] = conflicts(i, j)
			break
		i += 1
		j += 1

	# Top-Right to Bottom-Left (Diagonal)
	m = min(row, n-col-1)
	i = row-m
	j = col+m
	while(i < n and j >= 0):
		if board[i][j] == QUEEN and i != row and j != col:
			rowConflicts[i] = conflicts(i, j)
			break
		i += 1
		j -= 1


def move(row, old, new):
	row[old] = EMPTY
	row[new] = QUEEN


def printBoard():
	for i in range(n):
		print("".join(board[i]))
	print "-"*n


def solve(t):
	print "#%d Solving for %d Queens.." % (t+1, n)
	# Initialize Board: random assignment to all rows
	timeStart = float(time.time())
	for i in range(n):
		row = []
		for j in range(n):
			row.append(EMPTY)
		#choose least conflicted col
		minConflict = n
		minConflictIndex = 0
		cellsConflicts = []
		for j in range(n):
			conflictResult = conflicts(i, j)
			if conflictResult < minConflict:
				minConflict = conflictResult
			cellsConflicts.append(conflictResult)

		minCellsConflicts = []

		for j in range(n):
			if cellsConflicts[j] == minConflict:
				minCellsConflicts.append(j)

		if len(minCellsConflicts) > 0:
			rnd = random.randint(0,len(minCellsConflicts)-1)
			minConflictIndex = minCellsConflicts[rnd]

		row[minConflictIndex] = QUEEN
		board.append(row)

	timeEnd = float(time.time())
	timeDiff = float(timeEnd - timeStart)
	print "Board Initialized in %.3f seconds" % (timeDiff)
	timeStart = float(time.time())
	# -------------------------------------------------------------------

	# Initialize our conflicted rows storage
	for i in range(n):
		col = board[i].index(QUEEN)
		conflictResult = conflicts(i, col)
		rowConflicts.append(conflictResult)

	# Game Loop (one game)
	numberOfMoves = 0
	numberOfLoops = 0
	while(numberOfMoves < n*2):
		numberOfLoops += 1

		if sum(rowConflicts) == 0:
			printBoard()
			timeEnd = float(time.time())
			timeDiff = float(timeEnd - timeStart)
			print "DONE!"
			print "     \tN\tSeconds\tLoops\tMoves"
			print "     \t%d\t%.3f\t%d\t%d" % (n, timeDiff, numberOfLoops, numberOfMoves)
			print "--------------------------------------------------"
			return (timeDiff, numberOfLoops, numberOfMoves)
			break

		#get random row however in rowconflicts
		r = random.randint(0, n-1)
		while(rowConflicts[r] == 0):
			r = random.randint(0, n-1)

		myRow = board[r]
		minConflict = rowConflicts[r]
		initialIndex = board[r].index(QUEEN)
		minConflictIndex = initialIndex


		cellsConflicts = []

		for j in range(n):
			conflictResult = conflicts(r, j)
			if conflictResult < minConflict:
				minConflict = conflictResult
			cellsConflicts.append(conflictResult)

		minCellsConflicts = []

		for j in range(n):
			if cellsConflicts[j] == minConflict:
				minCellsConflicts.append(j)

		if len(minCellsConflicts) > 0:
			rnd = random.randint(0,len(minCellsConflicts)-1)
			minConflictIndex = minCellsConflicts[rnd]

		# Move
		numberOfMoves += 1
		move(myRow, initialIndex, minConflictIndex)
		rowConflicts[r] = minConflict
		updateConflicts(r, initialIndex)
		updateConflicts(r, minConflictIndex)

	return (0, 0, 0, 0)


if __name__ == "__main__":
	totalTime = float(time.time())
	# Get Input
	n = int(sys.argv[1])
	times = int(sys.argv[2])
	board = []
	rowConflicts = []
	stats = []
	tryNumber = 0
	while tryNumber < times:
		result = solve(tryNumber)
		board = []
		rowConflicts = []
		if result[1] != 0:
			stats.append(result)
			tryNumber += 1

	totalTimeDiff = 0
	totalNumberOfLoops = 0
	totalNumberOfMoves = 0

	for timeDiff, numberOfLoops, numberOfMoves in stats:
		totalTimeDiff += timeDiff
		totalNumberOfLoops += numberOfLoops
		totalNumberOfMoves += numberOfMoves

	avgTimeDiff = totalTimeDiff/times
	avgNumberOfLoops = totalNumberOfLoops/times
	avgNumberOfMoves = totalNumberOfMoves/times

	print "Average of %d times" % (times)
	print "\tN\tSeconds\tLoops\tMoves"
	print "\t%d\t%.3f\t%d\t%d" % (n, avgTimeDiff, avgNumberOfLoops, avgNumberOfMoves)
	print "Total time: %.3f seconds" % (time.time() - totalTime)
