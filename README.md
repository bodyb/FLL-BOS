# FLL-BOS

#ddd file:
contains everything needed for the pathfinding movement system
Contains gyro class, node class, Cardinal function, MoveInDirections function, ReturnHome function, Log function, and DetectMovement function.

Gyro class used to store the cardinal direction yaw values

Node and Astar made by Nicholas Swift
Here is the link
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
Node class used in the pathfinding system
Astar is the pathfinding system

Cardinal Function:
Used to turn the bot in any of the eight Cardinal directions
The turn may be off due to drag on the board
Input any cardinal direction name string value. Ex. Cardinal("North")

MoveInDirections Function:
Moves the bot across the board using the Cardinal function
Translates the path from Astar function to a list of possible outcomes
Then checks the new outcomes against a list and turns the bot to the new direction and moves the correct distance
Input the path, the length of each node on the map, the speed of the movement, if the path should be reversed. Ex. moveInDirections([(1, 2), (1, 3), (1, 2), (1, 1), (1, 2)], 11, 30, False)

returnHome Function:
Holds the map of the board
Returns the bot back to home
The memory of the spike is limited so this function breaks up the path locations so it creates multiple positions to travel to first and then to the end
Input any the starting position of the robot, then the target position. returnHome((9, 9), (1, 1))

Log Function:
Place after every piece of movement code
Enter either Gyro or Movement as the argument
Use gyro to detect turns and use Movement to detect movement
Logs the current angle and movement the robot travelled at the current time
Input to log the gyro or robot movement. Ex. Log("Gyro")

DetectMovement Function:
This function returns the position of the robot, it acts like a varible
Uses sign a cosign to detect the amount of movement the robot made veritcal and horizontal
The amount traveled is the hypotenuse of the triangle and sign and cosign of the current angle are multiple by amount traveled to get its position
Input the current vertical and horizontal movement, Ex. detectMovement(10, 20)

#Functions File:
Contains previously made functions used in the 2021 - 2022 FLL season
Contains Working Gyro class, UltraDrive function, turn function by David Dong, DUD function, DDUD function, GyroTurn, ForkLift function, and linefollow function

Contains In Progess / NOT working DoubleUltraDrive function, GyroDrive function, createMap function, pain function, Cardinal function, MoveInDirection function, Move function, and returnHome function

UltraDrive function:
drive the bot forward until target distance reached by the UltraSonic sensor
Input the target length and speed. Ex. UltraDrive(30, 30)

Turn function:
Turns the bot for the amount of degrees
Created by David Dong
Input the target amount of degrees to turn. Ex. turn(90)

DUD function:
drive the bot forward until target distance reached by the UltraSonic sensor
Uses gyro to keep straight
Input the target length and speed. Ex. DUD(30, 30)

DDUD function:
drive the bot forward until target distance reached by degree calculations
Uses gyro to keep straight
Input the target length and speed. Ex. DDUD(30, 30)

GyroTurn function:
Turns the bot the target degrees, in the target direction
Input new yaw value, turning direction, and speed. Ex. GyroTurn(40, "Right", 30)

ForkLift function:
Moves the forklift up and down based on the string input
Input whether to up or down. Ex. ForkLift("Up")

LineFollow function:
Follows the line on the board by turning across the black line
Input the target length and speed. Ex. LineFollow(30, 30)




