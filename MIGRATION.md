# Migration & Refactoring Plan

## Phase 1: Modularization
**Goal**: Break the monolithic `main.py` into maintainable sub-modules. This decouples the game logic from the rendering and data structures.

### 1. Extract Constants
Create `src/config.py` to hold all magic numbers and settings.
*   **Move**: `WINDOW_WIDTH`, `WINDOW_HEIGHT`, `CARD_WIDTH`, `CARD_HEIGHT`, `TOP_OFFSET`, `COLORS`.
*   **Benefit**: Easy tweaking of game balance and UI without touching logic code.

### 2. Extract Data Classes
Create `src/models.py`.
*   **Move**: `Card` class.
*   **Move**: `Button` class.
*   **Update**: Refactor direct `pygame` calls in these classes (drawing) to be potentially cleaner or passed in.

### 3. Extract Logic Utilities
Create `src/game_logic.py`.
*   **Move**: `find_linked_cards()` (The BFS algorithm).
*   **Move**: `find_tail()` (The new pile searching algorithm).
*   **Move**: `add_card_to_deck()` and `generate_random_color()`.

### 4. Clean Entry Point
Refactor `main.py` to only handle:
*   Pygame initialization.
*   The main `while running:` loop.
*   Input routing (calling functions in `game_logic`).
*   Render calls.

---

## Phase 2: Data Structure Optimization
**Goal**: Improve performance (currently O(N) for parent lookups) and logic robustness.

### 1. Doubly Linked Lists
Add a `parent` reference to the `Card` class (`card.parent_id`).
*   **Why**: Fixing the highlighting logic required disjointed O(N) searches to find "roots".
*   **Implementation**: Ensure every `card.linked = child` operation is paired with `child.parent = card`.

### 2. Physical vs Logical Separation
Currently, `Card` holds both physical (`rect`) and logical (`linked`) state.
*   **Refactor**: Create a `GameState` object that holds the graph of connections, separate from the `CardSprite` objects that hold positions and textures.

---

## Phase 3: Advanced Features
**Goal**: Add features that were previously too complex for the simple prototype.

- [ ] **Animations**: Add interpolation for "Snapping" (tweening `rect.x/y` instead of setting it instantly).
- [ ] **Save/Load**: Serialize the `cards` list to JSON, preserving `number` and `linked` IDs.
- [ ] **Camera/Zoom**: If the table gets too big, add a camera offset to the `draw()` calls.

## Phase 4: Testing Strategy
- [ ] **Unit Tests**: Test the `find_linked_cards` logic with mock card objects to ensure no infinite loops.
- [ ] **Integration Tests**: Simulate a "Pickup -> Move -> Drop" sequence and assert `linked` states are correct.
