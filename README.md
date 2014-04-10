------------------------------------------------------------
CMPUT 275 Winter 2014

Title: Conditional Heroes 
A Side Scrolling Hack n' Slash RPG 
Team Members: Quentin Lautischer (1295913), Josh White


Description:
A 2.5D side scroller, with AI controlled monsters along the lines of Castle Crashers.

The project will demonstrate sorting, pathfinding to determine movement of AI and basic inheritance in the form of different unit types, graph theory in the form of creating a grid like system for the map that determines where one can step and is used as a framework for AI movement. It will include server/serial communation by including an arduino as a controller for the game. Collision will be included for attacks to take effect (Box Exercise). We will have the game run on a sort of script allowing for a story like progression through the levels. 

The project will be written in Python 3 using pygame and an additional controller using the arduino with a server communication with our python game.  The Arduino will be set up to use as a player 2 controller.
--------------------------------------------------------------
Controls:
Menu Screen: Arrow Keys and Enter

Player 1: WASD: Movement Q: Shield E: Atk 1 R: Atk 2

Player 2: IJKL: Movement U: Shield O: Atk 1 P: Atk 2

Arduino controls are straight forward. Joystick and buttons


--------------------------------------------------------------
%%%%% COPYRIGHT %%%%%
The elements of this project are not our own:

Modules:
sounds.py was taken from assignment #4
graph_module.py was worked on in class

Sounds:
All sound files were downloaded from https://www.freesound.org/

Images:
All unit sprites and spell effects were taken from http://www.perioncorner.com/ and http://www.mapleme.net/
	
	Within the images/Taken Images/

	BackgroundCastle1.png and Sky.png are from https://forum.kag2d.com/threads/wip-castle-crashers-sprite-pack.8763/
	interface_panel is cut from from http://us.battle.net/wow/en/warlords-of-draenor/
	bridge.jpg http://imgs.tuts.dragoart.com/how-to-draw-a-bridge_1_000000003287_5.jpg
	dark_forst.jpg http://hdw.eweb4.com/out/1051440.html
	mystic_forest.jpg http://www.wallconvert.com/converted/271138-185101.html
	red_mush.jpg http://www.shutterstock.com/pic-109870277/stock-photo-illustration-of-red-mushrooms-on-a-white-background.html
	river_drawing.jpg http://anastaciavargas.wordpress.com/2012/07/12/my-drawing-of-a-river/
	bush.jpg http://imgs.tuts.dragoart.com/how-to-draw-a-bush_1_000000003749_2.jpg
	bushes.jpg http://www.shutterstock.com/pic-138593246/stock-vector-trees-top-view-for-landscape-vector-illustration.html
	mushroom illustration.jpg http://www.naturaldesignsstudio.com/uploads/1/9/5/1/1951222/3590964.jpg?636
	menu.jpg http://www.psdvault.com/inspirations/20-absolutely-gorgeous-landscape-scenery-digital-artworks-to-inspire-you/
	shield.jpg http://www.ssbwiki.com/shield

--------------------------------------------------------------
Milestone 1:
Basic rendering of game elements (maps, player units, enemy units) this includes a proper depth sorting algorithm to draw the items according to depth (ie: A unit that is close to the screen is drawn on top of something farther)

Milestone 2:
Unit movement/attack. Units will have health and spells that cause damage to enemies (Animated of course). 

Milestone 3:
Map grid system. Using graph theory we will have a customizable grid system that will allow movement only in certain areas with different maps. (This grid may also aid in AI design)

Milestone 4:
AI design. Monsters move according to a pre-determined script that is ajusted according to player position.

Milestone 5:
Arduino Controller. Server/Client implementation run during game logic.

Optional:
Scripting the game. Including a story that can be follow as you proceed through the game.  Also maybe some custom music for gameplay. Collision may also be extended to apply to characters passing through each other so that they can't.

Our demonstration will be a playable version of the game.
In the demo you will proceed through a rushed play through of the game.
-------------------------------------------------------------
