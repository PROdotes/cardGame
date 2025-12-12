import pygame
import random


# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Set the dimensions of the window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# other stuff
OVERLAP_ALLOW = 0.05
CARD_HEIGHT = 80
CARD_WIDTH = 55
TOP_OFFSET = CARD_HEIGHT * 0.2
PRE_GENERATE_CARDS = 100
CARDS_TO_ADD = 10

# Set up the display
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Draggable Cards")

clock = pygame.time.Clock()


# Define Button class
class Button:
    """Button class for GUI button"""

    def __init__(self, position, size):
        x, y = position
        width, height = size
        self.rect_out = pygame.Rect(position, size)
        self.rect_in = pygame.Rect((x + 10, y + 10), (width - 20, height - 20))

    def draw(self, text_font):
        pygame.draw.rect(window, BLACK, self.rect_out)
        pygame.draw.rect(window, GREY, self.rect_in)
        text = text_font.render("Add Card", True, WHITE)
        text_rect = text.get_rect(center=self.rect_out.center)
        window.blit(text, text_rect)

    def collide(self, mouse_position):
        return self.rect_in.collidepoint(mouse_position)


# Define Card class
class Card:
    """Card class representing draggable cards"""

    def __init__(self, x_position, y_position, color, card_number):
        self.rect = pygame.Rect(x_position, y_position, CARD_WIDTH, CARD_HEIGHT)
        self.color = color
        self.number = card_number
        self.dragging = False
        self.linked = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def draw(self, font, opacity=255, outline_color=None, outline_width=3):
        # Draw card body and text onto a temporary surface to handle transparency
        temp_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        temp_surface.fill(self.color)
        
        text_surface = font.render(str(self.number), True, WHITE)
        text_rect = text_surface.get_rect(center=(CARD_WIDTH/2, CARD_HEIGHT/2))
        temp_surface.blit(text_surface, text_rect)
        
        if opacity < 255:
            temp_surface.set_alpha(opacity)
        
        window.blit(temp_surface, self.rect)
        
        if outline_color:
            pygame.draw.rect(window, outline_color, self.rect, outline_width)

    def update_position(self, mouse_position):
        x, y = mouse_position
        self.rect.topleft = (x - self.drag_offset_x, y - self.drag_offset_y)

    def is_mouse_over(self, mouse_position):
        return self.rect.collidepoint(mouse_position)

    def calculate_overlap(self, other_card):
        overlap_rect = self.rect.clip(other_card.rect)
        overlap_area = overlap_rect.width * overlap_rect.height
        card_area = CARD_WIDTH * CARD_HEIGHT
        return overlap_area / card_area


def generate_random_color():
    red = random.randint(50, 250)
    green = random.randint(50, 250)
    blue = random.randint(50, 250)

    return red, green, blue


