# DungeonCrawler
Dungeon Crawler: an ASCII-Animated Dungeon Game

# Description
Dungeon Crawler is a simple ASCII-based in-terminal dungeon game. The game follows the MVC design pattern and utilizes procedural generation to provide the user with a consistently unique experience with each use. In the game, users battle mobs and struggle to stay alive, while journeying further and further into the depths of the dungeon. Users have the ability to save their data in one of three save slots, and likewise to delete save data from any of said save slots. 

As previously mentioned the game follows the MVC design pattern and thus consists of three main classes, the model, the view, and the controller. The model maintains all game data and delineates the logic through which this data may be manipulated. The view defines the manner in which the data within the model is portrayed to the user. The controller takes user input, manipulates the model within legal bounds, and updates the view accordingly. This design pattern not only provides a strong organizational framework but encourages encapsulation and abstraction throughout the design.

Additionally, the incorporation of multithreading into the application allowed for smooth game-play and continuous data flow. Furthermore, the non-blocking aspect of multithreading allowed for keyboard input to be collected without interfering with view rendering and model manipulation. The purpose of this game is simply to entertain the user. The potential users of this game would be anybody who likes to play adventure games.

# Required Libraries
In order to run Dungeon Crawler, you must have the follow libraries installed: numpy, math, os, random, multithreading, dill, pynput, and itertools.

# Instructions
To run Dungeon Crawler, first ensure that you have all of the required libraries installed, then run the python script main.py which resides within the /src directory - using the command python3 main.py. Movement, be it in-game or in-menu, is governed by the 'a', 's', 'd', and 'f' keys, as convention defines. Selecting menu options and attacking in-game is done using the spacebar. Additionally, the escape key may be used to exit to a previous menu from a nested menu, or to pause in-game. Lastly, in the load menu, the 'c' key may be used to clear an occupied save slot. Note that the controls are case-sensitive, the game will not accept capital letters.

# Force Quitting
If for whatever reason you wish to force quit the game, press the '.' key.

ENJOY!
