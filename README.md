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

MoveInDirections Function:
Moves the bot across the board using the Cardinal function
Translates the path from Astar function to a list of possible outcomes
Then checks the new outcomes against a list and turns the bot to the new direction and moves the correct distance

returnHome Function:
Holds the map of the board
Returns the bot back to home
The memory of the spike is limited so this function breaks up the path locations so it creates multiple positions to travel to first and then to the end

Log Function:
Place after every piece of movement code
Logs the current angle and movement the robot travelled at the current time

DetectMovement Function:
This function returns the position of the robot, it acts like a varible
Uses sign a cosign to detect the amount of movement the robot made veritcal and horizontal
The amount traveled is the hypotenuse of the triangle and sign and cosign of the current angle are multiple by amount traveled to get its position

#Functions File:
Contains previously made functions used in the 2021 - 2022 FLL season
Contains Working Gyro class, UltraDrive function, turn function by David Dong, DUD function, DDUD function, GyroTurn, ForkLift function, and linefollow function

Contains In Progess / NOT working DoubleUltraDrive function, GyroDrive function, createMap function, pain function, Cardinal function, MoveInDirection function, Move function, and returnHome function

UltraDrive function:
drive the bot forward until target distance reached by the UltraSonic sensor

Turn function:
Turns the bot for the amount of degrees
Created by David Dong

DUD function:
drive the bot forward until target distance reached by the UltraSonic sensor
Uses gyro to keep straight

DDUD function:
drive the bot forward until target distance reached by degree calculations
Uses gyro to keep straight

GyroTurn function:
Turns the bot the target degrees, in the target direction

ForkLift function:
Moves the forklift up and down based on the string input

LineFollow function:
Follows the line on the board by turning across the black line