# Main function
def main():
    """Main function to run the program"""
    running = True
    cards = []
    button = Button((10, 10), (150, 50))
    font = pygame.font.Font(None, 36)

    mouse_over_cards = []
    top_card_num = None
    drag_start_card_num = None
    current_dragging_ids = set()
    linked_card_num = None
    is_dragging = False
    for _ in range(PRE_GENERATE_CARDS):
        add_card_to_deck(cards)

    def find_linked_cards(starting_card_number):
        linked_cards = set()
        stack = [starting_card_number]

        while stack:
            current_card = stack.pop()
            linked_cards.add(current_card)

            for card in cards:
                if card.number == current_card and card.linked is not None:
                    if card.linked not in linked_cards:
                        stack.append(card.linked)

        return linked_cards

    while running:
        window.fill(GREY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collide(pygame.mouse.get_pos()):
                    for _ in range(CARDS_TO_ADD):
                        add_card_to_deck(cards)
                else:
                    if top_card_num is None:
                         top_card_num = next(
                            (card.number for card in reversed(cards) if card.is_mouse_over(pygame.mouse.get_pos())),
                            None)

                    if top_card_num is not None:
                        drag_start_card_num = top_card_num
                        dragging_cards = find_linked_cards(top_card_num)

                        current_dragging_ids = set(dragging_cards)
                        dragging_cards_set = set(dragging_cards)
                        dragged_cards = [card for card in cards if card.number in dragging_cards_set]
                        cards = [card for card in cards if card not in dragged_cards]
                        cards.extend(dragged_cards)

                        mouse_pos = pygame.mouse.get_pos()
                        for card in cards:
                            if card.number in dragging_cards:
                                card.drag_offset_x = mouse_pos[0] - card.rect[0]
                                card.drag_offset_y = mouse_pos[1] - card.rect[1]
                                card.dragging = True
                            else:
                                card.dragging = False
                        is_dragging = True
                    else:
                        is_dragging = False
                        drag_start_card_num = None

            elif event.type == pygame.MOUSEMOTION:
                mouse_over_cards = [card.number for card in cards if card.is_mouse_over(pygame.mouse.get_pos())]

                top_card_num = next(
                    (card.number for card in reversed(cards) if card.is_mouse_over(pygame.mouse.get_pos())),
                    None)

                linked_card_num = next((card.linked for card in cards if card.number == top_card_num), None)

                if is_dragging:
                    for card in cards:
                        if card.dragging:
                            card.update_position(pygame.mouse.get_pos())

            elif event.type == pygame.MOUSEBUTTONUP:
                if is_dragging and drag_start_card_num is not None:
                    # Identify the stack of cards being moved
                    moving_stack_ids = find_linked_cards(drag_start_card_num)
                    
                    # Unlink from previous parent (disconnect the stack from where it was)
                    for card in cards:
                        if card.linked == drag_start_card_num:
                            card.linked = None
                            break

                    # Find a drop target under the mouse
                    mouse_pos = pygame.mouse.get_pos()
                    target_card = None
                    # Search from top (end of list) to bottom
                    for card in reversed(cards):
                        if card.is_mouse_over(mouse_pos):
                            # Ensure we don't drop on ourselves or our own stack
                            if card.number not in moving_stack_ids:
                                target_card = card
                                break
                    
                    # If we found a target, we must find the BOTTOM/END of that pile to snap onto.
                    # We cannot insert into the middle. We snap to the end.
                    if target_card is not None:
                         # Traverse down to find the true valid target (the tail)
                         visited = set()
                         while target_card.linked is not None and target_card.number not in visited:
                             if target_card.linked == drag_start_card_num:
                                 break
                             
                             visited.add(target_card.number)
                             next_id = target_card.linked
                             found_next = False
                             for c in cards:
                                 if c.number == next_id:
                                     target_card = c
                                     found_next = True
                                     break
                             if not found_next:
                                 break

                    # If valid target found
                    if target_card is not None and (target_card.linked is None or target_card.linked == drag_start_card_num):
                        # Snap logical link
                        target_card.linked = drag_start_card_num
                        print(f"Linked {drag_start_card_num} to {target_card.number}")
                        
                        # Snap physical positions (Re-stack the moving cards onto the target)
                        overlap_count = 0
                        target_x = target_card.rect.x
                        target_y = target_card.rect.y
                        
                        for move_card in cards:
                            if move_card.number in moving_stack_ids:
                                overlap_count += 1
                                move_card.rect.x = target_x
                                move_card.rect.y = target_y + (TOP_OFFSET * overlap_count)
                        
                    # Reset dragging state
                    for card in cards:
                        card.dragging = False
                    is_dragging = False
                    drag_start_card_num = None
                    current_dragging_ids.clear()

        # Calculate hover target for visual feedback
        hover_target_num = None
        hover_pile_ids = set()
        
        if is_dragging:
            mouse_pos = pygame.mouse.get_pos()
            for card in reversed(cards):
                if card.is_mouse_over(mouse_pos) and card.number not in current_dragging_ids:
                    # We are hovering over 'card'. 
                    # We want to behave as if we are hovering over the TAIL of 'card's pile.
                    real_target = card
                    visited = set()
                    
                    # Traverse to find the tail
                    while real_target.linked is not None and real_target.number not in visited:
                        if real_target.linked == drag_start_card_num:
                            break
                        visited.add(real_target.number)
                        found_next = False
                        for c in cards:
                             if c.number == real_target.linked:
                                 real_target = c
                                 found_next = True
                                 break
                        if not found_next:
                             break

                    # Check if tail is a valid drop spot
                    if real_target.linked is None or real_target.linked == drag_start_card_num:
                        hover_target_num = real_target.number
                        # Use real_target for finding the root to highlight the whole pile correctly
                        card = real_target
                        
                        # Find the root of the pile for this target card
                        current_root = card.number
                        changed = True
                        while changed:
                            changed = False
                            for c in cards:
                                if c.linked == current_root:
                                    current_root = c.number
                                    changed = True
                                    break
                        
                        # Traverse down from root to collect all IDs in this pile
                        hover_pile_ids.add(current_root)
                        stack = [current_root]
                        while stack:
                            curr_id = stack.pop()
                            for c in cards:
                                if c.number == curr_id and c.linked is not None:
                                    hover_pile_ids.add(c.linked)
                                    stack.append(c.linked)
                                    break 
                        
                        break

        # Draw button
        button.draw(font)
        # Draw cards
        for card in cards:
            opacity = 255
            outline = None
            thickness = 3
            
            if card.number in current_dragging_ids:
                opacity = 180  # ~70% opacity
            
            if card.number in hover_pile_ids:
                outline = WHITE
                if card.number != hover_target_num:
                    thickness = 1 # Smaller line for the rest of the pile
                else:
                    thickness = 3 # Thick line for direct target
                
            card.draw(font, opacity, outline, thickness)

        # Draw text showing the number of the card mouse is over
        fps_text = font.render("FPS: {:.1f}".format(clock.get_fps()), True, BLACK)
        window.blit(fps_text, (WINDOW_WIDTH - 150, 10))
        if len(mouse_over_cards) != 0:
            text = font.render("Mouse over card: {}".format(mouse_over_cards), True, BLACK)
            top_text = font.render("Top card: {}".format(top_card_num), True, BLACK)
            linked_text = font.render("Linked card: {}".format(linked_card_num), True, BLACK)
            window.blit(text, (10, WINDOW_HEIGHT - 40))
            window.blit(top_text, (10, WINDOW_HEIGHT - 80))
            window.blit(linked_text, (10, WINDOW_HEIGHT - 120))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def add_card_to_deck(deck):
    color = generate_random_color()
    new_card = Card(random.randint(50, WINDOW_WIDTH - CARD_WIDTH * 2),
                    random.randint(50, WINDOW_HEIGHT - CARD_HEIGHT * 2),
                    color, len(deck) + 1)
    deck.append(new_card)


if __name__ == "__main__":
    main()
