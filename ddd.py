from spike import PrimeHub, Motor, MotorPair

from math import *

hub = PrimeHub()

#Creates the gyro class
class Gyro():
    def __init__(self, current_yaw, updated_yaw, currentCardinal):
        self.current_yaw = current_yaw
        #Defines the yaw values for the different Cardinal Directions and creates an array with the names of the different directions 
        self.north = 0
        self.south = -180
        self.east = 90
        self.west = -90
        self.north_west = -45
        self.north_east = 45
        self.south_west = -135
        self.south_east = 135
        self.currentCardinal = currentCardinal
        self.cardinalList = ["North", "South", "West", "East", "North_East", "North_West", "South_West", "South_East"]
        self.updated_yaw = updated_yaw

#Creates instances of the different motor and sensor classes 
drive = MotorPair('D', 'B')
left = Motor('D')
right = Motor('B')
gyro = Gyro(0, 0, "North")
#Defines two arrays used in the movement detection system
gyroLog = []
movementLog = []
wheel_circumference = 18 #cm

#Creates the Node Class
class Node():
    def __init__(self, parent=None, position=None):
        #Adds to the node its parent and position on the map
        self.parent = parent
        self.position = position
        #Adds the G, H, and F costs used in the pathfinding system
        self.g = 0
        self.h = 0
        self.f = 0
    #Allows for two instances of the node class to be compared to another node's position
    def __eq__(self, other):
        return self.position == other.position

#Creates the Pathfinding Function
def astar(maze, start, end):
    #Creates the start and end nodes
    start_node = Node(None, start)
    #Sets their g, h, and f cost to 0
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    #Creates the open and closed list array to run through the new nodes
    open_list = []
    closed_list = []
    #Adds the start node to the open list
    open_list.append(start_node)
    #While there is something in the open list
    while len(open_list) > 0:
        #Makes the current node the first item in the open list
        current_node = open_list[0]
        current_index = 0
        #
        for index, item in enumerate(open_list):
            #If the new node has a lower f cost than the current node
            if item.f < current_node.f:
                #Then it makes the current node the new node and sets the current index to the amount of runs that the loop had to do
                current_node = item
                current_index = index
        #Takes out the node at the index value
        open_list.pop(current_index)
        #Adds the new node to the closed list
        closed_list.append(current_node)

        #If the current node = the end node it stops search
        if current_node == end_node:
            #Creates the path array
            path = []
            current = current_node
            #While the current node exsits
            while current is not None:
                #Adds to the path the current nodes position
                path.append(current.position)
                current = current.parent
            #Returns the reversed path
            return path[::-1]

        #Starts to trace back the path
        children = []

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: 
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)
        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            #Defines the different costs of the nodes g, h, and f
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            open_list.append(child)

#Creates the turning function for the movement code
def Cardinal(direction):
    #Defines the starting yaw of the bot
    gyro.current_yaw = hub.motion_sensor.get_yaw_angle()
    while True:
        #Defines the current yaw of the bot
        gyro.updated_yaw = hub.motion_sensor.get_yaw_angle()
        #Creates the target and movement value
        target_cardinal = 0
        movement_length = 0
        #Creates an array to run through during for loop
        intCardinal = [gyro.north, gyro.south, gyro.west, gyro.east, gyro.north_east, gyro.north_west, gyro.south_west, gyro.south_east]
        #Runs through the list of cardinal directions to find the targeted one in the argument for the function
        for i in range(len(gyro.cardinalList)):
            #If the argument for the function matches the current cardinal in the list and the target current does not equal the current cardinal direction of the bot
            if direction == gyro.cardinalList[i] and gyro.currentCardinal != direction:
                #Sets the target direction to the last matched in the loop
                target_cardinal = intCardinal[i]
                gyro.currentCardinal = gyro.cardinalList[i]
        #Due to the different system of the motion sensor on the bot, this code creates the amount the robot has to move the get the correct movement lenght
        if gyro.current_yaw > 0:
            movement_length = target_cardinal - gyro.current_yaw
        if gyro.current_yaw < 0:
            movement_length = target_cardinal + gyro.current_yaw
        if gyro.current_yaw == 0:
            movement_length = target_cardinal
        print(target_cardinal, movement_length)
        #Turns the bot to the calculated movement length
        drive.move_tank(movement_length * 1.75, "degrees", left_speed = 25, right_speed = -25)
        break

