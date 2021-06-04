from random import randint, choice
from GameMap import *
from enum import Enum

class MAZE_GENERATOR_TYPE(Enum):
	RECURSIVE_BACKTRACKER = 0,
	UNION_FIND_SET = 1,

generator_types = {MAZE_GENERATOR_TYPE.RECURSIVE_BACKTRACKER:"Easy", MAZE_GENERATOR_TYPE.UNION_FIND_SET:"Hard"}


def checkAdjacentPos(map, x, y, width, height, checklist):
	directions = []
	if x > 0:
		if not map.isVisited(2 * (x - 1) + 1, 2 * y + 1):
			directions.append(WALL_DIRECTION.WALL_LEFT)

	if y > 0:
		if not map.isVisited(2 * x + 1, 2 * (y - 1) + 1):
			directions.append(WALL_DIRECTION.WALL_UP)

	if x < width - 1:
		if not map.isVisited(2 * (x + 1) + 1, 2 * y + 1):
			directions.append(WALL_DIRECTION.WALL_RIGHT)

	if y < height - 1:
		if not map.isVisited(2 * x + 1, 2 * (y + 1) + 1):
			directions.append(WALL_DIRECTION.WALL_DOWN)

	if len(directions):
		direction = choice(directions)
		if direction == WALL_DIRECTION.WALL_LEFT:
			map.setMap(2 * (x - 1) + 1, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
			map.setMap(2 * x, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
			checklist.append((x - 1, y))

		elif direction == WALL_DIRECTION.WALL_UP:
			map.setMap(2 * x + 1, 2 * (y - 1) + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
			map.setMap(2 * x + 1, 2 * y, MAP_ENTRY_TYPE.MAP_EMPTY)
			checklist.append((x, y - 1))

		elif direction == WALL_DIRECTION.WALL_RIGHT:
			map.setMap(2 * (x + 1) + 1, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
			map.setMap(2 * x + 2, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
			checklist.append((x + 1, y))

		elif direction == WALL_DIRECTION.WALL_DOWN:
			map.setMap(2 * x + 1, 2 * (y + 1) + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
			map.setMap(2 * x + 1, 2 * y + 2, MAP_ENTRY_TYPE.MAP_EMPTY)
			checklist.append((x, y + 1))

		return True
	else:
		return False


def recursiveBacktracker(map, width, height):
	startX, startY = (randint(0, width-1), randint(0, height-1))
	map.setMap(2*startX+1, 2*startY+1, MAP_ENTRY_TYPE.MAP_EMPTY)

	checklist = []
	checklist.append((startX, startY))
	while len(checklist):
		entry = checklist[-1]
		if not checkAdjacentPos(map, entry[0], entry[1], width, height, checklist):
			checklist.remove(entry)

def doRecursiveBacktracker(map):
	map.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)
	recursiveBacktracker(map, (map.width-1)//2, (map.height-1)//2)

def unionFindSet(map, width, height):
	def findSet(parent, index):
		if index != parent[index]:
			return findSet(parent, parent[index])

		return parent[index]
	
	def getNodeIndex(x, y):
		return x * height + y

	def unionSet(parent, index1, index2, weightlist):
		root1 = findSet(parent, index1)
		root2 = findSet(parent, index2)
		if root1 == root2:
			return

		if root1 != root2:
			if weightlist[root1] > weightlist[root2]:
				parent[root2] = root1
				weightlist[root1] += weightlist[root2]

			else:
				parent[root1] = root2
				weightlist[root2] += weightlist[root2]
			
	def checkAdjacentPos(map, x, y, width, height, parentlist, weightlist):
		directions = []
		node1 = getNodeIndex(x,y)
		root1 = findSet(parentlist, node1)

		if x > 0:		
			root2 = findSet(parentlist, getNodeIndex(x-1, y))
			if root1 != root2:
				directions.append(WALL_DIRECTION.WALL_LEFT)
					
		if y > 0:
			root2 = findSet(parentlist, getNodeIndex(x, y-1))
			if root1 != root2:
				directions.append(WALL_DIRECTION.WALL_UP)

		if x < width -1:
			root2 = findSet(parentlist, getNodeIndex(x+1, y))
			if root1 != root2:
				directions.append(WALL_DIRECTION.WALL_RIGHT)
			
		if y < height -1:
			root2 = findSet(parentlist, getNodeIndex(x, y+1))
			if root1 != root2:
				directions.append(WALL_DIRECTION.WALL_DOWN)
			
		if len(directions):
			direction = choice(directions)
			if direction == WALL_DIRECTION.WALL_LEFT:
				adj_x, adj_y = (x-1, y)
				map.setMap(2*x, 2*y+1, MAP_ENTRY_TYPE.MAP_EMPTY)				
			elif direction == WALL_DIRECTION.WALL_UP:
				adj_x, adj_y = (x, y-1)
				map.setMap(2*x+1, 2*y, MAP_ENTRY_TYPE.MAP_EMPTY)
			elif direction == WALL_DIRECTION.WALL_RIGHT:
				adj_x, adj_y = (x+1, y)
				map.setMap(2*x+2, 2*y+1, MAP_ENTRY_TYPE.MAP_EMPTY)
			elif direction == WALL_DIRECTION.WALL_DOWN:
				adj_x, adj_y = (x, y+1)
				map.setMap(2*x+1, 2*y+2, MAP_ENTRY_TYPE.MAP_EMPTY)
			
			node2 = getNodeIndex(adj_x, adj_y)
			unionSet(parentlist, node1, node2, weightlist)
			return True
		else:
			return False
			
	parentlist = [x*height+y for x in range(width) for y in range(height)]
	weightlist = [1 for x in range(width) for y in range(height)] 
	checklist = []
	for x in range(width):
		for y in range(height):
			checklist.append((x,y))
			map.setMap(2*x+1, 2*y+1, MAP_ENTRY_TYPE.MAP_EMPTY)
		
	while len(checklist):
		entry = choice(checklist)
		if not checkAdjacentPos(map, entry[0], entry[1], width, height, parentlist, weightlist):
			checklist.remove(entry)

			
def doUnionFindSet(map):
	map.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)
	unionFindSet(map, (map.width-1)//2, (map.height-1)//2)
	
def generateMap(map, type):
	if type == MAZE_GENERATOR_TYPE.RECURSIVE_BACKTRACKER:
		doRecursiveBacktracker(map)
	elif type == MAZE_GENERATOR_TYPE.UNION_FIND_SET:
		doUnionFindSet(map)
	
def run():
	WIDTH = 31
	HEIGHT = 21
	
	map = Map(WIDTH, HEIGHT)
	generateMap(map, MAZE_GENERATOR_TYPE.UNION_FIND_SET)
	source = map.generatePos((1,1),(1,HEIGHT-1))
	dest = map.generatePos((WIDTH-2,WIDTH-2),(1,HEIGHT-1))
	print("source:", source)
	print("dest:", dest)
	map.showMap()	
	

#if __name__ == "__main__":
#	run()
