

# Card Game

This Python-based card game is built using the Pygame library and offers a fun and interactive way to play a card game on your computer. It supports various functionalities such as dealing cards, selecting hands, scoring, and discarding cards.

## Features
- **Interactive User Interface:** Built with Pygame, providing an engaging graphical interface.
- **Card Selection:** Click on cards to select and form a hand.
- **Scoring System:** Automatically calculates the score based on the best hand.
- **Dynamic Card Movement:** Cards move up when hovered and can be selected or deselected.
- **Deck Management:** Handles dealing, discarding, and reshuffling of cards.
- **Customizable Rules:** Easy to modify the game rules and card properties.

## Installation
To get started with this project, follow these steps:

## Gameplay
- **Hover Over Cards:** Move your mouse over a card to see it move up, indicating it is ready to be selected.
- **Select Cards:** Click on a card to select it for your hand. Selected cards will move to the hand display area.
- **Submit Hand:** Click the "Submit Hand" button to evaluate and score your selected hand.
- **Discard Cards:** Click the "Discard" button to discard your current hand and draw new cards from the deck.

## Code Structure
- `card_game.py`: The main game logic and GUI.
- `handUtil.py`: Utility functions for evaluating hands and checking for combinations like straight and flush.

### `card_game.py`

```python
import pygame as pg
from handUtil import checkHand, checkForStraight, checkForFlush

# Main game logic and GUI implementation
# Contains classes for Game, Card, and Button, handling the game flow, card interactions, and UI elements

class Card(pg.sprite.Sprite):
    # Card class for handling individual card properties and behaviors

class Game:
    # Game class for managing the overall game state, including events, updates, and rendering

class Button(pg.sprite.Sprite):
    # Button class for handling button interactions within the game

# Run the game
if __name__ == '__main__':
    g = Game()
    g.run()
```

### `handUtil.py`

```python
import pygame

# Utility functions for evaluating hands and checking for combinations

def checkHand(card_list):
    # Function to check the best hand from a list of cards

def checkForStraight(card_list):
    # Function to check if a straight is present in the hand

def checkForFlush(card_list):
    # Function to check if a flush is present in the hand

def checkForPairs(card_list):
    # Function to check for pairs, three of a kind, four of a kind, and full house in the hand
```

- **Edgar Vargas**
- [GitHub Profile](https://github.com/Edgar-Vargas)
- [LinkedIn](https://www.linkedin.com/in/edgar-vargas)

---