#Movement Function
def moveInDirections(path, grid_rate, speed, reverse):
    #If the reverse argument is True the path reverses
    if reverse == True:
        path.reverse()
    #Creates the array of the directions from the path
    directions = []
    #Defines the distance of the amount of movement the bot has to move
    straight_line = grid_rate
    dianogal_line = sqrt(grid_rate^2 + grid_rate^2)
    #Starts the loop that creates the directions from the path
    for x in range(len(path) - 1):
        #Takes the current node and subtracts in from the next node then inserts it into the directions array
        current_node = path[len(path) - 1 - x]
        possible_outcomes = [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]
        next_node = path[len(path) - 2 - x]
        direction = [current_node[0] - next_node[0], current_node[1] - next_node[1]]
        directions.insert(x, [current_node[0] - next_node[0], current_node[1] - next_node[1]])
        print(directions)
        #Starts a secondary loop to move the bot
        for v in range(len(possible_outcomes)):
            #Checks the current direction against the possible outcomes
            if directions[x] == possible_outcomes[v]:
                #Turns the bot with the Cardinal function
                Cardinal(gyro.cardinalList[v])
                #Moves the bot a different amount if the amount of loops execeds 5
                if v > 4:
                    drive.move(dianogal_line, "cm", 0, speed)
                elif v < 5:
                    drive.move(straight_line, "cm", 0, speed)

#Creates the logging function of the movement detection
def log():
    #Defines the amount of degrees travelled to detection the movement
    leftDegrees = left.get_degrees_counted()
    #Adds the current yaw to the gyroLog array
    gyroLog.append(drive.currentAngle)
    #Adds the amount travelled by the bot to the movementLog array
    if len(movementLog) > 0:
        #If there is more than one item in the list it subtracts the current movement from the previous movement
        movementLog.append((leftDegrees / 360 * wheel_circumference) - movementLog[len(movementLog) - 2])   
    else:
        #Else it just adds the orginal movement
        movementLog.append(leftDegrees / 360 * wheel_circumference)
    print(gyroLog, movementLog)

#Defines the movement detection function
def detectMovement(verticalMovement, horizontalMovement):
    #Defines the current angle and movement
    angle = movement = 0
    #Starts a loop 
    for i in range(len(gyroLog)):
        #print(i)
        #defines both the angle and the movement to by tracked 
        angle = gyroLog[i]
        movement = movementLog[i]
        #Calculates the Veritcal and Horizontal movement by using basic trigonometry
        #Takes the length of the hypotenuse (Movement Length) multiplies it by the cosign of the angle to get the vertical movement
        #Takes the length of the hypotenuse (Movement Length) multiplies it by the sign of the angle to get the horizontal movement
        verticalMovement = verticalMovement + cos(angle) * movement
        horizontalMovement = horizontalMovement + sin(angle) * movement
        #print(angle, movement, verticalMovement, horizontalMovement)
        #Puts the two values in to a tuple and then returns them
        pair = (horizontalMovement, verticalMovement)
    return pair

