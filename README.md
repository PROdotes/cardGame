# Draggable Card Game

A Python-based interactive card sorting demonstration using `pygame`. This project features a robust drag-and-drop system with support for stacking, splitting piles, and visual feedback.

## Features

- **Dynamic Card Stacking**: Cards can be stacked on top of each other to form piles. Piles travel together when dragged.
- **Smart Drag-and-Drop**:
  - **Snap-to-End**: Dropping a card anywhere on an existing pile automatically snaps it to the bottom of that pile.
  - **Pile Splitting**: Picking up a card from the middle of a stack cleanly separates it (and its children) from the parent.
- **Visual Feedback**:
  - **Transparency**: Cards currently being dragged become semi-transparent.
  - **Highlighting**: Valid drop targets are highlighted with a thick white border. The entire connected pile lights up with a thinner border to indicate the group relationship.
- **Card Generation**: Includes a button to generate new random cards on the fly.

## Requirements

- Python 3.x
- `pygame`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PROdotes/cardGame.git
   ```
2. Install dependencies:
   ```bash
   pip install pygame
   ```

## Usage

Run the main script to start the application:

```bash
python main.py
```

### Controls
- **Left Click & Drag**: Pick up and move cards or stacks.
- **Release**: Drop the card. If dropped over another pile, it will snap to the end of that pile.
- **"Add Card" Button**: Spawns a new random card on the board.
