import pygame
from grid import Grid

window = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Tic-tac-toe")

pygame.font.init()
winner_font = pygame.font.SysFont("Comic Sans MS", 40)
restart_font = pygame.font.SysFont("Comic Sans MS", 25)

grid = Grid(pygame)
# grid.show_grid()

running = True
letter = "X"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False
                grid.tie_game = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[1] < 600:
                    x = mouse_pos[0] // 200
                    y = mouse_pos[1] // 200
                    grid.mouse_click(x, y, letter)
                    if grid.switch_letter:
                        if letter == "X":
                            letter = "O"
                        else:
                            letter = "X"

    window.fill((0, 0, 0))

    grid.draw(window)

    if grid.game_over and not grid.tie_game:
        color = (0, 255, 0) if grid.winner_letter == "X" else (255, 0, 0)
        won_surface = winner_font.render(f"{grid.winner_letter} Wins!", False, color)
        window.blit(won_surface, (220, 650))

        restart_surface = restart_font.render("Press Space to restart!", False, color)
        window.blit(restart_surface, (150, 720))

    if grid.tie_game:
        tie_game_surface = winner_font.render("No one wins!", False, (255, 255, 255))
        window.blit(tie_game_surface, (180, 650))

        restart_surface = restart_font.render("Press Space to restart!", False, (255, 255, 255))
        window.blit(restart_surface, (150, 720))

    pygame.display.flip()