#Creates the returnHome Function
def returnHome(start_position, end_position):
    #Defines the map of the board, O = travellable space and X = nontravellable space
    O = 0
    X = 1
    current_map = [
        [O, O, O, X, X, O, O, X, X, X, O, O, O, O, X, X, X, O, O, O, X, X], #1
        [O, O, O, X, X, O, O, X, X, X, X, O, O, O, O, X, X, X, O, O, O, X], #2
        [O, O, O, O, O, O, X, O, X, X, X, O, O, O, O, X, X, X, O, O, X, X], #3
        [O, O, O, O, O, O, X, O, O, O, O, O, O, O, O, O, O, O, O, O, X, X], #4
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, X, X], #5
        [O, O, O, X, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, X, X], #6
        [O, O, O, X, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, X, X], #7
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, X, X], #8
        [O, O, O, O, O, O, O, X, X, X, X, X, X, X, X, X, X, O, O, O, X, X], #9
        [O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, X, X, X, X], #10
        [O, O, O, O, O, O, O, O, O, O, O, O, O, X, X, O, O, O, X, X, X, X], #11
        [O, O, O, O, O, O, O, O, O, O, O, O, O, X, X, O, X, O, X, X, X, X]#12
    ]
    #Defines the start and end position to the inputted values
    start = start_position
    end = end_position
    #Defines the width of the map and then subtracts it from the y value of the target location 
    width = len(current_map)
    target = abs(end[1] - width)
    #Checks if the target node is able to be travelled to
    if current_map[target][end[0]] == 0:
        #Checks if the distance of the path will overload the memory of the spike
        distCheck = [end[0] - start[0], end[1] - start[1]]
        if abs(distCheck[0]) >= 7 or abs(distCheck[1]) >= 7:
            #Creates multiple different positions to limit the amount of the work the pathfinding takes
            firstPosition = (round(end[0] / 2), round(end[1] / 2))
            secondPosition = None
            thirdPosition = None
            #If the firstPosition will still overload the memory it creates a secondPositon
            if firstPosition[0] + firstPosition[1] >= 7:
                secondPosition = firstPosition
                firstPosition = (round(end[0] / 3), round(end[1] / 3))
            #If the secondPosition will still overload the memory it creates a thridPosition
            if secondPosition[0] + secondPosition[1] >= 14:
                thirdPosition = firstPosition
                secondPosition = (round(end[0] / 3), round(end[1] / 3))
                firstPosition = (round(end[0] / 4), round(end[1] / 4))
            print(start, firstPosition, secondPosition, thirdPosition, end)
            #Creates the new paths the be combined
            pathA = pathB = pathC = pathD = (0, 0)
            #If the second position exsit and the thrid position does not exsit
            if secondPosition != None and thirdPosition == None:
                print("yes, no")
                #It makes path A, B, and C to be combined later
                pathA = astar(current_map, start, firstPosition)
                pathB = astar(current_map, firstPosition, secondPosition)
                pathC = astar(current_map, secondPosition, end)
                pathD = None
                print("PathA =", pathA, "PathB =", pathB, "PathC =", pathC, "PathD =", pathD)
            #If the second and thrid position do not exsit
            if secondPosition == None and thirdPosition == None:
                print("no, no")
                #It makes path A and B to be combined later
                pathA = astar(current_map, start, firstPosition)
                pathB = astar(current_map, firstPosition, end)
                pathC = None
                pathD = None
                print("PathA =", pathA, "PathB =", pathB, "PathC =", pathC, "PathD =", pathD)
            #If the second and thrid position do exsit
            if secondPosition != None and thirdPosition != None:
                print("yes, yes")
                #It makes path A, B, C, D to be combined later
                pathA = astar(current_map, start, firstPosition)
                pathB = astar(current_map, firstPosition, secondPosition)
                pathC = astar(current_map, secondPosition, thirdPosition)
                pathD = astar(current_map, thirdPosition, end)
                print("PathA =", pathA, "PathB =", pathB, "PathC =", pathC, "PathD =", pathD)
            #Creates the final path
            path = []
            #Adds together all the paths
            #Runs a loop
            for i in range(len(pathA)):
                #Inserts the nodes in path A into the final path
                path.insert(i, pathA[i])
                #Marks the last position
                lastPosition = i
                #print(i, path, lastPosition)
            #Runs a loop
            for i in range(len(pathB)):
                if i >= 0:
                    #Inserts the nodes in path B into the final path
                    path.insert(lastPosition + i, pathB[i])
                    #print(lastPosition + i, path, lastPosition)
                    #Marks last position
                    lastPosition = lastPosition + i
            #Checks if path C exsits
            if pathC != None:
                #Runs a loop
                for i in range(len(pathC)):
                    if i >= 0:
                        #Inserts the nodes in path C into the final path
                        path.insert(lastPosition + i, pathC[i])
                        #print(lastPosition + i, path, lastPosition)
                        #Marks last position
                        lastPosition = lastPosition + i
                #Checks if path D exsits
                if pathD != None:
                    #Runs a loop
                    for i in range(len(pathD)):
                        if i >= 0:
                            #Inserts the nodes in path D into the final path
                            path.insert(lastPosition + i, pathD[i])
                            #print(lastPosition + i, path, lastPosition)
                            #Marks last position
                            lastPosition = lastPosition + i
            print(path)
        else:
            #Runs the complete path if the memory will not overload
            path = astar(current_map, start, end)
            print(path, start, end)
        #Moement Function with created path
        moveInDirections(path, 11, 30, False)


hub.motion_sensor.reset_yaw_angle()
returnHome((9, 9), (1, 1))
#Cardinal("North")
#moveInDirections([(1, 2), (1, 3), (1, 2), (1, 1), (1, 2)], 11, 30, False)