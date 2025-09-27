# The_Mystic_Key_Adventure

Hybrid Text-Based 2D Adventure Story Game created for AQA A-Level Computer Science.

## Description
A Python-based adventure game combining text storytelling with 2D visuals. Players can choose to play as one of two interactive characters and explore a tilemap, engage in combat, solve puzzles, and complete challenges to collect missing keys: blue, green, yellow, and pink. Each key unlocks a door of the same color, behind which players face a new challenge. Players can save their progress and return later to continue from the same point. The story is explained through text popups on-screen, with the ultimate goal of escaping the mysterious dungeon.

## Features 
- User authentication and progress saving using **MySQL** with **XAMPP**
- GUI created with **Tkinter** and **Pygame**  
- Character selection  
- Combat and puzzles
- Interactive map
- Collectable items on-screen (potions, keys)
- All images self-created using [Pixilart](https://www.pixilart.com) and stored as **.png** files  

## Installation / Setup
To run the game, users need to set up the database using **XAMPP**:  

1. Download and install **XAMPP** ([https://www.apachefriends.org](https://www.apachefriends.org))  
2. Open the **XAMPP Control Panel** and start **Apache** and **MySQL** servers  
3. Access the database in a browser at [http://localhost/phpmyadmin/](http://localhost/phpmyadmin/)  
4. Run: `python main.py` 
