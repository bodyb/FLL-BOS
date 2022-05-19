# FLL-BOS

#ddd file:
returnHome() function

Gyro class used to store the cardinal direction yaw values

Node and Astar made by Nicholas Swift
Here is the link
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
Node class used in the pathfinding system
Astar is the pathfinding system

Cardinal Function:
Used to turn the bot in any of the eight Cardinal direction
The turn may be off due to drag on the board

MoveInDirections Function:
Moves the bot across the board using the Cardinal function
Translates the path from Astar function to a list of possible out comes
Then checks the new outcomes to a list and turns the bot to the new direction and moves the correct distance

returnHome Function:
Holds the map of the board
Returns the bot back to home
The memory of the spike is limited so this function breaks up the path locations so it creates multiple positions to travel to first and then to the end

Log Function:
Place after every piece of movment code
Logs the current angle and movement the robot travelled at the current time

Detect

