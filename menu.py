import pygame

def draw_menu(screen):
    font = pygame.font.Font(None, 74) # Стандартный шрифт
    title = font.render("МОРСКОЙ БОЙ", True, (255, 255, 255))

    # Определяем координаты кнопок
    start_btn_rect = pygame.Rect(200, 300, 500, 50)
    quit_btn_rect = pygame.Rect(200, 400, 500, 50)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    start_color = (255, 255, 255) if start_btn_rect.collidepoint(mouse_x, mouse_y) else (200, 200, 200)
    quit_color = (255, 255, 255) if quit_btn_rect.collidepoint(mouse_x, mouse_y) else (200, 200, 200)

    start_btn = font.render('Начать сражение!!', True, start_color)
    quit_btn = font.render('Покинуть корабль!', True, quit_color)

    # координаты для размещения
    screen.blit(title, (200, 100))
    screen.blit(start_btn, (200, 300))
    screen.blit(quit_btn, (200, 400))


