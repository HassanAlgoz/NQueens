import sys
print(sys.argv)

n = argv[1]

rows = [] # Throw queens on the board


def heuristic(x, y):
	threats = 0
	# Top-Left to Right-Down (Diagonal)
	m = min(x, y)
	topLeft = [x-m][y-m]
	while(n - max(x+i, y+i) > 0):
		if rows[x+i][y+i] == "Q":
			threats += 1
			break;
		i += 1
