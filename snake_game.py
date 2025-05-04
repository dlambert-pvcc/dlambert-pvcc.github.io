# https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/
#   followed this guide for much of my own program and
#   expanded upon it independently for features I wanted
#   to implement, including difficulty selection and
#   the option to play again
#
#   also researched from the official pygame documentation

# Imports:
import pygame
import random

# Global variables:
gray = (190, 190, 190) # arena background
purple = (210, 20, 210) # food
blue = (20, 20, 210) # snake
blackish = (40, 40, 40) # menu/game-over background
white = (245, 245, 245) # menu/game-over text

arena_width = 825
arena_height = 525
#   arena is based around 15-pixel tiles


# Gameplay function:
def main():
    # Initializations:
    pygame.init()
    window = pygame.display.set_mode((arena_width, arena_height))
    pygame.display.set_caption("Mal Lambert's Snake Game")
    time_var = pygame.time.Clock()

    # Initial selection screen:
    window.fill(blackish)

    difficulty_font = pygame.font.SysFont("Courier", 24, bold=True).render("Select difficulty: [E]asy, [M]edium, [H]ard", True, white)

    difficulty_surface = difficulty_font.get_rect(center=(arena_width / 2, arena_height / 2.25))

    window.blit(difficulty_font, difficulty_surface)
    pygame.display.flip()

    select_screen = True
    while select_screen == True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_e:
                    difficulty = 1
                    select_screen = False
                if e.key == pygame.K_m:
                    difficulty = 2
                    select_screen = False
                if e.key == pygame.K_h:
                    difficulty = 3
                    select_screen = False

    # Snake definitions:
    head = [75, 255]
    body = [[75, 255], [60, 255]]
    direction = "right"
    change_dir = direction

    # Place food:
    food_loc = [random.randint(0, (arena_width // 15 - 15)) * 15, random.randint(0, (arena_height // 15 - 15)) * 15]
               #   truncate floating points to integers with // operator
    food_ate = True

    # logic for the following loop is
    #  1. define movement,
    #  2. allow movement,
    #  3. update graphics based on movement,
    #  4. check for game over
    #  5. refresh display & update speed
    while True:
        window.fill(gray)

        # Define player movement:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
            #   let player hit Close button
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    change_dir = "left"
                if e.key == pygame.K_UP:
                    change_dir = "up"
                if e.key == pygame.K_RIGHT:
                    change_dir = "right"
                if e.key == pygame.K_DOWN:
                    change_dir = "down"

        # Disallow player from turning directly into their body:
        if change_dir == "left" and direction != "right":
            direction = "left"
        if change_dir == "up" and direction != "down":
            direction = "up"
        if change_dir == "right" and direction != "left":
            direction = "right"
        if change_dir == "down" and direction != "up":
            direction = "down"

        # Move snake:
        if direction == "left":
            head[0] -= 15 # width
        if direction == "up":
            head[1] -= 15 # height
        if direction == "right":
            head[0] += 15 # width
        if direction == "down":
            head[1] += 15 # height

        # Add a tail segment underneath head:
        body.insert(0, list(head))

        # Check if snake ate food, remove farthest tail segment if not:
        if (head[0] == food_loc[0]) and (head[1] == food_loc[1]):
            food_ate = False
        else:
            body.pop()

        # Reset food if none present:
        if food_ate == False:
            food_loc = [random.randint(0, (arena_width // 15 - 15)) * 15, random.randint(0, (arena_height // 15 - 15)) * 15]
            #   could implement a for-loop to respawn the food if it appears in
            #   the snake's body, but I don't want food to suddenly jump across
            #   the screen
            food_ate = True

        # Redraw background:
        window.fill(gray)

        # (Re)draw snake:
        for loc in body:
            pygame.draw.rect(window, blue, pygame.Rect(loc[0], loc[1], 15, 15))

        # (Re)draw food:
        pygame.draw.rect(window, purple, pygame.Rect(food_loc[0], food_loc[1], 15, 15))

        # Update score before checking game over:
        body_segments = len(body)
        score = int(body_segments - 2)

        # Check for game over:
        if ((head[0] < 0) or (head[0] > arena_width) or (head[1] < 0) or (head[1] > arena_height)):
            game_over("You ran into the wall.", window, score)
        for segment in body[1:]:
            if head[0] == segment[0] and head[1] == segment[1]:
                game_over("You ran into your tail.", window, score)

        # Refresh display:
        pygame.display.update()
        
        # Set and update speed of snake:
        if difficulty == 1:
            speed = (body_segments / 6) + 10
        if difficulty == 2:
            speed = (body_segments / 4) + 15
        if difficulty == 3:
            speed = (body_segments / 3) + 20
        time_var.tick(speed)
#end-main()


# Game-over function:
def game_over(reason, window, score):
    window.fill(blackish)

    g_o_font = pygame.font.SysFont("Courier", 24).render(f"{reason} Score: " + str(score) +". Play again? y/n", True, white)

    g_o_surface = g_o_font.get_rect(center=(arena_width / 2, arena_height / 2.25))

    window.blit(g_o_font, g_o_surface)
    pygame.display.flip()

    # Quit or play again:
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_n:
                    pygame.quit()
                    quit()
                if e.key == pygame.K_y:
                    main()
#end-game-over()


main()