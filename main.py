import pygame
import random

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0,255,0)
ORANGE = (255,165,0)
RED = (255,0,0)

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Math game")

# window size
window_width = 1382
window_height = 691

# Set up the display
win = pygame.display.set_mode((window_width, window_height))

# Button dimensions
button_width = 200
button_length = 100
font_size = 20
font = pygame.font.SysFont("comicsans", font_size)

class Button:
    def __init__(self, x, y, width, length, value):
        self.rect = pygame.Rect(x, y, width, length)
        self.value = value
        self.edge_color = BLACK

    def draw(self, surface):
        pygame.draw.rect(surface, self.edge_color, self.rect.inflate(2, 2))
        pygame.draw.rect(surface, WHITE, self.rect)
        text = font.render(self.value, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def click(self):
        return self.value

diff = 0 
def make_question():
    question_first_value = random.randint(diff + 1, (diff + 1) * 2)
    question = ""
    question += f"{question_first_value}"
    operators = ["+", "-", "*"]
    for _ in range(int(diff/5) + 1): # After 5 questions each, it will increase 1 more operator 
        # Pick a random operator and a random number
        op = random.choice(operators)
        number = random.randint(question_first_value, int(question_first_value * 5/4))
        # Add to the question string
        question += f" {op} {number}"
    
    result = eval(question)
    question = question.replace("*","X")
    return result, question

def create_buttons(x, y, width, height, amount, rows, correct_answer):
    buttons = []
    spacing = (window_width - (amount * width) - 2 * x) // (amount + 1)

    # Generate a list of incorrect answers
    incorrect_answers = set()
    while len(incorrect_answers) < (amount * rows - 1):  # One less than total buttons
        incorrect_answer = correct_answer + random.randint(-100, 200)  # Ensure it's within a reasonable range
        if incorrect_answer != correct_answer:
            incorrect_answers.add(incorrect_answer)

    # Convert the set to a list and shuffle it
    incorrect_answers = list(incorrect_answers)
    random.shuffle(incorrect_answers)

    # Determine the total number of buttons
    total_buttons = amount * rows
    # Choose a random index for the correct answer
    correct_index = random.randint(0, total_buttons - 1)

    # Add buttons to the list
    for i in range(total_buttons):
        if i == correct_index:  # Place the correct answer at the randomly chosen index
            value = str(correct_answer)
        else:
            value = str(incorrect_answers.pop())  # Get an incorrect answer
        
        button_x = int(spacing + (spacing + width) * (i % amount) + x)
        button_y = y + (i // amount) * (height + 20)  # Add spacing between rows
        buttons.append(Button(button_x, button_y, width, height, value))

    return buttons

# Create the initial question and buttons
result, question_text = make_question()
buttons = create_buttons(int(window_width / 14), int(window_height / 4), button_width, button_length, 5, 4, result)

start_button = Button( int(window_width / 2 - button_width / 2), int(window_height * 3 / 4), button_width, button_length, "Start game")

def welcome_screen():
    win.fill(WHITE)
    intro_text = """    Welcome to the math game
    In this game, you will need to calculate the correct answer in limited time.
    There is only 3 types of math symbols in here ('+', '-', 'x')
    Press start when you're ready"""
    intro_surface = font.render(intro_text, True, BLACK)
    win.blit(intro_surface, (int(window_width / 2 - intro_surface.get_width() / 2), int(window_height / 5)))
    
    start_button.draw(win)
    
def lost_screen():
    win.fill(WHITE)
    text = "Congratulation, you have lost!\nPress Q to restart the game"
    text_surface = font.render(text, True, BLACK)
    score = font.render(f"Your score: {temp_score}", True, BLACK)
    win.blit(text_surface, (int(window_width / 2 - text_surface.get_width() / 2), int(window_height / 2)))
    win.blit(score, (int(window_width / 2 - score.get_width() / 2), int(window_height / 2) + font_size * 3))
    
rect_x = 50
rect_y = 50
rect_width = 100
rect_height = 20
seconds = 0 # use to track the time left for that question

def ReDrawWindow():
    if screen_number == 1:
        welcome_screen()
    elif screen_number == 2:
        win.fill(WHITE)
        question_text_display = "Question: " + question_text + "\nScore: " + f"{diff}"
        text_surface = font.render(question_text_display, True, BLACK)
        win.blit(text_surface, (int(window_width / 2 - text_surface.get_width() / 2), int(window_height / 10)))
        color = BLACK
        if seconds >= length_of_time - 3: # use to change color for the time according to how much time is left
            color = RED
        elif seconds >= length_of_time - 6:
            color = ORANGE
        else:
            color = GREEN
        pygame.draw.rect(win, color, (rect_x, rect_y, rect_width, rect_height))
        for button in buttons:
            button.draw(win)
    elif screen_number == 3:
        lost_screen()
        
    pygame.display.update()

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def restart_question():
    result, question_text = make_question()
    buttons = create_buttons(int(window_width / 14), int(window_height / 4), button_width, button_length, 5, 4, result)
    start_ticks = pygame.time.get_ticks()  # Reset timer
    return result, question_text, buttons, start_ticks

def main():
    global result, question_text, buttons, screen_number,rect_width,seconds,diff,temp_score,length_of_time  # Declare variable as global
    length_of_time = 10
    length_of_time_display = window_width * 9 / 10
    
    # Initialize question and timer
    start_ticks = pygame.time.get_ticks()  # Start time for the question timer
    screen_number = 1 # the screen first start at 1 (welcome screen)
    running = True
    while running:
        if screen_number == 2:
            # Timer for updating question every 10 seconds (at first)
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Calculate elapsed time in seconds
            rect_width = length_of_time_display * (length_of_time - seconds)/length_of_time
            if seconds >= length_of_time:  # 10-second interval (at first)
                #result, question_text, buttons, start_ticks = restart_question() -> this is no use as when press Q to restart the game, it already did
                temp_score = diff
                screen_number = 3
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Check mouse
                mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                if screen_number == 1:
                    if start_button.rect.collidepoint(mouse_pos):
                        screen_number = 2
                        start_ticks = pygame.time.get_ticks()
                elif screen_number == 2:
                    for button in buttons:
                        if button.rect.collidepoint(mouse_pos):
                            if result == int(button.click()):
                                print("You are correct")
                                diff += 1
                                result, question_text, buttons, start_ticks = restart_question()
                                length_of_time += 0.5 #this will slowly increase the time for each harder question, to make sure we have more time to calculate harder question
                            else:
                                print("Your answer is wrong")
                                temp_score = diff
                                screen_number = 3
                                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    screen_number = 2
                    result, question_text, buttons, start_ticks = restart_question()
                    diff = 0
        ReDrawWindow()  # Redraw screen with updated question
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()
    
if __name__ == "__main__":
    main()
