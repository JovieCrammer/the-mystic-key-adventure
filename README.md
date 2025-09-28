# the-mystic-key-adventure

The Mysic Key Adventure is a hybrid text-based 2D adventure story game, aiming to combine the most loved elements of classic text-based story games such as **Colossal Cave Adventure** and **The Sumerian Game** with the user engagement found in modern games through visual storytelling and increased user input using keyoard and mouse.

This project was created for AQA A-Level Computer Science.

## Description
A Python-based adventure and roleplay game combining text storytelling with 2D visuals. Players can choose to play as one of two interactive characters (Coyote or Orcas). The user, playing as either Coyote or Orcas, unexpectedly wakes up and finds themselves locked in a mysterious underground bunker, surrounded by 5 different coloured doors (red, blue, green, yellow and pink). The storyline of the game is explained through on-screen text popups. The user explores an interactive tilemap, engages in combat, solves puzzles, and decrypts riddles in order to collect the four missing keys (blue, green, yellow and pink). Each key unlocks the door of the same color; behind each door players are faced with a new challenge. By successfully completing all challeges behind all doors and finding all the keys, the player can locate the bunker exit and escape.

Pressing the **esc** key during gameplay will take the user to the pause menu where they can choose to resume, quit or save their progress. If the player chooses to press save, they can leave the game and return later, continuing from the same point.

## Features 
- User authentication and progress saving (created using **MySQL** and **XAMPP**)
- Interactive GUI (created using **Tkinter** and **Pygame**)
- Character Selection
- Character movement using WASD and Mouse
- Combat
- Puzzles
- Interactive map
- Collectable items on-screen (potions, keys)

## Installation and Setup
To run the game, users need to set up the database using **XAMPP**:  

1. Download and install **XAMPP** [https://www.apachefriends.org](https://www.apachefriends.org)
2. Open the **XAMPP Control Panel**
3. Start **Apache** and **MySQL** servers  
4. Access the database in a browser at [http://localhost/phpmyadmin/](http://localhost/phpmyadmin/)  
5. Run: `python main.py`

## Credits
- All images self-designed and self-created using [Pixilart](https://www.pixilart.com) then stored as **.png** files
